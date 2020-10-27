"""Models instantiated by the companies api."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple


@dataclass(frozen=True)
class Company:
    """Contains all details of a company.

    Attributes:
        id: Numeric unique ID identifying a maritime company.
        updated_date: Date, format YYYY-MM-DD HH:MM:SS, corresponding to the
            latest update.
        company_name: String, official name of the maritime company.
        website: String, website of the company.
        fleet_list: String, link to the fleet list of the company if it has
            vessels under commercial management.
        synonyms: Strings representing synonyms, acronyms or other names the
            company goes by in the shipping market.
        charterer_vessel_types: String, indicates in which market segments the
            company operates as charterer. Possible VesselTypes are "Tanker,
            Dry, Containers, LNG, LPG".
        commercial_operator_vessel_types: String, indicates in which market
            segments the company operates as commercial operator, therefore
            commercially manages vessel. Possible VesselTypes are "Tanker, Dry,
            Containers, LNG, LPG".
        geo_asset_owner_vessel_types: String, indicates if the company owns
            specific facilities such as shipyards or refineries relative to a
            particular vessel type. Possible VesselTypes are "Tanker, Dry,
            Containers, LNG, LPG".
        broker_vessel_types: String, indicates for which market segments the
            company operates as broker. Possible VesselTypes are "Tanker, Dry,
            Containers, LNG, LPG".
        port_agent_vessel_types: String, indicates for which market segments
            the company operates as port agent. Possible VesselTypes are
            "Tanker, Dry, Containers, LNG, LPG".
        parent_company_id: Companies can have parent-child relationships, that
            is being legally related and having common interests. This numeric
            ID corresponds to the parent company or umbrella under which the
            company is.
        children_companies_ids: ID(s) of all companies acting as children of
            the initial company. Please note that a company can either have
            parent or children. We do not support two degrees relationships.
    """

    id: int
    updated_date: datetime
    company_name: Optional[str] = None
    website: Optional[str] = None
    fleet_list: Optional[str] = None
    synonyms: Optional[Tuple[str, ...]] = None
    charterer_vessel_types: Optional[Tuple[str, ...]] = None
    commercial_operator_vessel_types: Optional[Tuple[str, ...]] = None
    geo_asset_owner_vessel_types: Optional[Tuple[str, ...]] = None
    broker_vessel_types: Optional[Tuple[str, ...]] = None
    port_agent_vessel_types: Optional[Tuple[str, ...]] = None
    parent_company_id: Optional[int] = None
    children_companies_ids: Optional[Tuple[int, ...]] = None
