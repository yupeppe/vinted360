from flask import Flask, render_template_string, request, jsonify
from routes.main import run_scraper

app = Flask(__name__)

HTML = """<!doctype html><html lang='it'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>Multi Scraper Hub</title></head><body><h1>Multi Scraper Hub</h1></body></html>"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.get_json(force=True, silent=True) or {}
    platform = data.get('platform', 'all')
    query = data.get('query', '')
    items = run_scraper(platform, query, data)
    return jsonify({'ok': True, 'platform': platform, 'query': query, 'items': items})
