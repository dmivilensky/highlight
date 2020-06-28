import sys

from celery import shared_task
from slugify import slugify
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from collections import defaultdict
import time
import datetime
import pprint
from pymongo import MongoClient
import pickle
import io
import os
from apiclient import errors


sys.path.insert(1, (os.path.dirname(os.path.realpath(__file__)) + '/../api/highlight_server/server'))
from main import push_to_db, delete_from_db_all

keys = {
        'дата'                   : 'date',
        'заголовок'              : 'name',
        'заголовок документа'    : 'name',
        'ключевые слова'         : 'keywords',
        'номер документа'        : 'number',
        'описание'               : 'description',
        'описание документа'     : 'description',
        'переводчики'            : 'translators',
        'ссылка на первоисточник': 'source',
        'страна'                 : 'country',
        'doi'                    : 'doi'
}

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.path.dirname(os.path.realpath(__file__)) + '/../google_creds1.json'
SAVED_FALE = 'saved_dirs.pickle'
BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/../files/integrated_from_gd'
if not os.path.isdir(BASE_DIR):
        os.mkdir(BASE_DIR)

ROOT_DIR = 'Highlight переводы COVID-19'
RD_ID = '1U3tfvjjKuUbcWBhlFB2XY4Hio0OGL8-l'


def is_file_in_folder(service, folder_id, file_id):
  """Check if a file is in a specific folder.

  Args:
    service: Drive API service instance.
    folder_id: ID of the folder.
    file_id: ID of the file.
  Returns:
    Whether or not the file is in the folder.
  """
  try:
    service.parents().get(fileId=file_id, parentId=folder_id).execute()
  except errors.HttpError as error:
    if error.resp.status == 404:
      return False
    else:
      print('An error occurred: %s' % error)
      raise error
  return True


def download_file(file_id, filename, service):
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
        with open(filename, mode="wb+") as f:
                f.write(fh.getvalue())
        return 1


def put_to_mongo(files, directory):
        try:
                client = MongoClient()
                db = client.highlight
                lang_storage = db.files_info
                if type(files[directory]["name"]) == list:
                        files[directory]["name"] = ", ".join(files[directory]["name"])
                files[directory]["status"] = "WAITING_FOR_TRANSLATION" if not (
                                "translate_path" in files[directory].keys()) else "TRANSLATED"

                pf = lang_storage.find_one(
                        {"name": (str(files[directory]["number"]) + " " + str(files[directory]["name"])),
                         "status": {"$in": ["WAITING_FOR_TRANSLATION", "NEED_CHECK", "TRANSLATED"]}})

                if not pf is None:
                        delete_from_db_all(str(pf["_id"]))

                if not "lang" in files[directory].keys():
                        files[directory]["lang"] = "OTH"

                files[directory]["number"] = files[directory]["number"].split(".")[0]

                if files[directory]["status"] == "WAITING_FOR_TRANSLATION":
                        did = push_to_db(
                                lang_storage.count_documents({"status": "WAITING_FOR_TRANSLATION"}) + 1,
                                (files[directory]["number"] + " " + files[directory]["name"]),
                                files[directory]["status"], files[directory]["lang"],
                                tags=",".join(files[directory]["keywords"]), pieces_count=0,
                                importance=0,
                                orig_path=files[directory]["original_path"], abstract=files[directory]["description"] if "description" in files[directory].keys() else "",
                                author=files[directory]["country"],
                                journal=files[directory]["doi"] if "doi" in files[directory].keys() else "",
                                journal_link=files[directory]["source"] if "source" in files[directory].keys() else "")
                else:
                        if not "original_path" in files[directory].keys():
                                files[directory]["original_path"] = ""
                        if not "translate_path" in files[directory].keys():
                                files[directory]["translate_path"] = ""
                        did = push_to_db(lang_storage.count_documents({"status": {
                                "$in": ["WAITING_FOR_TRANSLATION", "NEED_CHECK", "TRANSLATED"]}}) + 1,
                                         (files[directory]["number"] + " " + files[directory]["name"]),
                                         files[directory]["status"],
                                         files[directory]["lang"], orig_path=files[directory]["original_path"],
                                         path=files[directory]["translate_path"], to_lang="RUS",
                                         tags=",".join(files[directory]["keywords"]),
                                         importance=0, translator=files[directory]["translators"],
                                         chief=[], author=files[directory]["country"], abstract=files[directory]["description"] if "description" in files[directory].keys() else "",
                                         journal=files[directory]["doi"] if "doi" in files[
                                                 directory].keys() else "",
                                         journal_link=files[directory]["source"] if "source" in files[directory].keys() else "", orig_preview="",
                                         orig_txt_path="")
        except Exception as e:
                print(str(files[directory]["number"] if "number" in files[directory].keys() else files[directory]) + str(e))


