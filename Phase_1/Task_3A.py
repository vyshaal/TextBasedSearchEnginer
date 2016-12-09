import pickle
from collections import Counter
from Phase_1 import RetrievalModel
import operator
import csv

stop_words_path = "../given_files/common_words"

inverted_index = pickle.load(open("inverted_index.p", "rb"))
document_tokens = pickle.load(open("document_tokens.p", "rb"))
query_dict = pickle.load(open("query_dict.p", "rb"))
relevance_dict = pickle.load(open("relevance_dict.p", "rb"))

N = len(document_tokens)

stop_table = "stopping_vsm.csv"


def retrieve_docs():
    stop_words = retrieve_stop_words()
    updated_document_tokens = update_docs(stop_words)
    updated_query_dict = update_queries(stop_words)
    model = RetrievalModel.CosineSimilarity(N, inverted_index, updated_document_tokens)
    ranked_list = model.cosine_similarity_list(updated_query_dict)

    with open(stop_table, "w") as file:
        csv_writer = csv.writer(file)
        for query_id, scores in ranked_list.items():
            i = 0
            for score in scores:
                i += 1
                csv_writer.writerow((query_id, "Q0", score[0], i, score[1], "using_stop_words"))
                print(query_id,query_dict[query_id])
                print(score)
    file.close()


def retrieve_stop_words():
    stop_words = []
    with open(stop_words_path) as file:
        for line in file:
            stop_words.append(line.split()[0])

    return stop_words


def update_docs(stop_words):
    for key,values in document_tokens.items():
        document_tokens[key] = [x for x in values if x not in stop_words]

    return document_tokens


def update_queries(stop_words):
    for key,values in query_dict.items():
        query_dict[key] = " ".join([x for x in values.split() if x not in stop_words])

    return query_dict

retrieve_docs()