"""Tonnage List API models."""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import (
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
    overload,
)

import pandas as pd  # type: ignore

from .data_frame import Column, DataFrameRow, IndexLevel
from .._internals import (
    IterableConstants,
    QueryString,
    format_iso_date,
    contains_caseless,
)


class LocationTaxonomy(metaclass=IterableConstants):
    """Contains constants for available location taxonomies."""

    PORT = "Port"
    """A port."""

    COUNTRY = "Country"
    """A country."""

    NARROW_AREA = "Narrow Area"
    """A narrow geographical Area."""

    WIDE_AREA = "Wide Area"
    """A wide geographical area."""


@dataclass(frozen=True)
class Area:
    """A geographical area.

    Attributes:
        name: The area's name.
        location_taxonomy: The area's location taxonomy. See the
            `LocationTaxonomy` class for available values.
    """

    name: str
    location_taxonomy: str


@dataclass(frozen=True, eq=False)
class Vessel:
    """Holds information for a vessel that's present in a `TonnageList`.

    Contains both static and point-in-time vessel data. When converted to a
    data frame, all point-in-time data is suffixed with `_point_in_time`. See
    the `Column` class for the available data frame column names.

    Attributes:
        imo: The vessel's IMO number.
        name: The vessel's name.
        vessel_class: Name of the vessel class the vessel is categorized as.
        ice_class: The vessel's ice class.
        year_built: The year the vessel has been built.
        deadweight: The vessel's deadweight.
        length_overall: The vessel's length overall.
        breadth_extreme: The vessel's breadth extreme.
        market_deployment: Market deployment of the vessel at the tonnage
            lists' point in time. See the `MarketDeployment` class for
            available values.
        push_type: Push type of the vessel at the tonnage lists' point in time.
            See the `PushType` class for available values.
        open_port: The vessel's open port name at the tonnage lists' point in
            time.
        open_date: The vessel's open date at the tonnage lists' point in time.
        operational_status: Operational status of the vessel at the tonnage
            lists' point in time. See the `OperationalStatus` class for
            available values.
        commercial_operator: The vessel's commercial operator at the tonnage
            lists' point in time.
        commercial_status: Commercial status of the vessel at the tonnage
            lists' point in time. See the `CommercialStatus` class for
            available values.
        eta: Estimated time of arrival at the tonnage lists' point in time.
        latest_ais: Timestamp of the vessel's latest AIS information at the
            tonnage lists' point in time.
        subclass: The vessel's subclass. See the `VesselSubclass` class for
            available values.
        willing_to_switch_subclass: When `True`, the vessel is willing to
            switch its subclass.
        open_prediction_accuracy: How accurate, in terms of location taxonomy,
            is the vessel's open prediction at the tonnage lists' point in
            time. See the `LocationTaxonomy` class for available values.
        open_areas: A hierarchical collection of areas the vessel opens at at
            the tonnage lists' point in time.

            If a vessel opens at a specific port, this attribute
            will contain areas containing the port. For example, the continent,
            wide/narrow areas, country, etc.
        availability_port_type: Prediction source of the vessel's open port at
            the tonnage lists' point in time. See the `SourceType` class for
            possible values.
        availability_date_type: Prediction source of the vessel's open date at
            the tonnage lists' point in time. See the `SourceType` class for
            possible values.
    """

    imo: int
    name: str
    vessel_class: str
    ice_class: Optional[str]
    year_built: int
    deadweight: int
    length_overall: float
    breadth_extreme: int
    market_deployment: str
    push_type: str
    open_port: str
    open_date: Optional[datetime]
    operational_status: str
    commercial_operator: str
    commercial_status: str
    eta: Optional[datetime]
    latest_ais: Optional[datetime]
    subclass: str
    willing_to_switch_subclass: bool
    open_prediction_accuracy: str
    open_areas: Tuple[Area, ...]
    availability_port_type: str
    availability_date_type: str

    def __post_init__(self) -> None:  # noqa: D105
        if self.open_areas is None:
            object.__setattr__(self, "open_areas", tuple())

    @property
    def open_country(self) -> Optional[str]:
        """The vessel's open country name.

        Returns:
            The name of the open country or `None` if an area with
            `LocationTaxonomy.COUNTRY` was not present.
        """
        return self.__area_name_by_taxonomy(LocationTaxonomy.COUNTRY)

    @property
    def open_narrow_area(self) -> Optional[str]:
        """The vessel's narrow open area name.

        Returns:
            The name of the narrow open area or `None` if an area with
            `LocationTaxonomy.NARROW_AREA` was not present.
        """
        return self.__area_name_by_taxonomy(LocationTaxonomy.NARROW_AREA)

    @property
    def open_wide_area(self) -> Optional[str]:
        """The vessel's wide open area name.

        Returns:
            The name of the wide open area or `None` if an area with
            `LocationTaxonomy.WIDE_AREA` was not present.
        """
        return self.__area_name_by_taxonomy(LocationTaxonomy.WIDE_AREA)

    def __area_name_by_taxonomy(self, taxonomy: str) -> Optional[str]:
        for a in self.open_areas:
            if a.location_taxonomy == taxonomy:
                return a.name
        return None

    def _to_data_frame_row(self) -> DataFrameRow:
        return Column._create_row(
            name=self.name,
            vessel_class=self.vessel_class,
            ice_class=self.ice_class,
            year_built=self.year_built,
            deadweight=self.deadweight,
            length_overall=self.length_overall,
            breadth_extreme=self.breadth_extreme,
            subclass=self.subclass,
            market_deployment=self.market_deployment,
            push_type=self.push_type,
            open_port=self.open_port,
            open_date=self.open_date,
            operational_status=self.operational_status,
            commercial_operator=self.commercial_operator,
            commercial_status=self.commercial_status,
            eta=self.eta,
            latest_ais=self.latest_ais,
            open_prediction_accuracy=self.open_prediction_accuracy,
            open_country=self.open_country,
            open_narrow_area=self.open_narrow_area,
            open_wide_area=self.open_wide_area,
            availability_port_type=self.availability_port_type,
            availability_date_type=self.availability_date_type,
        )


