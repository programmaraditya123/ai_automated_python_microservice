import requests
from services.topicdiscovery.trendingtopicdiscovery import get_titles
from services.trendingfetcher.youtubetrendfetch import get_latest_videos
import os

EXPRESS_API=os.getenv("EXPRESS_API")


TOPICS = [
    # Science
    "Physics", "Chemistry", "Biology", "Astronomy", "Geology", "Environmental Science",
    "Nanotechnology", "Quantum Computing", "Robotics", "Neuroscience", "Genetics",
    
    # Technology
    "Artificial Intelligence", "Machine Learning", "Deep Learning", "Cybersecurity", "Blockchain",
    "ReactJS vs NextJS", "Python Programming", "Web Development", "Cloud Computing",
    "Internet of Things", "5G Technology", "Virtual Reality", "Augmented Reality",
    
    # Arts & Culture
    "Modern Art", "Literature", "Music Trends", "Movies 2025", "Fashion Industry",
    "Photography", "Theatre", "Cultural Heritage", "Animation",
    
    # History & Politics
    "Ancient Civilizations", "World War 2", "Cold War", "Modern Democracies",
    "Geopolitics", "United Nations", "Elections", "Global Conflicts",
    
    # Sports
    "Football World Cup", "Cricket World Cup", "Olympics", "NBA", "Tennis Grand Slam",
    "Formula 1", "eSports", "Marathons", "Chess",
    
    # Economy & Business
    "Stock Market", "Global Economy", "Startups", "Entrepreneurship",
    "Cryptocurrency", "E-commerce", "Green Economy", "Real Estate",
    
    # Health & Lifestyle
    "Mental Health", "Fitness", "Nutrition", "Yoga", "Travel", "Food Trends",
    "Diseases", "Vaccines", "Longevity Research",
    
    # Society
    "Education", "Philosophy", "Languages", "Psychology", "Religion",
    "Gender Equality", "Human Rights", "Law and Order",
    
    # Global Issues
    "Climate Change", "Poverty", "Energy Crisis", "Water Scarcity", "Migration",
    "Sustainability", "Biodiversity Loss", "Plastic Pollution"
]

current_index = {"value": 0}

def getTitles():
    topic = TOPICS[current_index["value"]]

    # move index forward (wrap around to 0 at the end)
    current_index["value"] = (current_index["value"] + 1) % len(TOPICS)

    print(f"🔎 Querying topic: {topic}")

    data = get_latest_videos(q=topic,max_results=5)
    if not data:
        return "No videos found"
    video = data[0]
    titles = get_titles(video["title"],video["description"],video["comments"])
    print("88888888",titles)
    try:
        response = requests.post(f"{EXPRESS_API}/titles",json={"titles":titles})
        print(response.json(),"1111111111")
        return {"status":"success","sent_title":titles}
    except Exception as e:
        print("Error sending titles to express",e)
        return {"message":str(e)}