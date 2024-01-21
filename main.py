from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont

subscription_key = 'e90f0995b50a47638fa613c88452ba84'
endpoint = 'https://20240105.cognitiveservices.azure.com/'

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def get_tags(filepath):
    local_image = open(filepath, "rb")
    tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)  
    return tags_name

def detect_objects(filepath):
    local_image = open(filepath, "rb")
    print("==== Detect Objects -local ====")
    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results.objects
    return objects



st.title('ばんちゃんの物体検出アプリ')

uploaded_file = st.file_uploader("写真を選択してください", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    objects = detect_objects(img_path)


    #描画
    draw = ImageDraw.Draw(img)
    for object  in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

        font = ImageFont.truetype(font='./Helvetica.ttf', size=50)
        #text_w, text_h = draw.textbbox((0, 0), caption, font=font)  # Use (0, 0) as placeholder coordinates
        text_w, text_h, *other_values = draw.textbbox((0, 0), caption, font=font)

        draw.rectangle([(x,y), (x+w, y+h)], fill = None, outline='green', width=20)
        draw.rectangle([(x,y), (x+text_w, y+text_h)], fill = 'green' , width=200)
        draw.text((x,y), caption, fill='white', font=font)

    st.image(img)




    st.markdown('認識されたコンテンツタグ')
    
    tags = get_tags(img_path)
    st.markdown(tags)



