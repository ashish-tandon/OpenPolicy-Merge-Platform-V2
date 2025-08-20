"""
Data ingestion module for OpenParliament.ca V2

Following FUNDAMENTAL RULE: Uses existing legacy data structure
"""

from .legacy_data_ingester import LegacyDataIngester

__all__ = [
    "LegacyDataIngester",
]
