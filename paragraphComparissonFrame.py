import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Canvas
from verticalScrolledFrame import VerticalScrolledFrame
from neighborsManager import NeighborsManager

class ParagraphComparissonFrame(ttk.Frame):
    def __init__(self, container, main_doc, comp_doc, options):
        super().__init__(container)

        self.main_doc = main_doc
        self.comp_doc = comp_doc
        self.options = options

        # Load up the paragraphs
        self.main_doc.saveParagraphs()
        self.comp_doc.saveParagraphs()

        # create the scroll frame
        self.vsf_paragraphs = VerticalScrolledFrame(self)
        self.vsf_paragraphs.pack(expand=True, fill="both", side=tk.LEFT)

        # canvas to hold paragraphs comparissons:
        # 2 labels and 2 textareas
        self.cv_paragraph_comp = tk.Canvas(container)
        self.cv_paragraph_comp.pack(side=tk.RIGHT)

        # main doc label
        self.label_main_doc = tk.Label(
            self.cv_paragraph_comp, text=self.main_doc.getFilename())
        self.label_main_doc.pack(side=tk.TOP)

        # main paragraphs textarea
        self.ta_main_doc_paragraphs = scrolledtext.ScrolledText(self.cv_paragraph_comp,
                                            wrap = tk.WORD,  
                                            width = 40,  
                                            height = 15,  
                                            font = ("Verdana", 
                                              12))
        self.ta_main_doc_paragraphs.pack(side=tk.TOP)
                                            
        # comp doc label
        self.label_comp_doc = tk.Label(
            self.cv_paragraph_comp, text=self.comp_doc.getFilename())
        self.label_comp_doc.pack(side=tk.TOP)

        # comp paragraphs textarea
        self.ta_comp_doc_paragraphs = scrolledtext.ScrolledText(self.cv_paragraph_comp,
                                            wrap = tk.WORD,  
                                            width = 40,  
                                            height = 15,  
                                            font = ("Verdana", 
                                              12))
        self.ta_comp_doc_paragraphs.pack(side=tk.TOP)

        # disable both textareas
        self.ta_main_doc_paragraphs.configure(state="disabled")
        self.ta_comp_doc_paragraphs.configure(state="disabled")

        # I don't have an idea of the number of paragraphs available in a document beforehand
        # That's why I have to limit the kneighbors value in the main screen 
        # to the max amount of paragraphs in the comparisson document
        if self.options["kn_para"] > self.comp_doc.getParagraphsLength():
            self.options["kn_para"] = self.comp_doc.getParagraphsLength()

        # compute the model
        self.neighbors_man = NeighborsManager(
            self.main_doc.getCleanParagraphs(), 
            self.comp_doc.getCleanParagraphs(), 
            self.options["kn_para"], self.options["ngrams"],
            self.options["metric"])

        # get the model and the vector of the comparisson doc
        self.model, self.comp_vector = self.neighbors_man.getModel()

        # array of buttons
        self.btn_paragraphs = []

        # dict to save idx and distances based on the number
        # of paragraphs in the main doc
        # self.neighbors = {i:[] for i in range(len(self.main_paragraphs))}
        self.neighbors = {i:[] for i in range(len(self.main_doc.getParagraphs()))}

        # create buttons for potential plagiarized paragraphs
        # add the indices and distances to the dict
        for idx, paragraph in enumerate(self.comp_vector):
            p_dist, p_idx = self.model.kneighbors(paragraph.toarray())
            btn_created = False
            ix_str = str(self.main_doc.getParagraph(idx))[:35]
            for ix, dist in zip(p_idx[0], p_dist[0]):
                percentage_dist = (1 - dist) * 100
                if percentage_dist > self.options["percentage"]:
                    if not btn_created:
                        self.btn_paragraphs.append(
                            tk.Button(self.vsf_paragraphs.interior, height=1, width=20, relief=tk.FLAT, 
                            bg = "gray99", fg = "black",
                            font = "Dosis", text = ix_str, command=self.paragraphBtnClickHandler(idx)))
                        self.btn_paragraphs[-1].pack(
                            padx = 10, pady = 5, side = tk.TOP, expand=True, fill="both")
                        btn_created = True
                    self.neighbors[idx].append({
                        "distance": '{:.2f}%'.format(percentage_dist),
                        "ix": ix 
                    })
                    

        self.pack(expand=True, fill="both")
    
    def paragraphBtnClickHandler(self, ix):
        return lambda: self.paragraphComparisson(ix)
    
    def paragraphComparisson(self, ix):
        main_para_str = "Párrafo " + str(ix + 1) + ":\n\n" + self.main_doc.getParagraph(ix) + "\n\n"
        
        comp_paras_str = ""
        for neighbor in self.neighbors[ix]:
            comp_para_ix = neighbor["ix"]
            comp_para = self.comp_doc.getParagraph(comp_para_ix)
            plagiarism_percentage = str(neighbor["distance"])
            comp_para_str = "Párrafo " + str(comp_para_ix + 1) + ":\n\n" + comp_para + "\n\nPorcentaje de plagio: " + plagiarism_percentage
            comp_paras_str += comp_para_str + "\n\n\n"
        
        self.ta_main_doc_paragraphs.configure(state="normal")
        self.ta_main_doc_paragraphs.delete('1.0', tk.END)
        self.ta_main_doc_paragraphs.insert(tk.END, main_para_str)
        self.ta_main_doc_paragraphs.configure(state="disabled")

        self.ta_comp_doc_paragraphs.configure(state="normal")
        self.ta_comp_doc_paragraphs.delete('1.0', tk.END)
        self.ta_comp_doc_paragraphs.insert(tk.END, comp_paras_str)
        self.ta_comp_doc_paragraphs.configure(state="disabled")