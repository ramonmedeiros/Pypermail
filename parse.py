#/usr/bin/python

import lxml
import re

from lxml.html import parse
from utils import getContent


#
# CONSTANTS
#
MONTH_EXP = re.compile("<A href=\"(?P<year>[0-9]*)-(?P<month>.*)/thread.html")
THREAD_ID = re.compile("(?P<id>[0-9]*).html")

class MailingList():
    """
    Create a class that represents a mailing list
    """

    def __init__(self, url):
        """
        Create the class setting the url
        """
        self.__url = url
        self.months = None

        # update months
        self.updateMonths()

    def getMonths(self):
        """
        Wrapper for months
        """
        return self.months

    def updateMonths(self):
        """
        Retrieves months to search threads
        """
        # download url
        content = getContent(self.__url)

        if content == "":
            return None

        self.months = [ i.groupdict() for i in MONTH_EXP.finditer(content) ]

    def getPatch(self, url):
        """
        Retrieves patch content 
        """
        doc = parse(url).getroot()

        for i in doc.body.getchildren():
            if i.tag == "pre":
                return i.text_content()

    def listThreadsNew(self, month, year):
        """
        List threads using html parser
        """
        def encapsulateEmail(email):
            # get information
            subject = email[0].text_content()
            id = THREAD_ID.match(email[0].get("href")).groupdict()["id"]
            url = "%s/%s-%s/%s" % (self.__url, year, month, email[0].get("href"))
            author = email[2].text_content()

            return {"subject": subject,
                    "id": id,
                    "url": url,
                    "author": author}

        # download page
        doc = parse("%s/%s-%s/thread.html" % (self.__url, year, month))

        # get second <ul>, each <li> will be and email
        emails = doc.getroot().body.getchildren()[5].getchildren()

        threads = []

        for email in emails:

            # to avoid comments, only parse html elements
            if isinstance(email, lxml.html.HtmlElement) == False:
                continue

            # is a email: encapsulate
            mail = encapsulateEmail(email)

            # 4 children: no answers
            if len(email.getchildren()) > 4:

                # more than 4 children: append answers
                mail["emails"] = []
                for submail in email.getchildren()[3].getchildren():

                    # to avoid comments, only parse html elements
                    if isinstance(submail, lxml.html.HtmlElement):
                        mail["emails"].append(encapsulateEmail(submail))

            threads.append(mail)

        return threads

