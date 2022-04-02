from typing import List
from joblib import load
import os

class LeakDetection:
    def __init__(self, dirname='.'):
        print(dirname)
        self.model = self.load_model(dirname)

    def load_model(self, dirname):
        """
        Loads your pretrained model to use it for prediction. If no model was build you can ignore this.
        :return:
        """
        return load(os.path.join(dirname, 'tree.joblib'))

    def predict(self, features: List) -> bool:
        """
        Your implementation for prediction. If leak is detected it should return true.
        :param features: A list of features
        :return: Should return true if leak is detected. Otherwise, it should return false.
        """
        pred = self.model.predict([[0,1]])
        return pred[0] == 1
