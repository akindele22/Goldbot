from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
import pickle
import os


def pred_clf_xau():
    loaded_model = pickle.load(open("GOLD BOT/XAUUSDc_model.pkl", "rb"))
    return loaded_model