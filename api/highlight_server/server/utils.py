import os
import random
import time

import docx
from bson import ObjectId

from .forms import UploadFileForm
from .views import HTTPMETHOD
from .main import PATH_TO_FILES
from .logger import Logger
from . import main as mn
from pymongo import MongoClient
import asyncio
from collections.abc import Iterable

SECS = 5

ITERATIONS = 100


def iterable(obj):
    return isinstance(obj, Iterable)


def doc_ids_replace(result):
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    result1 = result
    for doc in result1["document"]:
        doc["_id"] = str(doc["_id"])

        if "orig_path" in doc.keys():
            doc["orig_path"] = doc["orig_path"] if not("Users" in doc["orig_path"].split("/") and "highlight" in doc["orig_path"].split("/") and "files" in doc["orig_path"].split("/") or "var" in doc["orig_path"].split("/") and "www" in doc["orig_path"].split("/") and "files" in doc["orig_path"].split("/")) else "/".join(doc["orig_path"].split("/")[list(doc["orig_path"].split("/")).index("files"):])
        if "path" in doc.keys():
            doc["path"] = doc["path"] if not("var" in doc["path"].split("/") and "www" in doc["path"].split("/") and "files" in doc["path"].split("/")) else "/".join(doc["path"].split("/")[list(doc["path"].split("/")).index("files"):])
        if "orig_txt_path" in doc.keys():
            doc["orig_txt_path"] = doc["orig_txt_path"] if not("var" in doc["orig_txt_path"].split("/") and "www" in doc["orig_txt_path"].split("/") and "files" in doc["orig_txt_path"].split("/")) else "/".join(doc["orig_txt_path"].split("/")[list(doc["orig_txt_path"].split("/")).index("files"):])
        if "txt_path" in doc.keys():
            doc["txt_path"] = doc["txt_path"] if not("var" in doc["txt_path"].split("/") and "www" in doc["txt_path"].split("/") and "files" in doc["txt_path"].split("/")) else "/".join(doc["txt_path"].split("/")[list(doc["txt_path"].split("/")).index("files"):])

        doc["lastModified"] = str(doc["lastModified"])
        if "translator" in doc.keys():
            doc = user_replacer_iterator(acc, doc, "translator")

        if "chief" in doc.keys():
            if iterable(doc["chief"]) and type(doc["chief"]) != str:
                doc = user_replacer_iterator(acc, doc, "chief")
            else:
                uac = acc.find_one({"_id": ObjectId(doc["chief"])})
                doc["chief"] = create_name_by_user(uac)

    return result1


def user_replacer_iterator(acc, doc, key):
    for i in range(len(doc[key])):
        try:
            uac = acc.find_one({"_id": ObjectId(doc[key][i])})
            doc[key][i] = create_name_by_user(uac)
        except Exception as e:
            print(e)
    return doc


def replace_pieces_id(f, not_user=True, find_in_list=False):
    f1 = f
    if find_in_list:
        for p in f1:
            if not_user:
                p["_id"] = str(p["_id"])
                p["lastModified"] = str(p["lastModified"])
            else:
                p["reservation_date"] = str(p["reservation_date"])
    else:
        for p in f1["pieces"]:
            if not_user:
                p["_id"] = str(p["_id"])
                p["lastModified"] = str(p["lastModified"])
            else:
                p["reservation_date"] = str(p["reservation_date"])

    return f1


def check_for_exeption(path):
    if path == "":
        return False
    try:
        mn.find_file_by_path(path)
        return False
    except docx.opc.exceptions.PackageNotFoundError:
        return True

