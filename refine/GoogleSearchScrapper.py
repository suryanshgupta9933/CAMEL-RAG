# from googe_search import search
from src.my_google_search import search
from typing import List
import logging
import time
from apify_client import ApifyClient
from contextlib import contextmanager
import concurrent.futures
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

    def __init__(self, topics: List[str]):

        self.topics = topics
        self.master_list = []
        self.successful_topics = 0

    # @calculate_time_taken

    def get_url(self, topic: str):
        retries = 0
        success = False
        filtered_urls = []

        while retries < 2 and not success:

            try:
                result = search(topic)

                url_list = [url for url in result]

                twitter_regex = r'https?://(www\.)?twitter\.com/'
                youtube_regex = r'https?://(www\.)?youtube\.com/'
                linkedin_regex = r'https?://(www\.)?linkedin\.com/'
                instagram_regex = r'https?://(www\.)?instagram\.com/'
                facebook_regex = r'https?://(www\.)?facebook\.com/'

                for url in url_list:
                    # Check if the URL matches any of the regular expressions
                    if not re.search(twitter_regex, url) and \
                            not re.search(youtube_regex, url) and \
                            not re.search(linkedin_regex, url) and \
                            not re.search(instagram_regex, url) and \
                            not re.search(facebook_regex, url):
                        # If the URL does not match any of the regular expressions, add it to the filtered list
                        filtered_urls.append(url)

                success = True
                self.successful_topics += 1

                return list(filtered_urls)[:2]

            except Exception as e:
                retries += 1
                print(f"retry : {retries}")
                time.sleep(3)

        return filtered_urls

    @calculate_time_taken
    def get_all_urls(self, topics: List[str]):

        master_urls = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self.get_url, topic)
                       for topic in topics]
            concurrent.futures.wait(futures)
            urls = [future.result() for future in futures]

        for url_list in urls:
            if len(url_list) != 0:
                master_urls.extend(url_list)

        logging.info(
            f" Scrapped {len(master_urls)} urls from {self.successful_topics}/{len(topics)} topics")

        return master_urls


'''
topics = ['what is data visualization in startup investments',
          'key data visualization techniques for evaluating startups',
          'how to use data visualization to spot investment potential',
          'examples of successful startup investments identified through data visualization',
          'tools for data visualization in startup analysis',
          'importance of data visualization in venture capital',
          'common pitfalls in interpreting startup data visualizations',
          'data visualization metrics for startup success potential',
          'case studies on data visualization leading to successful investments',
          'how to learn data visualization for startup investment analysis']


m = GoogleSearchModule(topics)
result = m.get_all_urls(topics)
'''
