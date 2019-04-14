import csv
import io
import itertools

import nltk
# nltk.download('punkt') # perform on first run
# nltk.download('averaged_perceptron_tagger')
# nltk.download('universal_tagset')
import requests
from tika import parser

from ml.classifier import train_classifier, classify_single


#TODO: Put this somewhere else
classifier = train_classifier('./datasets/training/training-data.txt')
#TODO: Need to replace the gene names with gene1 and gene2, and make the sentence lower case
is_interaction = classify_single('gene1 interacts with gene2', classifier)


def pdf_to_txt(pdf_file_name, out_txt_file_name):
    content = parser.from_file(pdf_file_name)
    with open(out_txt_file_name, 'w') as file:
        file.write(content['content'])


# use this method to find which proteins have been mentioned in the paper
def intersection(lst1, lst2):
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return set(lst3)


def gene_request(gene):
    url_query = 'http://string-db.org/api/json/network'
    params = {'identifier': gene, 'species': 9606}
    resp = requests.get(url=url_query, params=params)
    return resp.json()


def query_gene_details(genes):
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
    return result


def get_gene_details(genes, paper_content, detected_interactions=None):
    result = detect_genes(genes, paper_content)
    gene_details = query_gene_details(result)
    interaction_details = []

    if detected_interactions is not None:
        # check if genes in paper are first degree neighbours
        for detected_interaction in detected_interactions:
            combinations = detected_interaction["interactions"]
            interaction_detail = {"sentence": detected_interaction["sentence"]}
            combo_interactions = []
            for combo in combinations:
                interacts = False
                for gene in gene_details:
                    if gene["name"] in combo:
                        for known_interaction in gene["known_interactions"]:
                            pair_interaction = (
                            known_interaction['preferredName_A'], known_interaction['preferredName_B'])
                            if pair_interaction == combo or tuple(reversed(pair_interaction)) == combo:
                                interacts = True
                combo_interactions.append({"combo": combo, "interacts": interacts})
            interaction_detail.update({"interaction_details": combo_interactions})
            interaction_details.append(interaction_detail)

    return gene_details, interaction_details


def read_genes_from_tsv(file_name, name_headers):
    tokenizer = nltk.RegexpTokenizer(r"[\w\.'-]{3,}")
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


def search_gene_sentences(gene_names, paper_content, min_genes_in_sentence):
    data = []
    sentences = nltk.sent_tokenize(paper_content)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        genes = intersection(words, gene_names)
        if len(genes) >= min_genes_in_sentence:
            data.append({
                'genes': genes,
                'sentence': sentence
            })
    return data


def detect_interactions(genes, paper):
    # use grammar rules to check if mentioned genes interact

    gene_sentences = search_gene_sentences(genes, paper, 2)
    interacting_genes = []
    gene_pairs = []
    for match in gene_sentences:
        sentence = match['sentence']
        words = nltk.word_tokenize(sentence)

        tagged = nltk.pos_tag(words, tagset='universal')
        grammar = "CHUNK: {<JJ>*<NOUN><VERB><ADP>?<NOUN>(<CONJ><NOUN>)*}"
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(tagged)
        sentence_genes = detect_genes(genes, sentence)
        if result is not None and sentence_genes not in interacting_genes:
            interacting_genes.append(sentence_genes)
            combos = list(itertools.combinations(sentence_genes, 2))
            gene_pairs.append({"sentence": sentence, "interactions": combos})

    return gene_pairs


if __name__ == "__main__":
    gene_names_file = './genes/reviewed-home-sapien-genes.tab'
    paper_file_name = './corpus/3.txt'

    gene_names = read_genes_from_tsv(gene_names_file, ['Gene names  (primary )', 'Gene names  (synonym )'])
    paper = read_paper_text_file(paper_file_name)
    gene_sentences = search_gene_sentences(gene_names, paper, 2)

    lemmatizer = nltk.stem.WordNetLemmatizer()
    ps = nltk.stem.PorterStemmer()
    tokenizer = nltk.RegexpTokenizer(r'\w[\w-][\w.][\w/]+')

    for match in gene_sentences:
        sentence = match['sentence']
        # print (match['genes'])

        words = nltk.word_tokenize(sentence)
        # words_lemmatized = [lemmatizer.lemmatize(w) for w in words]
        # words_stemmed = [ps.stem(w) for w in words_lemmatized]

        tagged = nltk.pos_tag(words, tagset='universal')
        grammar = "CHUNK: {<JJ>*<NOUN><VERB><ADP>?<NOUN>(<CONJ><NOUN>)*}"
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(tagged)
        for subtree in result.subtrees():
            if subtree.label() == "CHUNK":
                print(subtree.leaves())
        print(sentence)
        # print(tagged)
        # print(words_stemmed)
        print(result)
        print('')

