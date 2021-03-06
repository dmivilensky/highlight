from pymongo import MongoClient
import pymongo as pm
from bson.objectid import ObjectId

from .logger import Logger

ARTICLES_PER_PAGE = 15


def get_from_db(search, tags, status=None, substatus=None, page=-1):
    """
    :param search: user input
    :param tags: tags
    :param status: list of statuses
    :param substatus: substatus for translated
    :param page: page number
    :return: matching docs of id, name, tags, status, path, etc.
    :structure: dict('code': string, 'document': list(type=WaitingForTranslation or type=NeedCheck or type=Translated)
    """
    if status is None:
        status = {"TRANSLATED", "NEED_CHECK", "WAITING_FOR_TRANSLATION"}

    if type(page) == str:
        try:
            page = int(page)
        except ValueError:
            lgr = Logger()
            lgr.log("log", "Searching: ", "page: " + page)
            page = -1

    client = MongoClient()
    db = client.highlight
    lang_storage = db.files_info
    index = db.index_holder
    w2a = index.find_one({"name": "index"})["word2articles"] if not(index.find_one({"name": "index"}) is None) else dict()
    search_set = set(search.lower())
    hl = []
    for i in search.split(" "):
        hl.extend(map(lambda a: a.lower(), i.split("_")))
    search_set_words = set(hl)
    search_tags = set(tags.lower().split(","))
    matching_docs = list()
    for doc in lang_storage.find({"status": {"$in": ["TRANSLATED", "NEED_CHECK", "WAITING_FOR_TRANSLATION"]}}):
        doc_stat = doc["status"]
        relev = 0
        if doc_stat == "TRANSLATED":
            relev += 100
        elif doc_stat == "NEED_CHECK":
            relev += 50
        elif doc_stat == "WAITING_FOR_TRANSLATION":
            relev += 0
        doc_name_set = set(doc["name"].lower())
        doc_tags_set = set(doc["tags"].lower().split(","))
        doc_id = doc["number"]
        tag_inrsc = search_tags.intersection(doc_tags_set)
        name_inrsc = search_set.intersection(doc_name_set)

        if len(search_tags) > 0:
            relev += len(tag_inrsc) * 7

            if doc["lang"] in search_tags:
                relev += 4

        if len(search_set) > 0:
            relev += len(name_inrsc) * 20

            if doc_id in search_set_words:
                relev += 8
            
            if doc["name"].find(search) != -1:
                relev += 50
            for w in search_set_words:
                if w in w2a.keys():
                    if doc["_id"] in w2a[w]:
                        relev += 15

        matching_docs.append((relev, doc))

    if substatus is None:
        return {"code": "OK", "document": list(d for n, d in sorted(matching_docs, key=lambda t: t[0], reverse=True) if d["status"] in status)[(page * ARTICLES_PER_PAGE if page >= 0 else 0):((page + 1) * ARTICLES_PER_PAGE if page >= 0 else 50)]}
    else:
        return {"code": "OK", "document": list(
            d for n, d in sorted(matching_docs, key=lambda t: t[0], reverse=True) if d["status"] in status if "substatus" in d.keys() if d["substatus"] == substatus)[(page * ARTICLES_PER_PAGE if page >= 0 else 0):((page + 1) * ARTICLES_PER_PAGE if page >= 0 else 50)]}


def get_for_chief_from_db(search, tags, page=-1):
    """
    :param search: same as get_from_db
    :param tags: same ag get_from_db
    :param page: page
    :return: same as get_from_db
    """
    return get_from_db(search, tags, status={"NEED_CHECK"}, substatus="DONE", page=page)


def get_for_verst_from_db(search, tags, page=-1):
    """
    :param search: same as get_from_db
    :param tags: same ag get_from_db
    :param page: page
    :return: same as get_from_db
    """
    return get_from_db(search, tags, substatus="MARKUP", page=page)


