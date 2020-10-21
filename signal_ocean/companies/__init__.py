"""Companies API Package.

Classes:
    CompaniesAPI: Represents Signal's Companies API.
    Company: Represents a Company.
"""

from .models import Company
from .companies_api import CompaniesAPI

__all__ = ["Company", "CompaniesAPI"]