# def upt_d(params, result):
#     name = params["name"]
#     lang = params["language"]
#     tags = params["tags"]
#     path = params["path"]
#     path = '/Users/Downloads/files_test' + path if not (path == "") else ""
#     iter1 = 0
#     while iter1 < ITERATIONS:
#         if not(check_for_exeption(path)):
#             file_data = mn.find_file_by_path(path) if not (path == "") else None
#             result = mn.update_docs(name, file_data, lang, tags, path=path) if not(file_data is None) else {"code": "5000"}
#             # f = open('program_logs.txt', 'w+')
#             # f.write('vsucsess i: ' + str(iter1))
#             # f.close()
#             break
#         # f = open('program_logs.txt', 'w+')
#         # f.write('vi: ' + str(iter1))
#         # f.close()
#         iter1 += 1
#         time.sleep(SECS)
#
#     if iter1 >= ITERATIONS:
#         result = {'code': "5000"}
#     return result
#
#
# def for_verif(params, result):
#     did = params["decision"]
#     uid = params["id"]
#     path = params["path"]
#     path = ((PATH_TO_FILES + path) if not(path == "") else path)
#     iter1 = 0
#     while iter1 < ITERATIONS:
#         if os.path.isfile(path):
#             result = mn.verify_file(did, uid,  path)
#             # f = open('program_logs.txt', 'w+')
#             # f.write('fsucsess i: ' + str(iter1))
#             # f.close()
#             break
#         # f = open('program_logs.txt', 'w+')
#         # f.write('fi: '+str(iter1))
#         # f.close()
#         iter1 += 1
#         time.sleep(SECS)
#
#     if iter1 >= ITERATIONS:
#         result = {'code': "5000"}
#     return result


def users_replace_ids(result, replace_login=False, replace_partly=False, full_security=False):
    result1 = result
    for us in result1["document"]:
        us["_id"] = "not permitted"
        us["password"] = "not permitted"
        if replace_login:
            us["login"] = "not permitted"
        if replace_partly:
            us["login"] = "not permitted"
            us["translated"] = "not permitted"
            us["pieces"] = "not permitted"
            us["verified"] = "not permitted"
        if full_security:
            us["login"] = "not permitted"
            us["vk"] = "not permitted"
            us["tg"] = "not permitted"
            us["fb"] = "not permitted"
            us["email"] = "not permitted"
            us["translated"] = "not permitted"
            us["pieces"] = "not permitted"
            us["verified"] = "not permitted"
        us = replace_pieces_id(us, not_user=False)
    return result1


def create_name_by_user(uac):
    if not(uac is None):
        return (uac["name"] if type(uac["name"]) == str else "") + " " + (
            uac["surname"] if type(uac["surname"]) == str else "") + " " + (
                   uac["mi"] if type(uac["mi"]) == str else "")
    else:
        return "Без редактора"


def handle_uploaded_file(f, ext="pdf"):
    path = PATH_TO_FILES + "/" + str(random.randint(0, 99999)) + str(random.randint(0, 99999)) + "." + ext
    while os.path.isfile(path):
        path = path[:-len(path.split(".")[-1])+1] + str(random.randint(0, 99999)) + "." + ext
    lgr = Logger()
    lgr.log("log", "loader status: ", "saving chunks")
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            lgr.log("log", "loading chunks: ", "chunk loaded")
            destination.write(chunk)
    return path


def hashCode(s):
    content = "" + s
    h = 0
    l = len(content)
    i = 0
    if (l > 0):
        while (i < l):
            h = (h << 5) - h + ord(content[i]) | 0
            i += 1
    return h


def file_loader_module(request):
    path = ""
    result = {'code': "4040"}
    lgr = Logger()
    lgr.log("log", "loader status: ", "loading")
    try:
        if request.method == HTTPMETHOD:
            # lgr.log("log", "loader status: ", "request = post")
            form = UploadFileForm(get_params(request), request.FILES)
            lgr.log("log", "form status: ", form)
            lgr.log("log", "form status: ", request.FILES)
            lgr.log("log", "form status: ", form.is_valid())
            lgr.log("log", "form status: ", form.errors)
            lgr.log("log", "form status", "name " + request.FILES['file'].name.split('.')[-1])
            if form.is_valid():
                path = handle_uploaded_file(request.FILES['file'], ext=request.FILES['file'].name.split('.')[-1])
            else:
                path = ""
    except Exception as e:
        lgr.log("log", "error", str(e))
    return lgr, path


def get_params(request):
    return request.POST if (request.method == "POST") else request.GET


def test():
    pass


if __name__ == "__main__":
    test()