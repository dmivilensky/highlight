import mongobackup as mb

class Backup_Manager:
    def __init__(self):
        pass

    def backup(self, where="/var/www/html/highlight.spb.ru/backups/mongo/", db="highlight", mu="", mp=""):
        mb.backup(mu, mp, where, database=db)

    def restore(self, where="/var/www/html/highlight.spb.ru/backups/mongo/", what="backup" + ".tbz", mu="", mp=""):
        mb.restore(mu, mp, where+what)


if __name__ == '__main__':
    manager = Backup_Manager()
    manager.backup()