# 🔄 ETL PIPELINE IMPLEMENTATION
## Merge V2: Legacy System Integration Architecture

**Date:** August 21, 2025  
**Version:** 1.0  
**Status:** 🔴 IMPLEMENTATION READY  
**Scope:** Complete ETL pipeline for legacy system integration  

---

## 🎯 ETL PIPELINE OBJECTIVES

### **Primary Goals**
1. **Unified Data Extraction** - Single interface for all legacy systems
2. **Data Transformation** - Consistent format across all sources
3. **Data Quality Validation** - Comprehensive validation and error handling
4. **Incremental Updates** - Efficient data synchronization
5. **Monitoring & Alerting** - Real-time pipeline status and metrics

### **Success Criteria**
- 100% of legacy systems integrated
- Real-time data synchronization
- Data quality validation passing
- Comprehensive error handling and recovery
- Performance monitoring and alerting

---

## 🏗️ ETL ARCHITECTURE OVERVIEW

### **Pipeline Components**
```
Legacy Systems → Extractors → Transformers → Validators → Loaders → Unified Database
     ↓              ↓            ↓            ↓          ↓           ↓
  OpenParliament  Connector   Data Model   Quality     Storage    PostgreSQL
  Municipal Data   Connector   Mapper      Checks      Engine     + Redis
  Civic Scraper   Connector   Normalizer  Validation  Cache      + Search
```

### **Data Flow**
1. **Extract** - Pull data from legacy systems
2. **Transform** - Convert to unified data model
3. **Validate** - Check data quality and integrity
4. **Load** - Store in unified database
5. **Monitor** - Track performance and errors

---

## 🔌 LEGACY SYSTEM CONNECTORS

### **Base Connector Interface**
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import asyncio
import aiohttp
from datetime import datetime
import logging

