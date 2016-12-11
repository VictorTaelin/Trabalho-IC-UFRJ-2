import numpy as np
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
import scatter as sc 
from itertools import imap
from matplotlib import cm
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import svm
from sklearn.model_selection import cross_val_score

from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

# Loads dataset
df = pd.read_csv("dataset/dataset.csv")

# Removes turn outliers
df = df[df.turn < df.turn.mean() + df.turn.std()*3]
cols = df.columns
dim = df.shape

ins = ["turn","a_elo","a_health","a_hp","a_atk","a_def","a_spa","a_spd","a_spe","a_usage","a_boost","a_status","a_party","b_elo","b_health","b_hp","b_atk","b_def","b_spa","b_spd","b_spe","b_usage","b_boost","b_status","b_party"]
out = "switch"

def naive_bayes():
  X = df.as_matrix(columns=ins)
  Y = df[out].as_matrix()

  X_ = X[0:22000]
  Y_ = Y[0:22000]

  clfs = [
      KNeighborsClassifier(3),
      SVC(kernel="linear", C=0.025),
      SVC(gamma=2, C=1),
      GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
      DecisionTreeClassifier(max_depth=5),
      RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
      MLPClassifier(alpha=1),
      AdaBoostClassifier(),
      GaussianNB(),
      QuadraticDiscriminantAnalysis()]

  for i in xrange(10):
    if i != 2:
      scores = cross_val_score(clfs[6], X_, Y_, cv=8)
      print(i,"Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))



  #for i in xrange(200):
    #print (clf.predict([X[65000+i]]), Y[65000+i])

#naive_bayes()

#def plotDists():
  #dists = pd.read_csv("dists.csv")
  #dists.dist.plot()
  #plt.savefig("images/dists.png")

#def plotBox(attr):
  #plt.figure(figsize=(8,4))
  #df.boxplot(column=attr, vert=False, figsize=(6,6), showfliers=True)
  #plt.savefig("images/"+attr+"_boxplot.png")
##plotBox("a_hp")

#def plotScatterMatrix():
  #fst_half = cols[:13]
  #snd_half = cols[13:]
  #color = np.zeros((dim[0],4))
  #for i in xrange(dim[0]):
    #if df.switch.iloc[i] == 1:
      #color[i,0] = 1.0
      #color[i,1] = 0.0
      #color[i,2] = 0.0
      #color[i,3] = 0.045
    #else:
      #color[i,0] = 0.0
      #color[i,1] = 1.0
      #color[i,2] = 1.0
      #color[i,3] = 0.009
  #for j, a in zip(xrange(2), [fst_half, snd_half]):
    #for i, b in zip(xrange(2), [fst_half, snd_half]):
      #print "Computing matrix "+str(i)+" "+str(j)
      #sc.scatter_matrix(df, a, b, figsize=(16,16), color=color)
      #plt.savefig("images/scatter_matrix_"+str(i)+"_"+str(j)+".png")
##plotScatterMatrix()

#def plotHist():
  #df.hist(bins=32, alpha=0.5, layout=(13,2), figsize=(10,32))
  #plt.savefig("images/histograms.png")
##plotHist()

def plotCorr():
  #corr = np.vectorize(lambda x: (x+1)*0.5)(df.corr())
  corr = df.corr()
  print corr
  #plt.figure(figsize=(8,7))
  #sns.heatmap(corr, 
            #xticklabels=corr.columns.values,
            #yticklabels=corr.columns.values)
  #plt.xticks(rotation=90)
  #plt.yticks(rotation=0)
  #plt.savefig("images/corr_matrix.png")
plotCorr()

#def norm(df):
  #return (df - df.mean()) / (df.max() - df.min())

#def plotDist():
  ##dfs = df.sort_values(by=['switch'], ascending=[1])
  #dfm = norm(df)[0:5000].sort_values(by=['switch'], ascending=[1])
  #dist = squareform(pdist(dfm.values, metric='euclidean'))
  ##dist = cosine_similarity(dfm.values)
  
  #sns.heatmap(dist)
  #plt.savefig("images/dist_matrix.png")
##plotDist()

## Too damn slow, using JS instead
#def dists(df):
  #dists = []
  #for j in xrange(df.shape[0]):
    #print (j,df.shape[0])
    #dist = 0
    #this = df.iloc[j].values
    #for i in xrange(df.shape[0]):
      #if i != j:
        #that = df.iloc[i].values
        #dist += np.linalg.norm(this-that)
    #dist /= df.shape[0]
    #dists.append((j,dist))
  #return dists
    



  



