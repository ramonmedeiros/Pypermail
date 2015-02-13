#!/usr/bin/python

import urllib2


def getContent(url):
    """
    Retrives url content 
    """
    try:
        content = urllib2.urlopen(url)
    except IOError:
        return ""

    return content.read()
