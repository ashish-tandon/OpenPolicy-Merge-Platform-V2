# Unified Feature Mapping

## Master Inventory
- Based on 84/120+ features implemented (70% complete)

## Feature: Global Search
- ID: F001
- Name: Global Search with Postal Code MP Lookup  
- Priority (P0–P4): P0
- Data Entities (tables/indices): members, bills, debates, votes, jurisdictions
- API Endpoints (with methods): GET /api/v1/search, GET /api/v1/search/postcode/{postcode}
- UI Views/Components: GlobalSearch, SearchAutocomplete
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: Elasticsearch for full-text search
- Execution Checklist IDs: 3.6, 5.1

## Feature: MP Profile System
- ID: F002
- Name: Complete MP Database with Individual Profiles
- Priority (P0–P4): P0
- Data Entities (tables/indices): elected_members, representatives, offices, contact_details
- API Endpoints (with methods): GET /api/v1/members, GET /api/v1/members/{member_id}
- UI Views/Components: MPListView, MPDetailView, MPProfileCard
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: Photo storage, social media APIs
- Execution Checklist IDs: 3.2, 5.2

## Feature: Bills Tracking
- ID: F003
- Name: Complete Bills Database with Status Tracking
- Priority (P0–P4): P0
- Data Entities (tables/indices): bills, votes, bill_history
- API Endpoints (with methods): GET /api/v1/bills, GET /api/v1/bills/{bill_id}
- UI Views/Components: BillListView, BillDetailView, BillStatusTracker
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: LEGISinfo integration
- Execution Checklist IDs: 3.1, 5.3

## Feature: Voting Records
- ID: F004
- Name: Complete Voting Records with MP Positions
- Priority (P0–P4): P0
- Data Entities (tables/indices): votes, ballots, user_votes
- API Endpoints (with methods): GET /api/v1/votes, POST /api/v1/bills/{bill_id}/cast-vote
- UI Views/Components: VoteListView, VoteDetailView, VotingPositions
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: Real-time vote updates
- Execution Checklist IDs: 3.3, 5.4

## Feature: Debates Archive
- ID: F005
- Name: Complete Hansard Archive with AI Summaries
- Priority (P0–P4): P1
- Data Entities (tables/indices): debates, speeches, debate_summaries
- API Endpoints (with methods): GET /api/v1/debates, GET /api/v1/debates/{year}/{month}/{day}
- UI Views/Components: DebateListView, DebateDetailView, AISummaryDisplay
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: AI summarization service
- Execution Checklist IDs: 3.4, 5.5

## Feature: Committee Tracking
- ID: F006
- Name: Complete Committee Database with Meetings
- Priority (P0–P4): P1
- Data Entities (tables/indices): committees, committee_members, meetings
- API Endpoints (with methods): GET /api/v1/committees, GET /api/v1/committees/{committee_slug}
- UI Views/Components: CommitteeListView, CommitteeDetailView, MeetingSchedule
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Meeting calendar integration
- Execution Checklist IDs: 3.5, 5.6

## Feature: Multi-Level Government
- ID: F007
- Name: Federal/Provincial/Municipal Representative Database
- Priority (P0–P4): P0
- Data Entities (tables/indices): jurisdictions, representatives, offices, government_levels
- API Endpoints (with methods): GET /api/v1/jurisdictions, GET /api/v1/representatives
- UI Views/Components: JurisdictionSelector, RepresentativeList, GovernmentLevelFilter
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: Scraper scheduling system
- Execution Checklist IDs: 3.7, 4.1, 4.2, 4.3

## Feature: User Management
- ID: F008
- Name: User Authentication and Profile Management
- Priority (P0–P4): P0
- Data Entities (tables/indices): users, user_profiles, user_preferences
- API Endpoints (with methods): POST /api/v1/users, GET /api/v1/users/{user_id}
- UI Views/Components: LoginForm, UserProfile, PreferencesPanel
- Tests Required (unit/int/e2e/contract): unit, integration, e2e, security
- Dependencies & Flags: OAuth integration, JWT tokens
- Execution Checklist IDs: 3.8, 5.7, 10.1

