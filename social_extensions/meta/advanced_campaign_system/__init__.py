"""
Advanced Campaign System - Módulo de Campañas Avanzadas Meta
Sistema completo de optimización, distribución geográfica y etiquetado
"""

from .budget_optimizer import BudgetOptimizer, ClipData, ClipMetrics
from .campaign_tagging import (
    AudienceType,
    CampaignTagging,
    CampaignTags,
    CollaboratorProfile,
    GenrePrimary,
    MusicalElements,
)
from .geo_distribution import GeoAllocation, GeoDistribution, RegionalData

__all__ = [
    "BudgetOptimizer",
    "ClipData",
    "ClipMetrics",
    "GeoDistribution",
    "RegionalData",
    "GeoAllocation",
    "CampaignTagging",
    "CampaignTags",
    "CollaboratorProfile",
    "MusicalElements",
    "GenrePrimary",
    "AudienceType",
]

__version__ = "1.0.0"
