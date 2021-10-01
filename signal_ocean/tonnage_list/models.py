"""Tonnage List API models."""

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional, Sequence, Tuple, Union, overload

import pandas as pd  # type: ignore

from .data_frame import Column, IndexLevel
from .._internals import IterableConstants


class LocationTaxonomy(metaclass=IterableConstants):
    """Contains constants for available location taxonomies."""

    PORT = "Port"
    """
    Location Taxonomy Port.
    """
    COUNTRY = "Country"
    """
    Location Taxonomy Country.
    """
    NARROW_AREA = "Narrow Area"
    """
    Location Taxonomy Narrow Area.
    """
    WIDE_AREA = "Wide Area"
    """
    Location Taxonomy Wide Area.
    """


@dataclass(frozen=True)
class Area:
    """A geographical area.

    Attributes:
        name: The area name.
        location_taxonomy: The area's location taxonomy. See the
            LocationTaxonomy class for available values.
    """

    name: str
    location_taxonomy: str


@dataclass(frozen=True, eq=False)
class Vessel:
    """Holds information for a vessel that participates in a tonnage list.

    Contains both static vessel and point-in-time vessel data.
    All point in time data are annotated with the name _point_in_time
    when converted to data_frame, see column class for details

    Attributes:
        imo: The vessel's IMO number.
        name: The vessel's name.
        vessel_class: The vessel's class name.
        ice_class: The vessel's ice class.
        year_built: The year the vessel has been built.
        deadweight: The vessel's deadweight.
        length_overall: The vessel's length overall.
        breadth_extreme: The vessel's breadth extreme.
        market_deployment: Market deployment of the vessel.
             Point in time property.
             See the MarketDeployment class for available values.
        push_type: Push type of the vessel.
            Point in time property.
            See the PushType class for available values.
        open_port: The vessel's open port name.
            Point in time property.
        open_date: The vessel's open date.
            Point in time property.
        operational_status: Operational status of the vessel.
            Point in time property.
            See the OperationalStatus class for available values.
        commercial_operator: The vessel's commercial operator.
            Point in time property.
        commercial_status: Commercial status of the vessel.
            Point in time property.
            See the CommercialStatus class for available values.
        eta: Estimated time of arrival.
            Point in time property.
        latest_ais: Timestamp of the vessel's latest AIS information.
            Point in time property.
        subclass: The vessel's subclass.
            See the VesselSubclass class for available values.
        willing_to_switch_subclass: Is the vessel willing
            to switch its subclass.
        open_prediction_accuracy: How accurate is the open prediction.
            Point in time property. i.e: if a source is specifying the port
            then prediction is given at port level.
            See the LocationTaxonomy class for available values.
        open_areas: A hierarchical collection of areas the vessel opens
            at used to filtering.
            Point in time property.
            i.e: if a vessel opens in Rotterdam you get as open areas
            "openAreas":[{"id":24758,"label":"Continent","taxonomy":4},
            {"id":25016,"label":"UK Continent","taxonomy":5},
            {"id":25025,"label":"Mediterranean / UK Continent","taxonomy":6},
            {"id":25028,"label":"West","taxonomy":7},
            {"id":173,"label":"Netherlands","taxonomy":3}]
        availability_port_type: If it says source it means that there is
            hard evidence for the specific prediction of Port,
            if it says prediction it means the system is predicting
            based on the algorithm.
            Point in time property.
        availability_date_type: If it says source it means that there is
            hard evidence for
            the specific prediction of the Open date,
            if it says prediction it means the system is
            predicting based on the algorithm.
            Point in time property.
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
        """Returns the vessel's open country name.

        Returns:
            The name of the open country or None if an area with
            LocationTaxonomy.COUNTRY was not present.
        """
        return self.__area_name_by_taxonomy(LocationTaxonomy.COUNTRY)

    @property
    def open_narrow_area(self) -> Optional[str]:
        """Returns the vessel's open narrow area name.

        Returns:
            The name of the open narrow area or None if an area with
            LocationTaxonomy.NARROW_AREA was not present.
        """
        return self.__area_name_by_taxonomy(LocationTaxonomy.NARROW_AREA)

    @property
    def open_wide_area(self) -> Optional[str]:
        """Returns the vessel's open wide area name.

        Returns:
            The name of the open wide area or None if an area with
            LocationTaxonomy.WIDE_AREA was not present.
        """
        return self.__area_name_by_taxonomy(LocationTaxonomy.WIDE_AREA)

    def __area_name_by_taxonomy(self, taxonomy: str) -> Optional[str]:
        for a in self.open_areas:
            if a.location_taxonomy == taxonomy:
                return a.name
        return None


class TonnageList(Sequence[Vessel]):
    """A tonnage list as it occurred at a certain point in time.

    Attributes:
        vessels: Vessels present in the tonnage list at the time it was
            captured. For more details see the :py:class:`Vessel` class.
        date: The date and time at which the tonnage list was captured.
    """

    def __init__(self, vessels: Iterable[Vessel], date: datetime):
        """Initializes the tonnage list.

        Args:
            vessels: Vessels present in the tonnage list at the time it was
                captured. For more details see the :py:class:`Vessel` class.
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
        vessels_by_imo = {v.imo: Column._create_row(v) for v in self.vessels}
        data_frame = pd.DataFrame.from_dict(
            vessels_by_imo, orient="index", columns=list(Column)
        )
        data_frame.index.set_names(IndexLevel.IMO)

        return data_frame.astype(Column._get_data_types())


class HistoricalTonnageList(Sequence[TonnageList]):
    """The class that represents a Historical Tonnage List.

    A Historical Tonnage List consists from an collection of Tonnage Lists
    one for every day between the start and end date specified
    when querying the Historica Tonnage List API.
    """

    def __init__(self, tonnage_lists: Iterable[TonnageList]):
        """Initializes the Historical Tonnage List.

        Args:
            tonnage_lists: Tonnage Lists contained within the Historical
                Tonnage List.
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
                data.append(Column._create_row(vessel))

        data_frame = pd.DataFrame(
            data,
            index=pd.MultiIndex.from_tuples(
                index_tuples, names=[IndexLevel.DATE, IndexLevel.IMO]
            ),
            columns=list(Column),
        )

        return data_frame.astype(Column._get_data_types())


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
