"""Tonnage List API."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Iterable, List, Optional, Tuple, cast

from .. import Connection
from .models import HistoricalTonnageList, Port, TonnageList, VesselClass
from . import _json
from .._internals import (
    QueryString,
    IterableConstants,
    format_iso_date,
    contains_caseless,
)


class VesselSubclass(metaclass=IterableConstants):
    """Available vessel subclasses."""

    ALL = None
    """All vessel subclasses.

    Refers to all vessels without any classification regarding the cargo type
    they car carry.
    """

    DIRTY = "Dirty"
    """Vessels carrying dirty types of oil.

    Refers to all vessels that classify as carriers of dirty types of oil.
    Applies only to tankers.
    """

    CLEAN = "Clean"
    """Vessels carrying clean oil.

    Refers to all vessels that classify as carriers of clean types of oil.
    Applies only to tankers.
    """


class PushType(metaclass=IterableConstants):
    """Available push types."""

    NOT_PUSHED = "Not Pushed"
    """Vessels that are not pushed anymore."""

    PUSHED_POSS = "Pushed POSS"
    """Vessels actively pushed in the market with notification "Poss".

    "Poss" stands for "Possibly", meaning that vessels marked with this type
    are a broker projection.
    """

    PUSHED = "Pushed"
    """Vessels actively pushed in the market through tonnage or position lists.
    """


class MarketDeployment(metaclass=IterableConstants):
    """Available market deployments."""

    SPOT = "Spot"
    """Vessels participating in the spot market.

    Vessels controlled by commercial operators that participate in the spot
    market and are advertised through tonnage lists and reported fixtures.
    """

    PROGRAM = "Program"
    """Vessels controlled by charterers that do not participate in the spot
    market and are either not advertised through tonnage lists or tonnage lists
    report the fact that they are program
    """

    RELET = "Relet"
    """
    Vessels controlled by charterers that participate in the spot market
    and are advertised through Tonnage lists and get reported fixtures
    """

    CONTRACT = "Contract"
    """
    Vessels controlled by commercial operators that do not participate
    in the spot market and are typically
    doing system cargoes with repetitive trading patterns.
    """


@dataclass(eq=False)
class VesselFilter:
    """Used to filter vessels when retrieving tonnage lists.

    All attributes in this class are optional, i.e. no filtering will be
    performed on attributes whose value is None.

    Attributes that accept a list of values are used to perform an *OR*
    comparison. In other words, when a non-empty list of values is used, the
    tonnage lists will contain vessels that match on **any** of the specified
    values. Using an empty list will result in no filtering being performed.

    `VesselFilter` is mutable in order to allow making adjustments to existing
    instances if query results are unsatisfactory.

    Attributes:
        push_types: Return vessels with the specified push types. Use constants
            defined in the :py:class:`PushType` class as values of this
            attribute.
        market_deployments: Return vessels with the specified market deployment
            types. Use constants defined in the :py:class:`MarketDeployment`
            class as values of this attribute.
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
            "openCountry": self.open_country_ids,
        }


class DateRange:
    """A range of dates between a start and end date."""

    def __init__(self, start: Optional[date], end: Optional[date]):
        """Creates the date range.

        Args:
            start: The start date of the range (inclusive).
            end: The end date of the range (inclusive).
        """
        if start is not None and end is not None and end < start:
            raise ValueError("Start date cannot be after end date.")

        self.start = start
        self.end = end

    def _split(self, max_days: int) -> Iterable["DateRange"]:
        if max_days < 1:
            raise ValueError(
                f"Date range cannot be split into chunks of {max_days} days."
            )

        max_size = timedelta(days=max_days - 1)
        current_start = self.start

        if current_start is not None and self.end is not None:
            while self.end - current_start > max_size:
                current_end = current_start + max_size
                yield DateRange(current_start, current_end)
                current_start = current_end + timedelta(days=1)

        yield DateRange(current_start, self.end)

    def _to_query_string(self) -> QueryString:
        return {
            "startDate": format_iso_date(self.start),
            "endDate": format_iso_date(self.end),
        }


@dataclass(eq=False)
class PortFilter:
    """A filter used to find specific ports.

    Attributes:
        name_like: Used to find ports by name. When specified, ports whose
            names partially match (contain) the attribute's value will be
            returned. Matching is case-insensitive.
    """

    name_like: Optional[str] = None

    def _apply(self, ports: Iterable[Port]) -> Iterable[Port]:
        return filter(self.__does_port_match, ports)

    def __does_port_match(self, port: Port) -> bool:
        return not self.name_like or contains_caseless(
            self.name_like, port.name
        )


@dataclass(eq=False)
class VesselClassFilter:
    """A filter used to find specific vessel classes.

    Attributes:
        name_like: Used to find vessel classes by name. When specified, vessel
            classes whose names partially match (contain) the attribute's value
            will be returned. Matching is case-insensitive.
    """

    name_like: Optional[str] = None

    def _apply(
        self, vessel_classes: Iterable[VesselClass]
    ) -> Iterable[VesselClass]:
        return filter(self.__does_class_match, vessel_classes)

    def __does_class_match(self, vessel_class: VesselClass) -> bool:
        return not self.name_like or contains_caseless(
            self.name_like, vessel_class.name
        )


