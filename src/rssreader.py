import os
import json
import feedparser
import csv

def get_feed_info(feed):
    "extract information from a feedparser.feed object"
    feedInfo = {
        "feed-title" : feed.feed.title,
        "feed-link" : feed.feed.link         
    }
    posts = feed.entries
    postsList = []

    for post in posts: 
        postinfo = dict() 
        try: 
            postinfo["title"] = post.title 
            postinfo["link"] = post.link 
            postinfo["author"] = post.author 
            postinfo["time_published"] = post.published 
            postinfo["tags"] = [tag.term for tag in post.tags] 
            postinfo["authors"] = [author.name for author in post.authors] 
            postinfo["summary"] = post.summary 
        except e: 
            pass
        postsList.append(postinfo) 
        
    feedInfo["posts"] = postsList
    return feedInfo 

# get list of URLs
with open("../rssfeeds.csv") as feedsCSV:
    reader = csv.reader(feedsCSV)
    feeds = []
    for row in reader:
        feeds.append(row[1])

allposts = []

# parse RSS feeds from URLs
for url in feeds:
    feed = feedparser.parse(url)
    # do everything else here
    data = json.dumps(get_feed_info(feed))
    allposts.append(data)