class OperationalStatus(metaclass=IterableConstants):
    """Contains constants for available operational statuses."""

    BALLAST_FIXED = "Ballast Fixed"
    """The vessel is currently without cargo but fixed."""

    REPAIRS = "Repairs"
    """The vessel is undergoing repairs or is in dry dock."""

    WAITING_TO_LOAD = "Waiting to Load"
    """The vessel is waiting to load."""

    LOADING = "Loading"
    """The vessel is loading.

    This means the vessel has entered a jetty or is performing a ship-to-ship
    operation."""

    LADEN = "Laden"
    """The vesel has loaded."""

    WAITING_TO_DISCHARGE = "Waiting to Discharge"
    """The vessel is waiting to Discharge."""

    DISCHARGING = "Discharging"
    """The vessel is discharging.

    This means the vessel has entered a jetty or is performing a ship-to-ship
    operation."""

    ACTIVE_STORAGE = "Active Storage"
    """The vessel is in active storage.

    This means the vessel acts as short-term storage (in comparison to storage
    vessels).
    """

    BALLAST_UNFIXED = "Ballast Unfixed"
    """The vessel is currently without cargo and is not fixed (is prompt)."""

    BALLAST_FIXED_IMPLIED = "Ballast Fixed (implied)"
    """The vessel is currently without cargo and its AIS destination implies
    that it's fixed."""


class CommercialStatus(metaclass=IterableConstants):
    """Contains constants for available commercial statuses."""

    ON_SUBS = "On Subs"
    """The vessel is "on subs" for a new fixture."""

    FAILED = "Failed"
    """The last fixture failed for this vessel."""

    CANCELLED = "Cancelled"
    """The last fixture has been cancelled for this vessel."""

    AVAILABLE = "Available"
    """The vessel is available for a new voyage after its open date."""

    POTENTIALLY_FIXED = "Poss Fixed"
    """The vessel is assumed to be fixed for a new voyage based on available
    AIS information.
    """


class SourceType(metaclass=IterableConstants):
    """Contains constants for available prediction source types."""

    SOURCE = "Source"
    """There is hard evidence backing the given prediction."""

    PREDICTION = "Prediction"
    """The prediction was made based on an algorithm."""


@dataclass(frozen=True, eq=False)
class Port:
    """A maritime facility where vessels can dock.

    Attributes:
        id: The ID of the port.
        name: The name of the port.
    """

    id: int
    name: str


