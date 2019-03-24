# Text Processing
Contains the code that handles the text processing portion of the project

To run the code:

run: `pip install requirements.txt`

In `api/services/gene_interaction_detector.py` uncomment these lines: <br>
`nltk.download('punkt')` <br>
`nltk.download('averaged_perceptron_tagger')`<br>
`nltk.download('universal_tagset')`<br>
(comment them back after the first run)

Run `python app.py`

Navigate to `localhost:5000` on your browser to interact with the swagger docs


# Used Material
* reviewed-home-sapien-genes.tab from https://www.uniprot.org/uniprot/?query=*&fil=reviewed%3Ayes+AND+organism%3A%22Homo+sapiens+%28Human%29+%5B9606%5D%22