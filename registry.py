from .common import demo_item

try:
    from .vinted import search_vinted
except Exception:
    search_vinted = None


def run_scraper(platform, query, params=None):
    platform = (platform or 'all').lower()
    query = query or ''
    if platform == 'vinted' and search_vinted:
        try:
            return search_vinted(query)
        except Exception:
            return []
    if platform == 'all':
        items = []
        if search_vinted:
            try:
                items.extend(search_vinted(query))
            except Exception:
                pass
        return items
    return []
