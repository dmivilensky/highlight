from enum import Enum

from pickle import dump, load
from os import getcwd, remove
import os
from os.path import sep

import sys
import os
import subprocess
import re
import time

from PyPDF2 import PdfFileWriter, PdfFileReader
from docx2pdf import convert

if __name__ == "filemanager":
    from logger import Logger
else:
    from .logger import Logger

from subprocess import Popen, PIPE

class MergeStatus(Enum):
    composition = 'merged'
    piece = 'piece'


def convert_to(folder, source, timeout=None):
    args = ['convert_docx_to_pdf_working', source]
    lgr = Logger()
    lgr.log("log", "convertion", " ".join(args))

    # process = subprocess.run(args)
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    lgr.log("log", "convertion", str(p))
    lgr.log("log", "convertion", str(output))
    lgr.log("log", "convertion", str(err))

class FileManager:
    def __init__(self, root=getcwd()):
        self.path = root + sep
        self.state_file = self.path + 'filemanager_state.data'
        self.load_state()
    
    def load_state(self):
        self.last_index = 0
        if os.path.isfile(self.state_file):
            with open(self.state_file, 'rb') as file:
                self.last_index = load(file)
                
    def update_state(self):
        self.last_index += 1
        with open(self.state_file, 'wb') as file:
            dump(self.last_index, file)
            
    def split_pdf(self, file):
        lgr = Logger()
        lgr.log("log", "splitting", "entry FM " + self.path + file)
        try:
            source = PdfFileReader(open(self.path + file, 'rb'))
            pages = []
            
            for i in range(source.numPages):
                page_filename = 'page_{0}.pdf'.format(self.last_index)
                pages.append(page_filename)
                
                page = PdfFileWriter()
                page.addPage(source.getPage(i))
                with open(self.path + page_filename, 'wb') as file:
                    page.write(file)
                
                self.update_state()
        except Exception as e:
            lgr.log("log", "splitting", "exception FM " + str(e))

        return pages
    
    extention = lambda self, filename: filename.split('.')[-1]
    is_pdf = lambda self, filename: filename.split('.')[-1] == '.pdf'
        
    def compose_files(self, files, status=MergeStatus.composition, delete=True):
        merged_filename = None
        lgr = Logger()
        
        try:
            writer = PdfFileWriter()
            streams = []
            
            for filename in files:
                mergeable_filename = self.docx_to_pdf(filename, delete=False)
                lgr.log("log", "update pieces", "try " + self.path + mergeable_filename)
                streams.append(open(self.path + mergeable_filename, 'rb'))
                reader = PdfFileReader(streams[-1])
                for page in range(reader.numPages):
                    writer.addPage(reader.getPage(page))
                lgr.log("log", "update pieces", "ready " + self.path + mergeable_filename)
                
            merged_filename = '{0}_{1}.pdf'.format(status.value, self.last_index)
            with open(self.path + merged_filename, 'wb') as output:
                writer.write(output)
                
            for stream in streams:
                stream.close()
        except FileNotFoundError as file_error:
            lgr.log("log", "File not found", str(file_error))
        except Exception as e:
            lgr.log("log", "Error", str(e))
        else:
            self.update_state()
            if delete:
                self.delete_files(*files)
        
        return merged_filename
    
    def docx_to_pdf(self, file, delete=True):
        try:
            if file.split('/')[-1].split('.')[-1] == 'pdf':
                return file

            convert_to('files/', file.split('/')[-1])
            new_filename = file.split('/')[-1].split('.')[0] + '.pdf'
            if delete:
                self.delete_files(file)
        except Exception as e:
            lgr = Logger()
            lgr.log("log", "docx2pdf", "error" + str(e))
        
        return new_filename
    
    def delete_files(self, *files):
        for file in files:
            remove(self.path + file)

    def create_path(self, fname):
        name = (fname + '_{0}.pdf').format(self.last_index)
        self.update_state()
        return name

