from bson import ObjectId
from pymongo import MongoClient


def doc_ids_replace(result):
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    result1 = result
    for doc in result1["document"]:
        doc["_id"] = str(doc["_id"])
        doc["lastModified"] = str(doc["lastModified"])
        if "translator" in doc.keys():
            for i in range(len(doc["translator"])):
                uac = acc.find_one({"_id": ObjectId(doc["translator"][i])})
                doc["translator"][i] = create_name_by_user(uac)

        if "chief" in doc.keys():
            uac = acc.find_one({"_id": ObjectId(doc["chief"])})
            doc["chief"] = create_name_by_user(uac)

    return result1


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


def users_replace_ids(result, replace_login=False, full_security=False):
    result1 = result
    for us in result1["document"]:
        us["_id"] = "not permitted"
        us["password"] = "not permitted"
        if replace_login:
            us["login"] = "not permitted"
        if full_security:
            us["login"] = "not permitted"
            us["vk"] = "not permitted"
            us["tg"] = "not permitted"
            us["fb"] = "not permitted"
            us["email"] = "not permitted"
        us = replace_pieces_id(us, not_user=False)
    return result1


def create_name_by_user(uac):
    return (uac["name"] if type(uac["name"]) == str else "") + " " + (
        uac["surname"] if type(uac["surname"]) == str else "") + " " + (
               uac["mi"] if type(uac["mi"]) == str else "")


def handle_uploaded_file(f):
    path = 'name.docx'
    with open('name.docx', 'wb+') as destination:
        for chunk in f.chunks():
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


def get_params(request):
    return request.POST if (request.method == "POST") else request.GET


def test():
    pass


if __name__ == "__main__":
    test()