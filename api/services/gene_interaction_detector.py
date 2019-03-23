import io
import csv

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

        gene_data = {'name': gene, 'known_interactions': []}

        for gene_interaction in gene_interactions:
            if gene_interaction['preferredName_A'] == gene or gene_interaction['preferredName_B'] == gene:
                gene_data['known_interactions'].append(gene_interaction)

        data.append(gene_data)
    return data


def detect_genes(genes, paper_content):
    # create a regex tokenizer that captures whole words, words with hyphens, full commas and forward slashes
    tokenizer = nltk.RegexpTokenizer(r'\w[\w-][\w.][\w/]+')
    paper_text = tokenizer.tokenize(paper_content)
    result = intersection(genes, paper_text)
    return get_gene_details(result)


def read_genes_from_tsv(file_name, name_headers):
    tokenizer = nltk.RegexpTokenizer(r'[\w\.-\\\'-]+')
    genes_names = []
    with open(file_name) as f:
        reader = csv.DictReader(f, dialect='excel-tab')
        for row in reader:
            cols = list([row[h] for h in name_headers])
            names = ' '.join(cols)
            genes_names.extend(tokenizer.tokenize(names))
    return set(genes_names)


def read_paper_text_file(file_name):
    with io.open(file_name, 'rU', encoding='utf-8') as paper_file:
        content = ''.join(paper_file.readlines())
        return content


if __name__ == "__main__":
    gene_names_file = '../../genes/reviewed-home-sapien-genes.tab'
    paper_file_name = '../../corpus/1.txt'

    gene_names = read_genes_from_tsv(gene_names_file, ['Gene names  (primary )', 'Gene names  (synonym )'])
    genes = detect_genes(gene_names, paper_file_name)
    print(len(genes))
    print(genes)

