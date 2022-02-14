from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

class NeighborsManager():
    def __init__(self, main_doc, comp_docs, nn, ngram=4, metric="cosine"):
        self.main_doc = main_doc
        self.comp_docs = comp_docs
        self.nn = nn
        self.ngram = ngram
        self.metric = metric
        if metric == "cosine":
            self.algorithm = "brute"
        elif metric == "jaccard":
            self.algorithm = "ball_tree"
        else:
            self.algorithm = "auto"

    def getModel(self):
        pipe = Pipeline([('n_gram', CountVectorizer(ngram_range=(self.ngram, self.ngram))),
                 ('tfidf', TfidfTransformer())]).fit(self.comp_docs)
        comp_vector = pipe.transform(self.comp_docs)
        main_vector = pipe.transform(self.main_doc)
        return NearestNeighbors(
            n_neighbors=self.nn, metric=self.metric, 
            algorithm=self.algorithm).fit(comp_vector.toarray()), main_vector
    
    def getNeighbors(self):
        pipe = Pipeline([('n_gram', CountVectorizer(ngram_range=(self.ngram, self.ngram))),
                 ('tfidf', TfidfTransformer())]).fit(self.comp_docs)
        comp_vector = pipe.transform(self.comp_docs)
        main_vector = pipe.transform(self.main_doc)
        nbrs = NearestNeighbors(
            n_neighbors=self.nn, metric=self.metric, 
            algorithm=self.algorithm).fit(comp_vector.toarray())
        dist, ix = nbrs.kneighbors(main_vector.toarray())
        return dist, ix