def get_users():
    """
    :return: all unverified users
    :structure: dict('code': string, 'document': list(type=User))
    """
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    return {"code": "OK", "document": list(acc.find({"verified": False}))}


def get_users_by_doc_or_piece(rid):
    """
    :param rid: file or piece mongo id
    :return: users working on corresponding document
    :structure: dict('code': string, 'document': list(type=User))
    """
    added_ids = []
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    l_s = db.files_info
    ps = l_s.find_one({"_id": ObjectId(rid)})
    pieces = list(l_s.find({"name": ps["name"], "number": ps["number"], "lang": ps["lang"], "status": "PIECE"}))
    res = []
    added_ids = []
    for p in pieces:
        if p["translator"] not in added_ids:
            res.append(acc.find_one({"_id": ObjectId(p["translator"])}))
            added_ids.append(p["translator"])
    return {"code": "OK", "document": res}


def get_docs_and_trans():
    """
    :return: docs (translated and not) and translator count
    :structure: dict('code': string, 'document': dict('documents': int, 'translators': int, 'translated_documents': int)
    """
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    l_s = db.files_info
    return {"code": "OK", "document": {"documents": l_s.count_documents({"status": "WAITING_FOR_TRANSLATION"}), "translators": acc.count_documents({"status": {"$in": ["translator", "both"]}, "verified": True}), "translated_documents": l_s.count_documents({"status": "TRANSLATED"})}}


def get_translators_stat():
    """
    :return: all verified users
    :structure: dict('code': string, 'document': list(type=User)
    """
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    return {"code": "OK", "document": list(acc.find({"status": {"$in": ["translator", "both"]}, "verified": True}))}


def get_file_stat():
    """
    :return: file name, file pieces number (done and undone), importance
    :structure: dict('code': string, 'document': list(dict('name': string, 'status': string, 'importance': int, 'pieces_info': dict('done_pieces': int, 'all_pieces': int) (or dict() if file is translated))))
    """
    client = MongoClient()
    db = client.highlight
    l_s = db.files_info
    docs = []
    for t in l_s.find({"status": {"$in": ["TRANSLATED", "NEED_CHECK", "WAITING_FOR_TRANSLATION"]}}):
        if t["status"] in ["TRANSLATED", "NEED_CHECK"]:
            docs.append({"_id": str(t["_id"]), "name": t["name"], "pieces_info": {}, "status": t["status"], "importance": t["importance"] if "importance" in t.keys() else 0})
        else:
            done_pieces = 0
            for p in l_s.find({"name": t["name"], "number": t["number"], "lang": t["lang"], "status": "PIECE", "translation_status": "DONE"}):
                done_pieces += p["piece_end"] - p["piece_begin"] + 1
            docs.append({"_id": str(t["_id"]), "name": t["name"], "pieces_info": {"done_pieces": done_pieces, "all_pieces": t["piece_number"]}, "status": t["status"], "importance": t["importance"]})
    return {"code": "OK", "document": docs}


def get_pieces_stat():
    """
    :return: pieces
    :structure: dict('code': string, 'document': list(dict('name': string, 'status': string, 'importance': int, 'pieces_info': dict('done_pieces': int, 'all_pieces': int) (or dict() if file is translated))))
    """
    client = MongoClient()
    db = client.highlight
    l_s = db.files_info
    accs = db.accounts
    docs = []
    try:
        for t in l_s.find({"status": "PIECE", "translation_status": "UNDONE"}):
            acct = accs.find_one({"_id": ObjectId(t["translator"])})
            docs.append({
                "translator": acct["name"], 
                "name": t["name"], 
                "date": str(t["lastModified"]),
                "pb": t["piece_begin"],
                "pe": t["piece_end"]
                })
    except Exception as e:
        docs.append(str(e))
    return {"code": "OK", "document": docs}


def test():
    client = MongoClient()
    db = client.highlight
    acc = db.accounts


if __name__ == '__main__':
    test()