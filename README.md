# Python Plagiarism Detector

This is a basic external plagiarism detector that has two features: 
1. Compare a single document against a group of documents (that goes by the name of "corpus") and list the most similar documents within the corpus. Sorting by descendant order based on the plagiarism percentage of every similar document.
2. Check which paragraphs are similar against a single suspicious document. This includes a plagiarism percentage to show the similarity between the suspicious paragraph and the original paragraphs.

## Usage

First, locate the corpus folder, i.e. the folder where all the documents you want to compare are. Second, select an objective document, i.e. the document to compare against the rest. Once both tasks are done, you can immediately check the most similar documents in the corpus by pressing the "Compare" button, as the default options are in set. However, you can play with the following settings:

- Number of Neighbors (Documents): Set the maximum number of nearest neighbors (documents) around the objetive document. Note that the number of neighbors may be less than expected if the plagiarism percentage is high enough.

- Number of Neighbors (Paragraphs): Set the maximum number of nearest neighbors (paragraphs) around the paragraph that is being compared to. Similar to the setting above, the number of paragraph may be lower than the number set in the setting if the plagiarism percentage is high enough.

- Number of N-grams: Set the number of n-grams in the vocabulary. Lower n-grams may have higher false positives and higher n-grams may provide higher accuracy, but will skip sentences shorter than the number of n-grams set.

- Plagiarism Percentage: Set the minimum amount of plagiarism to detect. Please note that if set to 100% is restricted to the search of identical paragraphs in the documents, while set to 0% is an abosulte unrestricted search of any single identical word in a paragraph, thus may introduce false positives.

- Distance Metric: Set a distance metric for the search. Usually "Cosine" is enough, but may get inneficient if there's a big corpus. On the other hand, "Jaccard" is more efficient on large corpus, but can give lower results than "Cosine" which may impact plagiarism detection.

Afterwards, you will be presented with the "Similar Documents" view (check the screenshots), which is a list of the most similar documents in the corpus against the objective document, each and every one with their respective plagiarism percentage to measure how similar is to the objetive document. 

Click on any document and a new window will show up: the "Paragraph Comparisson" window. Here you can select any paragraph available in the list on the left side and compare it with the original paragraph. The available paragraphs depends on the custom settings set in the main view.

## Dependencies

- joblib
- lxml
- NumPy
- python-docx
- Scikit-Learn
- SciPy
- threadpoolctl

## Screenshots

![Document Input View](/screenshots/doc-input.png)
![Plagiarized Documents View] (/screenshots/plagiarized-docs.png)
![Paragraph Comparisson View](/screenshots/paragraph-comparisson.png)