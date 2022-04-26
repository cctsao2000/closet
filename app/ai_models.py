'''
This file contains all AI models and all relevant classes or methods.
'''

from pathlib import Path

import numpy as np
# import tensorflow as tf
import turicreate as tc
from django.conf import settings


def _load_classify_AI_model(pb_file_path):

    # model = tc.load_model(Path(settings.BASE_DIR, 'app', 'pretrained_ai_models', pb_file_path))
    model = tc.load_model('app/pretrained_ai_models/7class.model')

    return model

class Classifier():

    def __init__(self):
        self.model = _load_classify_AI_model('7class.model')

    def predict(self, image_file_path):
        model = _load_classify_AI_model('7class.model') # 'model' undefined without this line
        img = tc.Image(image_file_path)
        predict_result = model.predict(img)
        return predict_result

if __name__ == '__main__':

        # model = tc.load_model(Path('pretrained_ai_models', '7class.model'))
        model = tc.load_model('pretrained_ai_models/7class.model')
        model.summary()
        print('done')
        import sys
        sys.exit()
