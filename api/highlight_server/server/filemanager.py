from enum import Enum

from pickle import dump, load
from os import getcwd, remove
import os
from os.path import sep

from PyPDF2 import PdfFileWriter, PdfFileReader
from docx2pdf import convert


class MergeStatus(Enum):
    composition = 'merged'
    piece = 'piece'


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
        
        return pages
    
    extention = staticmethod(lambda filename: filename.split('.')[-1])
    is_pdf = staticmethod(lambda filename: extention(filename) == '.pdf')
        
    def compose_files(self, files, status=MergeStatus.composition, delete=True):
        merged_filename = None
        
        try:
            writer = PdfFileWriter()
            streams = []
            
            for filename in files:
                mergeable_filename = self.docx_to_pdf(filename)
                
                streams.append(open(self.path + filename, 'rb'))
                reader = PdfFileReader(streams[-1])
                for page in range(reader.numPages):
                    writer.addPage(reader.getPage(page))
                
            merged_filename = '{0}_{1}.pdf'.format(status.value, self.last_index)
            with open(self.path + merged_filename, 'wb') as output:
                writer.write(output)
                
            for stream in streams:
                stream.close()
        except FileNotFoundError as file_error:
            print('File not found: {0}'.format(file_error))
        else:
            self.update_state()
            if delete:
                self.delete_files(*files)
        
        return merged_filename
    
    def docx_to_pdf(self, file, delete=True):
        if is_pdf(file):
            return file
        
        new_filename = 'result_{0}.pdf'.format(self.last_index)
        convert(self.path + file, self.path + new_filename)
        self.update_state()
        if delete:
            delete_files(file)
        
        return new_filename
    
    def delete_files(self, *files):
        for file in files:
            remove(self.path + file)

    def create_path(self, fname):
        name = (fname + '_{0}.pdf').format(self.last_index)
        self.update_state()
        return name

