import json
# Create your views here.
import os
import asyncio

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# from .forms import UploadFileForm
import docx
import time

from .logger import Logger
from .forms import UploadFileForm

HTTPMETHOD: str = "POST"

if __name__ != '__main__':
    from . import registration as rg
    from . import get_functions as gf
    from . import find_functions as ff
    from . import main as mn
    from .utils import doc_ids_replace, users_replace_ids, handle_uploaded_file, hashCode, get_params, replace_pieces_id, \
    upt_d, for_verif, file_loader_module

if __name__ == '__main__':
    # import registration as rg
    import get_functions as gf
    import find_functions as ff
    import main as mn
    from utils import doc_ids_replace, users_replace_ids

ADKEY = "5e82-?XCGf3b24sxw515b61"
ADHASH = 75953932291808146177936


@csrf_exempt
def index(request):
    return HttpResponse("HELLO, USER")


@csrf_exempt
def registration_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        name = params["name"]
        surn = params["surname"]
        mi = params["mi"]
        email = params["email"]
        langs = params["languages"]
        login1 = params["login"]
        pwd = params["password"]
        status = params["status"]
        vk = params["vk"]
        fb = params["fb"]
        tg = params["tg"]
        result = rg.register(name, surn, mi, email, langs, login1, pwd, status, vk, tg, fb)
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def update_account(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        result = rg.update_acc(params)
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def login_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        login1 = params["login"]
        pwd = params["password"]
        if "type" in params.keys():
            type = params["type"]
        else:
            type = None
        result = rg.log_in(login1, pwd, type=type)
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def verify_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        key = params["key"]
        decision = params["decision"]
        ulog = params["login"]
        if key == ADKEY:
            result = rg.verify(ulog, "ADMITTED" if decision == "1" else "NOT")
            result["document"] = "ADMITTED" if decision == "1" else "NOT"
        else:
            result = {'code': "2004"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def find_pieces_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        uid = params["id"]
        if mn.is_there_any_body(uid):
            result = ff.find_pieces(uid)
            replace_pieces_id(result["document"], find_in_list=True)
        else:
            result = {'code': "2003"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def find_piece(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        uid = params["id"]
        pid = params["piece_id"]
        if mn.is_there_any_body(uid):
            result = ff.find_piece(pid)
            result["document"]["_id"] = str(result["document"]["_id"])
            result["document"]["lastModified"] = str(result["document"]["lastModified"])
        else:
            result = {'code': "2003"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def find_doc_by_lang_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        lang = params["language"]
        result = ff.find_doc_by_lang(lang)
        for f in result["document"]:
            f["doc"]["_id"] = str(f["doc"]["_id"])
            f["doc"]["lastModified"] = str(f["doc"]["lastModified"])
            f = replace_pieces_id(f)
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_from_db_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        sch = params["search"]
        tg = params["tags"]
        result = gf.get_from_db(sch, tg)
        result = doc_ids_replace(result)
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_from_db_for_chief_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        sch = params["search"]
        tg = params["tags"]
        result = gf.get_for_chief_from_db(sch, tg)
        result = doc_ids_replace(result)
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_from_db_for_verst_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        sch = params["search"]
        tg = params["tags"]
        result = gf.get_for_verst_from_db(sch, tg)
        result = doc_ids_replace(result)
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_users_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        key = params["key"]
        if key == ADKEY:
            result = gf.get_users()
            result = users_replace_ids(result)
        else:
            result = {'code': "2004"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_trans_and_docs_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        key = params["key"]
        if key == ADKEY:
            result = gf.get_docs_and_trans()
        else:
            result = {'code': "2004"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_translator_stats_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        key = params["key"]
        if key == ADKEY:
            result = gf.get_translators_stat()
            result = users_replace_ids(result, replace_login=True)
        else:
            result = {'code': "2004"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_user_by_doc_or_piece_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        uid = params["id"]
        rid = params["find_id"]
        if mn.is_there_any_body(uid):
            result = gf.get_users_by_doc_or_piece(rid)
            result = users_replace_ids(result, replace_partly=True)
        else:
            result = {'code': "2004"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_file_stat_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        key = params["key"]
        if key == ADKEY:
            result = gf.get_file_stat()
        else:
            result = {'code': "2004"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_pieces_stat_cover(request):
    result = {'code': "4040"}
    params = get_params(request)
    try:
        key = params["key"]
        if key == ADKEY:
            result = gf.get_pieces_stat()
        else:
            result = {'code': "2004"}
            
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def verify_file_cover(request):
    result = {'code': "4040"}
    lgr, path = file_loader_module(request)
    params = get_params(request)
    try:
        # result = for_verif(params, result)
        did = params["document_id"]
        uid = params["id"]
        # path = params["path"]
        result = mn.verify_file(did, uid, path if path != "" else None)
        # f = open('program_logs.txt', 'w+')
        # f.write('fsucsess i: ' + str(iter))
        # f.close()
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    # a = mn.delete_from_doc_storage("/var/www/html/highlight.spb.ru/public_html/files/" + path) if not(path is None) else ""
    # a = mn.delete_from_doc_storage("/Users/sevakabrits/Downloads/files_test/" + path) if not(path is None) else ""
    return HttpResponse(text)


@csrf_exempt
def markup_file(request):
    result = {'code': "4040"}
    lgr, path = file_loader_module(request)
    params = get_params(request)
    try:
        # result = for_verif(params, result)
        did = params["document_id"]
        uid = params["id"]
        # path = params["path"]
        result = mn.verify_file(did, uid, path if path != "" else None)
        # f = open('program_logs.txt', 'w+')
        # f.write('fsucsess i: ' + str(iter))
        # f.close()
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    # a = mn.delete_from_doc_storage("/var/www/html/highlight.spb.ru/public_html/files/" + path) if not(path is None) else ""
    # a = mn.delete_from_doc_storage("/Users/sevakabrits/Downloads/files_test/" + path) if not(path is None) else ""
    return HttpResponse(text)


@csrf_exempt
def update_importance_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        did = params["id"]
        result = mn.update_importance(did)
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def update_docs_cover(request):
    lgr, path = file_loader_module(request)
    params = get_params(request)
    # f = open('program_logs.txt', 'w+')
    # f.write('zas')
    # f.close()
    try:
        lgr.log("log", "loader status: ", "in try/catch")
        name = params["name"]
        lang = params["language"]
        tags = params["tags"]
        # f = open('program_logs.txt', 'w+')
        # f.write('zas')
        # f.close()
        # result = upt_d(params, result)
        lgr.log("log", "loader status: ", "main function")
        # file_data = mn.find_file_by_path(path) if not (path == "") else None
        result = mn.update_docs(name, None, lang, tags, path=path) if not (path == "") else {"code": "5000"}
    except KeyError:
        result = {'code': "5001"}

    lgr.log("log", "result: ", result)

    # f = open('program_logs.txt', 'w+')
    # f.write(str(result))
    # f.close()
    # a = mn.delete_from_doc_storage("/Users/sevakabrits/Downloads/files_test/" + path) if not(path is None) else ""

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def update_pieces_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        uid = params["id"]
        did = params["document_id"]
        # return json.dumps({"document": dict(params.keys)})
        pids = params["pcid"].split("#del#")
        tl = params["to_language"] if "to_language" in params.keys() else "RUS"
        if mn.is_there_any_body(uid):
            result = mn.update_pieces(uid, did, pids, to_lang=tl)
        else:
            result = {'code': "2003"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def update_translating_pieces_cover(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    lgr, path = file_loader_module(request)
    params = get_params(request)
    try:
        uid = params["id"]
        pid = params["piece_id"]
        tt = path if not(path == "") else None
        ts = params["status"] if "status" in params.keys() else "UNDONE"
        if mn.is_there_any_body(uid):
            result = mn.update_translating_pieces(pid, tr_txt=tt, tr_stat=ts)
        else:
            result = {'code': "2003"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def delete_file(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        key = params["key"]
        did = params["document_id"]
        if key == ADKEY:
            result = mn.delete_from_db_all(did)
        else:
            result = {'code': "2004"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def let_my_people_pass(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        log = params["login"]
        pswd = params["password"]
        adhash = hashCode(log+pswd)
        if adhash == ADHASH:
            result = {'code': "OK", "key": ADKEY}
        else:
            result = {'code': "2004"}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def check_user(request):
    result = {'code': "4040"}
    # if request.method == HTTPMETHOD:
    params = get_params(request)
    try:
        uid = params["id"]
        result = {'code': "OK", "result": mn.is_there_any_body(uid)}
    except KeyError:
        result = {'code': "5001"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def test():
    print(ADKEY)
    try:
        print(mn.find_file_by_path("/Users/Downloads/05_Sladkiy_mirazh.docx").paragraphs[10].text)
    except docx.opc.exceptions.PackageNotFoundError:
        print('err')


if __name__ == '__main__':
    test()
