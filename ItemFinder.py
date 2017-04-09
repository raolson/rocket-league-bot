#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw
import sys
from DBConnect import Connect


class Finder(object):
    def __init__(self):
        self.repliedFile = 'finder_replied.txt'
        self.subFind = 'rocketleagueexchange'
        self.subReply = 'rocketleaguefinder'
        self.badChars = '[]()'
        self.botProfile = 'bot1'

    def run(self):
        """
        Entry point to search subreddit to be summoned
        """
        # Get replied comment IDs
        repliedContent = self.getReplied()

        # Create instance of Reddit
        reddit = praw.Reddit(self.botProfile)
        subreddit = reddit.subreddit(self.subReply)

        for submission in subreddit.new(limit=10):
            if submission.id not in repliedContent:
                    title = str(submission.title.encode('utf-8')).lower()
                    platform = self.getPlatform(title)
                    itemList = self.getItemList(title)
                    results = self.findAll(platform, itemList)
                    if results:
                        submission.reply(results)
                        repliedContent.append(submission.id)

                        # Write IDs of replied post
                        self.writeReplied(repliedContent)

                        # Store in sqlite db
                        Connect().storeData(submission.id, title, results)
                        """
                        Exiting after 1 reply per API limit
                        Profile needs more karma to increase limit
                        """
                        sys.exit()

    def writeReplied(self, content):
        """ Write exising and new IDs to file """
        with open(self.repliedFile, 'w') as f:
            for postID in content:
                f.write(postID + '\n')

    def findAll(self, platform, itemList):
        """
        Find all occurances in posts and comments
        Return formatted response
        """
        postList = []
        commentList = []
        reddit = praw.Reddit(self.botProfile)
        subreddit = reddit.subreddit(self.subFind)
        for submission in subreddit.new(limit=500):
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
        response = self.formatResponse(postList, commentList)
        return response

    def formatAsLink(self, text, url):
        """ Remove special chars and format as Reddit URL link """
        for c in self.badChars:
            text = text.replace(c, '')
        return '[' + text + '](' + url + ')'

    def formatResponse(self, posts, comments):
        """ Format Bot response for readability """
        return 'Posts\n' + '\n\n'.join(posts) + '\n\nComments\n' + '\n\n'.join(comments)

    def getItemList(self, title):
        """ Get requested item list less platform """
        return title.lower().split('-')[1:]

    def getPlatform(self, title):
        """ Get platform by title"""
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

