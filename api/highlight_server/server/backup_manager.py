import mongobackup as mb

BACKUPS_MONGO_ = "../../../backups/mongo/"


class Backup_Manager:
    def __init__(self):
        pass

    def backup(self, where=("%s" % BACKUPS_MONGO_), db="highlight", mu="a", mp="a"):
        mb.backup(mu, mp, where, database=db)

    def restore(self, where=("%s" % BACKUPS_MONGO_), what="backup" + ".tbz", mu="a", mp="a"):
        mb.restore(mu, mp, where+what)


if __name__ == '__main__':
    manager = Backup_Manager()
    manager.backup()