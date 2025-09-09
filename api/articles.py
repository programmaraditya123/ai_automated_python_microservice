import requests
# from ..services.topic_discovery.trending_topic_discovery import get_titles
# from ..services.trending_fetcher.youtube_service import get_latest_videos
from services.topicdiscovery.trendingtopicdiscovery import get_titles
from services.trendingfetcher.youtubetrendfetch import get_latest_videos

def getTitles():
    data = get_latest_videos(q="reactjs vs nextjs ",max_results=5)
    if not data:
        return "No videos found"
    video = data[0]
    titles = get_titles(video["title"],video["description"],video["comments"])
    print("88888888",titles)
    try:
        response = requests.post("http://localhost:8080/titles",json={"titles":titles})
        print(response.json(),"1111111111")
        return {"status":"success","sent_title":titles}
    except Exception as e:
        print("Error sending titles to express",e)
        return {"message":str(e)}