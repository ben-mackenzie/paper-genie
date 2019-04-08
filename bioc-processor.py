import os
from bioc import *

dtd_file = 'bioc.dtd'


def read_bioc_file(bioc_file, dtd_valid_file):
    """
    Read a single BioC document file and extracts the passages contains genes and their interactions
    :param bioc_file: The path of the BioC XML file
    :param dtd_valid_file: The BioC DTD file describing the data in the XML file
    :return: List containing genes and interactions found in the BioC document
    """
    bioc_reader = BioCReader(bioc_file, dtd_valid_file)
    bioc_reader.read()

    returned_data = []

    for document in bioc_reader.collection.documents:
        for passage in document:
            has_gene = False
            has_interaction = False
            entry = {'genes': [], 'interactions': []}

            for annotation in passage.annotations:
                if annotation.infons['type'].lower() == 'gene':
                    entry['genes'].append(annotation.text)
                    has_gene = True
                elif annotation.infons['type'].lower() == 'ppimention':
                    entry['interactions'].append(annotation.text)
                    has_interaction = True

            if has_gene and has_interaction:
                returned_data.append(entry)

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
    data = []
    for file_name in files:
        file_path = in_dir + '/' + file_name
        data.extend(read_bioc_file(file_path, dtd_valid_file))
    return data


corpus = read_bioc_files('./bioc-corpus', dtd_file)
for c in corpus:
    print c
#print(corpus)
