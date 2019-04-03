import feedparser

def get_rss_data(rssurl):
    """
    :param rssurl: url of rss feed to pull data from
    :return: array of arrays which contain each entry's title and corresponding url
    """
    fp = feedparser.parse(rssurl)
    entries = fp.entries
    completedata = []
    for entry in entries:
        completedata.append([entry.title, entry.link])
    return completedata


def get_feed_title(rssurl):
    """
    :param rssurl: url of rss feed to pull data from
    :return: feed's title string or empty string if title dne
    """
    fp = feedparser.parse(rssurl)
    if('title' in fp.feed):
        return fp.feed.title
    return "PLEASE PROVIDE A DIFFERENT RSS FEED URL"

