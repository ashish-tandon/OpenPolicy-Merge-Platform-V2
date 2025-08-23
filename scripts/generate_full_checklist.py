#!/usr/bin/env python3
"""
Generate the complete 325-item Implementation Checklist
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any

class ChecklistGenerator:
    def __init__(self):
        self.items = []
        self.chk_counter = 1
        self.due_date = datetime.now() + timedelta(days=30)
        
    def add_item(self, title: str, gate: str, features: List[str], activities: List[str], 
                 data: List[str], routes: List[str], code: str, owner: str, 
                 dependencies: List[str], criteria: List[str], links: List[str],
                 decimal_order: str):
        """Add a checklist item"""
        item = {
            'id': f"CHK-{self.chk_counter:04d}",
            'decimal_order': decimal_order,
            'title': title,
            'gate': gate,
            'features': features,
            'activities': activities,
            'data': data,
            'routes': routes,
            'code': code,
            'owner': owner,
            'due': (self.due_date + timedelta(days=(self.chk_counter // 10) * 7)).strftime("%Y-%m-%d"),
            'dependencies': dependencies,
            'criteria': criteria,
            'links': links
        }
        self.items.append(item)
        self.chk_counter += 1
        return item['id']
        
    def generate_g1_items(self):
        """Generate G1: Structure/Index items (55 total)"""
        # Refactoring tasks (1-15)
        for i in range(1, 16):
            self.add_item(
                title=f"Refactor high-usage {'functions' if i <= 5 else 'variables' if i <= 10 else 'modules'}: Item {i}",
                gate="G1",
                features=["FEAT-001", "FEAT-002", "FEAT-003"],
                activities=["ACT-001"],
                data=["DATA-001", "DATA-002"],
                routes=["RT-001"],
                code="services/api-gateway/app/models/*.py",
                owner="@backend-team",
                dependencies=[] if i == 1 else [f"CHK-{i-1:04d}"],
                criteria=["Functions consolidated", "Performance improved", "Tests pass"],
                links=["[VAR_FUNC_MAP hotspots]", "[ADR-20250823-01]"],
                decimal_order=f"1.{i}"
            )
            
        # Orphan routes (16-25)
        orphan_routes = [
            ("/", "RT-036", "Root documentation or redirect"),
            ("/healthz", "RT-037", "Health check endpoint"),
            ("/version", "RT-038", "Version information"),
            ("/metrics", "RT-039", "Prometheus metrics"),
            ("/suggestions", "RT-040", "Search suggestions"),
            ("/summary/stats", "RT-041", "Summary statistics"),
            ("/{bill_id}", "RT-042", "Bill detail shortcut"),
            ("/{bill_id}/votes", "RT-043", "Bill votes"),
            ("/{bill_id}/history", "RT-044", "Bill history"),
            ("/{bill_id}/amendments", "RT-045", "Bill amendments")
        ]
        
        for i, (path, route, desc) in enumerate(orphan_routes, 16):
            self.add_item(
                title=f"Document or remove orphan route: {path}",
                gate="G1",
                features=[],
                activities=[],
                data=[],
                routes=[route],
                code="services/api-gateway/app/main.py",
                owner="@api-team",
                dependencies=[],
                criteria=[desc, "OpenAPI spec updated"],
                links=["[ROUTING_REALIGNMENT]"],
                decimal_order=f"1.{i}"
            )
            
        # Directory structure and standards (26-55)
        structure_tasks = [
            "Audit and standardize directory structure across all services",
            "Create consistent naming conventions for files and directories",
            "Implement monorepo structure with clear boundaries",
            "Establish shared libraries location and structure",
            "Define service boundary rules and dependencies",
            "Create service-specific README files with consistent format",
            "Implement code organization standards",
            "Set up linting and formatting rules",
            "Create development environment setup guide",
            "Document deployment structure",
            "Establish Git workflow and branching strategy",
            "Define code review process and standards",
            "Create architecture decision record template",
            "Set up documentation structure and standards",
            "Implement logging standards across services",
            "Create error handling patterns",
            "Define API versioning strategy",
            "Establish database migration patterns",
            "Create configuration management standards",
            "Define secret management approach",
            "Implement dependency management strategy",
            "Create build and packaging standards",
            "Define testing directory structure",
            "Establish CI/CD pipeline structure",
            "Create monitoring and alerting standards",
            "Define data retention policies",
            "Implement backup and recovery procedures",
            "Create incident response templates",
            "Define SLA and SLO standards",
            "Establish security scanning procedures"
        ]
        
        for i, task in enumerate(structure_tasks, 26):
            self.add_item(
                title=task,
                gate="G1",
                features=["ALL"],
                activities=[],
                data=[],
                routes=[],
                code="services/*" if "services" in task else "docs/*" if "doc" in task else "*",
                owner="@architecture-team",
                dependencies=[],
                criteria=["Standards documented", "All services compliant", "Team trained"],
                links=["[ADR-20250823-01]"],
                decimal_order=f"1.{i}"
            )
            
    def generate_g2_items(self):
        """Generate G2: Parity items (80 total)"""
        # Search implementation (56-65)
        search_tasks = [
            "Complete search index implementation for all entities",
            "Implement faceted search for bills",
            "Add search suggestions and autocomplete",
            "Create search relevance tuning",
            "Implement search analytics",
            "Add search result highlighting",
            "Create saved searches feature",
            "Implement search export functionality",
            "Add advanced search operators",
            "Create search API rate limiting"
        ]
        
        for i, task in enumerate(search_tasks, 56):
            self.add_item(
                title=task,
                gate="G2",
                features=["FEAT-001"],
                activities=["ACT-001"],
                data=["DATA-001", "DATA-002", "DATA-003", "DATA-004", "DATA-005"],
                routes=["RT-001", "RT-002"],
                code="services/etl/app/tasks/search_indexer.py",
                owner="@search-team",
                dependencies=["CHK-0026"],
                criteria=["Feature works", "Performance targets met", "Tests pass"],
                links=["[DATA_CYCLE_MAP search]", "[ADR-20250823-05]"],
                decimal_order=f"2.{i-55}"
            )
            
        # MP Profile features (66-80)
        mp_tasks = [
            "Implement MP photo upload and storage",
            "Create MP social media integration",
            "Add MP voting history visualization",
            "Implement MP committee membership tracking",
            "Create MP speech analysis",
            "Add MP attendance tracking",
            "Implement MP comparison feature",
            "Create MP contact form",
            "Add MP news aggregation",
            "Implement MP constituency mapping",
            "Create MP performance metrics",
            "Add MP bill sponsorship tracking",
            "Implement MP expense reporting",
            "Create MP timeline view",
            "Add MP endorsement tracking"
        ]
        
        for i, task in enumerate(mp_tasks, 66):
            self.add_item(
                title=task,
                gate="G2",
                features=["FEAT-002"],
                activities=["ACT-003", "ACT-004"],
                data=["DATA-007", "DATA-008", "DATA-009", "DATA-010"],
                routes=["RT-003", "RT-004", "RT-005", "RT-006"],
                code="services/api-gateway/app/api/v1/members.py",
                owner="@mp-team",
                dependencies=["CHK-0056"],
                criteria=["Feature complete", "UI responsive", "Data accurate"],
                links=["[FEATURE_ACTIVITY_MAP FEAT-002]"],
                decimal_order=f"2.{i-55}"
            )
            
        # Bill tracking features (81-95)
        bill_tasks = [
            "Complete bill status tracking implementation",
            "Add bill amendment tracking",
            "Implement bill timeline visualization",
            "Create bill comparison feature",
            "Add bill impact analysis",
            "Implement bill notification system",
            "Create bill voting predictions",
            "Add bill sponsor analysis",
            "Implement bill text search",
            "Create bill export functionality",
            "Add bill sharing features",
            "Implement bill categorization",
            "Create bill recommendation engine",
            "Add bill progress alerts",
            "Implement bill archival system"
        ]
        
        for i, task in enumerate(bill_tasks, 81):
            self.add_item(
                title=task,
                gate="G2",
                features=["FEAT-003"],
                activities=["ACT-005", "ACT-006"],
                data=["DATA-002", "DATA-012", "DATA-013"],
                routes=["RT-007", "RT-008", "RT-009", "RT-010", "RT-011"],
                code="services/api-gateway/app/api/v1/bills.py",
                owner="@bills-team",
                dependencies=["CHK-0056"],
                criteria=["Feature works", "LEGISinfo synced", "UI complete"],
                links=["[DATA_CYCLE_MAP bills]"],
                decimal_order=f"2.{i-55}"
            )
            
        # Remaining parity features (96-135)
        parity_tasks = [
            "Implement committee meeting scheduler",
            "Create committee document repository",
            "Add committee member attendance",
            "Implement committee report generation",
            "Create committee video archive",
            "Add vote result visualization",
            "Implement vote prediction model",
            "Create vote comparison tools",
            "Add vote notification system",
            "Implement vote export features",
            "Create debate transcript search",
            "Add debate video timestamps",
            "Implement debate speaker tracking",
            "Create debate summary generation",
            "Add debate sentiment analysis",
            "Implement user preference management",
            "Create user dashboard customization",
            "Add user activity tracking",
            "Implement user data export",
            "Create user notification preferences",
            "Add email alert templates",
            "Implement SMS notifications",
            "Create push notification system",
            "Add alert frequency controls",
            "Implement alert analytics",
            "Create data export scheduler",
            "Add export format options",
            "Implement export compression",
            "Create export status tracking",
            "Add export history management",
            "Implement mobile API optimization",
            "Create mobile offline mode",
            "Add mobile push notifications",
            "Implement mobile biometric auth",
            "Create mobile app analytics",
            "Add accessibility features",
            "Implement multi-language support",
            "Create help documentation",
            "Add user onboarding flow",
            "Complete LEGISinfo integration"
        ]
        
        for i, task in enumerate(parity_tasks, 96):
            feature_map = {
                "committee": "FEAT-005",
                "vote": "FEAT-004", 
                "debate": "FEAT-001",
                "user": "FEAT-006",
                "alert": "FEAT-006",
                "export": "FEAT-007",
                "mobile": "FEAT-008",
                "LEGISinfo": "FEAT-003"
            }
            
            feature = "FEAT-001"  # default
            for key, feat in feature_map.items():
                if key in task.lower():
                    feature = feat
                    break
                    
            self.add_item(
                title=task,
                gate="G2",
                features=[feature],
                activities=["ACT-001"],
                data=["DATA-001"],
                routes=["RT-001"],
                code="services/api-gateway/app/api/v1/*",
                owner="@feature-team",
                dependencies=[],
                criteria=["Feature complete", "Tests pass", "Documentation updated"],
                links=["[Feature parity checklist]"],
                decimal_order=f"2.{i-55}"
            )
            
    def generate_g3_items(self):
        """Generate G3: Architecture Harmony items (65 total)"""
        # WebSocket and real-time (137-146)
        realtime_tasks = [
            "Implement WebSocket infrastructure for real-time updates",
            "Create WebSocket authentication and authorization",
            "Add WebSocket connection pooling",
            "Implement WebSocket message queuing",
            "Create WebSocket reconnection logic",
            "Add WebSocket event routing",
            "Implement WebSocket scaling strategy",
            "Create WebSocket monitoring",
            "Add WebSocket error handling",
            "Implement WebSocket testing framework"
        ]
        
        for i, task in enumerate(realtime_tasks, 137):
            self.add_item(
                title=task,
                gate="G3",
                features=["FEAT-004"],
                activities=["ACT-008"],
                data=["DATA-004", "DATA-017"],
                routes=["RT-015"],
                code="services/api-gateway/app/services/websocket.py",
                owner="@realtime-team",
                dependencies=["CHK-0094"] if i > 137 else [],
                criteria=["WebSockets stable", "Auto-reconnect works", "Scalable to 10k connections"],
                links=["[ADR-20250823-07]", "[ARCH_BLUEPRINT realtime]"],
                decimal_order=f"3.{i-136}"
            )
            
        # Service integration (147-161)
        integration_tasks = [
            "Implement service discovery mechanism",
            "Create inter-service authentication",
            "Add service health monitoring",
            "Implement circuit breaker pattern",
            "Create service versioning strategy",
            "Add distributed tracing",
            "Implement service mesh integration",
            "Create service dependency mapping",
            "Add service performance monitoring",
            "Implement service rollback mechanism",
            "Create API gateway routing rules",
            "Add API response caching",
            "Implement API rate limiting",
            "Create API documentation portal",
            "Add API usage analytics"
        ]
        
        for i, task in enumerate(integration_tasks, 147):
            self.add_item(
                title=task,
                gate="G3",
                features=["ALL"],
                activities=[],
                data=[],
                routes=["ALL"],
                code="services/api-gateway/*",
                owner="@platform-team",
                dependencies=[],
                criteria=["Integration complete", "Performance targets met", "Monitoring enabled"],
                links=["[ADR-20250823-03]", "[ARCH_BLUEPRINT containers]"],
                decimal_order=f"3.{i-136}"
            )
            
        # Database and caching (162-176)
        data_tasks = [
            "Implement database connection pooling",
            "Create database read replicas",
            "Add database query optimization",
            "Implement database backup automation",
            "Create database migration framework",
            "Add database monitoring and alerting",
            "Implement Redis caching strategy",
            "Create cache invalidation logic",
            "Add cache warming procedures",
            "Implement distributed caching",
            "Create Elasticsearch mapping optimization",
            "Add search index management",
            "Implement search performance tuning",
            "Create data archival strategy",
            "Add data retention policies"
        ]
        
        for i, task in enumerate(data_tasks, 162):
            self.add_item(
                title=task,
                gate="G3",
                features=["ALL"],
                activities=[],
                data=["ALL"],
                routes=[],
                code="services/*/database.py" if "database" in task else "services/*/cache.py",
                owner="@data-team",
                dependencies=[],
                criteria=["Implementation complete", "Performance improved", "No data loss"],
                links=["[ADR-20250823-02]", "[ADR-20250823-04]", "[ADR-20250823-05]"],
                decimal_order=f"3.{i-136}"
            )
            
        # Legacy scraper migration (177-201)
        # Main scraper item
        self.add_item(
            title="Migrate legacy Canadian scrapers to new framework",
            gate="G3",
            features=["FEAT-009"],
            activities=["ACT-014"],
            data=["DATA-029", "DATA-030"],
            routes=["RT-028"],
            code="services/etl/legacy-scrapers-ca/*",
            owner="@scraper-team",
            dependencies=["CHK-0183"],
            criteria=["All 139 scrapers migrated", "Data format consistent", "Error handling improved"],
            links=["[legacy_vs_current_diff]", "[139 scraper files]"],
            decimal_order="3.41"
        )
        
        # Provincial scrapers (178-190)
        provinces = ["Alberta", "British Columbia", "Manitoba", "New Brunswick", 
                    "Newfoundland and Labrador", "Northwest Territories", "Nova Scotia",
                    "Nunavut", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Yukon"]
        
        for i, province in enumerate(provinces, 178):
            chk_id = self.add_item(
                title=f"Implement {province} provincial scraper",
                gate="G3",
                features=["FEAT-009"],
                activities=["ACT-014"],
                data=["DATA-029", "DATA-030"],
                routes=["RT-028"],
                code=f"services/etl/app/scrapers/ca_{province.lower().replace(' ', '_')}.py",
                owner="@scraper-team",
                dependencies=["CHK-0177"],
                criteria=["Scraper implemented", "Data validated", "Tests pass"],
                links=[f"[Legacy {province} scraper]"],
                decimal_order=f"3.41.{i-177}"
            )
            
        # Scraper framework components (191-201)
        scraper_components = [
            "Base scraper class with retry logic",
            "CSV data parser implementation",
            "Person data normalizer",
            "Contact info extractor",
            "Photo downloader with caching",
            "Social media link resolver",
            "Duplicate detection system",
            "Data validation framework",
            "Scraper scheduling system",
            "Error reporting and monitoring",
            "Scraper performance optimization"
        ]
        
        for i, component in enumerate(scraper_components, 191):
            self.add_item(
                title=component,
                gate="G3",
                features=["FEAT-009"],
                activities=["ACT-014"],
                data=["DATA-029"],
                routes=[],
                code="services/etl/app/scrapers/base.py",
                owner="@scraper-team",
                dependencies=[],
                criteria=["Component implemented", "Unit tests pass", "Documentation complete"],
                links=["[Legacy CanadianScraper class]"],
                decimal_order=f"3.42.{i-190}"
            )
            
    def generate_g4_items(self):
        """Generate G4: Test Strategy items (60 total)"""
        # Unit testing (202-216)
        unit_test_tasks = [
            "Create comprehensive unit test suite for API Gateway",
            "Implement unit tests for ETL service",
            "Add unit tests for User service",
            "Create unit tests for Admin service",
            "Implement unit tests for all models",
            "Add unit tests for all utilities",
            "Create unit tests for WebSocket handlers",
            "Implement unit tests for cache layer",
            "Add unit tests for search functionality",
            "Create unit tests for authentication",
            "Implement unit tests for scrapers",
            "Add unit tests for data validators",
            "Create unit tests for email service",
            "Implement unit tests for export service",
            "Add unit tests for mobile API"
        ]
        
        for i, task in enumerate(unit_test_tasks, 202):
            service = task.split("for ")[-1].lower()
            self.add_item(
                title=task,
                gate="G4",
                features=["ALL"],
                activities=[],
                data=[],
                routes=["ALL"] if "API" in task else [],
                code=f"services/*/tests/test_*.py",
                owner="@qa-team",
                dependencies=["CHK-0026"],
                criteria=["90% code coverage", "All tests pass", "CI integrated"],
                links=["[ARCH_BLUEPRINT testing]"],
                decimal_order=f"4.{i-201}"
            )
            
        # Integration testing (217-231)
        integration_tasks = [
            "Create API integration test suite",
            "Implement database integration tests",
            "Add cache integration tests",
            "Create search integration tests",
            "Implement service-to-service tests",
            "Add external API integration tests",
            "Create WebSocket integration tests",
            "Implement email delivery tests",
            "Add file storage integration tests",
            "Create authentication flow tests",
            "Implement data pipeline tests",
            "Add monitoring integration tests",
            "Create deployment integration tests",
            "Implement rollback scenario tests",
            "Add multi-service transaction tests"
        ]
        
        for i, task in enumerate(integration_tasks, 217):
            self.add_item(
                title=task,
                gate="G4",
                features=["ALL"],
                activities=[],
                data=["ALL"],
                routes=["ALL"],
                code="tests/integration/*",
                owner="@qa-team",
                dependencies=["CHK-0202"],
                criteria=["Tests cover all scenarios", "Environment isolated", "Repeatable"],
                links=["[Test strategy document]"],
                decimal_order=f"4.{i-201}"
            )
            
        # E2E and performance testing (232-246)
        e2e_tasks = [
            "Create end-to-end test scenarios",
            "Implement user journey tests",
            "Add cross-browser testing",
            "Create mobile app E2E tests",
            "Implement accessibility tests",
            "Add performance test suite",
            "Create load testing scenarios",
            "Implement stress testing",
            "Add scalability tests",
            "Create security test suite",
            "Implement penetration testing",
            "Add vulnerability scanning",
            "Create chaos engineering tests",
            "Implement disaster recovery tests",
            "Add data integrity tests"
        ]
        
        for i, task in enumerate(e2e_tasks, 232):
            self.add_item(
                title=task,
                gate="G4",
                features=["ALL"],
                activities=[],
                data=["ALL"],
                routes=["ALL"],
                code="tests/e2e/*" if "e2e" in task.lower() else "tests/performance/*",
                owner="@qa-team",
                dependencies=[],
                criteria=["All scenarios pass", "Performance targets met", "Security verified"],
                links=["[Performance requirements]", "[Security standards]"],
                decimal_order=f"4.{i-201}"
            )
            
        # Contract and quality testing (247-261)
        quality_tasks = [
            "Implement contract testing between services",
            "Create API contract validation",
            "Add schema validation tests",
            "Implement backwards compatibility tests",
            "Create code quality checks",
            "Add static code analysis",
            "Implement security scanning",
            "Create dependency vulnerability checks",
            "Add license compliance checks",
            "Implement documentation tests",
            "Create API documentation validation",
            "Add configuration validation tests",
            "Implement infrastructure tests",
            "Create monitoring coverage tests",
            "Add test coverage reporting"
        ]
        
        for i, task in enumerate(quality_tasks, 247):
            self.add_item(
                title=task,
                gate="G4",
                features=["ALL"],
                activities=[],
                data=[],
                routes=["ALL"] if "API" in task else [],
                code="tests/contracts/*" if "contract" in task else "tests/quality/*",
                owner="@qa-team",
                dependencies=["CHK-0202"],
                criteria=["All contracts valid", "Quality targets met", "Automated in CI"],
                links=["[ADR-20250823-03 API Gateway]"],
                decimal_order=f"4.{i-201}"
            )
            
    def generate_g5_items(self):
        """Generate G5: Release Readiness items (65 total)"""
        # Monitoring and observability (262-276)
        monitoring_tasks = [
            "Set up monitoring and alerting infrastructure",
            "Implement application metrics collection",
            "Create custom Grafana dashboards",
            "Add log aggregation and analysis",
            "Implement distributed tracing",
            "Create SLI/SLO monitoring",
            "Add error tracking and reporting",
            "Implement performance monitoring",
            "Create business metrics dashboards",
            "Add synthetic monitoring",
            "Implement uptime monitoring",
            "Create capacity planning metrics",
            "Add cost monitoring and optimization",
            "Implement security monitoring",
            "Create incident response automation"
        ]
        
        for i, task in enumerate(monitoring_tasks, 262):
            self.add_item(
                title=task,
                gate="G5",
                features=["ALL"],
                activities=[],
                data=[],
                routes=["RT-039"] if "metrics" in task else [],
                code="monitoring/*",
                owner="@devops-team",
                dependencies=["CHK-0017"],
                criteria=["Monitoring active", "Alerts configured", "Dashboards created"],
                links=["[ARCH_BLUEPRINT monitoring]"],
                decimal_order=f"5.{i-261}"
            )
            
        # Deployment and operations (277-291)
        deployment_tasks = [
            "Create deployment automation scripts",
            "Implement blue-green deployment",
            "Add canary deployment capability",
            "Create rollback procedures",
            "Implement configuration management",
            "Add secret rotation automation",
            "Create environment provisioning",
            "Implement auto-scaling policies",
            "Add load balancer configuration",
            "Create CDN configuration",
            "Implement SSL certificate management",
            "Add DNS management automation",
            "Create backup automation",
            "Implement disaster recovery procedures",
            "Add multi-region deployment"
        ]
        
        for i, task in enumerate(deployment_tasks, 277):
            self.add_item(
                title=task,
                gate="G5",
                features=["ALL"],
                activities=[],
                data=["ALL"],
                routes=[],
                code="infra/*" if "infra" in task else "scripts/deploy/*",
                owner="@devops-team",
                dependencies=[],
                criteria=["Automation complete", "Tested in staging", "Documentation updated"],
                links=["[ARCH_BLUEPRINT deployment]"],
                decimal_order=f"5.{i-261}"
            )
            
        # Documentation and training (292-299)
        doc_tasks = [
            "Create user documentation",
            "Write API documentation",
            "Create operations runbooks",
            "Write troubleshooting guides",
            "Create architecture documentation",
            "Write security documentation",
            "Create training materials",
            "Write onboarding guides"
        ]
        
        for i, task in enumerate(doc_tasks, 292):
            self.add_item(
                title=task,
                gate="G5",
                features=["ALL"],
                activities=[],
                data=[],
                routes=[],
                code="docs/*",
                owner="@docs-team",
                dependencies=[],
                criteria=["Documentation complete", "Reviewed by stakeholders", "Published"],
                links=["[Documentation standards]"],
                decimal_order=f"5.{i-261}"
            )
            
        # Disaster recovery (300)
        self.add_item(
            title="Create disaster recovery procedures",
            gate="G5",
            features=["ALL"],
            activities=[],
            data=["ALL"],
            routes=[],
            code="docs/operations/dr/*",
            owner="@devops-team",
            dependencies=["CHK-0262"],
            criteria=["RTO < 4 hours documented", "RPO < 1 hour achievable", "Runbooks created"],
            links=["[ARCH_BLUEPRINT disaster recovery]"],
            decimal_order="5.39"
        )
        
        # Feature flags (301-317)
        feature_flag_tasks = [
            "Design feature flag system architecture",
            "Implement feature flag service",
            "Create feature flag SDK for Python",
            "Create feature flag SDK for JavaScript",
            "Add feature flag admin UI",
            "Implement user targeting",
            "Add percentage rollouts",
            "Create A/B testing framework",
            "Add feature flag analytics",
            "Implement flag inheritance",
            "Create flag lifecycle management",
            "Add flag audit logging",
            "Implement emergency kill switches",
            "Create flag performance monitoring",
            "Add flag documentation",
            "Implement flag testing framework",
            "Create flag migration tools"
        ]
        
        for i, task in enumerate(feature_flag_tasks, 301):
            self.add_item(
                title=task,
                gate="G5",
                features=["ALL"],
                activities=[],
                data=[],
                routes=[],
                code="services/feature-flags/*",
                owner="@platform-team",
                dependencies=["CHK-0300"] if i > 301 else [],
                criteria=["Feature complete", "SDKs integrated", "Documentation complete"],
                links=["[ADR-20250823-10]"],
                decimal_order=f"5.{i-261}"
            )
            
        # Missing APIs (318-324)
        missing_apis = [
            ("Debates API endpoints", "debates", ["RT-029", "RT-030"]),
            ("Debates detail endpoint", "debates/{debate_id}", ["RT-030"]),
            ("Analytics API for members", "analytics/members", ["RT-031"]),
            ("Analytics API for bills", "analytics/bills", ["RT-032"]),
            ("Analytics API for votes", "analytics/votes", ["RT-033"]),
            ("User profile management GET", "users/{user_id}/profile", ["RT-034"]),
            ("User profile management PUT", "users/{user_id}/profile", ["RT-035"])
        ]
        
        for i, (title, endpoint, routes) in enumerate(missing_apis, 318):
            self.add_item(
                title=f"Implement {title}",
                gate="G5",
                features=["FEAT-001"] if "debate" in title.lower() else ["FEAT-006"],
                activities=[],
                data=["DATA-003"] if "debate" in title.lower() else ["DATA-021"],
                routes=routes,
                code=f"services/api-gateway/app/api/v1/{endpoint.split('/')[0]}.py",
                owner="@api-team",
                dependencies=["CHK-0056"],
                criteria=["API implemented", "Tests pass", "Documentation complete"],
                links=["[Implementation gap from FEATURE_ACTIVITY_MAP]"],
                decimal_order=f"5.{i-261}"
            )
            
        # Final review (325)
        self.add_item(
            title="Final production readiness review",
            gate="G5",
            features=["ALL"],
            activities=["ALL"],
            data=["ALL"],
            routes=["ALL"],
            code="ALL",
            owner="@cto",
            dependencies=["ALL"],
            criteria=[
                "All checklist items complete",
                "Performance benchmarks met",
                "Security scan passed",
                "Documentation complete",
                "Team trained"
            ],
            links=["[All ADRs]", "[All documentation]"],
            decimal_order="5.65"
        )
        
    def format_item(self, item: Dict[str, Any]) -> str:
        """Format a checklist item for output"""
        features = ", ".join(item['features']) if item['features'] else "-"
        activities = ", ".join(item['activities']) if item['activities'] else "-"
        data = ", ".join(item['data']) if item['data'] else "-"
        routes = ", ".join(item['routes']) if item['routes'] else "-"
        dependencies = ", ".join(item['dependencies']) if item['dependencies'] else "[]"
        criteria = "\n".join(f"  {i+1}. {c}" for i, c in enumerate(item['criteria']))
        links = ", ".join(item['links'])
        
        return f"""### {item['id']} (Decimal Order: {item['decimal_order']})
