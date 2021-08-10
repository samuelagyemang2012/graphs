# from engine.graphs import Graphs
#
# graph = Graphs()
#
# book_path = "books/"
# output_path = "json_books/"
# book = "market.xml"
#
# # Load book data
# graph.parse_xml(book_path + book, output_path + book.split(".")[0] + ".json")
# print(book + " parsed")
#
# # Display graph
# res = graph.display_graph(output_path + book.split(".")[0] + ".json", "test.html", False)
# print(res)

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
def cosine(u,v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"

pp = "C:\\Users\\Administrator\\Desktop\\Sam\\graph\\063d866c06683311b44b4992fd46003be952409c"
model = hub.load(pp)
print("module %s loaded" % pp)

sentences = ["I ate dinner.",
             "We had a three-course meal.",
             "Brad came to dinner with us.",
             "He loves fish tacos.",
             "In the end, we all felt like we ate too much.",
             "We all agreed; it was a magnificent evening."]

sentence_embeddings = model(sentences)
query = "I had pizza and pasta"

query_vec = model([query])[0]

for sent in sentences:
  sim = cosine(query_vec, model.encode([sent])[0])
  print("Sentence = ", sent, "; similarity = ", sim)
