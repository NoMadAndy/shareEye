from flask import Flask, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

SAMPLE_NEWS = [
    {
        "title": "Tech-Giganten glänzen nach Quartalszahlen",
        "summary": "Starke Cloud-Umsätze treiben die Kurse in die Höhe und sorgen für gute Stimmung an der Börse.",
        "image": "https://images.unsplash.com/photo-1444653614773-995cb1ef9efa?auto=format&fit=crop&w=900&q=80",
        "source": "FinTimes",
        "url": "https://example.com/bericht-tech",
        "published_at": "2024-05-04T08:15:00Z",
    },
    {
        "title": "Grüne Energie bleibt Liebling der Anleger",
        "summary": "Aktien aus dem Bereich Solar und Windkraft erreichen neue Jahreshochs nach positiven Fördermeldungen.",
        "image": "https://images.unsplash.com/photo-1509395062183-67c5ad6faff9?auto=format&fit=crop&w=900&q=80",
        "source": "MarketDaily",
        "url": "https://example.com/energie-report",
        "published_at": "2024-05-04T07:10:00Z",
    },
    {
        "title": "Banken überraschen mit soliden Margen",
        "summary": "Trotz Zinsdruck zeigen sich die Gewinne stabil, was die Aktienkurse stützt.",
        "image": "https://images.unsplash.com/photo-1454165205744-3b78555e5572?auto=format&fit=crop&w=900&q=80",
        "source": "BörsenWoche",
        "url": "https://example.com/banken-update",
        "published_at": "2024-05-04T06:30:00Z",
    },
    {
        "title": "E-Mobility startet mit Rallye ins Wochenende",
        "summary": "Neue Batteriedurchbrüche sorgen für Fantasie und lassen die Kurse von Autobauern springen.",
        "image": "https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=900&q=80",
        "source": "Pulse",
        "url": "https://example.com/emobility-news",
        "published_at": "2024-05-04T05:45:00Z",
    },
]


