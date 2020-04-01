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
    :param translator: mongo id of translator or list of mongo ids of translators
    :param piece_begin: piece beginning paragraph
    :param piece_end: piece ending paragraph
    :param txt: piece text
    :param translated_txt: translated piece
    :param translation_status: whether translation done or not (DONE/UNDONE)
    :param chief: translates verifier

Types:
    User:
        {"name": name,
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
         
    WaitingForTranslation:
        {"number": number,
        "name": name,
        "lang": lang,
        "orig_path": orig_path,
        "piece_number": pieces_count,
        "tags": tags,
        "importance": importance,
        "status": status,
        "lastModified": datetime.datetime.utcnow()}
        
    WaitingPiece:
        {"number": number,
        "name": name,
        "lang": lang,
        "txt": txt,
        "index": index,
        "freedom": freedom,
        "status": status,
        "lastModified": datetime.datetime.utcnow()}
        
    Piece:
        {"number": number,
        "name": name,
        "lang": lang,
        "piece_begin": piece_begin,
        "piece_end": piece_end,
        "txt": txt,
        "translated_txt": translated_txt,
        "translator": translator,
        "to_lang": to_lang,
        "translation_status": translation_status,
        "status": status,
        "lastModified": datetime.datetime.utcnow()}
    
    NeedCheck or Translated:
    {"number": number,
    "name": name,
    "lang": lang,
    "path": path,
    "orig_path": orig_path,
    "to_lang": to_lang,
    "tags": tags,
    "translator": translator,
    "chief": chief,
    "status": status,
    "lastModified": datetime.datetime.utcnow()}
    
Each function has an explanation of returning params and types (field structure)
Syntax notification: if type is builtin, it is stated as it is (string/int and etc.), but if type is from here it is stated type=TYPE (where TYPE in Types)