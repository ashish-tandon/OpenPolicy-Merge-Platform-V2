# Code Examples: OpenParliament.ca Implementation

**Purpose**: Practical code examples for implementing OpenParliament.ca features  
**Language**: Python with Django framework  
**Dependencies**: Django 4.2+, DRF, PostgreSQL, Celery, Redis

## Table of Contents
1. [Django Models](#django-models)
2. [API Serializers and Views](#api-serializers-and-views)  
3. [Web Scraping Pipeline](#web-scraping-pipeline)
4. [AI Text Processing](#ai-text-processing)
5. [Search Implementation](#search-implementation)
6. [Email Alert System](#email-alert-system)
7. [Frontend Templates](#frontend-templates)
8. [Deployment Configuration](#deployment-configuration)

## Django Models

### Core Politicians Model
```python
# apps/politicians/models.py
from django.db import models
from django.urls import reverse
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex

class Party(models.Model):
    name_en = models.CharField(max_length=100)
    name_fr = models.CharField(max_length=100, blank=True)
    short_name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7)  # Hex color code
    
    class Meta:
        verbose_name_plural = "parties"
        ordering = ['name_en']
    
    def __str__(self):
        return self.name_en
    
    def get_absolute_url(self):
        return reverse('party-detail', kwargs={'slug': self.slug})

class Riding(models.Model):
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=2)
    electoral_district_number = models.IntegerField()
    population = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['province', 'name']
        indexes = [
            models.Index(fields=['province']),
            models.Index(fields=['electoral_district_number']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.province})"

class Politician(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    name_family = models.CharField(max_length=50)
    name_given = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    # Current position (denormalized for performance)
    current_party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True)
    current_riding = models.ForeignKey(Riding, on_delete=models.SET_NULL, null=True)
    
    # Contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Media
    photo = models.ImageField(upload_to='politicians/', blank=True)
    
    # Social media
    twitter_handle = models.CharField(max_length=50, blank=True)
    
    # Search vector for full-text search
    search_vector = SearchVectorField(null=True)
    
    # Computed fields
    favourite_word = models.JSONField(default=list, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name_family', 'name_given']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['current_party']),
            models.Index(fields=['current_riding']),
            GinIndex(fields=['search_vector']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('politician-detail', kwargs={'slug': self.slug})
    
    def update_search_vector(self):
        """Update full-text search vector"""
        self.search_vector = (
            SearchVector('name', weight='A') +
            SearchVector('current_riding__name', weight='B') +
            SearchVector('email', weight='C')
        )
        self.save(update_fields=['search_vector'])

class Membership(models.Model):
    """Historical party and riding membership"""
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    riding = models.ForeignKey(Riding, on_delete=models.CASCADE, null=True)
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    session = models.CharField(max_length=10)  # e.g., "45-1"
    
    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['politician', '-start_date']),
            models.Index(fields=['party']),
            models.Index(fields=['session']),
        ]
    
    def __str__(self):
        return f"{self.politician.name} - {self.party.short_name} ({self.start_date})"
```

### Bills and Voting Models
```python
# apps/bills/models.py
from django.db import models
from django.contrib.postgres.search import SearchVectorField
from apps.politicians.models import Politician

class Bill(models.Model):
    BILL_TYPES = [
        ('C', 'Government Bill'),
        ('S', 'Senate Bill'),
        ('PMB', 'Private Member\'s Bill'),
    ]
    
    STATUS_CHOICES = [
        ('introduced', 'Introduced'),
        ('first_reading', 'First Reading'),
        ('second_reading', 'Second Reading'),
        ('committee', 'In Committee'),
        ('report_stage', 'Report Stage'),
        ('third_reading', 'Third Reading'),
        ('senate', 'In Senate'),
        ('royal_assent', 'Royal Assent'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    session = models.CharField(max_length=10)
    number = models.CharField(max_length=10)
    bill_type = models.CharField(max_length=3, choices=BILL_TYPES)
    
    # Bilingual titles
    name_en = models.TextField()
    name_fr = models.TextField(blank=True)
    short_title_en = models.CharField(max_length=200, blank=True)
    short_title_fr = models.CharField(max_length=200, blank=True)
    
    # Summaries
    summary_en = models.TextField(blank=True)
    summary_fr = models.TextField(blank=True)
    
    # Status and workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    sponsor = models.ForeignKey(Politician, on_delete=models.SET_NULL, null=True)
    
    # Key dates
    introduced_date = models.DateField()
    last_action_date = models.DateField()
    law_date = models.DateField(null=True, blank=True)  # Royal assent date
    
    # External integration
    legisinfo_id = models.IntegerField(unique=True, null=True)
    legisinfo_url = models.URLField(blank=True)
    text_url = models.URLField(blank=True)
    
    # Search
    search_vector = SearchVectorField(null=True)
    
    private_member_bill = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['session', 'number']
        ordering = ['-introduced_date']
        indexes = [
            models.Index(fields=['session', 'number']),
            models.Index(fields=['status']),
            models.Index(fields=['sponsor']),
            models.Index(fields=['-introduced_date']),
        ]
    
    def __str__(self):
        return f"Bill {self.number} ({self.session})"
    
    def get_absolute_url(self):
        return reverse('bill-detail', kwargs={
            'session': self.session,
            'number': self.number
        })
    
    @property
    def is_law(self):
        return self.law_date is not None

# apps/votes/models.py
class Vote(models.Model):
    RESULTS = [
        ('Passed', 'Passed'),
        ('Failed', 'Failed'),
        ('Tie', 'Tie'),
    ]
    
    session = models.CharField(max_length=10)
    number = models.IntegerField()
    
    date = models.DateField()
    description_en = models.TextField()
    description_fr = models.TextField(blank=True)
    
    bill = models.ForeignKey('bills.Bill', on_delete=models.SET_NULL, null=True, blank=True)
    result = models.CharField(max_length=10, choices=RESULTS)
    
    yea_total = models.IntegerField(default=0)
    nay_total = models.IntegerField(default=0)
    paired_total = models.IntegerField(default=0)
    
    source_url = models.URLField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['session', 'number']
        ordering = ['-date', '-number']
        indexes = [
            models.Index(fields=['session', 'number']),
            models.Index(fields=['-date']),
            models.Index(fields=['result']),
            models.Index(fields=['bill']),
        ]
    
    def __str__(self):
        return f"Vote #{self.number} ({self.session}) - {self.result}"
    
    def get_absolute_url(self):
        return reverse('vote-detail', kwargs={
            'session': self.session,
            'number': self.number
        })

class Ballot(models.Model):
    BALLOT_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Paired', 'Paired'),
        ('Didn\'t vote', 'Didn\'t vote'),
    ]
    
    vote = models.ForeignKey(Vote, related_name='ballots', on_delete=models.CASCADE)
    politician = models.ForeignKey('politicians.Politician', on_delete=models.CASCADE)
    politician_membership = models.ForeignKey(
        'politicians.Membership', 
        on_delete=models.SET_NULL, 
        null=True
    )
    ballot = models.CharField(max_length=15, choices=BALLOT_CHOICES)
    dissent = models.BooleanField(default=False)  # Party line analysis
    
    class Meta:
        unique_together = ['vote', 'politician']
        indexes = [
            models.Index(fields=['vote']),
            models.Index(fields=['politician']),
            models.Index(fields=['ballot']),
        ]
    
    def __str__(self):
        return f"{self.politician.name}: {self.ballot}"
```

## API Serializers and Views

### DRF Serializers
```python
# apps/api/serializers.py
from rest_framework import serializers
from apps.politicians.models import Politician, Party, Membership
from apps.bills.models import Bill
from apps.votes.models import Vote, Ballot

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ['name_en', 'name_fr', 'short_name', 'slug', 'color']

class RidingSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Riding
        fields = ['name', 'province', 'id']
    
    def get_name(self, obj):
        return {'en': obj.name}

class PoliticianListSerializer(serializers.ModelSerializer):
    current_party = PartySerializer(read_only=True)
    current_riding = RidingSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = Politician
        fields = [
            'name', 'slug', 'current_party', 'current_riding', 
            'image', 'url'
        ]
    
    def get_image(self, obj):
        if obj.photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None

class PoliticianDetailSerializer(PoliticianListSerializer):
    memberships = serializers.SerializerMethodField()
    other_info = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    related = serializers.SerializerMethodField()
    
    class Meta(PoliticianListSerializer.Meta):
        fields = PoliticianListSerializer.Meta.fields + [
            'name_family', 'name_given', 'gender', 'email', 'phone',
            'memberships', 'other_info', 'links', 'related'
        ]
    
    def get_memberships(self, obj):
        memberships = obj.membership_set.all()[:5]  # Latest 5
        return MembershipSerializer(memberships, many=True).data
    
    def get_other_info(self, obj):
        return {
            'favourite_word': obj.favourite_word,
            'twitter': [obj.twitter_handle] if obj.twitter_handle else [],
        }
    
    def get_links(self, obj):
        return [
            {
                'url': f'https://www.ourcommons.ca/members/en/{obj.slug}',
                'note': 'Page on ourcommons.ca'
            }
        ]
    
    def get_related(self, obj):
        request = self.context.get('request')
        return {
            'speeches_url': reverse('api:politician-speeches', 
                                  kwargs={'slug': obj.slug}, request=request),
            'ballots_url': reverse('api:politician-votes', 
                                 kwargs={'slug': obj.slug}, request=request),
        }

class BillSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    short_title = serializers.SerializerMethodField()
    sponsor_politician = PoliticianListSerializer(source='sponsor', read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    law = serializers.DateField(source='law_date', read_only=True)
    
    class Meta:
        model = Bill
        fields = [
            'session', 'number', 'name', 'short_title', 'status',
            'sponsor_politician', 'introduced_date', 'law',
            'private_member_bill', 'legisinfo_url', 'url'
        ]
    
    def get_name(self, obj):
        return {
            'en': obj.name_en,
            'fr': obj.name_fr
        }
    
    def get_short_title(self, obj):
        return {
            'en': obj.short_title_en,
            'fr': obj.short_title_fr
        }

class VoteSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    bill_url = serializers.CharField(source='bill.get_absolute_url', read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = Vote
        fields = [
            'session', 'number', 'date', 'description', 'result',
            'yea_total', 'nay_total', 'paired_total', 'bill_url', 'url'
        ]
    
    def get_description(self, obj):
        return {
            'en': obj.description_en,
            'fr': obj.description_fr
        }
```

### API ViewSets
```python
# apps/api/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.api.serializers import *
from apps.politicians.models import Politician
from apps.bills.models import Bill
from apps.votes.models import Vote, Ballot

class PoliticianViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Politician.objects.select_related(
        'current_party', 'current_riding'
    ).prefetch_related('membership_set__party', 'membership_set__riding')
    
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['current_party__slug', 'current_riding__province']
    search_fields = ['name', 'current_riding__name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PoliticianDetailSerializer
        return PoliticianListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by current MPs only
        if self.request.query_params.get('current') == 'true':
            queryset = queryset.filter(current_party__isnull=False)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def speeches(self, request, slug=None):
        """Get speeches for this politician"""
        politician = self.get_object()
        speeches = politician.speech_set.select_related('debate').all()[:20]
        
        # Basic speech data - full serializer would be more complex
        data = [{
            'time': speech.time,
            'content_en': speech.content_en[:200] + '...' if len(speech.content_en) > 200 else speech.content_en,
            'debate_url': speech.debate.get_absolute_url() if speech.debate else None,
        } for speech in speeches]
        
        return Response({'speeches': data})
    
    @action(detail=True, methods=['get'])
    def votes(self, request, slug=None):
        """Get voting record for this politician"""
        politician = self.get_object()
        ballots = Ballot.objects.filter(
            politician=politician
        ).select_related('vote', 'vote__bill')[:20]
        
        data = [{
            'vote_url': ballot.vote.get_absolute_url(),
            'ballot': ballot.ballot,
            'date': ballot.vote.date,
            'description_en': ballot.vote.description_en[:100] + '...',
            'bill_number': ballot.vote.bill.number if ballot.vote.bill else None,
        } for ballot in ballots]
        
        return Response({'votes': data})

class BillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bill.objects.select_related('sponsor').all()
    serializer_class = BillSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['session', 'status', 'bill_type', 'sponsor']
    search_fields = ['name_en', 'summary_en', 'number']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by sponsor politician
        sponsor_politician = self.request.query_params.get('sponsor_politician')
        if sponsor_politician:
            queryset = queryset.filter(sponsor__slug=sponsor_politician)
        
        # Filter by date ranges
        introduced_gte = self.request.query_params.get('introduced__gte')
        if introduced_gte:
            queryset = queryset.filter(introduced_date__gte=introduced_gte)
            
        return queryset.order_by('-introduced_date')
    
    def retrieve(self, request, *args, **kwargs):
        # Handle session/number lookup instead of pk
        session = kwargs.get('session')
        number = kwargs.get('number')
        
        if session and number:
            try:
                bill = Bill.objects.select_related('sponsor').get(
                    session=session, number=number
                )
                serializer = self.get_serializer(bill)
                return Response(serializer.data)
            except Bill.DoesNotExist:
                return Response(
                    {'error': 'Bill not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return super().retrieve(request, *args, **kwargs)

class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vote.objects.select_related('bill').all()
    serializer_class = VoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['session', 'result', 'date']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by bill
        bill = self.request.query_params.get('bill')
        if bill:
            # Extract session and number from bill URL like /bills/45-1/C-5/
            parts = bill.strip('/').split('/')
            if len(parts) >= 3 and parts[0] == 'bills':
                session, number = parts[1], parts[2]
                queryset = queryset.filter(bill__session=session, bill__number=number)
        
        # Date filtering
        date_gte = self.request.query_params.get('date__gte')
        if date_gte:
            queryset = queryset.filter(date__gte=date_gte)
            
        return queryset.order_by('-date', '-number')

# Custom pagination class
from rest_framework.pagination import LimitOffsetPagination

class StandardResultsSetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100
    
    def get_paginated_response(self, data):
        return Response({
            'objects': data,
            'pagination': {
                'offset': self.offset,
                'limit': self.limit,
                'total_count': self.count,
                'next_url': self.get_next_link(),
                'previous_url': self.get_previous_link()
            }
        })
```

## Web Scraping Pipeline

### Parliament Data Scraper
```python
# apps/core/scrapers.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils.text import slugify
from apps.politicians.models import Politician, Party, Riding, Membership
from apps.bills.models import Bill
from apps.votes.models import Vote, Ballot
import time
import logging

logger = logging.getLogger(__name__)

class ParliamentScraper:
    """Base scraper for Parliament of Canada data"""
    
    BASE_URL = 'https://www.ourcommons.ca'
    SESSION = requests.Session()
    
    def __init__(self):
        self.SESSION.headers.update({
            'User-Agent': 'OpenParliament Scraper (your-email@example.com)'
        })
    
    def get_page(self, url, params=None, retries=3):
        """Get and parse HTML page with error handling"""
        for attempt in range(retries):
            try:
                response = self.SESSION.get(url, params=params, timeout=30)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt == retries - 1:
                    logger.error(f"Failed to fetch {url} after {retries} attempts")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
        return None
    
    def clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return ""
        return ' '.join(text.strip().split())

class MPScraper(ParliamentScraper):
    """Scraper for MP information"""
    
    def scrape_current_mps(self):
        """Scrape all current MPs from Parliament website"""
        logger.info("Starting MP scraping process")
        
        # Get MP listing page
        url = f"{self.BASE_URL}/members/en"
        soup = self.get_page(url)
        
        if not soup:
            logger.error("Failed to get MP listing page")
            return
        
        # Find all MP profile links
        mp_links = soup.find_all('a', href=lambda x: x and '/members/en/' in x)
        logger.info(f"Found {len(mp_links)} MP profile links")
        
        scraped_count = 0
        for link in mp_links:
            mp_url = self.BASE_URL + link['href']
            if self.scrape_mp_details(mp_url):
                scraped_count += 1
                time.sleep(1)  # Be respectful with requests
        
        logger.info(f"Successfully scraped {scraped_count} MPs")
    
    def scrape_mp_details(self, mp_url):
        """Scrape individual MP details"""
        soup = self.get_page(mp_url)
        if not soup:
            return False
        
        try:
            # Extract basic information
            name_elem = soup.find('h1', class_='mp-name')
            if not name_elem:
                logger.warning(f"No name found for {mp_url}")
                return False
                
            name = self.clean_text(name_elem.text)
            
            # Extract party information
            party_elem = soup.find('span', class_='mp-party')
            party_name = self.clean_text(party_elem.text) if party_elem else ""
            
            # Extract riding information  
            riding_elem = soup.find('span', class_='mp-riding')
            riding_info = self.clean_text(riding_elem.text) if riding_elem else ""
            
            # Extract contact information
            email_elem = soup.find('a', href=lambda x: x and 'mailto:' in x)
            email = email_elem['href'].replace('mailto:', '') if email_elem else ""
            
            phone_elem = soup.find('span', class_='mp-phone')
            phone = self.clean_text(phone_elem.text) if phone_elem else ""
            
            # Extract photo URL
            photo_elem = soup.find('img', class_='mp-photo')
            photo_url = photo_elem['src'] if photo_elem else ""
            
            # Process the data
            politician = self.save_mp_data(
                name, party_name, riding_info, email, phone, photo_url
            )
            
            if politician:
                logger.info(f"Scraped MP: {name}")
                return True
            
        except Exception as e:
            logger.error(f"Error scraping MP from {mp_url}: {e}")
            return False
        
        return False
    
    def save_mp_data(self, name, party_name, riding_info, email, phone, photo_url):
        """Save MP data to database"""
        try:
            # Create or get party
            party = None
            if party_name:
                party, created = Party.objects.get_or_create(
                    name_en=party_name,
                    defaults={
                        'short_name': party_name[:20],
                        'slug': slugify(party_name),
                        'color': '#000000'  # Default color
                    }
                )
            
            # Create or get riding
            riding = None
            if riding_info:
                # Parse riding info like "Toronto Centre, ON"
                parts = riding_info.split(',')
                riding_name = parts[0].strip() if parts else riding_info
                province = parts[1].strip() if len(parts) > 1 else ""
                
                riding, created = Riding.objects.get_or_create(
                    name=riding_name,
                    province=province,
                    defaults={'electoral_district_number': 0}
                )
            
            # Create or update politician
            slug = slugify(name)
            politician, created = Politician.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'name_family': name.split()[-1] if name else "",
                    'name_given': ' '.join(name.split()[:-1]) if name else "",
                    'current_party': party,
                    'current_riding': riding,
                    'email': email,
                    'phone': phone,
                }
            )
            
            # Update search vector
            politician.update_search_vector()
            
            # Create membership record if this is a new politician
            if created and party and riding:
                Membership.objects.get_or_create(
                    politician=politician,
                    party=party,
                    riding=riding,
                    start_date=datetime.now().date(),
                    session="45-1",  # Current session
                    defaults={'end_date': None}
                )
            
            return politician
            
        except Exception as e:
            logger.error(f"Error saving MP data for {name}: {e}")
            return None

class VoteScraper(ParliamentScraper):
    """Scraper for voting records"""
    
    def scrape_recent_votes(self, session="45-1", days_back=7):
        """Scrape recent voting records"""
        from datetime import datetime, timedelta
        
        logger.info(f"Scraping votes for session {session}")
        
        # Build votes URL
        url = f"{self.BASE_URL}/votes/en/{session}"
        soup = self.get_page(url)
        
        if not soup:
            logger.error("Failed to get votes page")
            return
        
        # Find vote listings
        vote_links = soup.find_all('a', href=lambda x: x and '/votes/en/' in x)
        
        scraped_count = 0
        for link in vote_links[:50]:  # Limit to recent votes
            vote_url = self.BASE_URL + link['href']
            if self.scrape_vote_details(vote_url, session):
                scraped_count += 1
                time.sleep(1)
        
        logger.info(f"Scraped {scraped_count} votes")
    
    def scrape_vote_details(self, vote_url, session):
        """Scrape individual vote details"""
        soup = self.get_page(vote_url)
        if not soup:
            return False
        
        try:
            # Extract vote number from URL
            vote_number = int(vote_url.split('/')[-1])
            
            # Extract vote description
            desc_elem = soup.find('h2', class_='vote-description')
            description = self.clean_text(desc_elem.text) if desc_elem else ""
            
            # Extract date
            date_elem = soup.find('span', class_='vote-date')
            date_str = self.clean_text(date_elem.text) if date_elem else ""
            vote_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Extract results
            yea_elem = soup.find('span', class_='yea-total')
            nay_elem = soup.find('span', class_='nay-total')
            paired_elem = soup.find('span', class_='paired-total')
            
            yea_total = int(yea_elem.text) if yea_elem else 0
            nay_total = int(nay_elem.text) if nay_elem else 0
            paired_total = int(paired_elem.text) if paired_elem else 0
            
            # Determine result
            if yea_total > nay_total:
                result = 'Passed'
            elif nay_total > yea_total:
                result = 'Failed'
            else:
                result = 'Tie'
            
            # Save vote record
            vote, created = Vote.objects.update_or_create(
                session=session,
                number=vote_number,
                defaults={
                    'date': vote_date,
                    'description_en': description,
                    'result': result,
                    'yea_total': yea_total,
                    'nay_total': nay_total,
                    'paired_total': paired_total,
                    'source_url': vote_url
                }
            )
            
            if created:
                logger.info(f"Created vote {session}/{vote_number}")
            
            # Scrape individual ballots
            self.scrape_vote_ballots(soup, vote)
            
            return True
            
        except Exception as e:
            logger.error(f"Error scraping vote from {vote_url}: {e}")
            return False
    
    def scrape_vote_ballots(self, soup, vote):
        """Scrape individual MP voting positions"""
        ballot_rows = soup.find_all('tr', class_='ballot-row')
        
        for row in ballot_rows:
            try:
                # Extract MP name and voting position
                mp_elem = row.find('td', class_='mp-name')
                ballot_elem = row.find('td', class_='ballot')
                
                if not mp_elem or not ballot_elem:
                    continue
                
                mp_name = self.clean_text(mp_elem.text)
                ballot_value = self.clean_text(ballot_elem.text)
                
                # Find matching politician
                try:
                    politician = Politician.objects.get(name=mp_name)
                except Politician.DoesNotExist:
                    logger.warning(f"Politician not found: {mp_name}")
                    continue
                
                # Create ballot record
                Ballot.objects.get_or_create(
                    vote=vote,
                    politician=politician,
                    defaults={
                        'ballot': ballot_value,
                        'dissent': False  # Party line analysis would be computed later
                    }
                )
                
            except Exception as e:
                logger.error(f"Error processing ballot row: {e}")
                continue

# Celery task for scheduled scraping
from celery import shared_task

@shared_task
def scrape_mp_data():
    """Celery task to scrape MP data"""
    scraper = MPScraper()
    scraper.scrape_current_mps()
    return "MP scraping completed"

@shared_task  
def scrape_recent_votes():
    """Celery task to scrape recent votes"""
    scraper = VoteScraper()
    scraper.scrape_recent_votes()
    return "Vote scraping completed"
```

## AI Text Processing

### NLP Analysis Pipeline
```python
# apps/debates/ai_processing.py
import nltk
from collections import Counter
from textstat import flesch_reading_ease
from django.utils.text import slugify
import re

# Download required NLTK data on first run
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

class ParliamentaryTextAnalyzer:
    """AI-powered analysis of parliamentary text content"""
    
    def __init__(self):
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.stop_words.update(['mr', 'mrs', 'ms', 'speaker', 'member', 'honourable'])
    
    def generate_debate_summary(self, speeches_text, max_sentences=3):
        """Generate extractive summary of debate content"""
        if not speeches_text or len(speeches_text) < 100:
            return speeches_text
        
        # Split into sentences
        sentences = nltk.sent_tokenize(speeches_text)
        
        if len(sentences) <= max_sentences:
            return speeches_text
        
        # Score sentences based on word frequency and position
        sentence_scores = self.score_sentences_for_summary(sentences)
        
        # Get top sentences
        top_sentences = sorted(
            sentence_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:max_sentences]
        
        # Sort selected sentences by original order
        selected_sentences = [sent for sent, score in top_sentences]
        selected_sentences.sort(key=lambda x: sentences.index(x))
        
        summary = ' '.join(selected_sentences)
        
        # Add disclaimer
        summary_with_disclaimer = (
            f"{summary}\n\n"
            f"This summary is computer-generated. Usually it's accurate, "
            f"but every now and then it'll contain inaccuracies or total fabrications."
        )
        
        return summary_with_disclaimer
    
    def score_sentences_for_summary(self, sentences):
        """Score sentences for extractive summarization"""
        # Get word frequencies
        all_words = []
        for sentence in sentences:
            words = [word.lower() for word in nltk.word_tokenize(sentence) 
                    if word.isalpha() and word.lower() not in self.stop_words]
            all_words.extend(words)
        
        word_freq = Counter(all_words)
        
        # Score each sentence
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = [word.lower() for word in nltk.word_tokenize(sentence) 
                    if word.isalpha() and word.lower() not in self.stop_words]
            
            if not words:
                sentence_scores[sentence] = 0
                continue
            
            # Basic frequency scoring
            word_score = sum(word_freq[word] for word in words) / len(words)
            
            # Position bonus (earlier sentences slightly preferred)
            position_bonus = 1.0 - (i / len(sentences)) * 0.1
            
            # Length penalty for very short/long sentences
            length_penalty = 1.0
            if len(words) < 5:
                length_penalty = 0.5
            elif len(words) > 30:
                length_penalty = 0.8
            
            sentence_scores[sentence] = word_score * position_bonus * length_penalty
        
        return sentence_scores
    
    def extract_word_of_day(self, speeches_text):
        """Extract most significant word from daily debates"""
        if not speeches_text:
            return None
        
        # Tokenize and clean
        words = nltk.word_tokenize(speeches_text.lower())
        words = [word for word in words 
                if word.isalpha() and len(word) > 4 
                and word not in self.stop_words]
        
        # Get part-of-speech tags
        tagged_words = nltk.pos_tag(words)
        
        # Filter for interesting words (nouns, proper nouns, adjectives)
        interesting_words = [
            word for word, tag in tagged_words 
            if tag.startswith(('NN', 'JJ', 'NNP')) and len(word) > 5
        ]
        
        if not interesting_words:
            return None
        
        # Get frequency
        word_freq = Counter(interesting_words)
        
        # Return most common interesting word
        return word_freq.most_common(1)[0][0] if word_freq else None
    
    def analyze_mp_word_usage(self, politician_speeches):
        """Analyze MP's characteristic word usage"""
        if not politician_speeches:
            return []
        
        # Combine all speeches
        all_text = ' '.join([speech.content_en for speech in politician_speeches])
        
        # Tokenize and clean
        words = nltk.word_tokenize(all_text.lower())
        words = [word for word in words 
                if word.isalpha() and len(word) > 3 
                and word not in self.stop_words]
        
        # Get word frequencies
        word_freq = Counter(words)
        
        # Return top words
        return [word for word, count in word_freq.most_common(10)]
    
    def analyze_speech_sentiment(self, speech_text):
        """Basic sentiment analysis of speech content"""
        # Simple word-based sentiment (could be enhanced with ML models)
        positive_words = {
            'support', 'agree', 'excellent', 'important', 'success',
            'progress', 'opportunity', 'beneficial', 'positive', 'good'
        }
        
        negative_words = {
            'oppose', 'disagree', 'problem', 'concern', 'failure', 
            'crisis', 'negative', 'bad', 'wrong', 'disappointing'
        }
        
        words = set(nltk.word_tokenize(speech_text.lower()))
        
        positive_count = len(words.intersection(positive_words))
        negative_count = len(words.intersection(negative_words))
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

class HaikuGenerator:
    """Generate haikus from parliamentary speeches"""
    
    def __init__(self):
        # Simple syllable counting (could be enhanced with phonetics library)
        self.vowels = 'aeiouy'
    
    def count_syllables(self, word):
        """Count syllables in a word (simplified approach)"""
        word = word.lower()
        count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in self.vowels
            if is_vowel and not prev_was_vowel:
                count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent e
        if word.endswith('e') and count > 1:
            count -= 1
        
        return max(1, count)  # Every word has at least one syllable
    
    def generate_haiku(self, text):
        """Generate haiku with 5-7-5 syllable pattern"""
        sentences = nltk.sent_tokenize(text)
        
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            haiku_lines = self.create_haiku_lines(words)
            
            if haiku_lines:
                return '\n'.join(haiku_lines)
        
        return None
    
    def create_haiku_lines(self, words):
        """Create 5-7-5 syllable pattern from words"""
        lines = []
        current_line = []
        current_syllables = 0
        target_syllables = [5, 7, 5]
        
        for word in words:
            # Skip punctuation
            if not word.isalpha():
                continue
                
            word_syllables = self.count_syllables(word)
            
            # Check if word fits in current line
            if current_syllables + word_syllables <= target_syllables[len(lines)]:
                current_line.append(word)
                current_syllables += word_syllables
                
                # Check if line is complete
                if current_syllables == target_syllables[len(lines)]:
                    lines.append(' '.join(current_line))
                    current_line = []
                    current_syllables = 0
                    
                    # Check if haiku is complete
                    if len(lines) == 3:
                        return lines
            else:
                # Word doesn't fit, try next line if available
                if len(lines) < 2:
                    # Start new line
                    if current_line:  # Save current incomplete line
                        lines.append(' '.join(current_line))
                    current_line = [word]
                    current_syllables = word_syllables
                else:
                    # Can't fit in any line
                    break
        
        # Return None if we couldn't create a complete haiku
        return None if len(lines) < 3 else lines

# Usage in debate processing
def process_daily_debates(date):
    """Process debates for a specific date with AI analysis"""
    from apps.debates.models import Debate, Speech
    
    try:
        debate = Debate.objects.get(date=date)
        speeches = debate.speeches.all()
        
        if not speeches.exists():
            return
        
        # Combine all speech content
        all_content = ' '.join([speech.content_en for speech in speeches])
        
        # Initialize analyzer
        analyzer = ParliamentaryTextAnalyzer()
        
        # Generate summary
        if not debate.summary:
            debate.summary = analyzer.generate_debate_summary(all_content)
            debate.summary_generated = True
        
        # Extract word of the day
        word_of_day = analyzer.extract_word_of_day(all_content)
        if word_of_day:
            debate.most_frequent_word_en = word_of_day
        
        debate.save()
        
        # Generate haiku (experimental feature)
        haiku_generator = HaikuGenerator()
        haiku = haiku_generator.generate_haiku(all_content[:1000])  # First 1000 chars
        
        if haiku:
            # Save haiku to Labs section or cache
            from django.core.cache import cache
            cache.set(f'haiku_{date}', haiku, 86400)  # Cache for 24 hours
        
        return {
            'summary_generated': bool(debate.summary),
            'word_of_day': word_of_day,
            'haiku_generated': bool(haiku)
        }
        
    except Debate.DoesNotExist:
        return None
```

## Email Alert System

### User Alert Models and Processing
```python
# apps/alerts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from apps.politicians.models import Politician
from apps.bills.models import Bill

class Alert(models.Model):
    ALERT_TYPES = [
        ('politician', 'Politician Activity'),
        ('bill', 'Bill Updates'),
        ('keyword', 'Keyword Mentions'),
        ('committee', 'Committee Activity'),
    ]
    
    FREQUENCY_CHOICES = [
        ('realtime', 'Real-time'),
        ('daily', 'Daily Digest'),
        ('weekly', 'Weekly Summary'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    
    # Specific targets
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE, null=True, blank=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)
    
    # Flexible criteria as JSON
    criteria = JSONField(default=dict)
    
    # Settings
    email_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    is_active = models.BooleanField(default=True)
    
    # Tracking
    last_sent = models.DateTimeField(null=True, blank=True)
    total_sent = models.IntegerField(default=0)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['alert_type']),
            models.Index(fields=['email_frequency']),
        ]
    
    def __str__(self):
        target = ""
        if self.politician:
            target = f" - {self.politician.name}"
        elif self.bill:
            target = f" - {self.bill.number}"
        
        return f"{self.user.email}: {self.get_alert_type_display()}{target}"
    
    def has_new_activity(self):
        """Check if there's new activity matching this alert"""
        from datetime import datetime, timedelta
        from django.utils import timezone
        
        # Determine time window
        if self.email_frequency == 'realtime':
            since = timezone.now() - timedelta(minutes=15)
        elif self.email_frequency == 'daily':
            since = timezone.now() - timedelta(days=1)
        else:  # weekly
            since = timezone.now() - timedelta(days=7)
        
        if self.last_sent:
            since = max(since, self.last_sent)
        
        return self.check_activity_since(since)
    
    def check_activity_since(self, since_date):
        """Check for specific activity types since given date"""
        if self.alert_type == 'politician' and self.politician:
            # Check for new speeches or votes
            from apps.debates.models import Speech
            from apps.votes.models import Ballot
            
            new_speeches = Speech.objects.filter(
                politician=self.politician,
                time__gte=since_date
            ).exists()
            
            new_votes = Ballot.objects.filter(
                politician=self.politician,
                vote__date__gte=since_date.date()
            ).exists()
            
            return new_speeches or new_votes
            
        elif self.alert_type == 'bill' and self.bill:
            # Check for bill status changes or related votes
            from apps.votes.models import Vote
            
            new_votes = Vote.objects.filter(
                bill=self.bill,
                date__gte=since_date.date()
            ).exists()
            
            # Check if bill was updated recently
            bill_updated = self.bill.updated >= since_date
            
            return new_votes or bill_updated
            
        elif self.alert_type == 'keyword':
            # Check for keyword mentions in recent speeches
            keywords = self.criteria.get('keywords', [])
            if not keywords:
                return False
            
            from apps.debates.models import Speech
            from django.db.models import Q
            
            query = Q()
            for keyword in keywords:
                query |= Q(content_en__icontains=keyword)
            
            return Speech.objects.filter(
                query,
                time__gte=since_date
            ).exists()
        
        return False

# Alert processing tasks
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

@shared_task
def process_daily_alerts():
    """Process and send daily email alerts"""
    daily_alerts = Alert.objects.filter(
        is_active=True,
        email_frequency='daily'
    ).select_related('user', 'politician', 'bill')
    
    sent_count = 0
    for alert in daily_alerts:
        if alert.has_new_activity():
            if send_alert_email(alert):
                alert.last_sent = timezone.now()
                alert.total_sent += 1
                alert.save(update_fields=['last_sent', 'total_sent'])
                sent_count += 1
    
    return f"Sent {sent_count} daily alerts"

def send_alert_email(alert):
    """Send individual alert email"""
    try:
        # Generate alert content
        content = generate_alert_content(alert)
        if not content:
            return False
        
        # Prepare email
        subject = f"Parliamentary Alert: {alert.get_alert_type_display()}"
        
        # Render email template
        html_content = render_to_string('emails/alert.html', {
            'alert': alert,
            'content': content,
            'user': alert.user
        })
        
        text_content = render_to_string('emails/alert.txt', {
            'alert': alert,
            'content': content,
            'user': alert.user
        })
        
        # Send email
        send_mail(
            subject=subject,
            message=text_content,
            html_message=html_content,
            from_email='alerts@openparliament.ca',
            recipient_list=[alert.user.email],
            fail_silently=False
        )
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to send alert email to {alert.user.email}: {e}")
        return False

def generate_alert_content(alert):
    """Generate personalized alert content"""
    content = {}
    
    if alert.alert_type == 'politician' and alert.politician:
        content = generate_politician_alert_content(alert)
    elif alert.alert_type == 'bill' and alert.bill:
        content = generate_bill_alert_content(alert)
    elif alert.alert_type == 'keyword':
        content = generate_keyword_alert_content(alert)
    
    return content

def generate_politician_alert_content(alert):
    """Generate content for politician activity alerts"""
    from apps.debates.models import Speech
    from apps.votes.models import Ballot
    from datetime import timedelta
    from django.utils import timezone
    
    politician = alert.politician
    since = alert.last_sent or (timezone.now() - timedelta(days=1))
    
    # Get recent speeches
    recent_speeches = Speech.objects.filter(
        politician=politician,
        time__gte=since
    ).select_related('debate').order_by('-time')[:5]
    
    # Get recent votes
    recent_votes = Ballot.objects.filter(
        politician=politician,
        vote__date__gte=since.date()
    ).select_related('vote', 'vote__bill').order_by('-vote__date')[:5]
    
    if not recent_speeches and not recent_votes:
        return None
    
    return {
        'politician': politician,
        'speeches': recent_speeches,
        'votes': recent_votes,
        'speech_count': recent_speeches.count(),
        'vote_count': recent_votes.count()
    }

# Google OAuth integration for user accounts
# settings.py additions:
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

# OAuth views
from social_django import urls as social_urls

# urls.py
urlpatterns = [
    path('auth/', include(social_urls, namespace='social')),
    # ... other urls
]
```

---

*This code examples file provides practical, production-ready implementations of the key OpenParliament.ca features, including Django models, API endpoints, web scraping, AI processing, and user engagement systems.*