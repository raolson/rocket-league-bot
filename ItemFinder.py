#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw
import pdb
import re
import os


class Finder(object):
    def __init__(self):
        self.repliedFile = "finder_replied.txt"

    def run(self):
        # Get replied comment IDs
        repliedContent = self.getReplied()

        # Create instance of Reddit
        reddit = praw.Reddit('bot1')
        subreddit = reddit.subreddit('rocketleaguefinder')

        for submission in subreddit.new(limit=10):
            if submission.id not in repliedContent:
                    title = str(submission.title.encode('utf-8')).lower()
                    platform = self.getPlatform(title)
                    itemList = self.getItemList(title)

                    results = self.findByTitle(platform, itemList)
                    if results:
                        submission.reply(results)
                        repliedContent.append(submission.id)

        # Write IDs of replied posts
        self.writeReplied(repliedContent)

    def writeReplied(self, content):
        with open(self.repliedFile, 'w') as f:
            for postID in content:
                f.write(postID + '\n')

    def findByTitle(self, platform, itemList):
        urlList = []
        reddit = praw.Reddit('bot1')
        subreddit = reddit.subreddit('rocketleagueexchange')
        for submission in subreddit.new(limit=300):
            title = str(submission.title.encode('utf-8')).lower()

            if platform and platform in title:
                if all(x in title for x in itemList):
                    urlList.append(self.formatAsLink(title, submission.url))
        return '\n\n'.join(urlList)

    def formatAsLink(self, title, url):
        title = title.replace('[', '')
        title = title.replace(']', '')
        return '[' + title + '](' + url + ')'

    def getItemList(self, title):
        """ Get requested item list less platform """
        return title.lower().split('-')[1:]

    def getPlatform(self, title):
        """ Get platform """
        if 'xbox' in title.lower():
                return 'xbox'
        elif 'ps4' in title.lower():
            return 'ps4'
        elif 'pc' in title.lower():
            return 'pc'
        else:
            return None

    def getReplied(self):
        """ Load in IDs replied to """
        with open(self.repliedFile, 'r') as f:
                content = f.read()
                content = content.split("\n")
                content = list(filter(None, content))
                return content


if __name__ == "__main__":
    Finder().run()

