from flask import Flask, request, jsonify
app = Flask(__name__)

import pandas as pd 
import numpy as np
from keras.models import load_model
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator

file_path = 'D:/major-project/backend/trained_models/'


imageSize=224
image_details_data=pd.read_csv('D:/major-project/backend/upload/image.csv') 
images_directory='D:/major-project/backend/upload' 

images=image_details_data['image']
predict_images=pd.DataFrame(images,columns=['image'])
select_data=predict_images.iloc[0]
select_img=list(select_data)

def generate_image_datagenerator(select_img):
    predict_images1=pd.DataFrame(select_img,columns=['image'])
    predict_images1['result']='to predict'
    predict_data_gen=ImageDataGenerator(rescale=1./255.)
    predicting_generator=predict_data_gen.flow_from_dataframe(
    dataframe=predict_images1,
    directory=images_directory,
    x_col="image",
    y_col="result",
    batch_size=32,
    seed=42,
    shuffle=False,
    class_mode="categorical",
    target_size=(224,224))
    return predicting_generator


def check_for_disease(user_selected_choice):
        predicting_generator=generate_image_datagenerator(select_img)
        if(user_selected_choice==1): ##cataract detection
            cataract_model=load_model(file_path + 'cataract1.hdf5')
            pred1 = cataract_model.predict_generator(predicting_generator)
            predicted_class_idx1=np.argmax(pred1,axis=1)  ##0 for cataract
            

        elif(user_selected_choice==2): ##myopia detection
            myopia_model=load_model(file_path + 'Myopia.hdf5')
            pred1 = myopia_model.predict_generator(predicting_generator)
            predicted_class_idx1=np.argmax(pred1,axis=1)  ##0 for myopia
            

        elif(user_selected_choice==3):  ##hypertension detection
            hyp_gla_model=load_model(file_path + 'Hyp_Gla.hdf5')
            pred1 = hyp_gla_model.predict_generator(predicting_generator)
            predicted_class_idx1=np.argmax(pred1,axis=1) ##1 for hypertension
            
        
        elif(user_selected_choice==4):##glaucoma detection
            hyp_gla_model=load_model(file_path + 'Hyp_Gla.hdf5')
            pred1 = hyp_gla_model.predict_generator(predicting_generator)
            predicted_class_idx1=np.argmax(pred1,axis=1)  ##0 for glaucoma
            

        elif(user_selected_choice==5):  ##retinoblastoma detection
            retinoblastoma_model=load_model(file_path + 'retinoblastoma2_time.hdf5')
            pred1 = retinoblastoma_model.predict_generator(predicting_generator)
            predicted_class_idx1=np.argmax(pred1,axis=1)  ##1 for retinoblastoma
            

        elif(user_selected_choice==6):  ##normal
            normal_model=load_model(file_path + 'Normal.hdf5')
            pred1 = normal_model.predict_generator(predicting_generator)
            predicted_class_idx1=np.argmax(pred1,axis=1) ##0 for normal

        return predicted_class_idx1[0]


@app.route('/check_disease', methods=['POST'])
def check_disease():
    print(request.json)
    user_selected_choice = int(request.json['user_selected_choice'])
    predicted_class_idx = check_for_disease(user_selected_choice)
    return jsonify({'predicted_class_idx': str(predicted_class_idx)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)