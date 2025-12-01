# ShareEye - AI Coding Agent Guidelines

## Project Overview
**ShareEye** is a modern, responsive web application for displaying current stock market news with images. It's built with Flask (backend) and vanilla JavaScript (frontend), runs on port 5002, and fetches data from NewsAPI.

## Architecture & Key Components

### Backend Stack (Flask)
- **File**: `app.py` - Single monolithic Flask application
- **Key Pattern**: In-memory caching with 5-minute TTL for NewsAPI responses
- **Main Routes**:
  - `GET /` - Serves `index.html`
  - `GET /api/news?query=QUERY&limit=LIMIT` - Returns JSON with articles (default: "stock market")
  - `POST /api/refresh` - Force clears cache and fetches fresh data
  - `GET /health` - Health check endpoint

### Data Flow
1. Frontend calls `/api/news?query=STOCK+MARKET` or `/api/refresh` (POST)
2. Backend checks in-memory cache; if valid (< 5 min old), returns cached data
3. If cache expired, calls NewsAPI with 7-day date range filter
4. Filters articles to only include those with `urlToImage`
5. Returns structured JSON with: title, description, image, url, source, published, author

### Frontend Architecture
- **HTML**: `templates/index.html` - Template with semantic structure (header, stats-bar, news-grid)
- **CSS**: `static/css/style.css` - 700+ lines with CSS variables for theming
  - Design System: Glasmorphism effects, Inter/Poppins fonts
  - Dark/Light mode toggle via CSS variables root
  - Responsive grid layout for articles
- **JavaScript**: `static/js/app.js` - Class-based `ShareEyeApp` with lifecycle methods
  - Event listeners for search, refresh, theme toggle
  - Renders news as cards with lazy-loaded images
  - Updates stats bar with article count and timestamp

## Critical Developer Workflows

### Running the Application
```bash
pip install -r requirements.txt
python app.py
```
App runs on `http://localhost:5002` (all interfaces `0.0.0.0:5002`)

### Environment Setup
- NewsAPI key stored in `.env` file: `NEWS_API_KEY=fd66b8e5b8af43a18f257705baa68249`
- Python 3.8+, Flask 2.3.3, requests library required

### Testing Endpoints
```bash
# Fetch stock market news
curl "http://localhost:5002/api/news?query=stock%20market&limit=10"

# Force cache refresh
curl -X POST http://localhost:5002/api/refresh -H "Content-Type: application/json" -d '{"query":"apple"}'

# Health check
curl http://localhost:5002/health
```

## Project-Specific Conventions

### Naming Conventions
- Python functions: `snake_case` (e.g., `get_stock_news`, `format_date`)
- JavaScript class: `ShareEyeApp` - instantiated on page load
- CSS variables: kebab-case with semantic prefixes (e.g., `--color-*`, `--shadow-*`, `--space-*`)
- HTML IDs: camelCase for element identifiers (e.g., `searchInput`, `newsGrid`, `themeToggle`)

### Caching Strategy
- **Type**: In-memory dictionary `news_cache` with `data` and `timestamp` keys
- **TTL**: 300 seconds (5 minutes)
- **Validation**: Only articles with images (`urlToImage` field) are included
- **Refresh**: POST `/api/refresh` explicitly clears cache and refetches

### Error Handling
- Frontend: Try-catch around fetch calls; shows `.error-message` div with custom text
- Backend: Catches `RequestException` from NewsAPI, prints to console, returns empty array
- State indicators: Loading spinner, empty state, error state - all managed by showing/hiding divs

### Theming System
- **Dark Mode Toggle**: Button #themeToggle in header
- **Implementation**: CSS variables in `:root` switch between light and dark values
- **Persistence**: Theme preference saved to localStorage (checked in `getInitialDarkMode()`)
- **Design Patterns**: Glasmorphism effects maintained in both themes

## Integration Points & Dependencies

### External APIs
- **NewsAPI** (newsapi.org/v2/everything): Requires valid API key
  - Query Parameters: `q`, `sortBy`, `language`, `pageSize`, `apiKey`, `from`, `to`
  - Response structure: `{ articles: [...], totalResults, status }`
  - 7-day window filtering in backend (`from_date`, `to_date`)

### Python Dependencies (requirements.txt)
- Flask 2.3.3, Werkzeug 2.3.7, Jinja2 3.1.2 - Web framework
- requests 2.31.0 - HTTP client for NewsAPI
- python-dotenv 1.0.0 - Environment variable management

### Frontend Dependencies
- Google Fonts (Inter, Poppins) - Typography
- No build tools or bundlers; vanilla JavaScript and CSS

## Code Patterns to Follow

### Adding New Routes
Follow the existing pattern in `app.py`:
```python
@app.route('/api/endpoint', methods=['GET', 'POST'])
def endpoint_handler():
    # Validate input from request.args or request.json
    # Perform logic
    return jsonify({'success': True, 'data': result, 'timestamp': datetime.now().isoformat()})
```

### Frontend API Calls
Use async/await pattern with proper error handling:
```javascript
try {
    const response = await fetch(`/api/news?query=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    // Process data
} catch (error) {
    this.showError('User-friendly message');
}
```

### Styling New Components
- Use CSS variables from `:root` for colors, spacing, shadows
- Include dark mode variants for all new colors
- Maintain responsive design with grid/flexbox
- Add smooth transitions using `--transition-*` variables

## File Organization
```
shareEye/
├── app.py              # Flask backend (all routes & logic)
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (NEWS_API_KEY)
├── templates/
│   └── index.html     # Main HTML template
├── static/
│   ├── js/app.js      # Main JS app class
│   └── css/style.css  # Theming & layout
└── .github/
    └── copilot-instructions.md  # This file
```

## Performance Considerations
- **Caching**: 5-minute cache prevents excessive API calls and rate limiting
- **Lazy Loading**: Images load on-demand to reduce initial page load
- **API Filtering**: Backend filters by date range (7 days) and image presence
- **No Build Step**: Direct serving of JS/CSS minimizes deployment complexity

## Common Tasks

| Task | Command/Location |
|------|------------------|
| Add new API endpoint | Edit `app.py`, follow route decorator pattern |
| Modify styling | Edit `static/css/style.css`, use CSS variables |
| Update frontend logic | Edit `static/js/app.js`, add methods to `ShareEyeApp` class |
| Change API parameters | Modify `params` dict in `get_stock_news()` function |
| Add environment variable | Add to `.env` file, access with `os.getenv()` in `app.py` |
