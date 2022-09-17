import cv2
import numpy as np
import turicreate as tc
from .tc_loadmodel import loadSimilarityModel


def selectarea(img_path, userid):
    img_raw = cv2.imread(img_path)
    showCrosshair = False
    ROIs = cv2.selectROIs("Select ROIs",img_raw,showCrosshair)

    crop_number=0

    #loop over every bounding box save in array "ROIs"
    for rect in ROIs:
        cropped_image = img_raw[int(rect[1]):int(rect[1]+rect[3]),
                                int(rect[0]):int(rect[0]+rect[2])]
        #show cropped image
        filename = "crop"+str(crop_number)+".jpeg"
        cv2.imshow(filename[:-5],cropped_image)
        #save cropped image
        cv2.imwrite(filename,cropped_image)
        crop_number+=1
        print(loadSimilarityModel(userid+'_imageSimilarity.model',filename))

    #hold window
    cv2.waitKey(0)

def refreshSimilarityModel(sourceimgfolder, userid):
    reference_data  = tc.image_analysis.load_images(sourceimgfolder)
    print(sourceimgfolder)
    reference_data = reference_data.add_row_number()
    model = tc.image_similarity.create(reference_data)
    model.save(userid+'_imageSimilarity.model')

# input outfit image
# selectarea("test_original.jpeg")