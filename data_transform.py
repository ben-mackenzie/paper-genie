import os
import csv
import nltk


def read_file(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        return lines


def transform(sentences_list):
    stemmer = nltk.stem.PorterStemmer()
    transformed = []

    for sentence in sentences_list:
        sentence = sentence.strip()
        normalized = sentence.lower()
        words = nltk.word_tokenize(normalized)
        trimmed = trim(words)
        removed = word_removal(trimmed)
        stemmed = [stemmer.stem(w) for w in removed]

        transformed.append(' '.join(stemmed))

    return transformed


def trim(words, window_size=3):
    first = max(words.index('gene1') - window_size, 0)
    second = min(words.index('gene2') + window_size, len(words))
    trimmed = words[first:second]
    return trimmed


def word_removal(words):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = [w for w in words if w not in stop_words]

    short_words = [x for x in words if len(x) < 2]
    remove_from_list(words, short_words)

    digits = [x for x in words if x.isdigit()]
    remove_from_list(words, digits)

    return words


def remove_from_list(the_list, items):
    for i in items:
        the_list.remove(i)


def mkdir(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    print('Reading files')
    positives = read_file('./data-output/bioc-positives.txt')
    negatives = read_file('./data-output/bioc-negatives.txt')

    print('Transforming positives')
    transformed_positives = transform(positives)
    print('Transforming negatives')
    transformed_negatives = transform(negatives)

    ones = [1] * len(transformed_positives)
    zeros = [0] * len(transformed_negatives)
    relations = zip(transformed_positives, ones)
    non_relations = zip(transformed_negatives, zeros)

    all = []
    all.extend(relations)
    all.extend(non_relations)

    print('Writing output')
    directory = './data-output/'
    mkdir(directory)

    with open(directory + '/bioc-tranformed.txt', 'w') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerows(all)

    print("Done")
