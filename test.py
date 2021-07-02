from engine.graphs import Graphs

graph = Graphs()

book_path = "books/"
output_path = "json_books/"
book = "market.xml"

# Load book data
graph.parse_xml(book_path + book, output_path + book.split(".")[0] + ".json")
print(book + " parsed")

# Display graph
res = graph.display_graph(output_path + book.split(".")[0] + ".json", "test.html", False)
print(res)
