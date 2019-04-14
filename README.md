# Text Processing
Contains the code that handles the text processing portion of the project

# Prerequisites
* Python 2.7
* JAVA 8 Runtime

# Setup
1. Create a python 2.7 virtualenv/conda environment
2. Install dependencies. `pip install requirements.txt`
3. Download NLTK packages

In `api/services/gene_interaction_detector.py` uncomment these lines: <br>
`nltk.download('punkt')` <br>
`nltk.download('averaged_perceptron_tagger')`<br>
`nltk.download('universal_tagset')`<br>
(comment them back after the first run)

4. Run `python app.py`

5. Navigate to `localhost:5000` on your browser to interact with the swagger docs

# Used Material
* reviewed-home-sapien-genes.tab from https://www.uniprot.org/uniprot/?query=*&fil=reviewed%3Ayes+AND+organism%3A%22Homo+sapiens+%28Human%29+%5B9606%5D%22

# Datasets
* Custom made dataset of gene interaction sentences
* [BioC-BioGRID](ftp://ftp.ncbi.nlm.nih.gov/pub/wilbur/BioC-BioGRID/)

# Major Libraries Used
* [PyBioC](https://github.com/2mh/PyBioC)
* [NLTK](https://www.nltk.org/)
* [sikit-learn](https://scikit-learn.org/stable/)
