"""Models instantiated by the oilx cargo tracking api."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple


@dataclass(frozen=True)
class CargoFlow:
    """Contains information about a single Cargo Flow.

    Attributes:
        imo: Vessel’s international maritime organization unique number.
        id: Numeric ID of each cargo flow.
        vessel_class_id: Numeric ID corresponding to the different vessel
            classes of a certain vessel type.
        load_date: End date of loading
        load_geo_asset_id:
            Numeric ID of the load geo asset. Geo assets represent maritime
            facilities such as terminals, anchorages and lightering zones.
            Multiple geo assets are grouped under the same port.
        discharge_date: End date of discharge
        discharge_geo_asset_id:
            Numeric ID of the discharge geo asset.
            Geo assets represent maritime
            facilities such as terminals, anchorages and lightering zones.
            Multiple geo assets are grouped under the same port.
        load_port_id:
            ID corresponding to the load port. A port may be associated
            with multiple geo assets representing different terminals and
            anchorages within this port.
        load_sts_indicator: Ship-to-Ship indicator during loading
        crude_oil_grade_id:
            Numeric ID corresponding to the type of cargo the vessel
            carries in this cargo flow.
            For example 19-> Crude Oil, 16->Fueloil,
            9-> Naphtha, 135-> Unleaded Motor Spirit, 12-> Gasoil.
        crude_oil_grade_name: Crude oil grade name
        crude_oil_grade_group_id:
            Numeric ID corresponding to the high-level cargo the
            vessel carries in this cargo flow, therefore called cargo group.
            For example 130000->Dirty, 120000-> Clean.
        crude_oil_grade_group_name:
            String, it corresponds to the estimated high-level cargo
            the vessel carries in this cargo flow
        api_gravity: Crude oil API gravity
        gravity_band: Light / Heavy,
            classification of crude oil depending on its API gravity.
        sulphur_content: Crude oil sulphur content
        sulphur_band: Sweet / Sour,
            classification of crude oil depending on the amount
            of sulfur it contains.
        origin_country_id: Numeric ID corresponding to the Country of origin.
        origin_country_name: Crude oil country of origin
        load_quantity_kilo_tonnes: Load quantity in kilotonnes
        load_quantity_kilo_barrels: Load quantity in kilobarrels
        discharge_port_id:
            ID corresponding to the discharge port. A port may be associated
            with multiple geo assets representing different terminals and
            anchorages within this port.
        discharge_sts_indicator: Ship-to-Ship indicator during discharging
        supplier_name: Supplier’s company name
        buyer_name:  Buyer’s company name
        load_country_group_id:
            Numeric ID corresponding to global organizations of countries.
            This field is used to mark OECD and OPEC origin countries.
        load_country_group_name:
            String, it corresponds to global organizations of countries.
            This field is used to mark OECD and OPEC origin countries.
        destination_country_id:
            Numeric ID corresponding to the Country of destination.
        destination_country_name: Crude oil country of destination.
        voyage_id: string.
            The id of the voyage which is mapped to the specific cargo flow.
        load_event_id: string.
            The id of the event which is mapped to the
            loading operation of the specific cargo flow.
        discharge_event_id: string.
            The id of the event which is mapped to the
            discharge operation of the specific cargo flow.
        load_event_detail_id:  string.
            The id of the event detail which is mapped to the
            loading operation of the specific cargo flow.
        discharge_event_detail_id: string.
            The id of the event detail which is mapped to the
            discharge operation of the specific cargo flow.
        deleted: Boolean.
            Indicator of wether the mapped voyage is deleted or not
    """

    imo: int
    id: str
    vessel_name: Optional[str] = None
    vessel_class_id: Optional[int] = None
    load_date: Optional[datetime] = None
    load_geo_asset_id: Optional[int] = None
    discharge_date: Optional[datetime] = None
    discharge_geo_asset_id: Optional[int] = None
    load_port_id: Optional[int] = None
    load_sts_indicator: Optional[int] = None
    crude_oil_grade_id: Optional[int] = None
    crude_oil_grade_name: Optional[str] = None
    crude_oil_grade_group_id: Optional[int] = None
    crude_oil_grade_group_name: Optional[str] = None
    api_gravity: Optional[float] = None
    gravity_band: Optional[str] = None
    sulphur_content: Optional[float] = None
    sulphur_band: Optional[str] = None
    origin_country_id: Optional[int] = None
    origin_country_name: Optional[str] = None
    load_quantity_kilo_tonnes: Optional[float] = None
    load_quantity_kilo_barrels: Optional[float] = None
    discharge_port_id: Optional[int] = None
    discharge_sts_indicator: Optional[int] = None
    supplier_name: Optional[str] = None
    buyer_name: Optional[str] = None
    load_country_group_id: Optional[int] = None
    load_country_group_name: Optional[str] = None
    load_sub_country_id: Optional[int] = None
    load_sub_country_name: Optional[str] = None
    discharge_country_group_id: Optional[int] = None
    discharge_country_group_name: Optional[str] = None
    discharge_sub_country_id: Optional[int] = None
    discharge_sub_country_name: Optional[str] = None
    destination_country_id: Optional[int] = None
    destination_country_name: Optional[str] = None
    voyage_id: Optional[str] = None
    load_event_id: Optional[str] = None
    discharge_event_id: Optional[str] = None
    load_event_detail_id: Optional[str] = None
    discharge_event_detail_id: Optional[str] = None
    deleted: Optional[str] = None


@dataclass(frozen=True)
class CargoFlowsPagedResponse:
    """Paged response for oilx cargoes.

    Attributes:
        next_page_token: String. The key that should be used as a parameter of
            the token to retrieve the next page.
        next_request_token: String. Populated on the last page of incremental
            results and should be used in the next incremental update request.
        data: The structure that contains records retrieve for the current
            page.
    """

    next_page_token: Optional[str] = None
    next_request_token: Optional[str] = None
    data: Optional[Tuple[CargoFlow, ...]] = None