class TonnageListAPI:
    """Handles communication with Signal's Tonnage List API."""

    __MAX_DATE_RANGE_DAYS = 365

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes TonnageListAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_tonnage_list(
        self,
        loading_port: Port,
        vessel_class: VesselClass,
        laycan_end_in_days: Optional[int] = None,
        vessel_filter: Optional[VesselFilter] = None,
    ) -> TonnageList:
        """Retrieves a tonnage list.

        Args:
            loading_port: The loading port from which ETA will be calculated.
            vessel_class: Vessel class of vessels in the tonnage list.
            laycan_end_in_days: The maximum ETA expressed as a number of days
                from now.
            vessel_filter: A filter defining which vessels should be included
                in the response. See the VesselFilter class for more details.

        Returns:
            Returns a tonnage list containing vessels that match the specified
            criteria.
        """
        query_string: QueryString = {
            "loadingPort": loading_port.id,
            "vesselClass": vessel_class.id,
            "laycanEndInDays": laycan_end_in_days,
            **(vessel_filter._to_query_string() if vessel_filter else {}),
        }

        response = self.__connection._make_get_request(
            "htl-api/tonnage-list/", query_string
        )

        response.raise_for_status()
        return _json.parse_tonnage_list_response(response.json())

    def get_historical_tonnage_list(
        self,
        loading_port: Port,
        vessel_class: VesselClass,
        laycan_end_in_days: Optional[int] = None,
        date_range: Optional[DateRange] = None,
        vessel_filter: Optional[VesselFilter] = None,
    ) -> HistoricalTonnageList:
        """Retrieves a Historical Tonnage List.

        If no input dates are provided, the last 10 days will be fetched
        (including today).

        To get a tonnage list for a specific day, set both date parameters to
        the desired date.

        Args:
            loading_port: The loading port from which ETA will be calculated.
            vessel_class: The vessel class to calculate the tonnage lists.
            laycan_end_in_days: The maximum ETA expressed as a number of days
                after the end date.
            start_date: The date of the earliest tonnage list in the response.
            end_date: The date of the latest tonnage list in the response.
            time: Specifies the UTC time of day for which the state of
                the tonnage lists will be retrieved.
                It can get the values 00, 06, 12, 18.
            vessel_filter: A filter defining which vessels should be included
                in the response see Vessel Filter class for more details.

        Returns:
            Given a time-range, returns a Historical Tonnage List containing a
            Tonnage List for every day between the start and end dates, at the
            requested time of day.
        """
        date_ranges = (date_range or DateRange(start=None, end=None))._split(
            TonnageListAPI.__MAX_DATE_RANGE_DAYS
        )

        tonnage_lists = (
            tonnage_list
            for dr in date_ranges
            for tonnage_list in self._get_htl_chunk(
                loading_port,
                vessel_class,
                dr,
                laycan_end_in_days,
                vessel_filter,
            )
        )

        return HistoricalTonnageList(tonnage_lists)

    def _get_htl_chunk(
        self,
        loading_port: Port,
        vessel_class: VesselClass,
        date_range: DateRange,
        laycan_end_in_days: Optional[int] = None,
        vessel_filter: Optional[VesselFilter] = None,
    ) -> HistoricalTonnageList:
        query_string: QueryString = {
            "loadingPort": loading_port.id,
            "vesselClass": vessel_class.id,
            "laycanEndInDays": laycan_end_in_days,
            **date_range._to_query_string(),
            **(vessel_filter._to_query_string() if vessel_filter else {}),
        }

        response = self.__connection._make_get_request(
            "htl-api/historical-tonnage-list/", query_string
        )

        response.raise_for_status()
        return _json.parse_historical_tonnage_list_response(response.json())

    def get_ports(
        self, port_filter: Optional[PortFilter] = None
    ) -> Tuple[Port, ...]:
        """Retrieves available ports.

        Args:
            port_filter: A filter used to find specific ports. If not
            specified, returns all available ports.

        Returns:
            A tuple of available ports that match the filter.
        """
        response = self.__connection._make_get_request(
            "htl-api/historical-tonnage-list/ports"
        )
        response.raise_for_status()

        ports = (Port(**p) for p in response.json())
        port_filter = port_filter or PortFilter()

        return tuple(port_filter._apply(ports))

    def get_vessel_classes(
        self, class_filter: Optional[VesselClassFilter] = None
    ) -> Tuple[VesselClass, ...]:
        """Retrieves available vessel classes.

        Args:
            class_filter: A filter used to find specific vessel classes. If not
                specified, returns all available vessel classes.

        Returns:
            A tuple of available vessel classes that match the filter.
        """
        response = self.__connection._make_get_request(
            "htl-api/historical-tonnage-list/vessel-classes"
        )
        response.raise_for_status()

        classes = (VesselClass(**c) for c in response.json())
        class_filter = class_filter or VesselClassFilter()

        return tuple(class_filter._apply(classes))
