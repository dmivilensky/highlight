from pymongo import MongoClient
import pymongo as pm
from bson.objectid import ObjectId


def find_pieces(user_id):
    """
    :param user_id: user mongo id
    :return: all pieces taken by user
    """
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    pieces = sorted(lang_storage.find({"translator": user_id, "status": "PIECE", "translation status": "UNDONE"}),
                    key=lambda a: a["lastModified"], reverse=True)
    return {"code": "OK", "document": pieces}


def find_doc_by_lang(lang):
    """
    :param lang: language
    :return: array of tuples where first element is document name, second is list of pieces for this document
    :description: finds pieces as docs by language
    """
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    docs = dict()
    docs_o = dict()
    for piece in lang_storage.find({"lang": lang, "status": "WAITING_PIECE"}):
        orig_doc = lang_storage.find_one({"name": piece["name"], "number": piece["number"], "lang": piece["lang"], "status": "WAITING_FOR_TRANSLATION"})
        if piece["name"] in docs.keys():
            docs[piece["name"]].append(piece)
        else:
            docs[piece["name"]] = [piece]
            docs_o[piece["name"]] = orig_doc

    out = list()
    for key in docs.keys():
        docs[key] = sorted(docs[key], key=lambda a: a["index"])
        out.append({"name": key, "pieces": docs[key], "doc": docs_o[key]})
    out = sorted(out, key=lambda a: a[2], reverse=True)

    return {"code": "OK", "document": out}


def find_complete_docs_by_lang(lang):
    """
    :param lang: language
    :return: array of docs (id, name, tags, progress)
    :description: finds docs by language
    """
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    docs = list()
    for doc in lang_storage.find({"lang": lang, "status": { "$in": ["WAITING_FOR_TRANSLATION", "NEED_CHECK", "TRANSLATED"]}}):
        if doc["status"] in {"NEED_CHECK", "TRANSLATED"}:
            docs.append({"id": doc["_id"], "name": doc["name"], "tags": doc["tags"], "status": 1})
        else:
            pieces_count = doc["piece number"]
            taken_pieces_indexes = []
            pss = lang_storage.find({"number": doc["number"], "name": doc["name"], "lang": doc["lang"], "status": "PIECE",
                                     "translation status": "DONE"})
            for p in sorted(pss, key=lambda a: a["piece begin"]):
                taken_pieces_indexes.extend(range(p["piece begin"], p["piece end"] + 1))
            docs.append({"id": doc["_id"], "name": doc["name"], "tags": doc["tags"], "status": len(taken_pieces_indexes) / pieces_count})

    return {"code": "OK", "document": docs}


def test():
    client = MongoClient()
    db = client.highlight
    acc = db.accounts


if __name__ == '__main__':
    test()