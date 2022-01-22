from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
import sys

# flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json",
#    scopes=['https://www.googleapis.com/auth/youtube'])

# flow.run_local_server(port=8080, prompt="consent")   

# credentials = flow.credentials

DEVELOPER_KEY = "AIzaSyD5PSElg_tlHee9WlQMTxFcYx3GJZdxQ8c"
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, 
                YOUTUBE_API_VERSION, 
                developerKey=DEVELOPER_KEY)                

# youtube = build(YOUTUBE_API_SERVICE_NAME, 
#                 YOUTUBE_API_VERSION, 
#                 credentials=credentials)
#http://www.youtube.com/watch_videos?video_ids=ID1,ID2,ID3,ID4
# print(credentials.to_json())
# youtube.playlistItems().insert(part='snippet', 
#     body = 
#     { 'snippet':{
#         'playlistId': 'PLeYa4Iq4vdY8qeOXuFYRfqB8d1WM9WQve',
#         'resourceId': {
#             'kind': 'youtube#video',
#             'videoId': 'kegNKA3lm9A'
#         }
# }}).execute()

nextPageToken = None                
results = None
videos = []
videoNames_views = []
while True:
    results = youtube.playlistItems().list(part='contentDetails', 
                                            playlistId=sys.argv[1],
                                            maxResults=50,
                                            pageToken=nextPageToken).execute()   
# get video ids
    video_ids = list(map(lambda x : x['contentDetails']['videoId'], 
                                    results['items']))    
    
    videos = youtube.videos().list(part='statistics,snippet', 
                                    id=','.join(video_ids)).execute()

    videoNames_views = videoNames_views + list(map(lambda x: (x['id'], x['snippet']['title'], x['statistics']['viewCount']), videos['items']))

    nextPageToken = results.get('nextPageToken')                                                                                                                          
    if not nextPageToken:
        break                                            

           
videoNames_views.sort(key=lambda x : int(x[2]), reverse=True)
#http://www.youtube.com/watch_videos?video_ids=ID1,ID2,ID3,ID4
print 
print(videoNames_views[:15])
print("http://www.youtube.com/watch_videos?video_ids=" + ','.join(list(map(lambda x : x[0] , videoNames_views[:3]))))
