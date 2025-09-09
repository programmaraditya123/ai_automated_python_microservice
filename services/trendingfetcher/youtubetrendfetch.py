import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("YT_API_KEY")
print(API_KEY)
youtube = build("youtube","v3",developerKey=API_KEY)

def get_latest_videos(q="programming",max_results=2 ):
    search_response = youtube.search().list(
        q = q,
        part = "snippet",
        type = "video",
        order = "viewCount",
        maxResults = max_results
    ).execute()
    
    # print(json.dumps(search_response,indent=2))
    videos = []
    for item in search_response.get('items',[]):
     
        video_id =  item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        published_at = item["snippet"]["publishedAt"]

        #fetch comments 
        comments = get_video_comments(video_id)

        videos.append({
            "video_id":video_id,
            "title" : title,
            "description" : description,
            "published_at" : published_at,
            "comments" : comments
        })

    return videos

def get_video_comments(video_id,max_comments = 10):
    comments = []
    try:
        comment_response = youtube.commentThreads().list(
            part = "snippet",
            videoId = video_id,
            maxResults = max_comments,
            textFormat = "plainText"
        ).execute()

        for item in comment_response["items"]:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment_text)
    except Exception as e:
        print(f"Error fetching comments from video id {video_id} : {e}")
    return comments

if __name__ == "__main__":
    latest_videos = get_latest_videos(q="What are runnables in langchain",max_results=1)
    for videos in latest_videos:
        print(videos)
