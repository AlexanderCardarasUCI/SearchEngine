from Indices import IndexManager
from Tokenizer import Tokenize
from Utils import Timer
import math

index_manager = IndexManager.Backend()

def tf_idf(tokens):
    doc_scores = {}
    num_docs = index_manager.get_number_of_docs()
    print(num_docs)

    for token in tokens:
        # W = (1 + log(term_freq) * log(num_docs/ num_docs_with_term)
        docs_with_term = index_manager.get_docs_with_term(token)

        for doc, freq in docs_with_term:
            w = (1 + math.log(freq)) * math.log(num_docs / len(docs_with_term))
            if token in doc_scores:
                doc_scores[doc] += w
            else:
                doc_scores[doc] = w

    return doc_scores


def get_intersect_doc_id(l1, l2, key):
    answer = []
    print(l1)
    print(l2)
    p1 = 0
    p2 = 0

    while p1 < len(l1) and p2 < len(l2):
        if l1[p1][key] == l2[p2][key]:
            answer.append(l1[p1])
            p1 += 1
            p2 += 1
        elif l1[p1][key] < l2[p2][key]:
            p1 += 1
        else:
            p2 += 1
    return answer


def search(query):
    print("Searching for: \"{}\"".format(query))
    time = Timer.StopWatch()
    time.start_timer()

    tokens = Tokenize.tokenize(query, spellcheck=True)
    tokens = Tokenize.remove_duplicates(tokens)
    matches = tf_idf(tokens)
    sorted_matches = sorted(matches.items(), key=lambda kv: kv[1], reverse=True)

    id_url = index_manager.get_id_url()

    time.stop_timer()
    print("Found {} matches from {} documents in {} seconds".format(len(sorted_matches), len(id_url), time.duration()))


    urls = []
    num_display = 5
    for i, match in enumerate(sorted_matches):
        if i >= num_display:
            break
        urls.append(id_url[str(match[0])][:-1])

    return urls