# @shared_task
def integtate():
        pp = pprint.PrettyPrinter(indent=4)

        credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)

        results = service.files().list(pageSize=100,
                                       spaces='drive',
                                       fields="nextPageToken, files(id, name, mimeType, parents)").execute()
        nextPageToken = results.get('nextPageToken')
        while nextPageToken:
                nextPage = service.files().list(pageSize=100,
                                                spaces='drive',
                                                fields="nextPageToken, files(id, name, mimeType, parents)",
                                                pageToken=nextPageToken).execute()
                nextPageToken = nextPage.get('nextPageToken')
                results['files'] += nextPage['files']

        directories_before = set(os.listdir(BASE_DIR))

        directories = set()
        for v in results['files']:
                if v['mimeType'] == 'application/vnd.google-apps.folder' and  v['name'] != ROOT_DIR and 'parents' in v.keys() and RD_ID in v['parents']:
                        directories.add(v['name'])
        new = directories - directories_before
        files = defaultdict(dict)

        for v in results['files']:
                if v['mimeType'] != 'application/vnd.google-apps.folder':
                        directory = v['name'].split('.')[0].split('_')[0]
                        files[directory]['update_time'] = time.time()
                        if directory in new:
                                if v['name'].split('.')[-1] != 'txt':
                                        lang = v['name'].split('.')[0].split('_')[1]
                                        key = ('original' if lang.lower() != 'rus' else 'translate') + '_path'
                                        if lang.lower() != "rus":
                                                files[directory]["lang"] = lang

                                        if not os.path.isdir(BASE_DIR + '/' + directory):
                                                os.mkdir(BASE_DIR + '/' + directory)
                                        useless = download_file(v['id'], BASE_DIR + '/' + directory + '/' + v['name'], service)
                                        files[directory].update({ key: BASE_DIR + '/' + directory + '/' + v['name'] })
                                else:
                                        useless = download_file(v['id'], 'data', service)
                                        content = b''
                                        with open('data', 'rb') as content_file:
                                                content = content_file.read()
                                        content = content.decode('utf8')
                                        if "\r" in content:
                                                content = content.replace("\r", "")
                                        content = content.split('\n\n')
                                        fields = {}
                                        for field in content:
                                                if field.strip() == '':
                                                        continue
                                                some_data = field.strip().split('\n')
                                                if len(some_data) > 2:
                                                        some_data = [some_data[0], " ".join(some_data[1:])]
                                                tag, val = some_data
                                                tag = tag.lower().strip()
                                                if tag in keys:
                                                        if keys[tag] == 'date':
                                                                fields['time'] = time.mktime(datetime.datetime.strptime(val, "%d.%m.%Y").timetuple())
                                                        fields[keys[tag]] = val if ', ' not in val else val.split(', ')
                                                else:
                                                        fields[slugify(tag, separator='_')] = val if ', ' not in val else val.split(', ')
                                        files[directory].update(fields)
                                        os.remove('data')

        pp.pprint(files)
        time.sleep(10)
        for direct in files.keys():
                put_to_mongo(files, direct)


if __name__ == "__main__":
        # from celery.schedules import crontab
        #
        # CELERYBEAT_SCHEDULE = {
        #         # Executes every Monday morning at 7:30 A.M
        #         'every-monday-morning': {
        #                 'task': 'tasks.add',
        #                 'schedule': crontab(minute=1),
        #                 'args': (16, 16),
        #         },
        # }
        print("started")
        integtate()