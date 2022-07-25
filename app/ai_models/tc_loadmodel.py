import turicreate as tc
from colorClassify_v2 import colorClassify

def loadClassifyModel(model_path,img_path):
    model = tc.load_model(model_path)
    # predict image from internet by url
    # imgurl = 'https://fujitiensan.com/wp-content/uploads/2020/04/%E5%AF%8C%E5%A3%AB%E5%B1%B1%E8%A1%A3%E6%9C%8D_FUJI-ROCK-FESTIVAL-1-scaled.jpg'
    # img = tc.Image(imgurl)
    # predict image from local
    img = tc.Image(img_path)
    result = model.predict(img)
    return result

def loadSimilarityModel(model_path,img_path):
    model = tc.load_model(model_path)
    img = tc.Image(img_path)
    query_results = model.query(img, k=3)
    similar_rows = query_results[query_results['query_label'] == 0]['reference_label']
    reference_data = tc.load_sframe('similarity.sframe')
    print(similar_rows)
    reference_data.filter_by(similar_rows, 'id').explore()
    return query_results

print(loadClassifyModel('7class.model','test3.jpeg'))
print(colorClassify('test3.jpeg'))
print(loadSimilarityModel('imageSimilarity.model','test3.jpeg'))
