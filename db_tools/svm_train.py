from motors.models import *
import numpy as np

packs = CurrentSignalPack.objects.all()
dataset = []
harset = []
brbset = []
label =  [[ 0 for i in range(150)] + [1 for j in range(150) ] + [2 for k in range(150) ] + [3 for w in range(150) ] for h in range(3)]

for item in packs:
    dataset.append([item.uphase.frequency, item.ufeature.rms, item.ufeature.thd])
    harset.append(np.fromstring(item.ufeature.harmonics))
    brbset.append(np.fromstring(item.ufeature.fbrb))


data = np.array(dataset)
data = np.concatenate((dataset,harset,brbset),axis=1)
target = np.array(label).flatten()

mean = np.array([ np.mean(data[:,i]) for i in range(data.shape[1])])
var = np.array([ np.var(data[:,i]) for i in range(data.shape[1])])

from sklearn import svm
from sklearn import preprocessing

X = preprocessing.scale(data)

perm = np.random.permutation(1800)
X = X[perm]
Y = target[perm]
# split the dataset,8:2
X_train = X[:1200, :]
X_test = X[1200:, :]

Y_train = Y[0:1200]
Y_test = Y[1200:]
clf = svm.SVC(kernel='rbf', gamma= 'scale')
clf.fit(X_train, Y_train)
svm_score = clf.score(X_test, Y_test)
print(svm_score)

import pickle
s = pickle.dumps(clf)

f = open('./MLmodel/svm-rbf.txt', 'wb')
f.write(s)
f.close()


f2=open('./MLmodel/svm-rbf.txt','rb')
s2=f2.read()
clf2=pickle.loads(s2)