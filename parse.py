#/usr/bin/python

import re

from lxml.html import parse
from utils import getContent


#
# CONSTANTS
#
MONTH_EXP = re.compile("<A href=\"(?P<year>[0-9]*)-(?P<month>.*)/thread.html")
THREAD_EXP = re.compile("""<LI><A HREF="(?P<url>.*)">(?P<subject>.*)\n</A><A NAME="[0-9]*">\&nbsp;</A>\n<I>(?P<author>.*)\n</I>\n""")


class MailingList():
    """
    Create a class that represents a mailing list
    """

    def __init__(self, url):
        """
        Create the class setting the url
        """
        self.__url = url

    def listMonthTreads(self):
        """
        Retrieves months to search threads
        """
        # download url
        content = getContent(self.__url)

        months = [ i.groupdict() for i in MONTH_EXP.finditer(content) ]

        # get months
        return months

    def listThreads(self, month, year):
        """
        List threads each month
        """
        content = getContent("%s/%s-%s/thread.html" % (self.__url, year, month))
    
        threads = [ i.groupdict() for i in THREAD_EXP.finditer(content) ]
    
        # append full url
        for i in range(len(threads)):
            threads[i]["url"] = "%s/%s-%s/%s" % (self.__url, year, month, threads[i]["url"])

        return threads

    def getPatch(self, url):
        """
        Retrieves patch content 
        """
        doc = parse(url).getroot()

        for i in doc.body.getchildren():
            if i.tag == "pre":
                return i.text_content()

