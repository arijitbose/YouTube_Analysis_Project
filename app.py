import json
import requests
from bs4 import BeautifulSoup 
import pandas as pd
from urllib.request import urlopen
from flask import Flask,request,app,jsonify,url_for,render_template

import json
from pandas import json_normalize
from IPython.display import HTML
import os
import time
from urllib import response
import googleapiclient
from googleapiclient.discovery import build
import pandas as pd
import requests
import json
path='.secret/credentials.json'
def get_keys(path):
    with open(path) as f:
        return json.load(f)
keys = get_keys(path)
API_Key = keys['api_key'] 
from youtube_scrape import *
       




app=Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    parameter1=str(data.get('name'))
    channel_id = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&q='+parameter1+'&type=channel&key='+API_Key).json()['items'][0]['id']['channelId']
    print(channel_id)
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = API_Key)
    a=  get_channel_stats(youtube,channel_id) 
    b= get_video_id(youtube,a)
    c=','.join(b)
    d=get_video_details(youtube,c)
    video_data=pd.DataFrame(d)
    print(video_data)
    return str(video_data)
@app.route('/predict',methods=['POST'])
def predict():
   
    searchString1 = request.form.values()
    data1=''.join(searchString1)
    channel_id = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&q='+data1+'&type=channel&key='+API_Key).json()['items'][0]['id']['channelId']
    print(channel_id)
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = API_Key)
    a1=  get_channel_stats(youtube,channel_id) 
    b1= get_video_id(youtube,a1)
    c1=','.join(b1)
    d1=get_video_details(youtube,c1)
    video_data=pd.DataFrame(d1)
    # print(video_data)
    
    html_final = video_data.to_html()
    
    text_file = open("templates/result.html", "w")
    text_file.write(html_final)
     
    text_file.close()
   
   
    
    


    return render_template("result.html",name=predict) 
    # return str(video_data)    
    
   


if __name__=="__main__":
    app.run(debug=True)