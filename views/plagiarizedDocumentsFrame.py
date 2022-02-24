import tkinter as tk
from tkinter import ttk
from views.verticalScrolledFrame import VerticalScrolledFrame
from views.paragraphComparissonWindow import ParagraphComparissonWindow
from views.paragraphComparissonFrame import ParagraphComparissonFrame
from managers.neighborsManager import NeighborsManager

class PlagiarizedDocumentsFrame(ttk.Frame):
    def __init__(self, container, doc_man, options):
        super().__init__(container)

        self.doc_man = doc_man
        self.options = options

        self.neighbors_man = NeighborsManager(
            [self.doc_man.getMainDocument().getCleanText()], 
            self.doc_man.documentsToCleanText(),
            self.options["kn_docs"],
            self.options["ngrams"],
            self.options["metric"])

        # title label 
        self.label_title = ttk.Label(
            self, 
            text="Similar Documents",
            font=("Helvetica", 14))
        self.label_title.pack()

        # scrollable frame
        self.scframe = VerticalScrolledFrame(self)

        # array of buttons
        self.btn_documents = []

        # Get neighbors
        results_dist, results_ix = self.neighbors_man.getNeighbors()

        # Iterate through the results and create buttons if the
        # plagiarism percentage of the document is equal or higher
        # than the minimum specified in the previous frame.
        for ix, dist in zip(results_ix[0], results_dist[0]):
            percentage_dist = (1 - dist) * 100
            dist_str = '{:.2f}%'.format(percentage_dist)
            ix_str = self.doc_man.getDocumentFilename(ix)
            if percentage_dist > self.options["percentage"]:
                self.btn_documents.append(
                    tk.Button(self.scframe.interior, height=1, width=20, relief=tk.FLAT, 
                    bg="gray99", fg="black",
                    font="Dosis", text=ix_str + " (" + dist_str + ")", 
                    command=self.documentBtnClickHandler(ix))
                    )
                self.btn_documents[-1].pack(padx=10, pady=5, side=tk.TOP, fill="both", expand="True")

        self.scframe.pack(expand=True, fill="both")

        self.pack()

    def documentBtnClickHandler(self, ix):
        return lambda: self.openParagraphComparissonWindow(ix)
    
    def openParagraphComparissonWindow(self, ix):
        print(self.doc_man.getMainDocument().getFilename())
        pcw = ParagraphComparissonWindow()
        pcf = ParagraphComparissonFrame(
            pcw, self.doc_man.getMainDocument(), 
            self.doc_man.getCompDocument(ix), self.options)