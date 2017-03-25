#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw
import sys


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

                    results = self.findAll(platform, itemList)
                    if results:
                        submission.reply(results)
                        repliedContent.append(submission.id)

                        # Write IDs of replied post and exit
                        self.writeReplied(repliedContent)
                        sys.exit()

    def writeReplied(self, content):
        with open(self.repliedFile, 'w') as f:
            for postID in content:
                f.write(postID + '\n')

    def findAll(self, platform, itemList):
        postList = []
        commentList = []
        reddit = praw.Reddit('bot1')
        subreddit = reddit.subreddit('rocketleagueexchange')
        for submission in subreddit.new(limit=300):
            title = str(submission.title.encode('utf-8')).lower()

            if platform and platform in title:

                # add for title match
                if all(x in title for x in itemList):
                    postList.append(self.formatAsLink(title, submission.url))

                # add for comment match
                for comment in submission.comments.list():
                        text = comment.body.encode('utf-8').lower()
                        if all(x in text for x in itemList):
                            commentList.append(self.formatAsLink(text, submission.url))
        return 'Posts\n' + '\n\n'.join(postList) + '\nComments\n' + '\n\n'.join(commentList)

    def formatAsLink(self, text, url):
        text = text.replace('[', '')
        text = text.replace(']', '')
        return '[' + text + '](' + url + ')'

    def getItemList(self, title):
        """ Get requested item list less platform """
        return title.lower().split('-')[1:]

    def getPlatform(self, title):
        """ Get platform """
        if 'xbox' in title:
                return 'xbox'
        elif 'ps4' in title:
            return 'ps4'
        elif 'pc' in title:
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