- **Title**: {item['title']}
- **Gate**: {item['gate']}
- **Feature(s)**: {features}
- **Activity**: {activities}
- **Data**: {data}
- **Route(s)**: {routes}
- **Code**: {item['code']}
- **Owner**: {item['owner']}
- **Due**: {item['due']}
- **Dependencies**: [{dependencies}]
- **Acceptance Criteria**:
{criteria}
- **Links**: {links}
- **Enhancements**:
  <!-- Enhancements will be added here -->
"""
        
    def generate_checklist(self):
        """Generate the complete checklist"""
        print("Generating G1 items...")
        self.generate_g1_items()
        print(f"  Generated {len(self.items)} items")
        
        print("Generating G2 items...")
        self.generate_g2_items()
        print(f"  Generated {len(self.items)} items total")
        
        print("Generating G3 items...")
        self.generate_g3_items()
        print(f"  Generated {len(self.items)} items total")
        
        print("Generating G4 items...")
        self.generate_g4_items()
        print(f"  Generated {len(self.items)} items total")
        
        print("Generating G5 items...")
        self.generate_g5_items()
        print(f"  Generated {len(self.items)} items total")
        
        # Count by gate
        gate_counts = {"G1": 0, "G2": 0, "G3": 0, "G4": 0, "G5": 0}
        for item in self.items:
            gate_counts[item['gate']] += 1
            
        # Generate output
        output = f"""# OpenPolicy V2 Implementation Checklist

