'''
This file contains all AI models and all relevant classes or methods.
'''

from pathlib import Path

import numpy as np
import turicreate as tc
from colorClassify_v2 import colorClassify
from django.conf import settings
# import tc_imageSimilarity_v1

def _load_AI_model(pb_file_path):

    model = tc.load_model(str(Path(settings.BASE_DIR, 'app', 'ai_models', pb_file_path)))

    return model

class Classifier():

    def __init__(self):
        self.type_model  = _load_AI_model('7class.model')
        self.color_model = _load_AI_model('16color.model')

    def pred_type(self, image_file_path):
        img = tc.Image(image_file_path)
        predict_result = self.type_model.predict(img)
        return predict_result

    def pred_color(self, image_file_path):
        predict_result = colorClassify(image_file_path)
        # img = tc.Image(image_file_path)
        # predict_result = self.color_model.predict(img)
        return predict_result

class Recommender():
    def __init__(self):
        self.similar_model = _load_AI_model('imageSimilarity.model')

    def refresh_model(self):
        # new_model = tc_imageSimilarity_v1
        self.similar_model = _load_AI_model(new_model)

    def find_similar(self, image_file_path):
        img = tc.Image(image_file_path)
        query_results = model.query(img, k=3)
        return query_results



if __name__ == '__main__':

        model = tc.load_model(str(Path('ai_models', '7class.model')))
        model.summary()
        print('done')
        import sys
        sys.exit()
