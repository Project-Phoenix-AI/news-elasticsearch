import math

def ranked_retrieval(results, query, es):
    # index is a dictionary containing document lengths for each docID
    for posting in results:
        # Term frequency in corpus.
        tf = get_tf_corpus(query)
        # Document Length: number of words in d
        dl = len(posting['text'])
        # Document Frequency: "documents in the corpus which contain t"
        df_t = len(results)
        # Term Frequency: "occurrences of t in d"
        tf_df = get_tf_doc(posting.key(), es)

        idf_t = math.log(tf/df_t)
        tf_idf_dt = (tf_df * idf_t) / dl

        posting['score'] = tf_idf_dt

    # Sort the postings list according to scores
    results.sort(key=lambda x: x.score, reverse=True)
    return results

# Not finished
def rating_feedback(results, es, alpha, beta):
    ratedDoc = results.keys()['rate']

    # Create integer with number of relevant docs
    relevant_docs = sum(ratedDoc)

    # Create a hash map to store the term weights calculated based on relevance feedback.
    term_weights = {}

    # Calculate weights for relevant documents
    for i, is_relevant in enumerate(results.keys()['rate']):
        if is_relevant:
            doc_id = results[i].id

            # Call the get_tf method to calculate the term frequencies in the document
            term_frequencies = get_tf_doc(doc_id, es)
            dl = len(es.get(index='data', id=doc_id)['text'])
            # Calculate term weights using TF-IDF formula
            for term, tf in term_frequencies.items():
                df_t = 0

                idf_t = math.log(tf / df_t)
                tf_idf = (tf * idf_t) / dl

                tf_idf_dt = (beta * tf_idf) / relevant_docs

                term_weights[term] = term_weights.get(term, 0.0) + tf_idf_dt    

    # Update original query weights by multiplying with alpha
    for query in es.get(index='words'):
        query['weight'] *= alpha


# Read document and calculate term frequencies
def get_tf_doc(doc_id, es):
    # Create a dictionary to store term frequencies.
    tf = {}

    # Get the content of the document from the ElasticSearch index using the docID.
    content = es.get(index='data', id=doc_id)['text']

    # Tokenize the content and calculate the term frequencies
    for token in content.split():
        tf[token] = tf.get(token, 0) + 1

    # Return the dictionary containing the term frequencies for the document.
    return tf


# Read document and calculate term frequencies
def get_tf_corpus(query, es):
    # Create a dictionary to store term frequencies.
    tf = 0
    # Search for all values in inner_dict inside outer_dict
    for key, value in es.items():
        if isinstance(value, dict):  # check if the value is a dictionary
            for inner_key, inner_value in value.items():
                if query in inner_value['text']:
                    tf += 1
    
    # Return the dictionary containing the term frequencies for the document.
    return tf