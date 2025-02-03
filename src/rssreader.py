import os
import json
import feedparser
import csv

def get_feeds(feedsCSVpath):
    """extract RSS feeds from a CSV file"""
    # get list of URLs
    with open(feedsCSVpath) as feedsCSV:
        reader = csv.reader(feedsCSV)
        feedURLs = []
        for row in reader:
            feedURLs.append(row[1])
    allposts = []
    # parse RSS feeds from URLs
    for url in feedURLs:
        feed = feedparser.parse(url)
        feedInfo = get_feed_info(feed)
        # data = json.dumps(feedInfo)
        allposts.append(feedInfo)
    return allposts
    
def get_feed_info(feed):
    "extract information from a feedparser.feed object"
    feedInfo = {"feed-title": feed.feed.title, "feed-link": feed.feed.link}
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
        except Exception:
            Exception("Essential info missing")
        try:
            postinfo["author"] = post.author
        except Exception:
            pass
        try:
            postinfo["tags"] = [tag.term for tag in post.tags]
        except Exception:
            pass
        postsList.append(postinfo)

    feedInfo["posts"] = postsList
    return feedInfo

def list_post_titles(feedinfo):
    """for every post in an RSS feed print the title"""
    posts = feedinfo["posts"]
    for i, post in enumerate(posts):
        print(i, post["title"])
    return 0

def get_keywords(keywordsPath):
    with open(keywordsPath) as keywordsfile:
         keywordSTR = keywordsfile.read()
    keywords = keywordSTR.split("\n")
    if keywords[-1] == '':
        keywords.pop(-1)
    return keywords

def filter_posts(feed):
    """seach for mentions of keyword in title or summary of an article"""
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


if __name__ == "__main__":
    feedsCSVpath = "../rssfeeds.csv"
    feeds = get_feeds(feedsCSVpath)

    keywordsPath = "../keywords.txt"
    keywords = get_keywords(keywordsPath)

    summary = []
    for feed in feeds:
        # list_post_titles(feed)
        for filtered_post in filter_posts(feed):
            summary.append(filtered_post)

    for post in summary:
        print(post["title"])
        print("\t", post["link"])
