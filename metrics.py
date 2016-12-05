from results import *
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
from sklearn.metrics import accuracy_score, f1_score, fbeta_score, hamming_loss, precision_recall_fscore_support, precision_score, recall_score, confusion_matrix, classification_report
import pandas as pd

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def df_to_markdown(df, float_format='%.2g'):
    from os import linesep
    return linesep.join([
        '|'.join(df.columns),
        '|'.join(4 * '-' for i in df.columns),
        df.to_csv(sep='|', index=False, header=False, float_format=float_format)
    ]).replace('|', ' | ')

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
  "Steel": {"color": "#B8B8D0", "dashes": [2,2], "num":16}}
types = [k for k,v in styles.iteritems()]

for c in Ys:
  Yp = Ys[c]
  print c
  print ("Accuracy "+str(accuracy_score(Y, Yp)))
  #print ("Precision "+str(precision_score(Y, Yp)))
  #print ("Recall "+str(recall_score(Y, Yp)))









  conf = confusion_matrix(Y, Yp)

  df = pd.DataFrame(data=conf, columns=types, index=types)
  print "Confusion Matrix:"
  print df_to_markdown(df)
  print ""
  print ""

  cr = classification_report(Y, Yp)
  print cr
  #df = pd.DataFrame(data=cr, columns=types)
  #print df




