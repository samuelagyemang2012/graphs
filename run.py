from flask import Flask, session
from flask import render_template, flash, request, redirect, url_for
from engine.graphs import Graphs
import os
from os.path import join, dirname, realpath
from engine.embeddings import Embeddings

json_path = join(dirname(realpath(__file__)), "books\\json\\")
UPLOADS_PATH = join(dirname(realpath(__file__)), 'books\\xml\\')
cur_file = ""

# flask
app = Flask(__name__)
app.static_folder = 'static'
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

# graph
g = Graphs()

# embeddings
e = Embeddings()


@app.route('/')
def index():
    return render_template('index.html')


@app.post("/upload_book")
def upload_book():
    file = request.files['file']
    extension = file.filename.split(".")[1]

    if extension == "xml" or extension == "XML":
        file.save(app.config['UPLOAD_FOLDER'] + file.filename.lower())
        g.parse_xml(UPLOADS_PATH + file.filename, json_path + file.filename.split(".")[0] + ".json")
        flash("Your graph is ready!", "success")
        session['cur_path'] = file.filename.split(".")[0] + ".json"
        session['cur_name'] = file.filename.split(".")[0]

        return redirect(url_for("index"))

    else:
        flash("Please upload an xml file", "error")
        return redirect(url_for("index"))


@app.get("/view_graph")
def view_graph():
    # return json_path+session['cur_path']
    if request.accept_mimetypes.best == "application/json":
        json_data = g.display_graph(json_path + session['cur_path'], "dd", False)
        return str(json_data)

    return render_template('graph.html')


@app.get("/graph/<name>")
def view_a_graph(name):
    if request.accept_mimetypes.best == "application/json":
        json_data = g.display_graph(json_path + name.lower() + ".json", "dd", False)
        return str(json_data)

    return render_template('graph_.html', book_id=name.lower())


@app.get("/explore_graphs")
def explore_graphs():
    files = os.listdir(UPLOADS_PATH)
    for i in range(len(files)):
        files[i] = files[i].split(".")[0].capitalize()

    return render_template('explore_graphs.html', data=files)


@app.get("/get_similarity")
def get_graph_similarity():
    if request.accept_mimetypes.best == "application/json":
        books = request.args["data"].split("-")

        doc1 = g.get_book_content(json_path + books[0].lower() + ".json")
        doc2 = g.get_book_content(json_path + books[1].lower() + ".json")

        cosim = e.get_similarity(doc1, doc2)
        cosim = cosim.item()

        return {"title1": books[0].capitalize(),
                "title2": books[1].capitalize(),
                "doc1": doc1,
                "doc2": doc2,
                "score": round(cosim, 2)
                }

    files = os.listdir(UPLOADS_PATH)
    for i in range(len(files)):
        files[i] = files[i].split(".")[0].capitalize()
    return render_template('similarity.html', data=files)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True, port=5000)
