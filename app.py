from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# API-Keys und Endpunkte
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', 'demo_key')
FINNHUB_KEY = os.getenv('FINNHUB_KEY', 'demo_key')

# Stockfotos für Aktiennachrichten (als Fallback)
STOCK_IMAGES = [
    'https://images.unsplash.com/photo-1611974789855-9c2dc5810803?w=400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1552821206-6c00d52e9f30?w=400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1460925895917-adf4e565016f?w=400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1537903904737-13fc522b5c8a?w=400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1551431009-381d36ac3a14?w=400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1516321318423-f06f70d504d0?w=400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400&h=300&fit=crop',
]

def get_stock_news():
    """Fetch stock news von NewsAPI"""
    try:
        # Versuche mit NewsAPI zu arbeiten (funktioniert auch mit Demo-Key)
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': 'stock OR stocks OR market OR trading',
            'language': 'de',
            'sortBy': 'publishedAt',
            'pageSize': 12,
            'apiKey': NEWSAPI_KEY
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            # Format articles
            formatted_articles = []
            for idx, article in enumerate(articles):
                formatted_articles.append({
                    'title': article.get('title', 'Keine Überschrift'),
                    'description': article.get('description', article.get('content', 'Keine Beschreibung'))[:150] + '...',
                    'image': article.get('urlToImage') or STOCK_IMAGES[idx % len(STOCK_IMAGES)],
                    'url': article.get('url', '#'),
                    'source': article.get('source', {}).get('name', 'Unbekannte Quelle'),
                    'publishedAt': article.get('publishedAt', ''),
                    'date': format_date(article.get('publishedAt', '')),
                })
            
            return formatted_articles
        else:
            return get_mock_news()
            
    except Exception as e:
        print(f"Fehler beim Abrufen von News: {e}")
        return get_mock_news()

def get_mock_news():
    """Mock-Daten für Demo"""
    mock_data = [
        {
            'title': 'DAX erreicht neues Rekordhoch',
            'description': 'Der Deutsche Aktienindex durchbricht die 20.000er Marke zum ersten Mal in der Geschichte.',
            'image': STOCK_IMAGES[0],
            'url': '#',
            'source': 'ShareEye News',
            'publishedAt': datetime.now().isoformat(),
            'date': 'Heute'
        },
        {
            'title': 'Tech-Aktien im Aufschwung',
            'description': 'FAANG-Aktien zeigen stärkste Performance seit Jahresanfang mit zweistelligen Zuwächsen.',
            'image': STOCK_IMAGES[1],
            'url': '#',
            'source': 'ShareEye News',
            'publishedAt': datetime.now().isoformat(),
            'date': 'Heute'
        },
        {
            'title': 'Kryptomärkte stabilisieren sich',
            'description': 'Bitcoin und Ethereum zeigen nach volatiler Phase erste Stabilisierungszeichen.',
            'image': STOCK_IMAGES[2],
            'url': '#',
            'source': 'ShareEye News',
            'publishedAt': (datetime.now() - timedelta(hours=1)).isoformat(),
            'date': 'vor 1 Stunde'
        },
        {
            'title': 'Energiesektor überrascht mit Gewinnen',
            'description': 'Öl und Gasaktien zeigen unerwartete Stärke bei globaler Energiediskussion.',
            'image': STOCK_IMAGES[3],
            'url': '#',
            'source': 'ShareEye News',
            'publishedAt': (datetime.now() - timedelta(hours=2)).isoformat(),
            'date': 'vor 2 Stunden'
        },
        {
            'title': 'Pharma-Branche im Fokus',
            'description': 'Neue Medikamentenzulassungen treiben Kurse mehrerer Pharmaunternehmen an.',
            'image': STOCK_IMAGES[4],
            'url': '#',
            'source': 'ShareEye News',
            'publishedAt': (datetime.now() - timedelta(hours=3)).isoformat(),
            'date': 'vor 3 Stunden'
        },
        {
            'title': 'Einzelhandel meldet Rekordumsätze',
            'description': 'Weihnachtssaison bringt zweistellige Wachstumsraten für Einzelhandelsketten.',
            'image': STOCK_IMAGES[5],
            'url': '#',
            'source': 'ShareEye News',
            'publishedAt': (datetime.now() - timedelta(hours=4)).isoformat(),
            'date': 'vor 4 Stunden'
        }
    ]
    return mock_data

def format_date(date_string):
    """Konvertiere ISO-Datum zu lesbarem Format"""
    if not date_string:
        return 'Unbekannt'
    
    try:
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        now = datetime.now(date_obj.tzinfo) if date_obj.tzinfo else datetime.now()
        diff = now - date_obj
        
        if diff.days == 0:
            if diff.seconds < 60:
                return 'gerade eben'
            elif diff.seconds < 3600:
                mins = diff.seconds // 60
                return f'vor {mins} Minute{"n" if mins > 1 else ""}'
            else:
                hours = diff.seconds // 3600
                return f'vor {hours} Stunde{"n" if hours > 1 else ""}'
        elif diff.days == 1:
            return 'gestern'
        else:
            return f'vor {diff.days} Tagen'
    except:
        return 'Unbekannt'

@app.route('/')
def index():
    """Hauptseite"""
    return render_template('index.html')

@app.route('/api/news')
def api_news():
    """API für News-Daten"""
    news = get_stock_news()
    return jsonify(news)

@app.route('/api/status')
def api_status():
    """Status-Endpoint"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Auf allen Interfaces auf Port 5002 hören
    app.run(host='0.0.0.0', port=5002, debug=True)
