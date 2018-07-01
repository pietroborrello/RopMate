from flask import *
import string
import sys
import os
import numpy as np
import pandas as pd
import json
from matplotlib import pyplot as plt
from sklearn import manifold

app = Flask("ROPMate", static_folder="",
            template_folder="", static_url_path='')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/mds", methods=['POST'])
def mds():
    DISSIMILARITY = 'modified_regs'
    try:
        if not request.form['type'] or not request.form['params']:
            return json.dumps({'X': [], 'labels': []})

        with open('./files/baby_stack.json') as f:
            data_file = json.load(f)

        data_filter = filter(
            lambda d: d['type'] == request.form['type'] and d['params'] == request.form['params'], data_file)
        _data = []
    except KeyError:
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
    app.debug = True
    app.run()

