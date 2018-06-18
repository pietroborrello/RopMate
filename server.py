from flask import *
import string
import sys
import os
import numpy as np
import pandas as pd
import json
from matplotlib import pyplot as plt
from sklearn import manifold

app = Flask("RopVis", static_folder="",
            template_folder="", static_url_path='')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/mds", methods=['POST','GET'])
def mds():
    with open('./files/ls.json') as f:
        data_file = json.load(f)

    data_filter = filter(lambda d: d['type'] == 'LoadConst' and d['params'] == 'edi', data_file)
    _data = []

    for d in data_filter:
        _data.append(d)

    data = pd.io.json.read_json(json.dumps(_data))
    dissM=np.zeros((len(data),len(data))) #creates a zeros dissM

    for i in range(len(data)):
        for j in range (len(data)):
            a1 = set(data['modified_regs'][i])
            b1 = set(data['modified_regs'][j])
            a2 = set(data['mem'][i][0])
            b2 = set(data['mem'][j][0])
            dissM[i][j]= len((a1 | b1) - (a1 & b1))# + len((a2 | b2) - (a2 & b2))
    
    mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9,
                   dissimilarity="precomputed")
    pos = mds.fit(dissM).embedding_

    res = {'X': [], 'labels': []}
    for label, x, y in zip(data['modified_regs'], pos[:, 0], pos[:, 1]):
        res['X'].append({"x": x, "y": y})
        res['labels'].append(label)

    return json.dumps(res)



if __name__ == "__main__":
    app.debug = True
    app.run()