@dataclass(frozen=True, eq=False)
class VesselClass:
    """A group of vessels of similar characteristics, i.e. Aframax, Panamax, etc.

    Attributes:
        id: The vessel class ID.
        name: The vessel class name.
    """

    id: int
    name: str


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
    """Vessels controlled by commercial operators that participate in the spot
    market and are advertised through tonnage lists and reported fixtures.
    """

    PROGRAM = "Program"
    """Vessels that are controlled by charterers that do not participate in the
    spot market and are either not advertised through tonnage lists or tonnage
    lists report the fact that they participate in the program market.
    """

    RELET = "Relet"
    """Vessels controlled by charterers that participate in the spot market and
    are advertised through tonnage lists and reported fixtures.
    """

    CONTRACT = "Contract"
    """Vessels controlled by commercial operators that do not participate in
    the spot market and are typically carrying system cargoes with repetitive
    trading patterns.
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
            defined in the `PushType` class as values of this
            attribute.
        market_deployments: Return vessels with the specified market deployment
            types. Use constants defined in the `MarketDeployment`
            class as values of this attribute.
        commercial_statuses: Return vessels with the specified
            commercial statuses. Use constants defined in the
            `CommercialStatus` class for the values of this attribute.
        vessel_subclass: Return vessels of the specified subclass.
            Use constants defined in the `VesselSubclass` class for the values
            of this attribute.
        add_willing_to_switch_subclass: When True, returns vessels
            that do not match the subclass but are willing to switch to it.
        latest_ais_since: The maximum age, in days, of the vessel's
            AIS information at the time the tonnage list was captured.
        operational_statuses: Return vessels with the specified
            operational statuses. Use constants defined in the
            `OperationalStatus` class for the values of this attribute.
        min_liquid_capacity: The minimum liquid capacity, in cubic
            meters, the vessel should be able to hold.
        max_liquid_capacity: The maximum liquid capacity, in cubic
            meters, the vessel should be able to hold.
        fixture_types: Return vessels with the specified
            fixture types. Use constants defined in the `FixtureType` class for
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


class FixtureType(metaclass=IterableConstants):
    """Contains constants for available fixture types."""

    SCRAPED = "Scraped"
    """The fixture was scraped from an email."""

    MANUAL = "Manual"
    """The fixture was added manually."""

    IMPLIED = "Implied"
    """The fixture is implied by the vessel's AIS destination."""


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


class TonnageList(Sequence[Vessel]):
    """A tonnage list as it occurred at a certain point in time.

    Attributes:
        vessels: Vessels present in the tonnage list at the time it was
            captured. For more details see the `Vessel` class.
        date: The date and time at which the tonnage list was captured.
    """

    def __init__(self, vessels: Iterable[Vessel], date: datetime):
        """Initializes the tonnage list.

        Args:
            vessels: Vessels present in the tonnage list at the time it was
                captured. For more details see the `Vessel` class.
            date: The date and time at which the tonnage list was captured.
        """
        self.vessels = tuple(vessels)
        self.date = date

    @overload
    def __getitem__(self, index: int) -> Vessel:  # noqa: D105
        ...

    @overload
    def __getitem__(self, slice: slice) -> Sequence[Vessel]:  # noqa: D105
        ...

    def __getitem__(
        self, i: Union[int, slice]
    ) -> Union[Vessel, Sequence[Vessel]]:  # noqa: D105
        return self.vessels.__getitem__(i)

    def __len__(self) -> int:  # noqa: D105
        return self.vessels.__len__()

    def __repr__(self) -> str:  # noqa: D105
        class_name = self.__class__.__name__
        return f"{class_name}(vessels={self.vessels!r})"

    def to_data_frame(self) -> pd.DataFrame:
        """Converts the tonnage list to a pandas data frame."""
        vessels_by_imo = {v.imo: v._to_data_frame_row() for v in self.vessels}
        data_frame = pd.DataFrame.from_dict(
            vessels_by_imo, orient="index", columns=list(Column)
        )
        data_frame.index.set_names(IndexLevel.IMO)

        return data_frame.astype(Column._get_data_types())


class HistoricalTonnageList(Sequence[TonnageList]):
    """A historical tonnage list.

    A historical tonnage list consists of a collection of tonnage lists, one
    for every day between the start and end date specified when querying the
    Historical Tonnage List API.
    """

    def __init__(self, tonnage_lists: Iterable[TonnageList]):
        """Initializes the `HistoricalTonnageList`.

        Args:
            tonnage_lists: Tonnage lists per each day in the historical date
                range.
        """
        self.tonnage_lists = tuple(tonnage_lists)

    @overload
    def __getitem__(self, index: int) -> TonnageList:  # noqa: D105
        ...

    @overload
    def __getitem__(self, slice: slice) -> Sequence[TonnageList]:  # noqa: D105
        ...

    def __getitem__(
        self, i: Union[int, slice]
    ) -> Union[TonnageList, Sequence[TonnageList]]:  # noqa: D105
        return self.tonnage_lists.__getitem__(i)

    def __len__(self) -> int:  # noqa: D105
        return self.tonnage_lists.__len__()

    def __repr__(self) -> str:  # noqa: D105
        class_name = self.__class__.__name__
        return f"{class_name}(tonnage_lists={self.tonnage_lists!r})"

    def to_data_frame(self) -> pd.DataFrame:
        """Converts the Historical Tonnage List to a pandas data frame."""
        index_tuples = []
        data = []
        for tonnage_list in self.tonnage_lists:
            for vessel in tonnage_list.vessels:
                index_tuples.append((tonnage_list.date, vessel.imo))
                data.append(vessel._to_data_frame_row())

        data_frame = pd.DataFrame(
            data,
            index=pd.MultiIndex.from_tuples(
                index_tuples, names=[IndexLevel.DATE, IndexLevel.IMO]
            ),
            columns=list(Column),
        )

        return data_frame.astype(Column._get_data_types())
