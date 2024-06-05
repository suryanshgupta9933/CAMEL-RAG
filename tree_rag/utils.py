# Importing Dependencies
from .GoogleSearchScrapper import GoogleSearchModule

# Google Search Module
def get_filtered_urls(query):
    # Create an instance of GoogleSearchModule with the topic you want to search for
    search_module = GoogleSearchModule(query)
    # Get URLs, filtered to exclude certain social media sites
    filtered_urls = search_module.get_url(query)
    
    return filtered_urls