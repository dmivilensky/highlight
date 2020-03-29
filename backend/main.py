import pprint
from bson.objectid import ObjectId

from pymongo import MongoClient
import pymongo as pm

"""
responses:
:errors 1000: can't register user
:errors 2000: no account matching login
:errors 2001: wrong password
:errors 2002: account not verified
:errors 3000: pieces already taken
:errors 3001: not a single piece
:success OK: operation done
"""

BOOL_TO_ABB = ["ENG", "GER", "FRE", "ESP", "ITA", "JAP", "CHI"]


def register(name, surname, mi, email, langs, login, password, is_not_translator):
    """
    :param name: obvious
    :param surname: obvious
    :param mi: middle initials
    :param email: obvious
    :param langs: user languages
    :param login: obvious
    :param password: obvious
    :param is_not_translator: status translator/verifier
    :return: user id or None if failed
    """

    if is_not_translator:
        stat = "Translator"
    else:
        stat = "Chief"

    a = {"name": name,
         "surname": surname,
         "mi": mi,
         "email": email,
         "langs": langs,
         "login": login,
         "password": password,
         "status": stat,
         "verified": False}

    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    try:
        user_id = acc.insert_one(a).inserted_id
        return user_id
    except pm.errors.DuplicateKeyError:
        return None


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
        if user["password"] == password and user["verified"]:
            return user["_id"]
        else:
            return None
    else:
        return None


def Verify(user_id, key):
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    if key == "NICE":
        acc.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"verified": True}})


def push_to_file_storage(path, file):
    """
    :param path: file path
    :param file: file
    :return: Nothing
    """
    pass


def split_to_pieces(number, name, status, lang):
    """
       :param number: id number of document
       :param name: file name
       :param status: one of TRANSLATED/NEED_CHECK/PIECE/WAITING_PIECE/WAITING_FOR_TRANSLATION
       :param lang: language one of ENG, RUS, ESP, JAP, etc.
       :return: Nothing
   """
    pass


def push_to_db(number, name, status, lang, importance=None, pieces_count=None, path=None, orig_path=None, file_data=None, tags=None,
               freedom=None, index=None, to_lang=None, translator=None, piece_begin=None, piece_end=None, txt=None,
               translated_txt=None, chief=None):
    """
    :param number: id number of document
    :param name: file name
    :param status: one of TRANSLATED/NEED_CHECK/PIECE/WAITING_PIECE/WAITING_FOR_TRANSLATION
    :param lang: language one of ENG, RUS, ESP, JAP, etc.
    :param importance: number, how this doc is needed
    :param pieces_count: amount of pieces in document
    :param path: file path in the filesystem
    :param orig_path: path to original file
    :param file_data: file
    :param tags: additional tags
    :param freedom: is piece not taken True/False
    :param index: piece index
    :param to_lang: language file is translated to
    :param translator: mongo id of translator
    :param piece_begin: piece beginning paragraph
    :param piece_end: piece ending paragraph
    :param txt: piece text
    :param translated_txt: translated piece
    :param chief: translates verifier
    :return: file mongo id in DB
    """

    file = None
    client = MongoClient()
    db = client.highlight

    if status == "WAITING_FOR_TRANSLATION":
        file = {"number": number,
                "name": name,
                "lang": lang,
                "orig path": orig_path,
                "tags": tags,
                "importance": importance,
                "status": status}
        push_to_file_storage(path, file_data)
        split_to_pieces(number, name, status, lang)

    elif status == "WAITING_PIECE":
        file = {"number": number,
                "name": name,
                "lang": lang,
                "txt": txt,
                "index": index,
                "freedom": freedom,
                "status": status}

    elif status == "PIECE":
        file = {"number": number,
                "name": name,
                "lang": lang,
                "piece begin": piece_begin,
                "piece end": piece_end,
                "txt": txt,
                "translated txt": translated_txt,
                "translator": translator,
                "to lang": to_lang,
                "status": status}

    elif status == "NEED_CHECK":
        file = {"number": number,
                "name": name,
                "lang": lang,
                "path": path,
                "orig path": orig_path,
                "to lang": to_lang,
                "tags": tags,
                "translator": translator,
                "status": status}
        push_to_file_storage(path, file_data)

    elif status == "TRANSLATED":
        file = {"number": number,
                "name": name,
                "lang": lang,
                "path": path,
                "orig path": orig_path,
                "to lang": to_lang,
                "tags": tags,
                "translator": translator,
                "chief": chief,
                "status": status}
        push_to_file_storage(path, file_data)

    lang_storage = db.files_info
    file_id = lang_storage.insert_one(file).inserted_id

    return file_id