class LegacyConnector(ABC):
    """Abstract base class for legacy system connectors"""
    
    def __init__(self, source_name: str, config: Dict[str, Any]):
        self.source_name = source_name
        self.config = config
        self.session = None
        self.logger = logging.getLogger(f"connector.{source_name}")
        self.metrics = {
            "extracted_count": 0,
            "transformed_count": 0,
            "loaded_count": 0,
            "error_count": 0,
            "last_sync": None
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=300),
            headers={"User-Agent": "MergeV2-ETL/1.0"}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    @abstractmethod
    async def extract(self) -> List[Dict[str, Any]]:
        """Extract data from legacy system"""
        pass
    
    @abstractmethod
    async def transform(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform raw data to unified format"""
        pass
    
    async def load(self, entity: Dict[str, Any]) -> bool:
        """Load entity to unified system"""
        try:
            # Implementation with database storage
            success = await self._store_entity(entity)
            if success:
                self.metrics["loaded_count"] += 1
            return success
        except Exception as e:
            self.logger.error(f"Error loading entity: {e}")
            self.metrics["error_count"] += 1
            return False
    
    async def _store_entity(self, entity: Dict[str, Any]) -> bool:
        """Store entity in database"""
        # Database storage implementation
        pass
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get connector metrics"""
        return self.metrics.copy()
```

### **OpenParliament Connector**
```python
class OpenParliamentConnector(LegacyConnector):
    """Connector for OpenParliament legacy system"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("openparliament", config)
        self.base_url = config.get("base_url", "https://openparliament.ca")
        self.api_key = config.get("api_key")
        self.db_connection = config.get("database_connection")
    
    async def extract(self) -> List[Dict[str, Any]]:
        """Extract MPs, bills, votes from OpenParliament"""
        try:
            entities = []
            
            # Extract MPs
            mps = await self._extract_mps()
            entities.extend(mps)
            
            # Extract Bills
            bills = await self._extract_bills()
            entities.extend(bills)
            
            # Extract Votes
            votes = await self._extract_votes()
            entities.extend(votes)
            
            self.metrics["extracted_count"] = len(entities)
            self.logger.info(f"Extracted {len(entities)} entities from OpenParliament")
            
            return entities
            
        except Exception as e:
            self.logger.error(f"Error extracting from OpenParliament: {e}")
            raise
    
    async def _extract_mps(self) -> List[Dict[str, Any]]:
        """Extract MP data"""
        try:
            # API endpoint for MPs
            url = f"{self.base_url}/api/v1/mp/"
            params = {"limit": 1000, "format": "json"}
            
            if self.api_key:
                params["key"] = self.api_key
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("objects", [])
                else:
                    self.logger.error(f"Failed to extract MPs: {response.status}")
                    return []
                    
        except Exception as e:
            self.logger.error(f"Error extracting MPs: {e}")
            return []
    
    async def _extract_bills(self) -> List[Dict[str, Any]]:
        """Extract bill data"""
        try:
            url = f"{self.base_url}/api/v1/bill/"
            params = {"limit": 1000, "format": "json"}
            
            if self.api_key:
                params["key"] = self.api_key
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("objects", [])
                else:
                    self.logger.error(f"Failed to extract bills: {response.status}")
                    return []
                    
        except Exception as e:
            self.logger.error(f"Error extracting bills: {e}")
            return []
    
    async def _extract_votes(self) -> List[Dict[str, Any]]:
        """Extract vote data"""
        try:
            url = f"{self.base_url}/api/v1/vote/"
            params = {"limit": 1000, "format": "json"}
            
            if self.api_key:
                params["key"] = self.api_key
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("objects", [])
                else:
                    self.logger.error(f"Failed to extract votes: {response.status}")
                    return []
                    
        except Exception as e:
            self.logger.error(f"Error extracting votes: {e}")
            return []
    
    async def transform(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform OpenParliament data to unified format"""
        try:
            entity_type = self._determine_entity_type(raw_data)
            
            if entity_type == "mp":
                return self._transform_mp(raw_data)
            elif entity_type == "bill":
                return self._transform_bill(raw_data)
            elif entity_type == "vote":
                return self._transform_vote(raw_data)
            else:
                self.logger.warning(f"Unknown entity type: {entity_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error transforming data: {e}")
            return None
    
    def _determine_entity_type(self, data: Dict[str, Any]) -> str:
        """Determine entity type from raw data"""
        if "name" in data and "party" in data:
            return "mp"
        elif "title" in data and "status" in data:
            return "bill"
        elif "bill" in data and "outcome" in data:
            return "vote"
        else:
            return "unknown"
    
    def _transform_mp(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform MP data to unified format"""
        return {
            "type": "mp",
            "data": {
                "name": raw_data.get("name", ""),
                "party": raw_data.get("party", ""),
                "riding": raw_data.get("riding", ""),
                "province": raw_data.get("province", ""),
                "elected": raw_data.get("elected", ""),
                "photo_url": raw_data.get("photo", ""),
                "twitter": raw_data.get("twitter", ""),
                "website": raw_data.get("website", "")
            },
            "metadata": {
                "source_url": raw_data.get("url", ""),
                "last_updated": raw_data.get("updated", ""),
                "raw_data": raw_data
            },
            "source": "openparliament",
            "source_id": str(raw_data.get("id", "")),
            "relationships": []
        }
    
    def _transform_bill(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform bill data to unified format"""
        return {
            "type": "bill",
            "data": {
                "title": raw_data.get("title", ""),
                "short_title": raw_data.get("short_title", ""),
                "status": raw_data.get("status", ""),
                "session": raw_data.get("session", ""),
                "introduced": raw_data.get("introduced", ""),
                "summary": raw_data.get("summary", ""),
                "text_url": raw_data.get("text_url", "")
            },
            "metadata": {
                "source_url": raw_data.get("url", ""),
                "last_updated": raw_data.get("updated", ""),
                "raw_data": raw_data
            },
            "source": "openparliament",
            "source_id": str(raw_data.get("id", "")),
            "relationships": []
        }
    
    def _transform_vote(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform vote data to unified format"""
        return {
            "type": "vote",
            "data": {
                "bill": raw_data.get("bill", ""),
                "outcome": raw_data.get("outcome", ""),
                "date": raw_data.get("date", ""),
                "session": raw_data.get("session", ""),
                "description": raw_data.get("description", "")
            },
            "metadata": {
                "source_url": raw_data.get("url", ""),
                "last_updated": raw_data.get("updated", ""),
                "raw_data": raw_data
            },
            "source": "openparliament",
            "source_id": str(raw_data.get("id", "")),
            "relationships": []
        }
```

### **Municipal Scrapers Connector**
```python
class MunicipalScrapersConnector(LegacyConnector):
    """Connector for municipal government scrapers"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("municipal_scrapers", config)
        self.scrapers = config.get("scrapers", [])
        self.jurisdictions = config.get("jurisdictions", [])
    
    async def extract(self) -> List[Dict[str, Any]]:
        """Extract municipal data from various sources"""
        try:
            entities = []
            
            for scraper in self.scrapers:
                try:
                    scraper_data = await self._extract_from_scraper(scraper)
                    entities.extend(scraper_data)
                except Exception as e:
                    self.logger.error(f"Error extracting from scraper {scraper}: {e}")
                    continue
            
            self.metrics["extracted_count"] = len(entities)
            self.logger.info(f"Extracted {len(entities)} entities from municipal scrapers")
            
            return entities
            
        except Exception as e:
            self.logger.error(f"Error extracting from municipal scrapers: {e}")
            raise
    
    async def _extract_from_scraper(self, scraper: str) -> List[Dict[str, Any]]:
        """Extract data from a specific scraper"""
        try:
            # Implementation depends on scraper type
            if scraper.startswith("ca_on_"):
                return await self._extract_ontario_municipality(scraper)
            elif scraper.startswith("ca_bc_"):
                return await self._extract_bc_municipality(scraper)
            elif scraper.startswith("ca_ab_"):
                return await self._extract_alberta_municipality(scraper)
            else:
                self.logger.warning(f"Unknown scraper type: {scraper}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error extracting from scraper {scraper}: {e}")
            return []
    
    async def transform(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform municipal data to unified format"""
        try:
            return {
                "type": "jurisdiction",
                "data": {
                    "name": raw_data.get("name", ""),
                    "type": raw_data.get("type", ""),
                    "province": raw_data.get("province", ""),
                    "population": raw_data.get("population", 0),
                    "area": raw_data.get("area", 0),
                    "website": raw_data.get("website", ""),
                    "mayor": raw_data.get("mayor", ""),
                    "councillors": raw_data.get("councillors", [])
                },
                "metadata": {
                    "source_scraper": raw_data.get("scraper", ""),
                    "last_updated": raw_data.get("updated", ""),
                    "raw_data": raw_data
                },
                "source": "municipal_scrapers",
                "source_id": str(raw_data.get("id", "")),
                "relationships": []
            }
            
        except Exception as e:
            self.logger.error(f"Error transforming municipal data: {e}")
            return None
```

---

## 🔄 DATA TRANSFORMATION ENGINE

### **Unified Data Model Mapper**
```python
class DataModelMapper:
    """Maps legacy data to unified data model"""
    
    def __init__(self):
        self.transformers = {
            "mp": self._transform_mp,
            "bill": self._transform_bill",
            "vote": self._transform_vote",
            "debate": self._transform_debate,
            "committee": self._transform_committee,
            "session": self._transform_session,
            "jurisdiction": self._transform_jurisdiction
        }
    
    def transform(self, entity_type: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform data to unified format"""
        if entity_type in self.transformers:
            return self.transformers[entity_type](raw_data)
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")
    
    def _transform_mp(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform MP data to unified format"""
        return {
            "type": "mp",
            "data": {
                "name": raw_data.get("name", ""),
                "party": raw_data.get("party", ""),
                "riding": raw_data.get("riding", ""),
                "province": raw_data.get("province", ""),
                "elected": raw_data.get("elected", ""),
                "photo_url": raw_data.get("photo", ""),
                "twitter": raw_data.get("twitter", ""),
                "website": raw_data.get("website", "")
            },
            "metadata": {
                "source_url": raw_data.get("url", ""),
                "last_updated": raw_data.get("updated", ""),
                "raw_data": raw_data
            },
            "relationships": []
        }
    
    def _transform_bill(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform bill data to unified format"""
        return {
            "type": "bill",
            "data": {
                "title": raw_data.get("title", ""),
                "short_title": raw_data.get("short_title", ""),
                "status": raw_data.get("status", ""),
                "session": raw_data.get("session", ""),
                "introduced": raw_data.get("introduced", ""),
                "summary": raw_data.get("summary", ""),
                "text_url": raw_data.get("text_url", "")
            },
            "metadata": {
                "source_url": raw_data.get("url", ""),
                "last_updated": raw_data.get("updated", ""),
                "raw_data": raw_data
            },
            "relationships": []
        }
    
    def _transform_vote(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform vote data to unified format"""
        return {
            "type": "vote",
            "data": {
                "bill": raw_data.get("bill", ""),
                "outcome": raw_data.get("outcome", ""),
                "date": raw_data.get("date", ""),
                "session": raw_data.get("session", ""),
                "description": raw_data.get("description", "")
            },
            "metadata": {
                "source_url": raw_data.get("url", ""),
                "last_updated": raw_data.get("updated", ""),
                "raw_data": raw_data
            },
            "relationships": []
        }
    
    def _transform_debate(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform debate data to unified format"""
        return {
            "type": "debate",
            "data": {
                "title": raw_data.get("title", ""),
                "date": raw_data.get("date", ""),
                "session": raw_data.get("session", ""),
                "transcript": raw_data.get("transcript", ""),
                "participants": raw_data.get("participants", [])
            },
            "metadata": {
                "source_url": raw_data.get("url", ""),
                "last_updated": raw_data.get("updated", ""),
                "raw_data": raw_data
            },
            "relationships": []
        }
    
    def _transform_committee(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform committee data to unified format"""
        return {
            "type": "committee",
            "data": {
                "name": raw_data.get("name", ""),
                "type": raw_data.get("type", ""),
                "session": raw_data.get("session", ""),
                "members": raw_data.get("members", []),
                "chair": raw_data.get("chair", ""),
                "description": raw_data.get("description", "")
            },
            "metadata": {
                "source_url": raw_data.get("url", ""),
                "last_updated": raw_data.get("updated", ""),
                "raw_data": raw_data
            },
            "relationships": []
        }
    
    def _transform_session(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform session data to unified format"""
        return {
            "type": "session",
            "data": {
                "number": raw_data.get("number", ""),
                "start_date": raw_data.get("start_date", ""),
                "end_date": raw_data.get("end_date", ""),
                "status": raw_data.get("status", ""),
                "description": raw_data.get("description", "")
            },
            "metadata": {
                "source_url": raw_data.get("url", ""),
                "last_updated": raw_data.get("updated", ""),
                "raw_data": raw_data
            },
            "relationships": []
        }
    
    def _transform_jurisdiction(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform jurisdiction data to unified format"""
        return {
            "type": "jurisdiction",
            "data": {
                "name": raw_data.get("name", ""),
                "type": raw_data.get("type", ""),
                "province": raw_data.get("province", ""),
                "population": raw_data.get("population", 0),
                "area": raw_data.get("area", 0),
                "website": raw_data.get("website", ""),
                "mayor": raw_data.get("mayor", ""),
                "councillors": raw_data.get("councillors", [])
            },
            "metadata": {
                "source_scraper": raw_data.get("scraper", ""),
                "last_updated": raw_data.get("updated", ""),
                "raw_data": raw_data
            },
            "relationships": []
        }
```

---

## ✅ DATA VALIDATION ENGINE

### **Data Quality Validator**
```python
from typing import List, Dict, Any, Tuple
import jsonschema
from datetime import datetime

class DataValidator:
    """Validates data quality and integrity"""
    
    def __init__(self):
        self.schemas = self._load_validation_schemas()
        self.validators = {
            "mp": self._validate_mp,
            "bill": self._validate_bill",
            "vote": self._validate_vote",
            "debate": self._validate_debate,
            "committee": self._validate_committee,
            "session": self._validate_session,
            "jurisdiction": self._validate_jurisdiction
        }
    
    def validate(self, entity_type: str, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate entity data"""
        if entity_type in self.validators:
            return self.validators[entity_type](data)
        else:
            return False, [f"Unknown entity type: {entity_type}"]
    
    def _validate_mp(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate MP data"""
        errors = []
        
        # Required fields
        required_fields = ["name", "party", "riding"]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Field type validation
        if data.get("name") and not isinstance(data["name"], str):
            errors.append("Name must be a string")
        
        if data.get("party") and not isinstance(data["party"], str):
            errors.append("Party must be a string")
        
        if data.get("riding") and not isinstance(data["riding"], str):
            errors.append("Riding must be a string")
        
        # Field length validation
        if data.get("name") and len(data["name"]) > 200:
            errors.append("Name too long (max 200 characters)")
        
        if data.get("party") and len(data["party"]) > 100:
            errors.append("Party too long (max 100 characters)")
        
        return len(errors) == 0, errors
    
    def _validate_bill(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate bill data"""
        errors = []
        
        # Required fields
        required_fields = ["title", "status"]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Field type validation
        if data.get("title") and not isinstance(data["title"], str):
            errors.append("Title must be a string")
        
        if data.get("status") and not isinstance(data["status"], str):
            errors.append("Status must be a string")
        
        # Status validation
        valid_statuses = ["introduced", "in_committee", "passed", "failed", "law"]
        if data.get("status") and data["status"] not in valid_statuses:
            errors.append(f"Invalid status: {data['status']}")
        
        return len(errors) == 0, errors
    
    def _validate_vote(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate vote data"""
        errors = []
        
        # Required fields
        required_fields = ["bill", "outcome"]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Field type validation
        if data.get("bill") and not isinstance(data["bill"], str):
            errors.append("Bill must be a string")
        
        if data.get("outcome") and not isinstance(data["outcome"], str):
            errors.append("Outcome must be a string")
        
        # Outcome validation
        valid_outcomes = ["passed", "failed", "tied"]
        if data.get("outcome") and data["outcome"] not in valid_outcomes:
            errors.append(f"Invalid outcome: {data['outcome']}")
        
        return len(errors) == 0, errors
    
    def _validate_debate(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate debate data"""
        errors = []
        
        # Required fields
        required_fields = ["title", "date"]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Date validation
        if data.get("date"):
            try:
                datetime.fromisoformat(data["date"].replace("Z", "+00:00"))
            except ValueError:
                errors.append("Invalid date format")
        
        return len(errors) == 0, errors
    
    def _validate_committee(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate committee data"""
        errors = []
        
        # Required fields
        required_fields = ["name", "type"]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        return len(errors) == 0, errors
    
    def _validate_session(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate session data"""
        errors = []
        
        # Required fields
        required_fields = ["number"]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        return len(errors) == 0, errors
    
    def _validate_jurisdiction(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate jurisdiction data"""
        errors = []
        
        # Required fields
        required_fields = ["name", "type", "province"]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Province validation
        valid_provinces = ["ON", "BC", "AB", "QC", "NS", "NB", "MB", "SK", "NL", "PE", "NT", "NU", "YT"]
        if data.get("province") and data["province"] not in valid_provinces:
            errors.append(f"Invalid province: {data['province']}")
        
        return len(errors) == 0, errors
```

---

## 🚀 ETL PIPELINE ORCHESTRATOR

### **Pipeline Orchestrator**
```python
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import logging

class ETLOrchestrator:
    """Orchestrates the entire ETL pipeline"""
    
    def __init__(self, connectors: List[LegacyConnector]):
        self.connectors = connectors
        self.metrics = {}
        self.logger = logging.getLogger("etl_orchestrator")
        self.validator = DataValidator()
        self.mapper = DataModelMapper()
    
    async def run_full_sync(self) -> Dict[str, Any]:
        """Run full synchronization from all legacy systems"""
        start_time = datetime.utcnow()
        results = {}
        
        self.logger.info("Starting full ETL synchronization")
        
        for connector in self.connectors:
            try:
                self.logger.info(f"Processing connector: {connector.source_name}")
                
                async with connector:
                    # Extract
                    raw_data = await connector.extract()
                    self.logger.info(f"Extracted {len(raw_data)} entities from {connector.source_name}")
                    
                    # Transform and validate
                    entities = []
                    for data in raw_data:
                        try:
                            # Transform to unified format
                            transformed_data = await connector.transform(data)
                            
                            if transformed_data:
                                # Validate data
                                is_valid, errors = self.validator.validate(
                                    transformed_data["type"], 
                                    transformed_data["data"]
                                )
                                
                                if is_valid:
                                    # Load to database
                                    success = await connector.load(transformed_data)
                                    if success:
                                        entities.append(transformed_data)
                                    else:
                                        self.logger.error(f"Failed to load entity: {transformed_data.get('id')}")
                                else:
                                    self.logger.warning(f"Data validation failed: {errors}")
                            else:
                                self.logger.warning(f"Transformation failed for data: {data.get('id')}")
                                
                        except Exception as e:
                            self.logger.error(f"Error processing entity: {e}")
                            continue
                    
                    results[connector.source_name] = {
                        "extracted": len(raw_data),
                        "transformed": len(entities),
                        "loaded": len(entities),
                        "success": True,
                        "errors": []
                    }
                    
                    self.logger.info(f"Successfully processed {len(entities)} entities from {connector.source_name}")
                    
            except Exception as e:
                self.logger.error(f"Error processing connector {connector.source_name}: {e}")
                results[connector.source_name] = {
                    "extracted": 0,
                    "transformed": 0,
                    "loaded": 0,
                    "success": False,
                    "error": str(e)
                }
        
        # Update metrics
        self.metrics["last_sync"] = {
            "start_time": start_time,
            "end_time": datetime.utcnow(),
            "results": results
        }
        
        self.logger.info("ETL synchronization completed")
        return results
    
    async def run_incremental_sync(self) -> Dict[str, Any]:
        """Run incremental synchronization"""
        self.logger.info("Starting incremental ETL synchronization")
        
        # Implementation for incremental sync
        # This would check for changes since last sync
        pass
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get ETL pipeline metrics"""
        return self.metrics.copy()
    
    def get_connector_metrics(self) -> Dict[str, Any]:
        """Get metrics from all connectors"""
        return {
            connector.source_name: connector.get_metrics()
            for connector in self.connectors
        }
```

---

## 📊 MONITORING & ALERTING

### **ETL Pipeline Monitor**
```python
import time
from typing import Dict, Any
import logging

class ETLMonitor:
    """Monitors ETL pipeline performance and health"""
    
    def __init__(self):
        self.logger = logging.getLogger("etl_monitor")
        self.metrics = {
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "total_entities_processed": 0,
            "average_processing_time": 0,
            "last_run_status": "unknown",
            "last_run_time": None
        }
    
    def record_run(self, success: bool, entities_processed: int, processing_time: float):
        """Record ETL run metrics"""
        self.metrics["total_runs"] += 1
        
        if success:
            self.metrics["successful_runs"] += 1
            self.metrics["last_run_status"] = "success"
        else:
            self.metrics["failed_runs"] += 1
            self.metrics["last_run_status"] = "failed"
        
        self.metrics["total_entities_processed"] += entities_processed
        self.metrics["last_run_time"] = datetime.utcnow()
        
        # Update average processing time
        if self.metrics["total_runs"] > 0:
            current_avg = self.metrics["average_processing_time"]
            new_avg = (current_avg * (self.metrics["total_runs"] - 1) + processing_time) / self.metrics["total_runs"]
            self.metrics["average_processing_time"] = new_avg
    
    def check_health(self) -> Dict[str, Any]:
        """Check ETL pipeline health"""
        health_status = {
            "status": "healthy",
            "issues": [],
            "recommendations": []
        }
        
        # Check success rate
        if self.metrics["total_runs"] > 0:
            success_rate = self.metrics["successful_runs"] / self.metrics["total_runs"]
            if success_rate < 0.9:
                health_status["status"] = "warning"
                health_status["issues"].append(f"Low success rate: {success_rate:.2%}")
                health_status["recommendations"].append("Investigate recent failures")
        
        # Check processing time
        if self.metrics["average_processing_time"] > 300:  # 5 minutes
            health_status["status"] = "warning"
            health_status["issues"].append(f"High average processing time: {self.metrics['average_processing_time']:.2f}s")
            health_status["recommendations"].append("Optimize data processing")
        
        # Check last run
        if self.metrics["last_run_status"] == "failed":
            health_status["status"] = "critical"
            health_status["issues"].append("Last ETL run failed")
            health_status["recommendations"].append("Immediate investigation required")
        
        return health_status
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get monitoring metrics"""
        return self.metrics.copy()
```

---

## 🔧 CONFIGURATION & SETUP

### **ETL Configuration File**
```yaml
# etl_config.yaml
etl:
  # General settings
  batch_size: 1000
  max_workers: 4
  retry_attempts: 3
  retry_delay: 60
  
  # Connectors configuration
  connectors:
    openparliament:
      enabled: true
      type: "parliamentary"
      base_url: "https://openparliament.ca"
      api_key: "${OPENPARLIAMENT_API_KEY}"
      sync_frequency: 3600  # 1 hour
      batch_size: 500
      
    municipal_scrapers:
      enabled: true
      type: "municipal"
      scrapers:
        - "ca_on_toronto"
        - "ca_on_ottawa"
        - "ca_bc_vancouver"
        - "ca_ab_calgary"
      sync_frequency: 7200  # 2 hours
      batch_size: 100
      
    civic_scraper:
      enabled: true
      type: "civic"
      base_url: "https://civicdata.io"
      api_key: "${CIVIC_SCRAPER_API_KEY}"
      sync_frequency: 1800  # 30 minutes
      batch_size: 200
  
  # Data validation settings
  validation:
    strict_mode: true
    max_errors_per_batch: 100
    required_fields:
      mp: ["name", "party", "riding"]
      bill: ["title", "status"]
      vote: ["bill", "outcome"]
  
  # Monitoring settings
  monitoring:
    enabled: true
    metrics_interval: 300  # 5 minutes
    alert_thresholds:
      success_rate: 0.9
      processing_time: 300
      error_rate: 0.1
  
  # Storage settings
  storage:
    database_url: "${DATABASE_URL}"
    redis_url: "${REDIS_URL}"
    cache_ttl: 3600
    backup_enabled: true
    backup_retention_days: 30
```

---

## 🚀 IMPLEMENTATION CHECKLIST

### **Phase 1: Core Infrastructure**
- [ ] Implement base connector interface
- [ ] Create OpenParliament connector
- [ ] Create municipal scrapers connector
- [ ] Implement data transformation engine
- [ ] Set up data validation framework

### **Phase 2: Pipeline Orchestration**
- [ ] Implement ETL orchestrator
- [ ] Add error handling and retry logic
- [ ] Implement incremental sync capabilities
- [ ] Add data quality monitoring

### **Phase 3: Monitoring & Optimization**
- [ ] Set up performance monitoring
- [ ] Implement alerting system
- [ ] Add data quality metrics
- [ ] Optimize processing performance

---

## 📞 CONCLUSION

This ETL pipeline implementation provides:

- **Unified data extraction** from all legacy systems
- **Consistent data transformation** to unified format
- **Comprehensive data validation** and quality checks
- **Robust error handling** and recovery mechanisms
- **Real-time monitoring** and performance metrics
- **Scalable architecture** for future growth

**Ready for implementation and integration with legacy systems.**

**Status: ✅ ETL PIPELINE DESIGN COMPLETE - READY FOR IMPLEMENTATION**
