# noqa: D100

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

from .area import Area
from .location_taxonomy import LocationTaxonomy


@dataclass(frozen=True, eq=False)
class Vessel:
    """Represents a vessel in a historical tonnage list.

    Contains both static and point-in-time vessel data.

    Attributes:
        imo: The vessel's IMO number.
        name: The vessel's name.
        vessel_class: The vessel's class name.
        ice_class: The vessel's ice class.
        year_built: The year the vessel has been built.
        deadweight: The vessel's deadweight.
        length_overall: The vessel's length overall.
        breadth_extreme: The vessel's breadth extreme.
        market_deployment: Market deployment of the vessel. See the
            MarketDeployment class for available values.
        push_type: Push type of the vessel. See the PushType class for
            available values.
        open_port: The vessel's open port name.
        open_date: The vessel's open date.
        operational_status: Operational status of the vessel. See the
            OperationalStatus class for available values.
        commercial_operator: The vessel's commercial operator.
        commercial_status: Commercial status of the vessel. See the
            CommercialStatus class for available values.
        eta: Estimated time of arrival.
        latest_ais: Timestamp of the vessel's latest AIS information.
        subclass: The vessel's subclass. See the VesselSubclass class for
            available values.
        willing_to_switch_subclass: Is the vessel willing to switch its
            subclass.
        open_prediction_accuracy: How accurate is the open prediction.
            See the LocationTaxonomy class for available values.
        open_areas: A hierarchical collection of areas the vessel opens at.
        availability_port_type: Availability port type.
        availability_date_type: Availability date type.
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
