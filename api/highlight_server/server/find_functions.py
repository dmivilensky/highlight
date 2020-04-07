from pymongo import MongoClient
import pymongo as pm
from bson.objectid import ObjectId

ALL_LANGS = ["ENG", "GER", "FRE", "ESP", "ITA", "JAP", "CHI"]


def find_pieces(user_id):
    """
    :param user_id: user mongo id
    :return: all pieces taken by user and undone
    :structure: dict('code': string, 'document': list(type=Piece))
    """
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    pieces = sorted(lang_storage.find({"translator": user_id, "status": "PIECE"}),
                    key=lambda a: a["lastModified"], reverse=True)
    return {"code": "OK", "document": list(pieces)}


def find_piece(piece_id):
    """
    :param piece_id: mongo id of piece
    :return: piece taken by user
    :structure: dict('code': string, 'document': type=Piece)
    """
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    piece = lang_storage.find_one({"_id": ObjectId(piece_id)})
    return {"code": "OK", "document": piece}


def find_doc_by_lang(lang):
    """
    :param lang: language
    :return: array of tuples where first element is document name, second is list of pieces for this document
    :structure: dict('code': string, 'document': list(dict('name': string, 'pieces': list(type=WaitingPiece), 'doc': type=WaitingForTranslation))
    :description: finds pieces as docs and original docs by language
    """
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    docs = dict()
    docs_o = dict()
    if lang in set(ALL_LANGS):
        querya = list(lang_storage.find({"lang": lang, "status": "WAITING_PIECE"}))
    else:
        querya = list(lang_storage.find({"lang": {"$nin": ALL_LANGS}, "status": "WAITING_PIECE"}))
    if len(querya) == 0:
        return {"code": "3100"}
    for piece in querya:
        orig_doc = lang_storage.find_one({"name": piece["name"], "number": piece["number"], "lang": piece["lang"], "status": "WAITING_FOR_TRANSLATION"})
        if (piece["name"]+"#del#"+str(piece["number"])) in docs.keys():
            docs[(piece["name"]+"#del#"+str(piece["number"]))].append(piece)
        else:
            docs[(piece["name"]+"#del#"+str(piece["number"]))] = [piece]
            docs_o[(piece["name"]+"#del#"+str(piece["number"]))] = orig_doc

    out = list()
    for key in docs.keys():
        docs[key] = sorted(docs[key], key=lambda a: a["index"])
        out.append({"name": docs_o[key]["name"], "pieces": docs[key], "doc": docs_o[key]})
    out = sorted(out, key=lambda a: a["doc"]["importance"], reverse=True)

    return {"code": "OK", "document": out}


def find_complete_docs_by_lang(lang):
    """
    :param lang: language
    :return: array of docs (id, name, tags, progress), progress = 1 if all document pieces are translated or number between 0 and 1 - % of translated pieces
    :structure: dict('code': string, 'document': list(dict('id': string, 'name': string, 'tags': (same as were put to db, guess) array, 'progress': int))
    :description: finds docs by language for admin statistics
    """
    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    docs = list()
    for doc in lang_storage.find({"lang": lang, "status": { "$in": ["WAITING_FOR_TRANSLATION", "NEED_CHECK", "TRANSLATED"]}}):
        if doc["status"] in {"NEED_CHECK", "TRANSLATED"}:
            docs.append({"id": doc["_id"], "name": doc["name"], "tags": doc["tags"], "status": 1})
        else:
            pieces_count = doc["piece_number"]
            taken_pieces_indexes = []
            pss = lang_storage.find({"number": doc["number"], "name": doc["name"], "lang": doc["lang"], "status": "PIECE",
                                     "translation_status": "DONE"})
            for p in sorted(pss, key=lambda a: a["piece_begin"]):
                taken_pieces_indexes.extend(range(p["piece_begin"], p["piece_end"] + 1))
            docs.append({"id": doc["_id"], "name": doc["name"], "tags": doc["tags"], "status": len(taken_pieces_indexes) / pieces_count})

    return {"code": "OK", "document": docs}


def test():
    client = MongoClient()
    db = client.highlight
    acc = db.accounts


if __name__ == '__main__':
    test()