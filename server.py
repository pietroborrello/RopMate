from flask import *
import webbrowser
import string
import sys
import os
import numpy as np
import pandas as pd
import json
from sklearn import manifold

app = Flask("ROPMate", static_folder="",
            template_folder="", static_url_path='')

app.config['UPLOAD_FOLDER'] = './files'

PATH = "./files/default.json"
ALLOWED_EXTENSIONS = ['json']

@app.route("/")
def index():
    return render_template("index.html", path=PATH[1:])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get("files[]", None)
        if file and allowed_file(file.filename):
            filename = os.path.join(
                app.config['UPLOAD_FOLDER'], "default.json")
            file.save(filename)
            return redirect(url_for('index'))


@app.context_processor
def override_url_for_PATH():
    """
    Generate a new token on every request to prevent the browser from
    caching static files.
    """
    return dict(unique_url_for_PATH=dated_url_for_PATH)


def dated_url_for_PATH(endpoint, **values):
    date = str(os.stat(PATH).st_mtime)
    return PATH[1:] + '?q=' + date


@app.route("/mds", methods=['POST'])
def mds():
    DISSIMILARITY = 'modified_regs'
    try:
        if not request.form['type'] or not request.form['params']:
            return json.dumps({'X': [], 'labels': []})

        with open(PATH) as f:
            data_file = json.load(f)

        data_filter = filter(
            lambda d: d['type'] == request.form['type'] and d['params'] == request.form['params'], data_file)
        _data = []
    except (KeyError, FileNotFoundError):
        return json.dumps({'X': [], 'labels': []})

    added = set()
    for d in data_filter:
        dissimilar = frozenset(d[DISSIMILARITY])
        if dissimilar not in added:
            _data.append(d)
            added.add(dissimilar)

    data = pd.io.json.read_json(json.dumps(_data))
    dissM=np.zeros((len(data),len(data))) #creates a zeros dissM

    for i in range(len(data)):
        for j in range (len(data)):
            a = set(data[DISSIMILARITY][i])
            b = set(data[DISSIMILARITY][j])
            #a = set(data['mem'][i][0])
            #b = set(data['mem'][j][0])
            dissM[i][j]= len((a | b) - (a & b))

    mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9,
                   dissimilarity="precomputed")
    pos = mds.fit(dissM).embedding_

    res = {'X': [], 'labels': []}
    for label, x, y in zip(data[DISSIMILARITY], pos[:, 0], pos[:, 1]):
        res['X'].append({"x": x, "y": y})
        res['labels'].append(label)

    return json.dumps(res)



if __name__ == "__main__":
    app.debug = False
    url = 'http://127.0.0.1:5000'
    webbrowser.open_new(url)
    app.run()
    
