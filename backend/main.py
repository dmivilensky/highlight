import pprint

from pymongo import MongoClient
import pymongo as pm

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
         "status": stat}

    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    try:
        user_id = acc.insert_one(a).inserted_id
        return user_id
    except pm.errors.DuplicateKeyError:
        return None


def push_to_file_storage(path, file):
    """
    :param path: file path
    :param file: file
    :return: Nothing
    """
    pass


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
    if not(user is None):
        if user["password"] == password:
            return user["_id"]
        else:
            return None
    else:
        return None


def split_to_pieces(number, name, status, lang):
    """
       :param number: id number of document
       :param name: file name
       :param status: one of TRANSLATED/NEED_CHECK/PIECE/WAITING_PIECE/WAITING_FOR_TRANSLATION
       :param lang: language one of ENG, RUS, ESP, JAP, etc.
       :return: Nothing
   """
    pass


def push_to_db(number, name, status, lang, path=None, file_data=None, tags=None, freedom=None, index=None, to_lang=None, translator=None, piece_begin=None, piece_end=None, txt=None, chief=None):
    """
    :param number: id number of document
    :param name: file name
    :param status: one of TRANSLATED/NEED_CHECK/PIECE/WAITING_PIECE/WAITING_FOR_TRANSLATION
    :param lang: language one of ENG, RUS, ESP, JAP, etc.
    :param path: file path in the filesystem
    :param file_data: file
    :param tags: additional tags
    :param freedom: is piece taken
    :param index: piece index
    :param to_lang: language file is translated to
    :param translator: mongo id of translator
    :param piece_begin: piece beginning paragraph
    :param piece_end: piece ending paragraph
    :param txt: piece text
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
                "path": path,
                "tags": tags,
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
                "translator": translator,
                "to lang": to_lang,
                "status": status}

    elif status == "NEED_CHECK":
        file = {"number": number,
                "name": name,
                "lang": lang,
                "path": path,
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
                "to lang": to_lang,
                "tags": tags,
                "translator": translator,
                "chief": chief,
                "status": status}
        push_to_file_storage(path, file_data)

    lang_storage = db.files_info
    file_id = lang_storage.insert_one(file).inserted_id

    return file_id


def get_from_db(number, name, status):
    pass


def test():
    client = MongoClient()
    db = client.highlight
    acc = db.accounts
    acc.create_index([('login', pm.ASCENDING)], unique=True)

    print(register("seva", "obvious", "obvious", "obvious", "obvious", "seva", "tester", "obvious"))
    print(log_in("seva", "tester"))
    for i in acc.find():
        pprint.pprint(i)
    acc.delete_one({"_id": log_in("seva", "tester")})


if __name__ == '__main__':
    test()
