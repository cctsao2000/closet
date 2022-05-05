# '''
# This file contains all AI models and all relevant classes or methods.
# '''

# from pathlib import Path

<<<<<<< HEAD
# import numpy as np
# # import tensorflow as tf
# import turicreate as tc
# from django.conf import settings


# def _load_classify_AI_model(pb_file_path):

    # # model = tc.load_model(Path(settings.BASE_DIR, 'app', 'pretrained_ai_models', pb_file_path))
    # model = tc.load_model('app/pretrained_ai_models/7class.model')

    # return model
=======
import numpy as np
import turicreate as tc
from django.conf import settings


def _load_AI_model(pb_file_path):

    model = tc.load_model(str(Path(settings.BASE_DIR, 'app', 'ai_models', pb_file_path)))
    
    return model
>>>>>>> b8cbca1591acd2ca48f5e4cd9b6dbc2d6699d454

# class Classifier():

<<<<<<< HEAD
    # def __init__(self):
        # self.model = _load_classify_AI_model('7class.model')

    # def predict(self, image_file_path):
        # model = _load_classify_AI_model('7class.model') # 'model' undefined without this line
        # img = tc.Image(image_file_path)
        # predict_result = model.predict(img)
        # return predict_result
=======
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

>>>>>>> b8cbca1591acd2ca48f5e4cd9b6dbc2d6699d454

# if __name__ == '__main__':

<<<<<<< HEAD
        # # model = tc.load_model(Path('pretrained_ai_models', '7class.model'))
        # model = tc.load_model('pretrained_ai_models/7class.model')
        # model.summary()
        # print('done')
        # import sys
        # sys.exit()
=======
        model = tc.load_model(str(Path(settings.BASE_DIR, 'app','ai_models', '7class.model')))
        model.summary()
        print('done')
        import sys
        sys.exit()
>>>>>>> b8cbca1591acd2ca48f5e4cd9b6dbc2d6699d454
