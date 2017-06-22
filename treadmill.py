#!/usr/bin/env python

import os
import random
import urllib2
import xml.etree.ElementTree as ET
import pystache
import time

# Shells out to curl to tell Mailgun to send an email
import email

# How many bookmarks to ask user to categorize at a time
DIRTY_COUNT = 5

scriptDir = os.path.dirname(os.path.realpath(__file__))

def isDirty(p):
    return len(p.attrib['tag']) == 0 or p.attrib['description'] == 'untitled'

def getDirty(posts):
    # A post is dirty if it has no tags or has no title
    return filter(isDirty, posts)

def getUnread(posts):
    return filter(lambda p: 'toread' in p.attrib and p.attrib['toread'] == 'yes', posts)

def getEmail(posts):
    with open('{}/email.html'.format(scriptDir)) as templateFile:
        template = pystache.parse(unicode(templateFile.read()))

        allToRead = filter(lambda p: not isDirty(p), getUnread(posts))

        data = {
            'dirty': map(lambda p: p.attrib, random.sample(getDirty(posts), DIRTY_COUNT)),
            'toread': random.sample(allToRead, 1)[0].attrib,
            'date': time.strftime("%m/%d/%Y")
        }
        
        return pystache.render(template, data).encode('ascii', 'ignore')

with open('{}/token'.format(scriptDir)) as tokenFile:
    pinboardToken = tokenFile.read()
    allPosts = urllib2.urlopen('https://api.pinboard.in/v1/posts/all?auth_token={}'.format(pinboardToken)).read()
    posts = ET.fromstring(allPosts)
    message = getEmail(posts)
    print message
    print email.sendHTML('Treadmill', 'Exercises for {}'.format(time.strftime("%m/%d/%Y")), message)

