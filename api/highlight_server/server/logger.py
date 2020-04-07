from os import getcwd
from os.path import sep
from pprint import pformat


class Logger:
    def __init__(self, root=getcwd()):
        self.path = root + sep
    
    def log(self, category, status, message):
        log_filename = 'log_' + category + '.txt'
        isobject = type(message) != str
        
        with open(self.path + log_filename, 'a+') as file:
            file.write('{0}: {1}'.format(
                status.upper(),
                message if not isobject 
                else pformat(message, indent=4)
            ))