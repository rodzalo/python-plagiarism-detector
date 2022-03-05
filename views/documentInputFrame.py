import tkinter as tk
import glob
import os
from tkinter import ttk
from tkinter import filedialog
from tkinter import Frame

class DocumentInputFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.obj_filename = None
        self.docs_directory = None
        self.container = container

        frame = Frame(container)
        frame.pack()
        
        # title label 
        self.label_title = ttk.Label(
            frame, 
            text="Plagiarism Detector",
            font=("Helvetica", 14))
        self.label_title.grid(column=1, row=0, sticky=tk.NS, ipadx=5, ipady=5)

        # directory label
        self.label_dir = ttk.Label(
            frame,
            text="Corpus directory",
            font=("Helvetica", 10)
        )
        self.label_dir.grid(column=1, row=1, sticky=tk.NW, ipadx=5, ipady=5)

        # directory entry
        self.entry_dir = tk.Entry(frame, width=54)
        self.entry_dir["state"] = "disabled"
        self.entry_dir.grid(column=1, row=2, sticky=tk.W)

        # directory search button
        self.btn_search_dir = ttk.Button(frame, text="Search", command=self.dirDialog)
        self.btn_search_dir.grid(column=1, row=2, sticky=tk.E)

        # objective doc label
        self.label_obj_doc = ttk.Label(
            frame,
            text="Objective document",
            font=("Helvetica", 10)
        )
        self.label_obj_doc.grid(column=1, row=3, sticky=tk.NW, ipadx=5, ipady=5)

        # objective doc entry
        self.entry_obj_doc = tk.Entry(frame, width=54)
        self.entry_obj_doc["state"] = "disabled"
        self.entry_obj_doc.grid(column=1, row=4, sticky=tk.W)

        # objective doc search button
        self.btn_search_obj_doc = ttk.Button(frame, text="Search", command=self.fileDialog)
        self.btn_search_obj_doc.grid(column=1, row=4, sticky=tk.E)

        # Empty label (for padding to the options frame)
        self.label_empty = ttk.Label(frame)
        self.label_empty.grid(column=1, row=5, ipady=5)

        # options label frame
        self.lf_options = ttk.LabelFrame(
            frame,
            text="Settings"
        )
        self.lf_options.grid(column=1, row=6, sticky=tk.S, ipady=5, ipadx=15)

        self.lf_options.columnconfigure(0, weight=1)
        self.lf_options.columnconfigure(1, weight=1)

        # kneighbors (documents) label
        self.label_kneighbors_docs = ttk.Label(
            self.lf_options,
            text="No. of N. Neighbors (Documents)"
        )
        self.label_kneighbors_docs.grid(column=0, row=0, sticky=tk.N, ipady=5)

        # kneighbors (documents) combobox
        self.kneighbors_values = (1, 2, 3, 4, 5, 6, 7, 8)

        self.selected_k = tk.IntVar()

        self.cb_kneighbors = ttk.Combobox(
            self.lf_options, 
            textvariable=self.selected_k,
            values=self.kneighbors_values,
            state="readonly")
        self.cb_kneighbors["state"] = "disabled"
        self.cb_kneighbors.grid(column=0, row=1, sticky=tk.N)

        # kneighbors (paragraphs) label
        self.label_kneighbors_para = ttk.Label(
            self.lf_options,
            text="No. of N. Neighbors (Paragraphs)"
        )
        self.label_kneighbors_para.grid(column=1, row=0, sticky=tk.E, ipadx=6, ipady=5)

        # kneighbors (paragraphs) combobox
        self.selected_k_para = tk.IntVar()

        self.cb_kneighbors_para = ttk.Combobox(
            self.lf_options,
            textvariable=self.selected_k_para,
            values=self.kneighbors_values,
            state="readonly"
        )
        self.cb_kneighbors_para.set(self.kneighbors_values[1])
        self.cb_kneighbors_para.grid(column=1, row=1, sticky=tk.N)

        # n_grams label
        self.label_ngrams = ttk.Label(
            self.lf_options,
            text="No. of N-grams"
        )
        self.label_ngrams.grid(column=0, row=2, sticky=tk.N, ipady=5)

        # n_grams combobox
        self.ngram_values = (1, 2, 3, 4, 5)

        self.selected_ngram = tk.IntVar()

        self.cb_ngram = ttk.Combobox(
            self.lf_options,
            textvariable=self.selected_ngram,
            values=self.ngram_values,
            state="readonly"
        )
        self.cb_ngram.set(self.ngram_values[1])
        self.cb_ngram.grid(column=0, row=3, sticky=tk.N)

        # Plagiarism percentage label (title)
        self.label_pp_title = ttk.Label(
            self.lf_options,
            text="Plagiarism Percentage"
        )
        self.label_pp_title.grid(column=1, row=2, sticky=tk.N, ipadx=3, ipady=5)

        # Plagiarism percentage slider
        # Default value
        self.scale_pp_value = tk.IntVar()
        self.scale_pp_value.set(70)

        self.scale_pp = ttk.Scale(
            self.lf_options,
            from_=0,
            to=100,
            orient='horizontal',
            command=self.sliderChanged,
            variable=self.scale_pp_value
        )
        self.scale_pp.grid(column=1, row=3)

        # Plagiarism percentage value label (under the slider)
        self.label_pp_value = ttk.Label(
            self.lf_options,
            text=self.getCurrentValue()
        )
        self.label_pp_value.grid(column=1, row=4)

        # Distance metric label
        self.label_metric = ttk.Label(
            self.lf_options,
            text="Distance Metric"
        )
        self.label_metric.grid(column=0, row=4, sticky=tk.N, ipady=5)

        # Distance metric combobox
        self.metric_values = ('Cosine', 'Jaccard')

        self.cb_metric = ttk.Combobox(
            self.lf_options,
            values=self.metric_values,
            state="readonly"
        )
        self.cb_metric.set(self.metric_values[0])
        self.cb_metric.grid(column=0, row=5, sticky=tk.N)
    
    def fileDialog(self):
        self.obj_filename = filedialog.askopenfilename(
            filetypes=(("Microsoft Word documents (.docx)", "*.docx"),)
        )
        self.entry_obj_doc["state"] = "normal"
        self.entry_obj_doc.insert(0, self.obj_filename)
        self.entry_obj_doc["state"] = "disabled"

    def dirDialog(self):
        self.docs_directory = filedialog.askdirectory()
        self.entry_dir["state"] = "normal"
        self.entry_dir.insert(0, self.docs_directory)
        self.entry_dir["state"] = "disabled"
        self.enableNeighborsCB(self.docs_directory)

    def enableNeighborsCB(self, directory):
        # quickly check the number of .doc files
        curr_dir = os.getcwd()
        os.chdir(directory)
        n = len(glob.glob('*.docx'))
        os.chdir(curr_dir)
        # set the new kneighbor values
        self.kneighbors_values = [*range(1, n + 1)]
        self.cb_kneighbors.set(n)
        self.cb_kneighbors['values'] = self.kneighbors_values
        # enable de combobox
        self.cb_kneighbors["state"] = "readonly"

    def getCurrentValue(self):
        return '{}%'.format(self.scale_pp_value.get())

    def sliderChanged(self, event):
        self.label_pp_value.configure(text=self.getCurrentValue())

    def getDir(self):
        return self.docs_directory
    
    def getObjFilename(self):
        return self.obj_filename

    def getKNeighborsDocs(self):
        return self.cb_kneighbors.get()

    def getKNeighborsPara(self):
        return self.cb_kneighbors_para.get()
    
    def getNgram(self):
        return self.cb_ngram.get()

    # get all option values
    def getOptions(self):
        return {
            "dir": self.docs_directory,
            "main_doc": self.obj_filename,
            "kn_docs": int(self.cb_kneighbors.get()),
            "kn_para": int(self.cb_kneighbors_para.get()),
            "ngrams": int(self.cb_ngram.get()),
            "percentage": int(self.scale_pp_value.get()),
            "metric": self.cb_metric.get().lower() 
        }

    # get plagiarism percentage
    def getPlagiarismPercentage(self):
        return self.scale_pp_value.get()

    def isReadyToCompute(self):
        return self.obj_filename != None and self.docs_directory != None
