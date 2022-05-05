'''
This file contains all AI models and all relevant classes or methods.
'''

from pathlib import Path

import numpy as np
import turicreate as tc
from django.conf import settings


def _load_AI_model(pb_file_path):

    model = tc.load_model(str(Path(settings.BASE_DIR, 'app', 'ai_models', pb_file_path)))
    
    return model

class Classifier():

    def __init__(self):
        self.type_model  = _load_AI_model('7class.model')
        # TODO: need to change to color model
        self.color_model = _load_AI_model('7class.model') 

    def pred_type(self, image_file_path):
        img = tc.Image(image_file_path)
        predict_result = self.type_model.predict(img)
        return "type="+predict_result
    
    def pred_color(self, image_file_path):
        img = tc.Image(image_file_path)
        predict_result = self.color_model.predict(img)
        return "color="+predict_result


if __name__ == '__main__':

        model = tc.load_model(str(Path(settings.BASE_DIR, 'app','ai_models', '7class.model')))
        model.summary()
        print('done')
        import sys
        sys.exit()
