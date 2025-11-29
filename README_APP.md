# ShareEye - Stock News Webapp

Eine moderne, verspielte Webapp zum Anzeigen von aktuellen Aktiennachrichten mit reaktiver Oberfläche.

## Features

✨ **Design:**
- Moderne, responsive UI mit dunklem Theme
- Verspielte Animationen und Hover-Effekte
- Glasmorphism-Effekte
- Vollständig mobil-freundlich

📊 **Funktionalität:**
- Echte Aktiennachrichten (via NewsAPI)
- Nachrichtenbilder und Vorschautext
- Kategorien-Filter (Trending, Tech, Markt, Krypto)
- Auto-Refresh alle 5 Minuten
- Responsive Grid-Layout

🚀 **Technologie:**
- Flask Backend
- Vanilla JavaScript Frontend
- Moderne CSS mit Animationen
- RESTful API

## Installation

```bash
# Requirements installieren
pip install -r requirements.txt

# App starten
python app.py
```

Die Webapp läuft dann auf: **http://localhost:5002**

## Konfiguration

Optional kannst du eine `.env` Datei erstellen für API-Keys:

```env
NEWSAPI_KEY=your_api_key_here
FINNHUB_KEY=your_api_key_here
```

Ohne API-Keys werden Mock-Daten angezeigt.

## API Endpoints

- `GET /` - Hauptseite
- `GET /api/news` - Aktuelle Nachrichten (JSON)
- `GET /api/status` - Server-Status

## Browser-Unterstützung

- Chrome/Edge (empfohlen)
- Firefox
- Safari
- Mobile Browser

---

Viel Spaß mit ShareEye! 📈✨
