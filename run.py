from flask import Flask, session
from flask import render_template, flash, request, redirect, url_for
from engine.graphs import Graphs
from os.path import join, dirname, realpath

json_path = join(dirname(realpath(__file__)), "books\\json\\")
UPLOADS_PATH = join(dirname(realpath(__file__)), 'books\\xml\\')
cur_file = ""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

g = Graphs()


@app.route('/')
def index():
    return render_template('index.html')


@app.post("/upload_book")
def upload_book():
    file = request.files['file']
    extension = file.filename.split(".")[1]

    if extension == "xml" or extension == "XML":
        file.save(app.config['UPLOAD_FOLDER'] + file.filename)
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
    if request.accept_mimetypes.best == "application/json":
        json_data = g.display_graph(json_path + session['cur_path'], "dd", False)
        return str(json_data)

    return render_template('graph.html', data=session['cur_name'])


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True, port=8000)
