from sklearn.feature_extraction.text import TfidfVectorizer


def get_data():
    f = open('people.txt', 'r')

    corpus = []
    labels = []
    for line in f:
        label = int(line[0])
        text = line[2:]
        labels.append(label)
        corpus.append(text)

    vectorizer = TfidfVectorizer(min_df=1)
    tfidf = vectorizer.fit_transform(corpus)
    feat_names = vectorizer.get_feature_names()

    return tfidf, labels, feat_names
