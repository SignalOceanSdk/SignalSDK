"""Models instantiated by the scraped fixtures api."""
from dataclasses import dataclass
from datetime import date, datetime
from email.policy import strict
from pickle import NONE
from tkinter import N
from tkinter.messagebox import NO
from token import OP
from typing import Optional, Tuple

@dataclass(frozen=True)
class ScrapedFixture:
    """
    Detailed information about a scraped fixtures.
    """

    fixture_id: int = None
    message_id: int = None
    updated_date: str = None
    received_date: str = None
    reported_fixture_date: Optional[str] = None
    imo: Optional[int] = None
    vessel_class_id: Optional[int] = None
    laycan_from: Optional[date] = None
    laycan_to: Optional[date] = None
    load_geo_id: Optional[int] = None
    load_taxonomy_id: Optional[int] = None
    discharge_geo_id: Optional[int] = None
    discharge_taxonomy_id: Optional[int] = None
    charterer_id: Optional[int] = None
    cargo_type_id: Optional[int] = None
    cargo_group_id: Optional[int] = None
    quantity: Optional[float] = None
    quantity_buffer: Optional[float] = None
    quantity_from: Optional[float] = None
    quantity_to: Optional[float] = None
    rate_value: Optional[float] = None
    rate_type: Optional[str] = None
    open_geo_id: Optional[int] = None
    open_taxonomy_id: Optional[int] = None
    open_date: Optional[date] = None
    delivery_date_from: Optional[date] = None
    delivery_date_to: Optional[date] = None
    delivery_geo_id: Optional[int] = None
    delivery_taxonomy_id: Optional[int] = None
    redelivery_from_geo_id: Optional[int] = None
    redelivery_from_taxonomy_id: Optional[int] = None
    redelivery_to_geo_id: Optional[int] = None
    redelivery_to_taxonomy_id: Optional[int] = None
    charterer_type_id: Optional[int] = None
    fixture_status_id: Optional[int] = None
    is_owners_option: Optional[bool] = False
    is_coa: Optional[bool] = False
    
    #include details
    parsed_part_id: Optional[int] = None
    line_from: Optional[int] = None
    line_to: Optional[int] = None
    in_line_order: Optional[int] = None
    source: Optional[str] = None

    #include scraped fields
    scraped_vessel_name: Optional[str] = None
    scraped_deadweight: Optional[str] = None
    scraped_year_build: Optional[str] = None
    scraped_laycan: Optional[str] = None
    scraped_load: Optional[str] = None
    scraped_discharge: Optional[str] = None
    scraped_discharge_options: Optional[str] = None
    scraped_charterer: Optional[str] = None
    scraped_cargo_type: Optional[str] = None
    scraped_quantity: Optional[str] = None
    scraped_rate: Optional[str] = None
    scraped_options: Optional[str] = None
    scraped_delivery_date: Optional[str] = None
    scraped_delivery: Optional[str] = None
    scraped_redelivery_from: Optional[str] = None
    scraped_redelivery_to: Optional[str] = None
    
    #Include vessel details
    vessel_name: Optional[str] = None
    deadweight: Optional[int] = None
    year_build: Optional[int] = None
    liquid_capacity: Optional[int] = None
    vessel_type_id: Optional[int] = None
    vessel_type: Optional[str] = None
    vessel_class: Optional[str] = None
    commercial_operator_id: Optional[int] = None
    commercial_operator: Optional[str] = None
    

    #include labels
    load_name: Optional[str] = None
    load_taxonomy: Optional[str] = None
    discharge_name: Optional[str] = None
    discharge_taxonomy: Optional[str] = None
    charterer: Optional[str] = None
    cargo_type: Optional[str] = None
    cargo_group: Optional[str] = None
    open_taxonomy: Optional[str] = None
    redelivery_from_name: Optional[str] = None
    delivery_name: Optional[str] = None
    open_geo_name: Optional[str] = None
    redelivery_from_taxonomy: Optional[str] = None
    redelivery_to_name: Optional[str] = None
    redelivery_to_taxonomy: Optional[str] = None
    charterer_type: Optional[str] = None
    fixture_status: Optional[str] = None

    # include content
    content: Optional[str] = None

    # include sender
    sender: Optional[str] = None
    sender_name: Optional[str] = None
    sender_domain: Optional[str] = None
    mapped_sender: Optional[str] = None

    # include debug info
    is_public: Optional[bool] = False
    is_private: Optional[bool] = False
    is_shared: Optional[bool] = False
    is_invalidated: Optional[bool] = False
    is_partial: Optional[bool] = False