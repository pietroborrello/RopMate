
# coding: utf-8

# In[122]:


import numpy as np
import pandas as pd
import json
from matplotlib import pyplot as plt
from sklearn import manifold


# In[123]:


with open('/Users/pietro/Shared/RopVis/files/ls.json') as f:
    data_file = json.load(f)


# In[124]:


data_filter = filter(lambda d: d['type'] == 'LoadConst' and d['params'] == 'edi', data_file)
_data = []
for d in data_filter:
    _data.append(d)


# In[125]:


data = pd.io.json.read_json(json.dumps(_data))
data


# In[126]:


data['mem'][13][0]


# In[127]:


data['modified_regs'][13]


# In[128]:


dissM=np.zeros((len(data),len(data))) #creates a zeros dissM
for i in range(len(data)):
    for j in range (len(data)):
        a1 = set(data['modified_regs'][i])
        b1 = set(data['modified_regs'][j])
        a2 = set(data['mem'][i][0])
        b2 = set(data['mem'][j][0])
        dissM[i][j]= len((a1 | b1) - (a1 & b1))# + len((a2 | b2) - (a2 & b2))


# In[129]:


mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9,
                   dissimilarity="precomputed")
pos = mds.fit(dissM).embedding_

s = 50
plt.scatter(pos[:, 0], pos[:, 1], color='red',s=s, lw=0, label='Gadgets')


# In[130]:


for label, x, y in zip(data['modified_regs'], pos[:, 0], pos[:, 1]):
    plt.annotate(
        label,
        xy = (x, y), xytext = (-20, 20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.3', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
plt.legend()


# In[131]:


plt.show()

