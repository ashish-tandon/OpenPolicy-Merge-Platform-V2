"""
Data extractors for various parliamentary data sources.

Following FUNDAMENTAL RULE: Uses legacy OpenParliament importers
"""

from .legacy_adapters import (
    LegacyMPsAdapter,
    LegacyBillsAdapter,
    LegacyVotesAdapter,
    LegacyDataCollectionTask
)

__all__ = [
    "LegacyMPsAdapter",
    "LegacyBillsAdapter", 
    "LegacyVotesAdapter",
    "LegacyDataCollectionTask",
]