def update_pieces(user_id, doc_id, pieces_ids, to_lang=None):
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    pieces = list()
    document = lang_storage.find_one({"_id": ObjectId(doc_id)})
    no_intersections = True
    for piece_id in pieces_ids:
        p = lang_storage.find_one({"_id": ObjectId(piece_id)})
        pieces.append(p)
        if not p["freedom"]:
            no_intersections = False
            return "3000"
    pieces = sorted(pieces, key=lambda a: a["index"])
    txt = pieces[0]["txt"]
    for i in range(1, len(pieces)):
        if pieces[i]["index"] - pieces[i - 1]["index"] != 1:
            return "3001"
        txt.join("\n".join(pieces[i]["txt"]))
    begin_index = pieces[0]["index"]
    end_index = pieces[-1]["index"]
    if not no_intersections:
        return "3000"
    else:
        push_to_db(number=document["number"],
                   name=document["name"],
                   lang=document["lang"],
                   piece_begin=begin_index,
                   piece_end=end_index,
                   txt=txt,
                   translated_txt=None,
                   translator=user_id,
                   to_lang=to_lang,
                   status="PIECE")
        for p in pieces:
            lang_storage.update_one({"_id": p["_id"]}, {"$set": {"freedom": False}})
        return "OK"


def update_docs(doc, lang, tags):
    pass


def find_pieces(user_id):
    """
    :param user_id: user mongo id
    :return: all pieces taken by user
    """
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    pieces = lang_storage.find({"translator": ObjectId(user_id), "status": "PIECE"})
    return pieces


def find_doc_by_lang(lang):
    """
    :param lang: language
    :return: tuple where first element is document name, second is list of pieces for this document
    """
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    docs = dict()
    for piece in lang_storage.find({"lang": lang, "status": "WAITING_PIECE"}):
        if piece["name"] in docs.keys():
            docs[piece["name"]].append(piece)
        else:
            docs[piece["name"]] = [piece]

    out = list()
    for key in docs.keys():
        docs[key] = sorted(docs[key], key=lambda a: a["index"])
        out.append((key, docs[key]))

    return out


def get_from_db(search, tags):
    """
    :param search: user input
    :param tags: tags
    :return: matching docs of id, name, tags, status, path, etc.
    """
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    search_set = set(search)
    hl = []
    for i in search.split(" "):
        hl.extend(i.split("_"))
    search_set_words = set(hl)
    search_tags = set(tags.split(","))
    matching_docs = list()
    for doc in lang_storage.find():
        doc_stat = doc["status"]
        if doc_stat == "TRANSLATED" or doc_stat == "NEED_CHECK" or doc_stat == "WAITING_FOR_TRANSLATION":
            relev = 0
            if doc_stat == "TRANSLATED":
                relev += 100
            elif doc_stat == "NEED_CHECK":
                relev += 50
            elif doc_stat == "WAITING_FOR_TRANSLATION":
                relev += 0
            doc_name_set = set(doc["name"])
            doc_tags_set = set(doc["tags"])
            doc_id = doc["number"]
            tag_inrsc = search_tags.intersection(doc_tags_set)
            name_inrsc = search_set.intersection(doc_name_set)

            if len(search_tags) > 0:
                if len(tag_inrsc) >= len(search_tags) * 0.8:
                    relev += len(tag_inrsc) / len(search_tags) * 7

                if doc["lang"] in search_tags:
                    relev += 4

            if len(search_set) > 0:
                if len(name_inrsc) >= 0.6 * len(doc_name_set):
                    relev += len(name_inrsc) / len(doc_name_set) * 10

                if doc_id in search_set_words:
                    relev += 8

            if relev > 0:
                matching_docs.append((relev, doc))

    return list(d for n, d in sorted(matching_docs, key=lambda t: t[0], reverse=True))


def test():
    # client = MongoClient()
    # db = client.highlight
    # acc = db.accounts
    # acc.create_index([('login', pm.ASCENDING)], unique=True)
    # id = register("seva", "obvious", "obvious", "obvious", "obvious", "seva", "tester", "obvious")
    # print(id)
    # # Verify(id, "NICE")
    # print(log_in("seva", "tester"))
    # for i in acc.find():
    #     pprint.pprint(i)
    # acc.delete_one({"_id": log_in("seva", "tester")})
    a = [0, 1, 2]
    pprint.pprint(a[-1])


if __name__ == '__main__':
    test()
