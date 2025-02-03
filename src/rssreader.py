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
            postinfo["summary"] = post.summary 
            # postinfo["time_published"] = post.published 
            # postinfo["authors"] = [author.name for author in post.authors] 
        except e: 
            Exception("essential information missing")
        try:
            postinfo["author"] = post.author 
        except:
            pass
        try:
            postinfo["tags"] = [tag.term for tag in post.tags] 
        except:
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
    feedInfo = get_feed_info(feed)
    # do everything else here
    data = json.dumps(feedInfo)
    allposts.append(feedInfo)

def list_post_titles(feedinfo):
    # feedinfo as dict 
    posts = feedinfo['posts']
    for i, post in enumerate(posts):
        print(i, post["title"])
    return 0

keywords = [
    "quantum",
    "information",
    "computing",
    "entropy"
]

def keyword_search(feed):
    # seach for mentions of keyword in title or summary of an article
    posts = feed["posts"]
    goodPosts = []
    for post in posts:
        text = post["title"] + " " + post["summary"]
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        if score != 0:
            goodPosts.append(post)
    return goodPosts
            

list_post_titles(allposts[0])

print(keyword_search(allposts[0]))
