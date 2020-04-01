from pymongo import MongoClient
import pymongo as pm
from bson.objectid import ObjectId

from . import get_functions as gf


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
    :return: user id or error if failed
    :structure: dict('code': string, 'document': string)
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
        return {"id": str(user_id), "code": "OK"}
    except pm.errors.DuplicateKeyError:
        return {"code": "1000"}


def log_in(login, password, type=None):
    """
    :param login:
    :param password:
    :return: user id or error if failed
    :structure: dict('code': string, 'document': string)
    """
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    if type is None:
        user = acc.find_one({"login": login})
    else:
        user = acc.find_one({"login": login, "status": type})
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


def verify(user_login, decision="ADMITTED"):
    """
    :param user_login: user login
    :param decision: confirm or delete user (ADMITTED/anything else)
    :return: code OK
    :structure: dict('code': string)
    """
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    if decision == "ADMITTED":
        acc.update_one(
            {"login": user_login},
            {"$set": {"verified": True}})
    else:
        acc.delete_one({"login": user_login})
    return {"code": "OK"}


def test():
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    # acc.drop()
    # acc.create_index('login', unique=True)
    # did = register("1d", "g", "gf", "1s", "1s", "loo", "nndcxd1b", "gfgf")
    # print(did)
    # did1 = gf.get_users()[0]
    # print(did1["_id"])
    # verify(did1["_id"])
    # print(log_in("seva", "tester")["id"])
    # for i in acc.find():
    #     print(i)
    # acc.delete_one({"_id": ObjectId(log_in("seva", "tester")["id"])})
    # acc.delete_one({"_id": ObjectId("5e837394e1b35a1442eee197")})



if __name__ == '__main__':
    test()