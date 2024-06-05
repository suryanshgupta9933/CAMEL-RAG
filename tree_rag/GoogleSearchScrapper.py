from .google_search import search
from typing import List
import logging
import time
import re


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def calculate_time_taken(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        time_taken = end_time - start_time
        print(
            f"Time taken for GoogleSearchScrapper function to run : {time_taken} seconds")
        return result
    return wrapper


class GoogleSearchModule:

    def __init__(self, topic: str):

        self.topic = topic
        self.total_urls = 0

    def get_url(self, topic: str):
        try:
            result = search(topic, start=0, stop=3)
        except Exception as e:
            logging.error(
                f"GoogleSearchScrapper could not fetch urls for {topic} : {e}")
            return None

        url_list = [url for url in result]

        twitter_regex = r'https?://(www\.)?twitter\.com/'
        youtube_regex = r'https?://(www\.)?youtube\.com/'
        linkedin_regex = r'https?://(www\.)?linkedin\.com/'
        instagram_regex = r'https?://(www\.)?instagram\.com/'
        facebook_regex = r'https?://(www\.)?facebook\.com/'

        filtered_urls = []
        for url in url_list:
            # Check if the URL matches any of the regular expressions
            if not re.search(twitter_regex, url) and \
                    not re.search(youtube_regex, url) and \
                    not re.search(linkedin_regex, url) and \
                    not re.search(instagram_regex, url) and \
                    not re.search(facebook_regex, url):
                # If the URL does not match any of the regular expressions, add it to the filtered list
                filtered_urls.append(url)

        self.total_urls += len(filtered_urls)

        return list(filtered_urls)
