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
parameter1='KrishNaik'       
channel_id = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&q='+parameter1+'&type=channel&key='+API_Key).json()['items'][0]['id']['channelId']
print(channel_id)
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = API_Key)


def get_channel_stats(youtube,channel_id):
       request = youtube.channels().list(part="snippet,contentDetails,statistics",id=channel_id)
       response=request.execute()
       data=dict(channel_name=response['items'][0]['snippet']['title'],
       subcribers=response['items'][0]['statistics']['subscriberCount'],
       Total_videos=response['items'][0]['statistics']['videoCount'],
       views=response['items'][0]['statistics']['viewCount'],
       playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    
       )
       return data.get("playlist_id")
#get_channel_stats(youtube,channel_id)       
a=  get_channel_stats(youtube,channel_id)     
def get_video_id(youtube,a):
    request= youtube.playlistItems().list(part='contentDetails',playlistId=a,maxResults=50)
    response = request.execute()
    video_ids=[]
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

        
    
    
    return video_ids
b= get_video_id(youtube,a)
c=','.join(b)

def get_video_details(youtube,c):
    all_video_stats=[]
    
    request = youtube.videos().list(part='snippet,statistics',id=c)
    response = request.execute()
    for video in response['items']:
        video_stats=dict(Title=video['snippet']['title'],
                Views=video['statistics']['viewCount'],
                Likes=video['statistics']['likeCount'],      
                Comments=video['statistics']['commentCount'],
                )
        all_video_stats.append(video_stats)

    return all_video_stats

a=get_video_details(youtube,c)
video_data=pd.DataFrame(a)
print(video_data)



