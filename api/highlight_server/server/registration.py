from pymongo import MongoClient
import pymongo as pm
from bson.objectid import ObjectId

# from highlight.api.get_functions import get_users


def register(name, surname, mi, email, langs, login, password, status, vk=None, tg=None, fb=None):
    """
    :param name: obvious
    :param surname: obvious
    :param mi: middle initials
    :param email: obvious
    :param langs: user languages
    :param login: obvious
    :param password: obvious
    :param status: status translator/chief/both
    :return: user id or None if failed
    """

    a = {"name": name,
         "surname": surname,
         "mi": mi,
         "email": email,
         "langs": langs,
         "login": login,
         "password": password,
         "status": status,
         "vk": vk,
         "tg": tg,
         "fb": fb,
         "translated": 0,
         "pieces": [],
         "verified": False}

    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    try:
        user_id = acc.insert_one(a).inserted_id
        return ("OK", user_id)
    except pm.errors.DuplicateKeyError:
        return ("1000",)


def log_in(login, password):
    """
    :param login:
    :param password:
    :return: user id or None if failed
    """
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    user = acc.find_one({"login": login})
    if not (user is None):
        if user["password"] == password:
            if user["verified"]:
                return {"id": str(user["_id"]), "code": "0"}
            else:
                return {"code": "2002"}
        else:
            return {"code": "2001"}
    else:
        return {"code": "2000"}


def verify(user_id, key, decision="ADMITTED"):
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    if key == "NICE":
        if decision == "ADMITTED":
            acc.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"verified": True}})
        else:
            acc.delete_one({"_id": ObjectId(user_id)})
        return ("OK",)
    else:
        return ("2004",)


def test():
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    # acc.create_index([('login', pm.ASCENDING)], unique=True)
    did = register("seva", "obvious", "obvious", "obvious", "obvious", "seva", "tester", "obvious")
    # print(did)
    did1 = get_users()[0]
    print(did1["_id"])
    verify(did1["_id"], "NICE")
    # print(log_in("seva", "tester"))
    # for i in acc.find():
    #     pprint.pprint(i)
    # acc.delete_one({"_id": log_in("seva", "tester")})


if __name__ == '__main__':
    test()