'''
This file contains all AI models and all relevant classes or methods.
'''

from pathlib import Path

import numpy as np
import turicreate as tc
from django.conf import settings


def _load_classify_AI_model(pb_file_path):

    model = tc.load_model(str(Path(settings.BASE_DIR, 'app', 'ai_models', pb_file_path)))
    
    return model

class Classifier():

    def __init__(self):
        self.model = _load_classify_AI_model('7class.model')

    def predict(self, image_file_path):
        img = tc.Image(image_file_path)
        predict_result = self.model.predict(img)
        return predict_result

if __name__ == '__main__':

        model = tc.load_model(str(Path(settings.BASE_DIR, 'app','ai_models', '7class.model')))
        model.summary()
        print('done')
        import sys
        sys.exit()
