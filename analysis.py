import numpy as np
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict

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
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, fbeta_score, hamming_loss, precision_recall_fscore_support, precision_score, recall_score

# Config
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
np.set_printoptions(threshold=np.nan)

# Metadata
stats = ["hp","atk","def","spa","spd","spe"]
styles = {
  "Grass": {"color": "#78C850", "dashes": (None,None), "num":0},
  "Fire": {"color": "#F08030", "dashes": (None,None), "num":1},
  "Water": {"color": "#6890F0", "dashes": (None,None), "num":2},
  "Bug": {"color": "#A8B840", "dashes": [2,2], "num":3},
  "Normal": {"color": "#A8A878", "dashes": (None,None), "num":4},
  "Poison": {"color": "#A040A0", "dashes": (None,None), "num":5},
  "Electric": {"color": "#F8D030", "dashes": (None,None), "num":6},
  "Ground": {"color": "#E0C068", "dashes": (None,None), "num":7},
  "Fairy": {"color": "#FFAEC9", "dashes": [2,2], "num":8},
  "Fighting": {"color": "#C03028", "dashes": [2,2], "num":9},
  "Psychic": {"color": "#F85888", "dashes": [2,2], "num":10},
  "Rock": {"color": "#B8A038", "dashes": [2,2], "num":11},
  "Ghost": {"color": "#705898", "dashes": [2,2], "num":12},
  "Ice": {"color": "#98D8D8", "dashes": [2,2], "num":13},
  "Dragon": {"color": "#7038F8", "dashes": (None,None), "num":14},
  "Dark": {"color": "#705848", "dashes": [2,2], "num":15},
  "Steel": {"color": "#B8B8D0", "dashes": [2,2], "num":16},
  "Flying": {"color": "#A890F0", "dashes": (None,None), "num":17}
}
palette = [v['color'] for k,v in styles.iteritems()]
types = [k for k,v in styles.iteritems()]
type_nums = [v['num'] for k,v in styles.iteritems()]

# Loads dataset
df = pd.read_csv("data/dataset.csv")
df.index = df.type
cols = df.columns
dim = df.shape

# Analysis
def print_stats():
  print df.describe().transpose()

def plot_boxes():
  plt.figure(figsize=(8,4))
  df.boxplot(vert=False, figsize=(6,6), showfliers=True)
  plt.savefig("images/boxplot.png")

def plot_histograms():
  for stat in stats:
    fig = plt.figure(figsize=(10,7.5))
    ax = fig.add_subplot(111)
    ax.set_xlabel(stat.upper())
    ax.set_xlim([0,255])
    group = df.groupby('type')[stat]
    for k, v in group:
        plot = v.plot(kind = 'kde',
                     linewidth=2,
                     alpha = 0.8,
                     label = k,
                     dashes = styles[k]['dashes'],
                     color = styles[k]['color'])
    plt.legend(handlelength=3)
    plt.savefig("images/kde_"+stat+".png")

def plot_corr():
  corr = df.corr()
  sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)
  plt.xticks(rotation=90)
  plt.yticks(rotation=0)
  plt.savefig("images/corr_matrix.png")

def plot_scatter_matrix():
  sns.pairplot(df, hue="type", diag_kind="hist", palette=palette)
  plt.savefig("images/scatter_matrix.png")

def norm(df):
  return (df - df.mean()) / (df.max() - df.min())

def plot_dist():
  dfm = df.sort_values(by=["type"], ascending=[1]).loc[:,stats]
  dist = squareform(pdist(dfm.values, metric='euclidean'))
  sns.heatmap(dist)
  plt.savefig("images/dist_matrix.png")


def plot_count_per_type():
  g = df.groupby("type")
  vals = []
  labs = []
  cols = []
  for k,v in g:
    labs.append(k)
    vals.append(len(v))
    cols.append(styles[k]["color"])
    print (k,len(v))

  n_groups = len(vals)

  fig, ax = plt.subplots(figsize=(12,5))

  index = np.arange(n_groups)
  bar_width = 0.35

  opacity = 0.4
  error_config = {'ecolor': '0.3'}

  rects1 = plt.bar(index, vals, bar_width,
                  alpha=opacity,
                  color=cols)

  plt.xlabel('Type')
  plt.ylabel('Count')
  plt.title('Contagem de Pokemon por tipo')
  plt.xticks(index + bar_width, labs)
  plt.savefig("images/count.png")

#plot_count_per_type()















# ongoing work

df["type"] = df["type"].map(lambda x: styles[x]["num"])
dff = df[df.type != 17]
X = dff.as_matrix(columns=stats)
Y = dff["type"].as_matrix()

def classify():
  clfs = {
    #"naive_bayes": {"clf": GaussianNB(), "Y": None},
    "k-neighbors": {"clf": KNeighborsClassifier(1), "Y": None}
    #"SVC": {"clf": SVC(gamma=2, C=1), "Y":None},
    #"gaussian_process": {"clf": GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True), "Y": None},
    #"decision_tree": {"clf": DecisionTreeClassifier(max_depth=5), "Y": None},
    #"random_forest": {"clf": RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1), "Y": None},
    #"neural_network": {"clf": MLPClassifier(alpha=1), "Y": None}
    }

  #metrics = {
    #"accuracy_score": accuracy_score,
    #"fbeta_score": fbeta_score,
    #"hamming_loss": hamming_loss,
    #"precision_recall_fscore_support": precision_recall_fscore_support}
    #"precision_score": precision_score,
    #"recall_score": recall_score}

  print "True Y:"
  print Y

  for k,v in clfs.iteritems():
    print ("Cross validating", k)
    v["Y"] = cross_val_predict(v["clf"], X, Y, cv=10)
    print "Score:"
    print cross_val_score(v["clf"], X, Y, cv=10)
    print "Predicted Y:"
    print v["Y"]
    print ""

  #for metricName,metric in metrics.iteritems():
    #print ("Metric", metricName)
    #for clfName,clfData in clfs.iteritems():
      #print (clfName, metric(clfData["Y"], Y))


  #for i in range(10):
    #if i != 2 and i != 3:
      #scores = cross_val_score(clfs[i], X, Y, cv=9)
      #print(i, "Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

  #clf = GaussianNB()
  #clf.fit(X_, Y_)

  #for i in xrange(100):
    #print (i, clf.predict([X[i]]), Y[i])

classify()




  #X = np.array([[-1,-1], [-2,-1], [-3,-2], [1,1], [2,1], [3,2]])
  #Y = np.array([1, 1, 1, 2, 2, 2])
  #clf = GaussianNB(priors=None)
  #clf.fit(X, Y)
  #print clf.predict([[-1,-1]])

#tune_params()
#naive_bayes()

  



  

