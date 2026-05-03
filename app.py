from flask import Flask, render_template_string, request, jsonify
from scrapers.registry import run_scraper

app = Flask(__name__)

HTML = """<!doctype html>
<html lang='it'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>Multi Scraper Hub</title><style>body{margin:0;font-family:Arial,sans-serif;background:#111;color:#eee;padding:24px}.card{background:#1b1b1b;border:1px solid #2a2a2a;border-radius:16px;padding:18px;margin-bottom:14px}input,select,button{width:100%;box-sizing:border-box;padding:12px;border-radius:12px;border:1px solid #333;background:#222;color:#eee;margin-top:8px}button{cursor:pointer;font-weight:700}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.item{background:#202020;border:1px solid #303030;border-radius:16px;overflow:hidden}.item img{width:100%;height:200px;object-fit:cover;background:#111}.body{padding:12px}.muted{color:#aaa;font-size:13px}.price{font-size:18px;font-weight:700;margin:8px 0}a{color:#9ad1ff;text-decoration:none}</style></head><body><div class='card'><h1>Multi Scraper Hub</h1><p class='muted'>Accesso da browser, anche da iPhone.</p></div><div class='card'><label>Piattaforma</label><select id='platform'><option value='all'>Tutte</option><option value='vinted'>Vinted</option></select><label>Ricerca</label><input id='query' placeholder='es. usb'><button onclick='run()'>Avvia</button><div id='status' class='muted' style='margin-top:10px'>Pronto.</div></div><div class='card'><div id='results' class='grid'></div></div><script>async function run(){const s=document.getElementById('status');const r=document.getElementById('results');const platform=document.getElementById('platform').value;const query=document.getElementById('query').value.trim();r.innerHTML='';s.textContent='Ricerca in corso...';try{const res=await fetch('/api/search',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({platform,query})});const j=await res.json();const items=j.items||[];if(!items.length){s.textContent='Nessun risultato.';r.innerHTML='<div class="muted">Nessun risultato.</div>';return;}s.textContent='Risultati trovati: '+items.length;r.innerHTML=items.map(i=>`<div class='item'><img src='${i.image||""}' alt='${i.title||""}'><div class='body'><div class='muted'>${i.platform||''}</div><div><b>${i.title||''}</b></div><div class='price'>${i.price||''}</div><div class='muted'>${i.meta||''}</div><a href='${i.url||'#'}' target='_blank' rel='noopener'>Apri scheda</a></div></div>`).join('');}catch(e){s.textContent='Errore.';r.innerHTML='<div class="muted">Errore backend.</div>';}}</script></body></html>"""

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
