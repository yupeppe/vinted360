from scrapers.common import demo_item

def run_scraper(platform, query, params=None):
    return [demo_item('Vinted', query)] if query else []
