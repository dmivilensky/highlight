from pymongo import MongoClient
import csv


class IndexProcessor:
    def __init__(self, root=""):
        client = MongoClient()
        self.db = client.highlight
        self.index_storage = self.db.index_holder
        self.index_file = self.index_storage.find_one({"name": "index"})
        self.path = root
        self.w2a = self.index_file["word2articles"]

    def save(self, readable=False, pizdeition=False):
        csv_columns = ['№', 'Word', 'Articles']
        csv_data = []

        if readable:
            ls = self.db.files_info

        co = 1
        for k in self.w2a.keys():
            if readable:
                atc = list()
                for i in self.w2a[k]:
                    d = ls.find_one({"_id": i})
                    try:
                        atc.append((d if pizdeition else d["name"]))
                    except TypeError:
                        atc.append(d)
            else:
                atc = self.w2a[k]
            csv_data.append({'№': co, 'Word': k, 'Articles': atc})
            co += 1
            csv_data = sorted(csv_data, key=lambda a: a["Word"].lower())

        with open(self.path + ("r_" if readable else "u_") + "index.csv", "w+") as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            for data in csv_data:
                writer.writerow(data)


def test():
    ip = IndexProcessor()
    ip.save()
    ip.save(readable=True)

if __name__ == "__main__":
    test()