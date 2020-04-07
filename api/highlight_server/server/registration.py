from pymongo import MongoClient
import pymongo as pm
from bson.objectid import ObjectId

from .main import is_there_any_body
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
    :param status: status translator/chief/both/verif
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


def update_acc(params):
    """
    :param params: params you want to have updated and current password
    :return: code
    """
    uid = params["id"]
    name = params["name"] if "name" in params.keys() else None
    surn = params["surname"] if "surname" in params.keys() else None
    mi = params["mi"] if "mi" in params.keys() else None
    email = params["email"] if "email" in params.keys() else None
    login1 = params["login"] if "login" in params.keys() else None
    opwd = params["password"]
    pwd = params["npassword"] if "npassword" in params.keys() else None
    stat = params["status"] if "status" in params.keys() else None
    langs = params["languages"] if "languages" in params.keys() else None
    vk = params["vk"] if "vk" in params.keys() else None
    fb = params["fb"] if "fb" in params.keys() else None
    tg = params["tg"] if "tg" in params.keys() else None
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    usr = acc.find_one({"_id": ObjectId(uid), "password": opwd})
    if is_there_any_body(uid):
        if usr is None:
            return {"code": "2001"}
        a = {"name": name if not(name is None) else usr["name"],
             "surname": surn if not(surn is None) else usr["surname"],
             "mi": mi if not(mi is None) else usr["mi"],
             "email": email if not(email is None) else usr["email"],
             "login": login1 if not(login1 is None) else usr["login"],
             "password": pwd if not(pwd is None) else usr["password"],
             "status": stat if not(stat is None) else usr["status"],
             "langs": langs,
             "vk": vk if not(vk is None) else usr["vk"],
             "tg": tg if not(tg is None) else usr["tg"],
             "fb": fb if not(fb is None) else usr["fb"],
             "verified": True if stat is None and langs is None and name is None else False}
        acc.update_one({"_id": ObjectId(uid)},
                                {"$set": a})
        return {"code": "OK"}
    else:
        return {"code": "2003"}


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
                return {"id": str(user["_id"]), "code": "OK"}
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