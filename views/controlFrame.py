import tkinter as tk
from tkinter import ttk
from views.documentInputFrame import DocumentInputFrame
from views.plagiarizedDocumentsFrame import PlagiarizedDocumentsFrame
from managers.documentsManager import DocumentsManager
from tkinter import messagebox

class ControlFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        """container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.columnconfigure(2, weight=1)"""

        # Compute button
        self.btn_compute = ttk.Button(
            self, text="Calcular", command=lambda: self.changeFrame(container, 1)
        )
        
        # blank label (to pad the compute button)
        self.label_empty = ttk.Label(self)

        # Return to document input button
        self.btn_return = ttk.Button(
            self, text="Regresar", command=lambda: self.changeFrame(container, 0)
        )

        self.frame = DocumentInputFrame(container)
        #self.frame.grid(column=1, row=0)
        #self.label_empty.grid(column=1, row=7, ipady=10)
        #self.btn_compute.grid(column=1, row=8)
        self.btn_compute.pack()
        self.pack()

    def changeFrame(self, container, i):
        self.cleanFrame(container)
        if i == 0:
            self.frame = DocumentInputFrame(container)
            self.frame.pack(expand=True, fill="both")
            self.btn_compute.pack()
            self.pack()
        elif i == 1:
            if self.frame.isReadyToCompute():
                #doc_man = DocumentManager(self.frame.obj_filename, self.frame.docs_directory)
                #doc_man = DocumentsManager(self.frame.obj_filename, self.frame.docs_directory)
                doc_man = DocumentsManager(self.frame.getOptions()["main_doc"], self.frame.getOptions()["dir"])
                """self.frame = PlagiarizedDocumentsFrame(
                    container, doc_man, self.frame.getKNeighborsDocs(), self.frame.getKNeighborsPara(),
                    self.frame.getNgram(), self.frame.getPlagiarismPercentage())"""
                self.frame = PlagiarizedDocumentsFrame(
                    container, doc_man, self.frame.getOptions())
                self.frame.pack(expand=True, fill="both")
                self.btn_return.pack()
                self.pack()
            else:
                messagebox.showerror(
                    "Error", 
                    "Ingrese un directorio con documentos .docx y un documento .docx objetivo")
        
    
    def all_children(self, window) :
        _list = window.winfo_children()

        for item in _list :
            if item.winfo_children() :
                _list.extend(item.winfo_children())

        return _list


    def cleanFrame(self, window):
        widget_list = self.all_children(window)
        for item in widget_list:
            item.pack_forget()
        self.btn_compute.pack_forget()
        self.btn_return.pack_forget()
        self.frame.pack_forget()
        self.pack_forget()