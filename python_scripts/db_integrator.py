import configparser
import errno
import io
import os
import sys
from pprint import pprint
from apiclient import errors

from pymongo import MongoClient

sys.path.insert(1, (os.path.dirname(os.path.realpath(__file__)) + '/../api/highlight_server/server'))
from main import push_to_db

import httplib2
import apiclient.discovery
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials
import re
from itertools import zip_longest

def join_google_sheets():
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + "/google_addresses.ini")
    # Файл, полученный в Google Developer Console
    CREDENTIALS_FILE = os.path.dirname(os.path.realpath(__file__)) + '/../google_creds.json'
    # ID Google Sheets документа (можно взять из его URL)
    spreadsheet_id = config["Address"]["sheets_id"]
    drive_id = config["Address"]["docs_id"]

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Пример чтения файла
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Таблица',
        majorDimension='COLUMNS'
    ).execute()
    numbers = values["values"][1]
    tagss = list(map(lambda tagstr: list(map(lambda tag: tag.strip(), re.split('[.,]', tagstr.strip()))), values["values"][5]))
    names = values["values"][6]
    abstract = values["values"][7]
    folders = values["values"][10]
    tr_txt = values["values"][11]
    journal_link = values["values"][12]
    n2c = {"английский": "ENG", "немецкий": "GER", "французский": "FRE", "испанский": "ESP", "итальянский": "ITA", "японский": "JAP", "китайский": "CHI", "": "OTH"}
    lang = list(map(lambda a: n2c[a.strip().lower()] if a.strip().lower() in n2c.keys() else "OTH", values["values"][14]))
    journal = values["values"][15]
    status = list(map(lambda s: ("NEED_CHECK" if s.lower() == "на проверке" else ("TRANSLATED" if s.lower() == "проверен" or s.lower() == "-" else "NEED_CHECK")), values["values"][16]))
    for i in range(len(status)):
        try:
            status[i] = ("TRANSLATED" if values["values"][2][i].lower() in {"ок", "ok"} else "NEED_CHECK")
        except IndexError:
            break

    documents = list(map(lambda t: {"number": t[0], "tag": t[1], "name": t[2], "lang": t[3] if t[3] != "" else "OTH", "abstract": t[4], "folder": t[5], "tr_txt": t[6], "journal_link": t[7], "journal": t[8], "status": t[9] if t[9] != "" else "NEED_CHECK"}, zip_longest(numbers, tagss, names, lang, abstract, folders, tr_txt, journal_link, journal, status, fillvalue="")))
    pprint(documents)

    credentials1 = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE, scopes=['https://www.googleapis.com/auth/drive'])

    doc_storage = os.path.dirname(os.path.realpath(__file__)) + '/../files/integrated_from_sheets'
    gservice = apiclient.discovery.build('drive', 'v3', credentials=credentials1)

    for i in range(len(documents)):
        # Call the Drive v3 API
        results = gservice.files().list(pageSize=1000, includeItemsFromAllDrives=True, supportsAllDrives=True, q="'"+drive_id+"' in parents and name contains '" + str(documents[i]["number"]) + "'").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            documents[i]["RUSpath"] = documents[i]["tr_txt"]
            documents[i]["FORpath"] = documents[i]["journal_link"]
        else:
            print('Files:')
            page_token = results.get('nextPageToken')
            while True:
                sparams = {}
                if page_token:
                    sparams['pageToken'] = page_token
                for item in items:
                    print(item['name'].split("_")[0])
                    if item['name'].split("_")[0] in {str(documents[i]["number"]), ("0" + str(documents[i]["number"]))}:

                        if "doc" in documents[i].keys():
                            documents[i]["doc"][("FOR" if item['name'].split("_")[1] != "RUS" else "RUS")] = item
                        else:
                            documents[i]["doc"] = {("FOR" if item['name'].split("_")[1] != "RUS" else "RUS"): item}
                        print(u'{0} ({1})'.format(item['name'], item['id']))

                        filename = doc_storage + "/" + item['name']
                        if not os.path.isfile(filename):
                            if not os.path.exists(os.path.dirname(filename)):
                                try:
                                    os.makedirs(os.path.dirname(filename))
                                except OSError as exc:  # Guard against race condition
                                    if exc.errno != errno.EEXIST:
                                        raise

                            request = gservice.files().get_media(fileId=item['id'])
                            fb = bytes()
                            fh = io.BytesIO(fb)
                            downloader = MediaIoBaseDownload(fh, request)
                            done = False
                            while done is False:
                                status, done = downloader.next_chunk()
                                print("Download %d%%." % int(status.progress() * 100))
                            with open(filename, mode="wb+") as f:
                                f.write(fb)
                        else:
                            print("downloaded")
                        documents[i][("FOR" if item['name'].split("_")[1] != "RUS" else "RUS") + "path"] = filename

                if not page_token:
                    break

                try:
                    results = gservice.files().list(**sparams).execute()
                    items = results.get('files', [])
                    page_token = results.get('nextPageToken')
                except errors.HttpError as e:
                    print('An error occurred: %s' % e)
                    break

            documents[i]["status"] = "WAITING_FOR_TRANSLATION" if "doc" in documents[i].keys() and not("RUS" in documents[i]["doc"].keys()) else (documents[i]["status"] if documents[i]["status"] in {"NEED_CHECK", "TRANSLATED"} else "NEED_CHECK")

    pprint(documents)
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    for doc in documents:
        pf = lang_storage.find_one({"name": (doc["number"] + " " + doc["name"]), "status": doc["status"]})
        if pf is None:
            print(doc["number"])
            if doc["status"] == "WAITING_FOR_TRANSLATION":
                did = push_to_db(lang_storage.count_documents({"status": "WAITING_FOR_TRANSLATION"}) + 1, (doc["number"] + " " + doc["name"]),
                                 doc["status"], doc["lang"], tags=",".join(doc["tag"]), pieces_count=0, importance=0,
                                 orig_path=doc["FORpath"], abstract=doc["abstract"], author="", journal=doc["journal"],
                                 journal_link=doc["journal_link"])
            else:
                if not "FORpath" in doc.keys():
                    doc["FORpath"] = doc["journal_link"]
                if not "RUSpath" in doc.keys():
                    doc["RUSpath"] = doc["tr_txt"]
                did = push_to_db(lang_storage.count_documents({"status": {"$in": ["WAITING_FOR_TRANSLATION", "NEED_CHECK", "TRANSLATED"]}}) + 1, (doc["number"] + " " + doc["name"]), doc["status"], doc["lang"], orig_path=doc["FORpath"],
                                 path=doc["RUSpath"], to_lang="RUS", tags=",".join(doc["tag"]),
                                 importance=0, translator=[],
                                 chief=[], author="", abstract=doc["abstract"], journal=doc["journal"],
                                 journal_link=doc["journal_link"], orig_preview="",
                                 orig_txt_path="")


if __name__ == "__main__":
    join_google_sheets()