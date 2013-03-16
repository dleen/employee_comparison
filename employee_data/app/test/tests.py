""" tests for the our magic parser """
from nose.tools import *
import app.parser.crawler as crawl


def setup():
    print "TEAR UP!"


def teardown():
    print "TEAR DOWN!"


def test_crawler():
    url = "http://www.linkedin.com/in/dleen"
    crawler = crawl.LinkedinCrawler()
    items = crawler.start(url)
    print "items=", items
    assert items


def test_crawler_bad_format():
    url = "http://www.1linkedin.com/in/vasylvaskul"
    crawler = crawl.LinkedinCrawler()
    try:
        items = crawler.start(url)
    except BadFormatError:
        print "items=", items
        print ">>>>>>>>>>>>>>>>>Wrong URL"
