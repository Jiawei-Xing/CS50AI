import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as f:
            files[filename] = f.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.tokenize.word_tokenize(document.lower())
    output = []
    for word in words:
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            output.append(word)
    return output


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # unique words
    words = set()
    for doc in documents.values():
        words.update(doc)

    # idfs
    idfs = {}
    for word in words:
        appears = 0
        for doc in documents.values():
            if word in doc:
                appears += 1
        idfs[word] = math.log(len(documents) / appears)
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = {}
    for f in files:
        tf_idfs[f] = 0
        for q in query:
            tf_idfs[f] += files[f].count(q) * idfs[q]

    # sort by tf_idfs
    output = [k[0] for k in sorted(tf_idfs.items(), key=lambda x: x[1], reverse=True)]
    return output[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    rank = {}
    for s, w in sentences.items():
        rank[s] = [0, 0]

        # idfs
        for q in query:
            if q in w:
                rank[s][0] += idfs[q]

        # query term density
        for x in w:
            if x in query:
                rank[s][1] += 1 / len(w)

    # sort by idfs, tds
    output1 = {k: v[0] for k, v in sorted(rank.items(), key=lambda x: x[1][1], reverse=True)}
    output2 = [k[0] for k in sorted(output1.items(), key=lambda x: x[1], reverse=True)]
    return output2[:n]


if __name__ == "__main__":
    main()