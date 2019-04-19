import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

from ml.transform import transform


def train_classifier(training_file_name):
    """
    Trains a classifier
    :param training_file_name: The TSV training file name
    :return: The classifer that itself is a tuple of the classifier and the feature model classifier
    """
    train_data, train_labels = read_training_data_file(training_file_name)
    train_data_features, feature_model = bag_of_words(train_data)
    model = LogisticRegression().fit(train_data_features, train_labels)

    print('Classifier trained')
    return model, feature_model


def classify_single(sentence, classifier):
    """
    Classifies the given sentence as an interaction or non-interaction
    :param sentence: The str sentence
    :param classifier: The classifier returned by train_classifier method
    :return: 1 is the sentence contains an interaction, 0 otherwise
    """
    classification = classify([sentence], classifier)
    if len(classification) > 0:
        return classification[0]
    else:
        return 0


def classify(sentences_list, classifier):
    """
    Classifies a list of sentence as an interaction or non-interaction
    :param sentences_list: The list [str] of sentences
    :param classifier: The classifier returned by train_classifier method
    :return: 1 is the sentence contains an interaction, 0 otherwise
    """
    transformed_sentence = transform(sentences_list)
    features = classifier[1].transform(transformed_sentence)
    prediction = classifier[0].predict(features)
    return prediction.tolist()


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
        lines = [l.strip() for l in lines]
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

    # data, labels = read_training_data_file(file_name)
    # train_data, test_data, train_labels, test_labels = train_test_split(data, labels)
    # train_data_features, feature_model = bag_of_words(train_data)
    # model = MultinomialNB().fit(train_data_features, train_labels)
    #
    # test_data_features = feature_model.transform(test_data)
    # train_predict = model.predict(train_data_features)
    # test_predict = model.predict(test_data_features)
    #
    # train_report = classification_report(train_labels, train_predict)
    # test_report = classification_report(test_labels, test_predict)
    #
    # print(accuracy_score(train_predict, train_labels))
    # print(accuracy_score(test_predict, test_labels))


    test_data = positive_bioc + negative_bioc
    test_labels = ([1] * len(positive_bioc)) + ([0] * len(negative_bioc))

    classifier = train_classifier(file_name)

    train_data, train_labels = read_training_data_file(file_name)

    train_predict = classify(train_data, classifier)
    test_predict = classify(test_data, classifier)

    should_be_positives = []
    should_be_negatives = []
    for i in range(len(test_predict)):
        if test_predict[i] != test_labels[i]:
            if test_labels[i] == 0:
                should_be_negatives.append(test_data[i])
            else:
                should_be_positives.append(test_data[i])

    print('should be 1:')
    for s in should_be_positives:
        print(s)

    print('should be 0:')
    for s in should_be_negatives:
        print(s)

    train_report = classification_report(train_labels, train_predict)
    test_report = classification_report(test_labels, test_predict)

    # print(classify_single('gene1 interacts with gene2', classifier))
    # print(accuracy_score(train_predict, train_labels))
    print(accuracy_score(test_predict, test_labels))
    # print(train_report)
    print(test_report)
