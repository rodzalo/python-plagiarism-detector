from models.document import Document
import glob
import os
import numpy as np

class DocumentsManager():
    def __init__(self, main_doc_path, comp_docs_path):
        self.main_doc = Document(main_doc_path)
        self.comp_docs = self._loadDocsFiles(comp_docs_path)

    def _loadDocsFiles(self, path):
        cwd = os.getcwd()
        os.chdir(path)
        comp_docs_filenames = [os.path.abspath(file) for file in glob.iglob('*.docx')]
        comp_docs = [Document(filename) for filename in comp_docs_filenames]
        os.chdir(cwd)
        return comp_docs

    def documentsToPlainText(self):
        return [doc.getPlainText() for doc in self.comp_docs]

    def documentsToCleanText(self):
        return np.array([doc.getCleanText() for doc in self.comp_docs])

    def getDocumentFilename(self, ix):
        return self.comp_docs[ix].getFilename()

    def getCompDocument(self, ix):
        return self.comp_docs[ix]

    def getCompDocumentsLength(self):
        return len(self.comp_docs)
    
    def getMainDocument(self):
        return self.main_doc
