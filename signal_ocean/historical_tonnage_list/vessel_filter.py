# noqa: D100

from datetime import date
from dataclasses import dataclass, field
from typing import List, Optional, cast

from .vessel_subclass import VesselSubclass
from .._internals import QueryString, format_iso_date


@dataclass(eq=False)
class VesselFilter:
    """Enables vessel filtering in a Historical Tonnage List query.

    All attributes in this class are optional, i.e. no filtering will be
    performed on attributes whose value is None.

    Attributes that accept a list of values are used to perform an *OR*
    comparison. In other words, when a non-empty list of values is used,
    the Historical Tonnage List will contain vessels that match on **any**
    of the specified values. Using an empty list will result in no filtering
    at all.

    VesselFilter is mutable in order to allow making adjustments to
    existing instances if query results are unsatisfactory.

    Attributes:
        push_types: Return vessels with the specified push types.
            Use constants defined in the PushType class for the values of
            this attribute.
        market_deployments: Return vessels with the specified market
            deployment types. Use constants defined in the MarketDeployment
            class for the values of this attribute.
        commercial_statuses: Return vessels with the specified
            commercial statuses. Use constants defined in the CommercialStatus
            class for the values of this attribute.
        vessel_subclass: Return vessels of the specified subclass.
            Use constants defined in the VesselSubclass class for the values
            of this attribute.
        add_willing_to_switch_subclass: When True, returns vessels
            that do not match the subclass but are willing to switch to it.
        latest_ais_since: The maximum age, in days, of the vessel's
            AIS information at the time the tonnage list was captured.
        operational_statuses: Return vessels with the specified
            operational statuses. Use constants defined in the
            OperationalStatus class for the values of this attribute.
        min_liquid_capacity: The minimum liquid capacity, in cubic
            meters, the vessel should be able to hold.
        max_liquid_capacity: The maximum liquid capacity, in cubic
            meters, the vessel should be able to hold.
        fixture_types: Return vessels with the specified
            fixture types. Use constants defined in the FixtureType class for
            the values of this attribute.
        last_cargo_types: Return vessels with the specified last
            cargo type IDs.
        past_port_visits: Return vessels with the specified past
            port visits.
        open_port_ids: Return vessels with the specified open
            port ids.
        canakkale_cancelling: Return vessels with the specified
            Canakkale cancelling date.
        open_date: Return vessels with the specified open date.
        ice_classes: Return vessels with the specified ice classes.
        min_cranes_ton_capacity: Return vessels with the specified
            minimum cranes ton capacity.
        max_cranes_ton_capacity: Return vessels with the specified
            maximum cranes ton capacity.
        min_length_overall: Return vessels with the specified
            minimum length overall.
        max_length_overall: Return vessels with the specified
            maximum length overall.
        min_breadth_extreme: Return vessels with the specified
            minimum breadth extreme.
        max_breadth_extreme: Return vessels with the specified
            maximum breadth extreme.
        openAreas: Return vessels with the specified open area ids.
        openCountries: Return vessels with the specified open
            country ids.
    """

    push_types: Optional[List[str]] = cast(
        List[str], field(default_factory=list)
    )
    market_deployments: Optional[List[str]] = cast(
        List[str], field(default_factory=list)
    )
    commercial_statuses: Optional[List[str]] = cast(
        List[str], field(default_factory=list)
    )
    vessel_subclass: Optional[str] = VesselSubclass.ALL
    add_willing_to_switch_subclass: Optional[bool] = False
    latest_ais_since: Optional[int] = None
    operational_statuses: Optional[List[str]] = cast(
        List[str], field(default_factory=list)
    )
    min_liquid_capacity: Optional[int] = None
    max_liquid_capacity: Optional[int] = None
    fixture_types: Optional[List[str]] = cast(
        List[str], field(default_factory=list)
    )
    past_port_visits: Optional[List[int]] = cast(
        List[int], field(default_factory=list)
    )
    open_port_ids: Optional[List[int]] = cast(
        List[int], field(default_factory=list)
    )
    canakkale_cancelling: Optional[date] = None
    open_date: Optional[date] = None
    ice_classes: Optional[List[str]] = cast(
        List[str], field(default_factory=list)
    )
    min_cranes_ton_capacity: Optional[int] = None
    max_cranes_ton_capacity: Optional[int] = None
    min_length_overall: Optional[int] = None
    max_length_overall: Optional[int] = None
    min_breadth_extreme: Optional[int] = None
    max_breadth_extreme: Optional[int] = None
    open_area_ids: Optional[List[int]] = cast(
        List[int], field(default_factory=list)
    )
    open_country_ids: Optional[List[int]] = cast(
        List[int], field(default_factory=list)
    )

    def _to_query_string(self) -> QueryString:
        return {
            "pushType": self.push_types,
            "commercialStatus": self.commercial_statuses,
            "latestAisSince": self.latest_ais_since,
            "vesselSubclass": self.vessel_subclass,
            "addWillingToSwitchSubclass": self.add_willing_to_switch_subclass,
            "marketDeployment": self.market_deployments,
            "operationalStatus": self.operational_statuses,
            "minLiquidCapacity": self.min_liquid_capacity,
            "maxLiquidCapacity": self.max_liquid_capacity,
            "fixtureType": self.fixture_types,
            "pastPortVisit": self.past_port_visits,
            "openPortId": self.open_port_ids,
            "canakkaleCancelling": format_iso_date(self.canakkale_cancelling),
            "openDate": format_iso_date(self.open_date),
            "iceClass": self.ice_classes,
            "cranesTonCapacityMin": self.min_cranes_ton_capacity,
            "cranesTonCapacityMax": self.max_cranes_ton_capacity,
            "lengthOverallMin": self.min_length_overall,
            "lengthOverallMax": self.max_length_overall,
            "breadthExtremeMin": self.min_breadth_extreme,
            "breadthExtremeMax": self.max_breadth_extreme,
            "openArea": self.open_area_ids,
            "openCountry": self.open_country_ids
        }