## Feature: Mobile API Support
- ID: F009
- Name: Mobile-Optimized API Endpoints
- Priority (P0–P4): P1
- Data Entities (tables/indices): All core entities with mobile optimization
- API Endpoints (with methods): GET /api/v1/app/*, POST /api/v1/app-auth/*
- UI Views/Components: Mobile-specific components
- Tests Required (unit/int/e2e/contract): unit, integration, contract
- Dependencies & Flags: Push notification service
- Execution Checklist IDs: 6.1, 6.2

## Feature: Data Export
- ID: F010
- Name: Bulk Data Export Functionality
- Priority (P0–P4): P2
- Data Entities (tables/indices): All public entities
- API Endpoints (with methods): GET /api/v1/export/*, GET /api/v1/bulk/{dataset}
- UI Views/Components: ExportPanel, DatasetSelector
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Background job processing
- Execution Checklist IDs: 3.6

## Feature: Real-time House Status
- ID: F011
- Name: Dynamic House of Commons Status Banner
- Priority (P0–P4): P1
- Data Entities (tables/indices): house_status, session_calendar
- API Endpoints (with methods): GET /api/v1/house/status
- UI Views/Components: HouseStatusBanner, SessionIndicator
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: WebSocket for real-time updates
- Execution Checklist IDs: 5.1

## Feature: Scraper Monitoring
- ID: F012
- Name: ETL Pipeline Health Dashboard
- Priority (P0–P4): P2
- Data Entities (tables/indices): data_sources, ingestion_logs
- API Endpoints (with methods): GET /api/v1/data-sources, GET /api/v1/stats/system
- UI Views/Components: ScraperDashboard, IngestionStatus
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Monitoring alerts
- Execution Checklist IDs: 4.4, 4.5

## Feature: Historical Party Affiliation
- ID: F013
- Name: Track MP Party Membership Changes Over Time
- Priority (P0–P4): P2
- Data Entities (tables/indices): party_history, member_affiliations
- API Endpoints (with methods): GET /api/v1/members/{member_id}/party-history
- UI Views/Components: PartyAffiliationHistory, PartyTimeline
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Historical data import
- Execution Checklist IDs: 3.2, 5.2

## Feature: Electoral History
- ID: F014
- Name: Complete Electoral Results Archive
- Priority (P0–P4): P2
- Data Entities (tables/indices): elections, electoral_results, candidates
- API Endpoints (with methods): GET /api/v1/elections, GET /api/v1/elections/{year}
- UI Views/Components: ElectoralHistory, ElectionResults
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Elections Canada API
- Execution Checklist IDs: 3.2, 5.2

## Feature: Email Alerts
- ID: F015
- Name: Customizable Email Notification System
- Priority (P0–P4): P1
- Data Entities (tables/indices): email_subscriptions, notification_queue
- API Endpoints (with methods): POST /api/v1/alerts/subscribe, DELETE /api/v1/alerts/unsubscribe
- UI Views/Components: EmailAlertSignup, NotificationPreferences
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: Email service provider (SendGrid/SES)
- Execution Checklist IDs: 5.2, 10.1

## Feature: RSS Feeds
- ID: F016
- Name: RSS Feed Generation for All Content Types
- Priority (P0–P4): P3
- Data Entities (tables/indices): All content tables
- API Endpoints (with methods): GET /api/v1/feeds/*, GET /api/v1/members/{id}/rss
- UI Views/Components: RSSFeedLink, FeedManager
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: RSS library, caching
- Execution Checklist IDs: 3.2, 5.2

## Feature: Word Frequency Analysis
- ID: F017
- Name: "Favourite Word" Analysis for MPs
- Priority (P0–P4): P3
- Data Entities (tables/indices): word_frequencies, speech_analytics
- API Endpoints (with methods): GET /api/v1/members/{id}/word-analysis
- UI Views/Components: WordFrequencyAnalysis, WordCloud
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: NLP processing pipeline
- Execution Checklist IDs: 3.2, 5.2

## Feature: Social Media Integration
- ID: F018
- Name: Twitter/Social Media Profile Links
- Priority (P0–P4): P2
- Data Entities (tables/indices): social_media_accounts
- API Endpoints (with methods): GET /api/v1/members/{id}/social-media
- UI Views/Components: SocialMediaLinks, TwitterFeed
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: Twitter API v2
- Execution Checklist IDs: 3.2, 5.2

## Feature: Riding Geographic Data
- ID: F019
- Name: Electoral Boundary Mapping System
- Priority (P0–P4): P2
- Data Entities (tables/indices): electoral_boundaries, geographic_data
- API Endpoints (with methods): GET /api/v1/ridings, GET /api/v1/ridings/{id}/boundaries
- UI Views/Components: RidingMap, BoundaryViewer
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: GeoJSON data, mapping library
- Execution Checklist IDs: 3.2, 5.2

## Feature: Bill Status Visualization
- ID: F020
- Name: Legislative Process Status Tracker
- Priority (P0–P4): P1
- Data Entities (tables/indices): bill_status, legislative_stages
- API Endpoints (with methods): GET /api/v1/bills/{id}/status
- UI Views/Components: BillStatusTracker, LegislativeTimeline
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Status update webhooks
- Execution Checklist IDs: 3.1, 5.3

## Feature: Vote Pass/Fail Indicators
- ID: F021
- Name: Visual Vote Outcome Display System
- Priority (P0–P4): P1
- Data Entities (tables/indices): vote_outcomes
- API Endpoints (with methods): GET /api/v1/votes/{id}/outcome
- UI Views/Components: PassFailIndicators, VoteOutcomeChart
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: Real-time updates
- Execution Checklist IDs: 3.3, 5.4

## Feature: Committee Review Tracking
- ID: F022
- Name: Bill Committee Progress Monitor
- Priority (P0–P4): P2
- Data Entities (tables/indices): committee_reviews, review_stages
- API Endpoints (with methods): GET /api/v1/bills/{id}/committee-review
- UI Views/Components: CommitteeReviewTracker, ReviewTimeline
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Committee API integration
- Execution Checklist IDs: 3.5, 5.3

## Feature: Royal Assent Tracking
- ID: F023
- Name: Law Status and Royal Assent Monitor
- Priority (P0–P4): P2
- Data Entities (tables/indices): royal_assent, law_status
- API Endpoints (with methods): GET /api/v1/bills/{id}/royal-assent
- UI Views/Components: RoyalAssentIndicator, LawStatusBadge
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: Governor General's office feed
- Execution Checklist IDs: 3.1, 5.3

## Feature: Bill Amendment Tracking
- ID: F024
- Name: Legislative Amendment Management System
- Priority (P0–P4): P2
- Data Entities (tables/indices): amendments, amendment_votes
- API Endpoints (with methods): GET /api/v1/bills/{id}/amendments
- UI Views/Components: AmendmentTracker, AmendmentComparison
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Text diff engine
- Execution Checklist IDs: 3.1, 5.3

## Feature: Private Member Bill Analytics
- ID: F025
- Name: Private Bill Success Analysis System
- Priority (P0–P4): P3
- Data Entities (tables/indices): private_bills, success_metrics
- API Endpoints (with methods): GET /api/v1/analytics/private-bills
- UI Views/Components: PrivateBillAnalytics, SuccessPredictor
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: ML prediction model
- Execution Checklist IDs: 3.1, 5.3

## Feature: Party Line Voting Analysis
- ID: F026
- Name: Party Dissent Detection System
- Priority (P0–P4): P2
- Data Entities (tables/indices): party_votes, dissent_records
- API Endpoints (with methods): GET /api/v1/votes/{id}/party-analysis
- UI Views/Components: PartyLineAnalysis, DissentHighlighter
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Vote aggregation pipeline
- Execution Checklist IDs: 3.3, 5.4

## Feature: AI-Generated Summaries
- ID: F027
- Name: Automated Debate Summary Generation
- Priority (P0–P4): P1
- Data Entities (tables/indices): ai_summaries, summary_metadata
- API Endpoints (with methods): GET /api/v1/debates/{id}/summary
- UI Views/Components: AISummaryDisplay, SummaryGenerator
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: AI/ML service (GPT/Claude)
- Execution Checklist IDs: 3.4, 5.5

## Feature: Topic Extraction
- ID: F028
- Name: Automated Debate Topic Identification
- Priority (P0–P4): P2
- Data Entities (tables/indices): debate_topics, topic_taxonomy
- API Endpoints (with methods): GET /api/v1/debates/{id}/topics
- UI Views/Components: TopicExtractor, TopicCloud
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: NLP topic modeling
- Execution Checklist IDs: 3.4, 5.5

## Feature: Speech Attribution
- ID: F029
- Name: Speaker Identification and Attribution System
- Priority (P0–P4): P1
- Data Entities (tables/indices): speech_attributions, speaker_registry
- API Endpoints (with methods): GET /api/v1/speeches/{id}/attribution
- UI Views/Components: SpeakerAttribution, SpeechCard
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Speaker recognition algorithm
- Execution Checklist IDs: 3.4, 5.5

## Feature: Debate Analytics
- ID: F030
- Name: Parliamentary Debate Metrics Dashboard
- Priority (P0–P4): P2
- Data Entities (tables/indices): debate_metrics, participation_stats
- API Endpoints (with methods): GET /api/v1/debates/analytics
- UI Views/Components: DebateAnalytics, ParticipationChart
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: Analytics engine
- Execution Checklist IDs: 3.4, 5.5

## Feature: Word of the Day
- ID: F031
- Name: Daily Parliamentary Vocabulary Feature
- Priority (P0–P4): P3
- Data Entities (tables/indices): daily_words, word_usage_stats
- API Endpoints (with methods): GET /api/v1/words/daily
- UI Views/Components: WordOfTheDay, VocabularyHighlight
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: Scheduled job runner
- Execution Checklist IDs: 3.4, 5.5

## Feature: Cross-Parliament Search
- ID: F032
- Name: Multi-Session Debate Search Engine
- Priority (P0–P4): P1
- Data Entities (tables/indices): All debate/speech tables with FTS
- API Endpoints (with methods): GET /api/v1/search/debates
- UI Views/Components: CrossParliamentSearch, SearchFilters
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: Elasticsearch cluster
- Execution Checklist IDs: 3.6, 5.5

## Feature: Committee Membership
- ID: F033
- Name: Committee Member Tracking System
- Priority (P0–P4): P2
- Data Entities (tables/indices): committee_memberships, member_roles
- API Endpoints (with methods): GET /api/v1/committees/{id}/members
- UI Views/Components: MembershipTracker, MemberList
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: Historical membership data
- Execution Checklist IDs: 3.5, 5.6

## Feature: Active Studies Monitor
- ID: F034
- Name: Committee Investigation Tracker
- Priority (P0–P4): P2
- Data Entities (tables/indices): committee_studies, study_progress
- API Endpoints (with methods): GET /api/v1/committees/{id}/studies
- UI Views/Components: StudiesMonitor, InvestigationCard
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: Committee report feeds
- Execution Checklist IDs: 3.5, 5.6

## Feature: Meeting Schedule System
- ID: F035
- Name: Parliamentary Meeting Calendar
- Priority (P0–P4): P2
- Data Entities (tables/indices): meeting_schedule, calendar_events
- API Endpoints (with methods): GET /api/v1/committees/meetings
- UI Views/Components: MeetingSchedule, CalendarView
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: iCal export support
- Execution Checklist IDs: 3.5, 5.6

## Feature: Report Publication
- ID: F036
- Name: Committee Report Management System
- Priority (P0–P4): P2
- Data Entities (tables/indices): committee_reports, report_documents
- API Endpoints (with methods): GET /api/v1/committees/{id}/reports
- UI Views/Components: ReportPublisher, DocumentViewer
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: PDF generation service
- Execution Checklist IDs: 3.5, 5.6

## Feature: Haiku Generator
- ID: F037
- Name: Parliamentary Poetry Generation (5-7-5)
- Priority (P0–P4): P4
- Data Entities (tables/indices): generated_haikus, source_speeches
- API Endpoints (with methods): GET /api/v1/labs/haiku
- UI Views/Components: HaikuGenerator, PoetryDisplay
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: NLP syllable counter
- Execution Checklist IDs: 5.1

## Feature: Google OAuth
- ID: F038
- Name: Google Authentication Integration
- Priority (P0–P4): P1
- Data Entities (tables/indices): oauth_tokens, user_auth_providers
- API Endpoints (with methods): POST /api/v1/auth/google
- UI Views/Components: GoogleOAuthUI, LoginButton
- Tests Required (unit/int/e2e/contract): unit, integration, security
- Dependencies & Flags: Google OAuth2 credentials
- Execution Checklist IDs: 10.1, 5.7

## Feature: Custom Search Criteria
- ID: F039
- Name: Advanced Search Filter Builder
- Priority (P0–P4): P2
- Data Entities (tables/indices): saved_searches, search_criteria
- API Endpoints (with methods): POST /api/v1/search/custom
- UI Views/Components: CustomSearchUI, FilterBuilder
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Query builder library
- Execution Checklist IDs: 3.6, 5.1

## Feature: Bilingual Support
- ID: F040
- Name: French/English Language Toggle System
- Priority (P0–P4): P0
- Data Entities (tables/indices): translations, language_preferences
- API Endpoints (with methods): GET /api/v1/content/{lang}
- UI Views/Components: LanguageToggle, TranslatedContent
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: i18n framework, translation memory
- Execution Checklist IDs: 5.1

## Feature: Responsive Mobile Design
- ID: F041
- Name: Touch-Optimized Mobile Interface
- Priority (P0–P4): P0
- Data Entities (tables/indices): mobile_sessions, device_preferences
- API Endpoints (with methods): All endpoints with mobile optimization
- UI Views/Components: ResponsiveMobileLayout, TouchControls
- Tests Required (unit/int/e2e/contract): unit, e2e, device testing
- Dependencies & Flags: Viewport detection, PWA support
- Execution Checklist IDs: 5.1, 6.1

## Feature: Parliamentary Schedule
- ID: F042
- Name: Session Calendar Integration
- Priority (P0–P4): P1
- Data Entities (tables/indices): session_calendar, sitting_days
- API Endpoints (with methods): GET /api/v1/schedule
- UI Views/Components: ParliamentarySchedule, CalendarWidget
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Parliament calendar API
- Execution Checklist IDs: 5.1

## Feature: Daily Transcript Feature
- ID: F043
- Name: Latest Hansard Highlights Display
- Priority (P0–P4): P2
- Data Entities (tables/indices): daily_highlights, featured_speeches
- API Endpoints (with methods): GET /api/v1/hansard/daily
- UI Views/Components: DailyTranscriptFeature, HighlightCard
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: Content curation algorithm
- Execution Checklist IDs: 5.1

## Feature: Provincial MP Organization
- ID: F044
- Name: MPs Grouped by Province/Territory
- Priority (P0–P4): P2
- Data Entities (tables/indices): provincial_groupings
- API Endpoints (with methods): GET /api/v1/members/by-province
- UI Views/Components: ProvinceFilter, ProvincialGrouping
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: Geographic hierarchy
- Execution Checklist IDs: 3.2, 5.2

## Feature: Party-Based Filtering
- ID: F045
- Name: Political Party Filter System
- Priority (P0–P4): P2
- Data Entities (tables/indices): political_parties, party_members
- API Endpoints (with methods): GET /api/v1/members/by-party
- UI Views/Components: PartyFilter, PartySelector
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: Party registry updates
- Execution Checklist IDs: 3.2, 5.2

## Feature: Official Photo Management
- ID: F046
- Name: MP Portrait Display System
- Priority (P0–P4): P2
- Data Entities (tables/indices): member_photos, photo_metadata
- API Endpoints (with methods): GET /api/v1/members/{id}/photo
- UI Views/Components: MPPhotoGallery, PortraitDisplay
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: CDN for image delivery
- Execution Checklist IDs: 3.2, 5.2

## Feature: MP Contact Form
- ID: F047
- Name: Direct MP Communication System
- Priority (P0–P4): P2
- Data Entities (tables/indices): contact_messages, message_queue
- API Endpoints (with methods): POST /api/v1/members/{id}/contact
- UI Views/Components: MPContactForm, MessageComposer
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: CAPTCHA, email delivery
- Execution Checklist IDs: 3.2, 5.2

## Feature: LEGISinfo Integration
- ID: F048
- Name: Parliamentary Library Data Integration
- Priority (P0–P4): P1
- Data Entities (tables/indices): legisinfo_sync, external_refs
- API Endpoints (with methods): GET /api/v1/bills/{id}/legisinfo
- UI Views/Components: LEGISinfoLink, ExternalDataBadge
- Tests Required (unit/int/e2e/contract): integration
- Dependencies & Flags: LEGISinfo API access
- Execution Checklist IDs: 3.1, 5.3

## Feature: Session-Based Filtering
- ID: F049
- Name: Parliamentary Session Filter System
- Priority (P0–P4): P2
- Data Entities (tables/indices): parliamentary_sessions
- API Endpoints (with methods): GET /api/v1/bills/by-session
- UI Views/Components: SessionFilter, SessionSelector
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: Session metadata
- Execution Checklist IDs: 3.1, 5.3

## Feature: Bill Outcome Predictions
- ID: F050
- Name: Legislative Success Likelihood Analysis
- Priority (P0–P4): P3
- Data Entities (tables/indices): prediction_models, outcome_history
- API Endpoints (with methods): GET /api/v1/bills/{id}/prediction
- UI Views/Components: OutcomePrediction, PredictionChart
- Tests Required (unit/int/e2e/contract): unit
- Dependencies & Flags: ML prediction service
- Execution Checklist IDs: 3.1, 5.3