import io

import nltk
# nltk.download('punkt') # perform on first run
import requests
from tika import parser


def pdf_to_txt(pdf_file_name, out_txt_file_name):
    content = parser.from_file(pdf_file_name)
    with open(out_txt_file_name, 'w') as file:
        file.write(content['content'])


# use this method to find which proteins have been mentioned in the paper
def intersection(lst1, lst2):
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def gene_request(gene):
    url_query = 'http://string-db.org/api/json/network'
    params = {'identifier': gene, 'species': 9606}
    resp = requests.get(url=url_query, params=params)
    return resp.json()


def get_gene_details(genes):
    data = []
    for gene in genes:
        gene_interactions = gene_request(gene)

        gene_data = {'name': gene, 'interactions': []}

        for gene_interaction in gene_interactions:
            if gene_interaction['preferredName_A'] == gene or gene_interaction['preferredName_B'] == gene:
                gene_data['interactions'].append(gene_interaction)

        data.append(gene_data)
    return data


def detect_genes(gene_names_file, paper_file_name):
    with open(gene_names_file, 'r') as gene_file:
        content = ''.join(gene_file.readlines())

        # create a regex tokenizer that captures whole words, words with hyphens, full commas and forward slashes
        tokenizer = nltk.RegexpTokenizer(r'\w[\w-][\w.][\w/]+')

        gene_names = tokenizer.tokenize(content)

        paper_file = io.open(paper_file_name, 'rU', encoding='utf-8')
        content = ''.join(paper_file.readlines())
        paper_text = tokenizer.tokenize(content)

        result = intersection(gene_names, paper_text)

        return get_gene_details(result)


if __name__ == "__main__":
    gene_names_file = 'gene-names.txt'
    paper_file_name = 'corpus/1.txt'

    detect_genes(gene_names_file, paper_file_name)
