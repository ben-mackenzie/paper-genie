import os
import re
from itertools import permutations
from bioc import *

dtd_file = '../datasets/bioc-original/bioc.dtd'


def read_bioc_file(bioc_file, dtd_valid_file):
    """
    Read a single BioC document file and extracts the passages contains genes and their interactions
    :param bioc_file: The path of the BioC XML file
    :param dtd_valid_file: The BioC DTD file describing the data in the XML file
    :return: List containing genes and interactions found in the BioC document
    """
    bioc_reader = BioCReader(bioc_file, dtd_valid_file)
    bioc_reader.read()

    returned_data = {
        'with_interactions': [],
        'without_interactions': []
    }

    for document in bioc_reader.collection.documents:
        for passage in document:
            entry = {'genes': set(), 'interactions': [], 'text': passage.text}

            for annotation in passage.annotations:
                if annotation.infons['type'].lower() == 'gene':
                    entry['genes'].add(annotation.text)
                elif annotation.infons['type'].lower() == 'ppimention':
                    entry['interactions'].append(annotation.text)

            if len(entry['genes']) >= 2:
                if len(entry['interactions']):
                    returned_data['with_interactions'].append(entry)
                else:
                    returned_data['without_interactions'].append(entry)

    return returned_data


def read_bioc_files(in_dir, dtd_valid_file):
    """
    Reads all BioC files in the given directory and forms and collective corpus
    :param in_dir: The input directory which contains all the BioC XML files. This directory should not contain any
    file (or directory) other than the BioC files
    :param dtd_valid_file: The BioC DTD file
    :return: List of all the genes and interactions found in all the BioC documents in the directory
    """
    files = os.listdir(in_dir)
    returned_data = {
        'with_interactions': [],
        'without_interactions': []
    }

    for file_name in files:
        file_path = in_dir + '/' + file_name
        read_data = read_bioc_file(file_path, dtd_valid_file)
        returned_data['with_interactions'].extend(read_data['with_interactions'])
        returned_data['without_interactions'].extend(read_data['without_interactions'])

    return returned_data


def normalize_gene_names(bioc_corpus):
    """
    Normalizes the list of genes and interactions such that there is only 1 pair of genes and their interaction
    sentence per item in the list
    :param bioc_corpus: The BioC corpus
    :return: Tuple (+ves, -ves) containing list of sentences with the genes replace with generic names
    """
    positives = []
    negatives = []

    for item in bioc_corpus['with_interactions']:
        for interaction in item['interactions']:
            positives.extend(gene_replacement(interaction, item['genes']))

    for item in bioc_corpus['without_interactions']:
        negatives.extend(gene_replacement(item['text'], item['genes']))

    return positives, negatives


def gene_replacement(text, genes):
    """
    Makes a list of sentences out of the given text by replacing genes in the text, one pair at at ime
    :param text: The text string
    :param genes: A list/set of genes
    :return: List of sentences with gene pairs replaced with GENE1, GENE2 and the remaining genes with OTHER_GENE
    """
    sentences = []
    gene_pairs = permutations(genes, 2)

    for pair in gene_pairs:
        if pair[0] in text and pair[1] in text:
            other_genes = genes.difference(pair)
            modified_sentence = replace_genes(text, pair, other_genes)
            sentences.append(modified_sentence)

    return sentences


def replace_genes(interaction, genes_pair, other_genes):
    interaction = ireplace(interaction, genes_pair[0], 'GENE1')
    interaction = ireplace(interaction, genes_pair[1], 'GENE2')
    for gene in other_genes:
        interaction = ireplace(interaction, gene, 'OTHER_GENE')
    return interaction


def ireplace(string, old, new):
    """
    Case insensitive replace
    """
    return re.sub(re.compile(re.escape(old), re.IGNORECASE), new, string)


def mkdir(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == '__main__':
    print("Reading corpus files")
    bioc_corpus = read_bioc_files('../datasets/bioc-original/BioC-BioGRID', dtd_file)
    print("Processing")
    bioc_corpus = normalize_gene_names(bioc_corpus)

    directory = '../datasets/testing/'
    mkdir(directory)

    print("Writing output")
    with open(directory + '/BioC-BioGRID-positives.txt', 'w') as f:
        f.writelines('\n'.join(bioc_corpus[0]))

    with open(directory + '/BioC-BioGRID-negatives.txt', 'w') as f:
        f.writelines('\n'.join(bioc_corpus[1]))

    print("Output written successfully")
