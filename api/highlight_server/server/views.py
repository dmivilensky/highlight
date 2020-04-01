import json
# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm
from docx import Document

if __name__ != '__main__':
    from . import registration as rg
    from . import get_functions as gf
    from . import find_functions as ff
    from . import main as mn
    from .utils import doc_ids_replace, users_replace_ids, handle_uploaded_file

if __name__ == '__main__':
    # import registration as rg
    import get_functions as gf
    import find_functions as ff
    import main as mn
    from utils import doc_ids_replace, users_replace_ids

ADKEY = "5e82-?XCGf3b24sxw515b61"


@csrf_exempt
def index(request):
    return HttpResponse("HELLO, USER")


@csrf_exempt
def registration_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
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

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def login_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST

        login1 = params["login"]
        pwd = params["password"]
        result = rg.log_in(login1, pwd)

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def verify_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        key = params["key"]
        decision = params["decision"]
        uid = params["id"]
        if key == ADKEY:
            result = rg.verify(uid, "ADMITTED" if decision == 1 else "NOT")
        else:
            result = {'code': "2004"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def find_pieces_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        uid = params["id"]
        if mn.is_there_any_body(uid):
            result = ff.find_pieces(uid)
            for p in result["document"]:
                p["_id"] = str(p["_id"])
        else:
            result = {'code': "2003"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def find_doc_by_lang_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        lang = params["language"]
        result = ff.find_doc_by_lang(lang)
        for f in result["document"]:
            f["doc"]["_id"] = str(f["doc"]["_id"])
            for p in f["pieces"]:
                p["_id"] = str(p["_id"])

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_from_db_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        sch = params["search"]
        tg = params["tags"]
        result = gf.get_from_db(sch, tg)
        result = doc_ids_replace(result)

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_from_db_for_chief_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        sch = params["search"]
        tg = params["tags"]
        result = gf.get_for_chief_from_db(sch, tg)
        result = doc_ids_replace(result)

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_users_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        key = params["key"]
        if key == ADKEY:
            result = gf.get_users()
            result = users_replace_ids(result)
        else:
            result = {'code': "2004"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_trans_and_docs_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        key = params["key"]
        if key == ADKEY:
            result = gf.get_docs_and_trans()
        else:
            result = {'code': "2004"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_translator_stats_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        key = params["key"]
        if key == ADKEY:
            result = gf.get_translators_stat()
            result = users_replace_ids(result, replace_login=True)
        else:
            result = {'code': "2004"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def get_file_stat_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        key = params["key"]
        if key == ADKEY:
            result = gf.get_file_stat()
        else:
            result = {'code': "2004"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def verify_file_cover(request):
    result = {'code': "4040"}
    path = None
    if request.method == "POST":
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     path = handle_uploaded_file(request.FILES['file'])
        # else:
        #     path = None
        params = request.POST
        # file_data = mn.find_file_by_path(path) if not(path is None) else None
        did = params["decision"]
        uid = params["id"]
        path = params["path"]
        result = mn.verify_file(did, uid, path)

    text = json.dumps(result)
    a = mn.delete_from_doc_storage(path) if not(path is None) else ""
    print("File Removed!")
    return HttpResponse(text)


@csrf_exempt
def update_importance_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        did = params["id"]
        result = mn.update_importance(did)

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def update_docs_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     path = handle_uploaded_file(request.FILES['file'])
        # else:
        #     path = None
        params = request.POST
        name = params["name"]
        lang = params["language"]
        tags = params["tags"]
        path = params["path"]
        file_data = mn.find_file_by_path(path) if not(path == "") else None
        result = mn.update_docs(name, file_data, lang, tags) if not(file_data is None) else {"code": "5000"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def update_pieces_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        uid = params["id"]
        did = params["document id"]
        pids = params["pieces id"]
        tl = params["to language"] if "to language" in params.keys() else "RUS"
        if mn.is_there_any_body(uid):
            result = mn.update_pieces(uid, did, pids, tl)
        else:
            result = {'code': "2003"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def update_translating_pieces_cover(request):
    result = {'code': "4040"}
    if request.method == "POST":
        params = request.POST
        uid = params["id"]
        pid = params["piece id"]
        tt = params["txt"] if "txt" in params.keys() else None
        ts = params["status"] if "status" in params.keys() else "UNDONE"
        if mn.is_there_any_body(uid):
            result = mn.update_translating_pieces(pid, tt, ts)
        else:
            result = {'code': "2003"}

    text = json.dumps(result)
    return HttpResponse(text)


@csrf_exempt
def test():
    print(ADKEY)


if __name__ == '__main__':
    test()