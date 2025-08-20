# Technical Architecture: OpenParliament.ca

## System Overview

OpenParliament.ca implements a sophisticated **dual-architecture** system:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   Database      │
│                 │    │                  │    │                 │
│ Django Templates│◄───┤ Django Views     │◄───┤ PostgreSQL      │
│ JavaScript      │    │ DRF API          │    │ Full-text Search│
│ CSS/HTML        │    │ Celery Tasks     │    │ Indexes         │
│ D3.js Charts    │    │ Email System     │    │ Relationships   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Static Assets   │    │ External APIs    │    │   Data Sources  │
│                 │    │                  │    │                 │
│ CSS Files       │    │ ourcommons.ca    │    │ Web Scrapers    │
│ JavaScript      │    │ LEGISinfo        │    │ Parliament APIs │
│ Images          │    │ Google OAuth     │    │ RSS Feeds       │
│ Fonts           │    │ Email Services   │    │ Official Data   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Technology Stack

### Backend Framework
```
Primary Language: Python 3.12
Web Framework: Django 4.2+
API Framework: Django REST Framework (DRF)
Database: PostgreSQL 13+ with full-text search
Task Queue: Celery with Redis broker
Caching: Redis for session and query caching
```

### Frontend Technology
```
Templates: Django template system with inheritance
CSS Framework: Custom responsive grid system
JavaScript: Vanilla JS with selective jQuery
Visualization: D3.js for word clouds and charts
Icons: Font Awesome or similar icon system
```

### Data Processing
```
Web Scraping: Python requests + BeautifulSoup
Text Analysis: NLTK/spaCy for NLP processing
Search: PostgreSQL full-text search with ranking
File Processing: Python file handling for exports
```

### Infrastructure
```
Web Server: Nginx with uWSGI/Gunicorn
Database: PostgreSQL with read replicas
CDN: Static asset delivery system
Monitoring: Application performance monitoring
Backup: Automated database and file backups
```

## Core Architecture Components

### 1. Django Application Structure
```
openparliament/
├── manage.py
├── openparliament/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── politicians/      # MP management
│   ├── bills/             # Bill tracking
│   ├── votes/             # Voting records
│   ├── debates/           # Hansard system
│   ├── committees/        # Committee tracking
│   ├── core/              # Shared functionality
│   └── api/               # REST API endpoints
├── static/                # CSS, JS, images
├── media/                 # User uploads (MP photos)
└── templates/             # HTML templates
```

### 2. Database Architecture

#### Core Models Relationships
```
Politicians ←→ Memberships ←→ Parties
Politicians ←→ Ballots ←→ Votes ←→ Bills  
Debates ←→ Speeches ←→ Politicians
Committees ←→ Meetings ←→ Politicians
Bills ←→ Committee_Reviews ←→ Committees
```

#### Key Tables Structure
```sql
-- Politicians with current position
politicians_politician (
  id, name, slug, current_party_id, current_riding_id,
  email, phone, photo, search_vector
)

-- Bills with status tracking  
bills_bill (
  id, session, number, title_en, title_fr, 
  status, sponsor_id, introduced_date, law_date
)

-- Voting records
votes_vote (
  id, session, number, date, description_en, description_fr,
  bill_id, result, yea_total, nay_total, paired_total
)

-- Individual MP votes
votes_ballot (
  id, vote_id, politician_id, ballot
)

-- Parliamentary speeches
speeches_speech (
  id, debate_id, politician_id, time, content_en,
  content_fr, search_vector
)
```

### 3. API Architecture

#### REST API Design Principles
- **RESTful Resources**: Standard HTTP methods (GET, POST, PUT, DELETE)
- **Hyperlinked Relations**: URLs as resource identifiers
- **Comprehensive Filtering**: Multi-field query capabilities
- **Pagination**: Offset/limit with navigation URLs
- **Versioning**: API-Version header support (v1)
- **Rate Limiting**: Throttling with HTTP 429 responses

#### Key API Endpoints
```
/politicians/                    # MP listings
/politicians/{slug}/             # Individual MP details
/politicians/{slug}/speeches/    # MP speech history
/politicians/{slug}/votes/       # MP voting record

/bills/                          # Bill listings
/bills/{session}/{number}/       # Individual bill details
/bills/{session}/{number}/votes/ # Bill voting history

/votes/                          # Vote listings
/votes/{session}/{number}/       # Individual vote details
/votes/ballots/                  # Individual MP ballots

/debates/                        # Debate listings
/debates/{date}/                 # Daily Hansard
/speeches/                       # Speech search

/committees/                     # Committee listings
/committees/{slug}/              # Committee details
/committees/{slug}/meetings/     # Committee meetings
```

### 4. Data Processing Pipeline

