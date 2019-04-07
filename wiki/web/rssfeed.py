import feedparser

def get_rss_data(rssurl):
    """
    Parses the RSS feed for the url provided and for each entry in the feed,
    adds an array of two elements, the entry's title and url link, to one array
    that contains every entry's data. This array of arrays is then returned.

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
    Parses the rss feed for the url provided and returns its title. If it does not have
    a title the string "PLEASE PROVIDE A DIFFERENT RSS FEED URL" is returned

    :param rssurl: url of rss feed to pull data from
    :return: feed's title string or error message if title dne
    """
    fp = feedparser.parse(rssurl)
    if('title' in fp.feed):
        return fp.feed.title
    return "PLEASE PROVIDE A DIFFERENT RSS FEED URL"

