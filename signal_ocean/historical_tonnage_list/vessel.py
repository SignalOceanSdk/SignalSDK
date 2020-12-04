# noqa: D100

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

from .area import Area
from .location_taxonomy import LocationTaxonomy


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