@app.route("/")
def index():
    template = """
    <!doctype html>
    <html lang="de">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Aktuelle Börsenstories</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
        <style>
            :root {
                color-scheme: light dark;
                --bg: radial-gradient(circle at 10% 20%, #ffe0f0 0, #ffe0f0 20%, #f0f4ff 50%, #f8f9fb 100%);
                --text: #0f172a;
                --muted: #475569;
                --accent: #7c3aed;
                --accent-2: #f97316;
                --card: rgba(255, 255, 255, 0.75);
                --shadow: 0 20px 60px rgba(124, 58, 237, 0.15);
            }

            * { box-sizing: border-box; }

            body {
                margin: 0;
                font-family: 'Poppins', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: var(--bg);
                color: var(--text);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }

            header {
                padding: 32px 24px 16px;
                display: flex;
                flex-direction: column;
                gap: 10px;
                text-align: center;
            }

            .badge {
                display: inline-flex;
                align-self: center;
                align-items: center;
                gap: 8px;
                padding: 8px 14px;
                background: linear-gradient(120deg, var(--accent), var(--accent-2));
                color: white;
                border-radius: 999px;
                font-weight: 600;
                letter-spacing: 0.2px;
                box-shadow: var(--shadow);
            }

            h1 {
                margin: 0;
                font-size: clamp(1.8rem, 4vw, 2.5rem);
                letter-spacing: -0.02em;
            }

            p.lead {
                margin: 0 auto;
                max-width: 720px;
                color: var(--muted);
                font-size: 1rem;
            }

            main {
                padding: 0 24px 32px;
            }

            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 18px;
                width: 100%;
            }

            .card {
                background: var(--card);
                border-radius: 18px;
                overflow: hidden;
                border: 1px solid rgba(255,255,255,0.6);
                box-shadow: var(--shadow);
                display: flex;
                flex-direction: column;
                transition: transform 0.25s ease, box-shadow 0.25s ease;
            }

            .card:hover {
                transform: translateY(-6px) scale(1.01);
                box-shadow: 0 24px 64px rgba(124, 58, 237, 0.25);
            }

            .card img {
                width: 100%;
                height: 160px;
                object-fit: cover;
            }

            .content {
                padding: 16px 16px 18px;
                display: flex;
                flex-direction: column;
                gap: 10px;
                flex: 1;
            }

            .meta {
                display: flex;
                justify-content: space-between;
                align-items: center;
                color: var(--muted);
                font-size: 0.85rem;
            }

            a.link {
                color: var(--accent);
                font-weight: 600;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }

            a.link:hover { color: var(--accent-2); }

            .pulse {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #22c55e;
                position: relative;
            }

            .pulse::after {
                content: '';
                position: absolute;
                inset: -6px;
                border-radius: inherit;
                border: 2px solid rgba(34, 197, 94, 0.4);
                animation: pulse 1.6s infinite;
            }

            @keyframes pulse {
                0% { transform: scale(0.9); opacity: 1; }
                100% { transform: scale(1.5); opacity: 0; }
            }

            .pill {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 6px 10px;
                background: rgba(124,58,237,0.12);
                border-radius: 999px;
                color: var(--accent);
                font-weight: 600;
            }

            footer {
                text-align: center;
                padding: 10px 20px 24px;
                color: var(--muted);
                font-size: 0.9rem;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="badge">
                <span class="pulse"></span>
                Live Börsenstories
            </div>
            <h1>Frische Aktiennews, verspieltes Design</h1>
            <p class="lead">Entdecke die neuesten Schlagzeilen aus dem Markt in einem modernen, schnellen Interface – optimiert für Desktop und Mobile.</p>
        </header>

        <main>
            <div class="meta" style="margin-bottom: 14px; max-width: 1100px; margin-inline: auto;">
                <span class="pill" id="last-update">Aktualisiert: jetzt</span>
                <a class="link" href="#" id="refresh">Neu laden ↻</a>
            </div>
            <section class="grid" id="news-grid"></section>
        </main>

        <footer>
            Gebaut mit Liebe zu Daten, Design und Börse.
        </footer>

        <script>
            async function loadNews() {
                const grid = document.getElementById('news-grid');
                grid.innerHTML = '<p style="color:#475569;">Lade Schlagzeilen...</p>';
                const res = await fetch('/api/news');
                const data = await res.json();
                grid.innerHTML = '';
                const formatter = new Intl.DateTimeFormat('de-DE', { dateStyle: 'short', timeStyle: 'short' });

                data.items.forEach(item => {
                    const card = document.createElement('article');
                    card.className = 'card';
                    card.innerHTML = `
                        <img src="${item.image}" alt="${item.title}" loading="lazy">
                        <div class="content">
                            <div class="meta">
                                <span class="pill">${item.source}</span>
                                <span>${formatter.format(new Date(item.published_at))}</span>
                            </div>
                            <h3 style="margin:0;font-size:1.1rem;">${item.title}</h3>
                            <p style="margin:0;color:#475569;line-height:1.5;">${item.summary}</p>
                            <a class="link" href="${item.url}" target="_blank" rel="noreferrer">Zur Story →</a>
                        </div>
                    `;
                    grid.appendChild(card);
                });

                const lastUpdate = document.getElementById('last-update');
                lastUpdate.textContent = 'Aktualisiert: ' + formatter.format(new Date());
            }

            document.getElementById('refresh').addEventListener('click', (e) => {
                e.preventDefault();
                loadNews();
            });

            loadNews();
        </script>
    </body>
    </html>
    """
    return render_template_string(template)


@app.route("/api/news")
def api_news():
    items = []
    for entry in SAMPLE_NEWS:
        published = entry.get("published_at")
        parsed_time = datetime.fromisoformat(published.replace("Z", "+00:00")) if published else datetime.utcnow()
        items.append({**entry, "published_at": parsed_time.isoformat()})
    return jsonify({"items": items})


def main():
    app.run(host="0.0.0.0", port=5002)


if __name__ == "__main__":
    main()