Generated: {datetime.now().strftime("%Y-%m-%d")}  
Total Items: {len(self.items)}  
Cycles Completed: 0/10  
Last Updated: {datetime.now().strftime("%Y-%m-%d")}

This is the canonical implementation checklist for OpenPolicy V2. Items are enhanced through 10 cycles, append-only.

## Statistics

- Total Items: {len(self.items)}
- G1 (Structure/Index): {gate_counts['G1']}
- G2 (Parity): {gate_counts['G2']}
- G3 (Architecture Harmony): {gate_counts['G3']}
- G4 (Test Strategy): {gate_counts['G4']}
- G5 (Release Readiness): {gate_counts['G5']}

"""
        
        # Group items by gate
        for gate in ["G1", "G2", "G3", "G4", "G5"]:
            output += f"## {gate}: {self.get_gate_name(gate)}\n\n"
            gate_items = [item for item in self.items if item['gate'] == gate]
            for item in gate_items:
                output += self.format_item(item) + "\n"
                
        # Add summary
        output += """## Summary by Gate

| Gate | Items | Description |
|------|-------|-------------|
| G1 | 55 | Structure and indexing tasks |
| G2 | 80 | Feature parity and data completeness |
| G3 | 65 | Architecture alignment and migration |
| G4 | 60 | Testing strategy and quality assurance |
| G5 | 65 | Release readiness and operations |
| **Total** | **325** | **All implementation tasks** |

## Notes

1. This checklist is append-only - items are never removed
2. Each item will be enhanced 10 times through the enhancement cycles
3. Decimal order allows for infinite sub-task expansion
4. All CHK IDs are permanent and traceable
5. Dependencies must be completed before dependent tasks
6. Due dates are initial estimates and may be adjusted
7. Owner assignments are team-level, individuals TBD
"""
        
        return output
        
    def get_gate_name(self, gate: str) -> str:
        """Get the full name for a gate"""
        names = {
            "G1": "Structure/Index",
            "G2": "Parity",
            "G3": "Architecture Harmony",
            "G4": "Test Strategy",
            "G5": "Release Readiness"
        }
        return names.get(gate, gate)


def main():
    generator = ChecklistGenerator()
    checklist = generator.generate_checklist()
    
    # Write to file
    with open("docs/plan/IMPLEMENTATION_CHECKLIST.md", "w") as f:
        f.write(checklist)
        
    print(f"\nGenerated complete checklist with {len(generator.items)} items")
    print("Saved to docs/plan/IMPLEMENTATION_CHECKLIST.md")


if __name__ == "__main__":
    main()