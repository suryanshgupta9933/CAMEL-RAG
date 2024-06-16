from bs4 import BeautifulSoup
import urllib.request
import random
from urllib.parse import urlparse, parse_qs, quote
import re
import time

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931',
    # Add more User-Agents if needed
]


username = 'spxn1r0koz'
password = 'k3~3s5hqJboKnV3sVm'
proxy_url = f"https://{username}:{password}@in.smartproxy.com:10000"

proxy_handler = urllib.request.ProxyHandler(
    {'http': proxy_url, 'https': proxy_url})

auth = urllib.request.HTTPBasicAuthHandler()
auth.add_password(None, proxy_url, username, password)

opener = urllib.request.build_opener(
    proxy_handler, auth, urllib.request.HTTPHandler)
urllib.request.install_opener(opener)


def filter_result(link):
    try:

        # Decode hidden URLs.
        if link.startswith('/url?'):
            o = urlparse(link, 'http')
            link = parse_qs(o.query)['url'][0]

        # Valid results are absolute URLs not pointing to a Google domain,
        # like images.google.com or googleusercontent.com for example.
        # TODO this could be improved!
        o = urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link

    # On error, return None.
    except Exception as e:
        pass


def fetch_google_search_urls(html):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the anchor tags with href attributes
    links = soup.find_all('a', href=True)

    search_urls = []

    # Filter URLs, only keeping those that point to external sites and not other Google searches or services
    for link in links:
        filtered_url = filter_result(link['href'])
        if filtered_url is not None and not re.search(r'https?://\S+\.(jpg|jpeg|png|gif|bmp)', filtered_url):
            search_urls.append(filtered_url)

    return search_urls


def search(query: str):

    params = {
        'tld': 'com',  # Top-level domain, like 'com', 'co.uk', etc.
        # Language, like 'en' for English, 'es' for Spanish, etc.
        'lang': 'en',
        # The search query
        'query': quote(query),
        'tbs': '0',  # Time limits, 'qdr:h' for past hour, 'qdr:d' for past 24 hours, 'qdr:m' for past month
        'safe': 'off',  # Safe search, 'on' or 'off'
        # Country, like 'countryUS' for United States, 'countryUK' for United Kingdom, etc.
        'country': 'countryIN'
    }

    url_search = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
        "btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&" \
        "cr=%(country)s" % params

    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(url_search, headers=headers)

    response = urllib.request.urlopen(req)

    html = response.read()

    time.sleep(2)

    urls = fetch_google_search_urls(html)

    return urls
