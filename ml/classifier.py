import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.naive_bayes import MultinomialNB

from ml.transform import transform


def train_classifier(training_file_name):
    train_data, train_labels = read_training_data_file(training_file_name)
    train_data_features, feature_model = bag_of_words(train_data)
    model = MultinomialNB().fit(train_data_features, train_labels)
    return model, feature_model, train_data, train_labels


def read_training_data_file(file_name):
    data = []
    labels = []
    with open(file_name, 'rb') as in_file:
        reader = csv.reader(in_file, delimiter='\t')
        for row in reader:
            data.append(row[0])
            labels.append(int(row[1]))
    return data, labels


def read_testing_data_file(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        return lines


def bag_of_words(train_data):
    vectorizer = CountVectorizer(analyzer='word', binary=True, ngram_range=(1, 3))
    train_features = vectorizer.fit_transform(train_data)
    return train_features, vectorizer


def test_sentence(text, feature_model, classifier):
    transformed = transform([text])
    return classifier.predict(feature_model.transform(transformed))[0]


if __name__ == "__main__":
    datasets_directory = '../datasets/'
    file_name = datasets_directory + 'training/training-data.txt'

    positive_bioc = read_testing_data_file(datasets_directory + 'testing/BioC-BioGRID-positives.txt')
    negative_bioc = read_testing_data_file(datasets_directory + 'testing/BioC-BioGRID-negatives.txt')

    test_data = positive_bioc + negative_bioc
    test_labels = ([1] * len(positive_bioc)) + ([0] * len(negative_bioc))

    model, feature_model, train_data, train_labels = train_classifier(file_name)
    train_data_features = feature_model.transform(train_data)
    test_data_features = feature_model.transform(test_data)

    train_predict = model.predict(train_data_features)
    test_predict = model.predict(test_data_features)

    train_report = classification_report(train_labels, train_predict)
    test_report = classification_report(test_labels, test_predict)

    print(accuracy_score(train_predict, train_labels))
    print(accuracy_score(test_predict, test_labels))
    print(train_report)
    print(test_report)
