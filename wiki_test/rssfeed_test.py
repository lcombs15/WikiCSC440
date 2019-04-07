import unittest
from wiki.web.rssfeed import get_rss_data, get_feed_title


class TestRssFeed(unittest.TestCase):
    """
        Various unit tests for wiki.web.rssfeed
        Mary Grace Lammers
    """
    def test_get_feed_title(self):
        rssurl = 'https://www.reddit.com/r/python/.rss'
        self.assertEqual("Python", get_feed_title(rssurl))

    def test_get_bad_feed_title(self):
        rssurl = 'https://github.com/lcombs15/WikiCSC440/commits/master.atom?token=AkoYKxAmBxizsF72clfwxCdzYVN52qhcks66sSH-wA%3D%3D'
        self.assertEqual("PLEASE PROVIDE A DIFFERENT RSS FEED URL", get_feed_title(rssurl))

    def test_get_rss_data(self):
        rssurl = 'https://www.reddit.com/r/python/.rss'
        self.assertEqual(2, len(get_rss_data(rssurl)[0]))

    def test_get_bad_rss_data(self):
        rssurl = 'https://github.com/lcombs15/WikiCSC440/commits/master.atom?token=AkoYKxAmBxizsF72clfwxCdzYVN52qhcks66sSH-wA%3D%3D'
        self.assertEqual(0, len(get_rss_data(rssurl)))


if __name__ == '__main__':
    unittest.main()