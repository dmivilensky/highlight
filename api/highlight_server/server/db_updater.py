from functools import partial

from pymongo import MongoClient

if __name__ == "__main__":
    import main as mn
else:
    from . import main as mn


class DbUpdater:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.highlight
        self.docs = self.db.files_info
        self.accounts = self.db.accounts

    def update_docs(self, fields, any_file=False):
        if any_file:
            all_docs = self.docs.find({})
        else:
            all_docs = self.docs.find({"status": {"$in": ["WAITING_FOR_TRANSLATION", "NEED_CHECK", "TRANSLATED"]}})
        outdated_docs = list(map(partial(self.process_db_file, fields=fields), filter(partial(self.filter_db_files, fields=fields), list(all_docs))))

        for d in outdated_docs:
            self.docs.replace_one({"_id": d["_id"]}, d)

        return outdated_docs

    def process_db_file(self, doc, fields):
        if "__update_functions__" in fields.keys():
            uf = fields["__update_functions__"]
            if type(uf) == list:
                for f in uf:
                    doc = f(doc)
            elif callable(uf):
                doc = uf(doc)

        for field in fields.keys():
            if not(field in {"__update_functions__", "__criteria__"}):
                doc[field] = fields[field]
        return doc

    def filter_db_files(self, doc, fields):
        if not("__criteria__" in fields.keys()) or fields["__criteria__"](doc):
            for field in fields.keys():
                if field != "__update_functions__" and not(field in doc.keys()) or field == "__file_version__" and (not("__file_version__" in doc.keys()) or doc["__file_version__"] != fields["__file_version__"]):
                    return True
        return False

    def update_accounts(self, fields):
        all_accs = self.accounts.find({})
        outdated_accs = list(map(partial(self.process_db_file, fields=fields),
                                 filter(partial(self.filter_db_files, fields=fields), list(all_accs))))
        for a in outdated_accs:
            self.accounts.replace_one({"_id": a["_id"]}, a)

        return outdated_accs


def test():
    upd = DbUpdater()
    def m(a):
        a["kkk"] = 509
        return a
    doc = {"name": "lol", "eat": True}
    doca2 = {"name": "kool", "__file_version__": "qwe"}
    fields1 = {"name": "lol", "eat": True}
    f2 = {"name": "kool", "__file_version__": "qwe"}
    f3 = {"name": "kool", "__file_version__": "qwe1"}
    f4 = {"name": "kool1", "__file_version__": "qwe", "__update_functions__": m}
    # assert not upd.filter_db_files(doc, fields1)
    # assert upd.filter_db_files(doca2, fields1)
    # assert not upd.filter_db_files(doca2, f2)
    # assert upd.filter_db_files(doca2, f3)
    # assert not upd.filter_db_files(doca2, f4)
    all_d = [doc, doca2]
    outdated_docs = list(map(partial(upd.process_db_file, fields=f4),
                             filter(partial(upd.filter_db_files, fields=f4), list(all_d))))
    print(outdated_docs)


def run():
    cri = lambda a: a["status"] == "WAITING_FOR_TRANSLATION"
    upd = DbUpdater()
    updf = {"__file_version__": "upd1"}
    ds = upd.update_docs(updf)
    print(ds)
    updf = {"author": "", "journal": "", "journal_link": "", "abstract": "", "__file_version__": "upd1", "__update_functions__": partial(mn.combine_indexing_for_update, is_splitted=True, is_extracted=False)}
    ds = upd.update_docs(updf)
    print(ds)

if __name__ == "__main__":
    # test()
    run()