#### Real-time Data Ingestion
```python
# Celery-based task scheduling
@periodic_task(run_every=crontab(hour=2, minute=0))  # Daily at 2 AM
def update_mp_data():
    """Scrape current MP information"""
    
@periodic_task(run_every=crontab(minute=0))  # Hourly
def update_votes():
    """Check for new voting records"""
    
@periodic_task(run_every=crontab(hour=3, minute=0))  # Daily at 3 AM  
def process_hansard():
    """Process new Hansard transcripts"""
```

#### Web Scraping Architecture
```python
class ParliamentScraper:
    """Base scraper for Parliament of Canada data"""
    BASE_URL = 'https://www.ourcommons.ca'
    
    def get_page(self, url):
        """Fetch and parse HTML with error handling"""
        
    def extract_mp_data(self, mp_page):
        """Extract structured MP information"""
        
    def save_to_database(self, data):
        """Store data with conflict resolution"""
```

#### AI Text Processing
```python
class DebateAnalyzer:
    """AI-powered parliamentary text analysis"""
    
    def generate_summary(self, speeches_text):
        """Create computer-generated debate summaries"""
        
    def extract_keywords(self, text):
        """Identify important terms and topics"""
        
    def analyze_sentiment(self, speech):
        """Determine speech sentiment and tone"""
```

### 5. Search Architecture

#### Full-Text Search Implementation
```sql
-- PostgreSQL full-text search setup
CREATE INDEX speech_search_idx ON speeches_speech 
USING gin(to_tsvector('english', content_en));

-- Search ranking with multiple fields
SELECT *, ts_rank(search_vector, query) as rank
FROM politicians_politician, 
     to_tsquery('english', 'search_term') query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

#### Search Features
- **Cross-model Search**: Politicians, bills, speeches, committees
- **Autocomplete**: Real-time search suggestions
- **Faceted Search**: Filter by party, province, date ranges
- **Postal Code Lookup**: Geographic MP identification

### 6. User Authentication & Alerts

#### Email Alert System
```python
class Alert(models.Model):
    """User-configured parliamentary monitoring"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert_type = models.CharField(choices=ALERT_TYPES)
    politician = models.ForeignKey(Politician, null=True)
    keywords = models.TextField()  # JSON search criteria
    email_frequency = models.CharField(default='daily')

@shared_task
def process_alerts():
    """Check for new activity matching user alerts"""
    for alert in Alert.objects.filter(is_active=True):
        if alert.has_new_activity():
            send_alert_email(alert)
```

#### Google OAuth Integration
```python
# OAuth authentication for user accounts
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('GOOGLE_CLIENT_SECRET')
```

### 7. Performance Optimization

#### Database Optimization
```sql
-- Strategic indexes for common queries
CREATE INDEX idx_votes_session_date ON votes_vote(session, date DESC);
CREATE INDEX idx_ballots_politician_vote ON ballots_ballot(politician_id, vote_id);
CREATE INDEX idx_speeches_politician_time ON speeches_speech(politician_id, time DESC);

-- Partial indexes for active data
CREATE INDEX idx_current_politicians ON politicians_politician(id) 
WHERE current_party_id IS NOT NULL;
```

#### Caching Strategy
```python
# Redis caching configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# View-level caching
@cache_page(60 * 15)  # 15 minutes
def politician_list(request):
    """Cached MP listing"""
    
# Template fragment caching
{% load cache %}
{% cache 500 recent_votes %}
    <!-- Recent voting results -->
{% endcache %}
```

#### CDN Integration
```python
# Static files optimization
STATIC_URL = 'https://cdn.openparliament.ca/static/'
MEDIA_URL = 'https://cdn.openparliament.ca/media/'

# Compression and minification
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 8. Security Implementation

#### Django Security Settings
```python
# Production security configuration
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

#### API Security
```python
# DRF throttling configuration
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

### 9. Monitoring & Logging

#### Application Monitoring
```python
# Logging configuration
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/openparliament/django.log',
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
        },
        'openparliament': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}
```

#### Health Check System
```python
# System health monitoring
class HealthCheckView(APIView):
    """System status endpoint"""
    
    def get(self, request):
        return Response({
            'database': self.check_database(),
            'redis': self.check_redis(),
            'scraper': self.check_scraper_status(),
            'last_update': self.get_last_update_time()
        })
```

## Deployment Architecture

### Production Environment
```
Load Balancer (Nginx)
├── Web Servers (Multiple Gunicorn instances)
├── Static Files (CDN/Nginx)
├── Database (PostgreSQL Primary + Read Replicas)
├── Cache (Redis Cluster)
├── Task Queue (Celery Workers)
└── Monitoring (Prometheus + Grafana)
```

### Scaling Considerations
- **Horizontal Scaling**: Multiple web server instances
- **Database Scaling**: Read replicas for query performance
- **Cache Distribution**: Redis cluster for high availability
- **Task Distribution**: Multiple Celery worker nodes
- **Static Assets**: CDN for global content delivery

---

*This technical architecture represents the sophisticated system implemented at openparliament.ca, providing a complete blueprint for similar parliamentary monitoring platforms.*