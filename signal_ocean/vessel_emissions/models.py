"""The models for vessel emissions api."""
import dataclasses
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from operator import attrgetter


def _to_camel_case_with_special_keywords(s: str) -> str:
    special_keywords = [
        'imo', 'id', 'co', 'co2', 'ch', 'nmvoc',
    ]
    _to_camelcase = s.split('_')
    _to_camelcase = [
        word.capitalize() if word not in special_keywords
        else word.upper()
        for word in _to_camelcase
    ]
    result = ''.join(_to_camelcase)
    if 'Tons' in result:
        result = (
            result.replace('in', 'In').
            replace('Nmvoc', 'NMVOC').
            replace('Sox', 'SOx').
            replace('Nox', 'NOx').
            replace('Co', 'CO')
        )
    return result


@dataclass(frozen=True)
class Emissions:
    """Contains the reported emissions per gas type.

    Attributes:
    co2_in_tons: CO2 emissions in tons
    coin_tons: CO emissions in tons
    ch4_in_tons: CH4 emissions in tons
    n2_oin_tons: N20 emissions in tons
    nmvocin_tons: NMVOC emissions in tons
    nox_in_tons: NOX emissions in tons
    sox_in_tons: SOX emissions in tons
    pmin_tons: PM emissions in tons

    """
    co2_in_tons: Optional[float] = None
    coin_tons: Optional[float] = None
    ch4_in_tons: Optional[float] = None
    n2_oin_tons: Optional[float] = None
    nmvocin_tons: Optional[float] = None
    nox_in_tons: Optional[float] = None
    sox_in_tons: Optional[float] = None
    pmin_tons: Optional[float] = None


@dataclass(frozen=True)
class EmissionsBreakdown:
    """Contains emissions breakdown for different parts of the Voyage.

    Attributes:
        voyage: Vessel Emissions for the voyage
        ballast: Vessel Emissions for the ballast part of the voyage
        laden: Vessel Emissions for the laden part of the voyage
        port_call: Vessel Emissions for the port calls of the voyage
        stop: Vessel Emissions for the stops of the voyage
    """
    voyage: Emissions
    ballast: Optional[Emissions] = None
    laden: Optional[Emissions] = None
    port_call: Optional[Emissions] = None
    stop: Optional[Emissions] = None


@dataclass(frozen=True)
class Consumptions:
    """Contains the reported consumptions per gas type.

    Attributes:
    hfo_in_tons: HFO vessel consumption in tons
    lfo_in_tons: LFO vessel consumption in tons
    mgo_in_tons: MGO vessel consumption in tons
    lng_in_tons: LNG vessel consumption in tons
    lpg_propane_in_tons: LPG Propane vessel consumption in tons
    lpg_butane_in_tons: LPG Butane vessel consumption in tons
    total_in_tons: Total vessel consumption in tons

    """
    total_in_tons: float
    hfoin_tons: Optional[float] = None
    lfoin_tons: Optional[float] = None
    mgoin_tons: Optional[float] = None
    lngin_tons: Optional[float] = None
    lpgpropane_in_tons: Optional[float] = None
    lpgbutane_in_tons: Optional[float] = None


@dataclass(frozen=True)
class ConsumptionsBreakdown:
    """Contains consumptions breakdown for different parts of the Voyage.

    Attributes:
        voyage: Vessel Consumptions for the voyage
        ballast: Vessel Consumptions for the ballast part of the voyage
        laden: Vessel Consumptions for the laden part of the voyage
        port_call: Vessel Consumptions for the port calls of the voyage
        stop: Vessel Consumptions for the stops of the voyage
    """
    voyage: Consumptions
    ballast: Optional[Consumptions] = None
    laden: Optional[Consumptions] = None
    port_call: Optional[Consumptions] = None
    stop: Optional[Consumptions] = None


@dataclass(frozen=True)
class Duration:
    """Contains voyage duration information.

    Attributes:
        in_hours: Duration in Hours
        in_days: Duration in Days
    """
    in_hours: float
    in_days: float


@dataclass(frozen=True)
class DurationBreakdown:
    """Contains duration breakdown for the different parts of the voyage.

    Attributes:
        voyage: Duration of the voyage
        ballast: Duration of the ballast part of the voyage
        laden: Duration of the laden part of the voyage
        port_call: Duration of the port calls of the voyage
        stop: Duration of the stops of the voyage
    """
    voyage: Duration
    ballast: Optional[Duration] = None
    laden: Optional[Duration] = None
    port_call: Optional[Duration] = None
    stop: Optional[Duration] = None


@dataclass(frozen=True)
class Distance:
    """Contains Distance Info.

    Attributes:
        distance_travelled: Distance Travelled in NM

    """
    distance_travelled: float


@dataclass(frozen=True)
class DistancesBreakdown:
    """Contains Distance Info for different parts of the Voyage.

    Attributes:
        voyage: Distance Travelled for the voyage
        ballast: Distance Travelled for the ballast part of the voyage
        laden: Distance Travelled for the laden part of the voyage

    """
    voyage: Distance
    ballast: Distance
    laden: Distance


@dataclass(frozen=True)
class Metrics:
    """Vessel Metrics estimation.

    Attributes:
        voyage_cii: Carbon Intensity Indicator
        (VoyageCII)
        efficiency metrics for the voyage
        voyage_cii_unit: The unit of the voyage
        Carbon Intensity Indicator (VoyageCII)
        voyage_cii_rating: The rating of the vessel
        based on the VoyageCII
        voyage_cii_target: The alignment target for the
        Voyage CII efficiency metric of the current year
        voyage_cii_target_year: The year that has taken
        into account for calculating the alignment target
        for the VoyageCII efficiency metric
        capacity_eeoi: The EEOI efficiency metric when
        the quantity equals with the capacity of
        the vessel (CapacityEEOI)
        e.g. the deadweight of the vessel
        capacity_eeoi_unit: The unit of the Capacity
        EEOI efficiency metric
        capacity_eeoi_sea_cargo_charter_year_target:
        The alignment target for the Capacity EEOI
        efficiency metric based on the Sea Cargo
        Charter guidelines for the year of the voyage
        capacity_eeoi_sea_cargo_charter_class:
        The Sea Cargo Charter defined class
        that the vessel belongs to based on it's size
        capacity_eeoi_sea_cargo_charter_alignment_in_percentage:
        The alignment delta in percentage, based on the acquired
        Capacity EEOI and the given alignment target
        from Sea Cargo Charter. Negative is aligned,
        positive is misaligned
        eeoi: The EEOI efficiency metrics calculated for the voyage
        eeoi_unit: The unit of the EEOI efficiency metrics
        eeoi_sea_cargo_charter_year_target: The alignment
        target for the EEOI efficiency metric based on the Sea Cargo
        Charter guidelines for the year of the voyage
        eeoi_sea_cargo_charter_class: The Sea Cargo Charter
        defined class that the vessel belongs to based on it's size
        eeoi_sea_cargo_charter_alignment_in_percentage:
        The alignment delta in percentage, based on the acquired
        EOI and the given alignment target from Sea Cargo Charter.
        Negative is aligned, positive is misaligned.
        kg_co2_per_tonne_cargo: Kg of CO2 per tonne of cargo carried
        kg_co2_per_tonne_dwt: Kg of CO2 per tonne of the vessel's deadweight


    """
    voyage_cii: Optional[float] = None
    voyage_cii_unit: Optional[str] = None
    voyage_cii_rating: Optional[str] = None
    voyage_cii_target: Optional[float] = None
    voyage_cii_target_year: Optional[int] = None
    capacity_eeoi: Optional[float] = None
    capacity_eeoi_unit: Optional[str] = None
    capacity_eeoi_sea_cargo_charter_year_target: \
        Optional[float] = None
    capacity_eeoi_sea_cargo_charter_class: Optional[str] = None
    capacity_eeoi_sea_cargo_charter_alignment_in_percentage: \
        Optional[float] = None
    eeoi: Optional[float] = None
    eeoi_unit: Optional[str] = None
    eeoi_sea_cargo_charter_year_target: Optional[float] = None
    eeoi_sea_cargo_charter_class: Optional[str] = None
    eeoi_sea_cargo_charter_alignment_in_percentage: \
        Optional[float] = None
    kg_co2_per_tonne_cargo: Optional[float] = None
    kg_co2_per_tonne_dwt: Optional[float] = None


@dataclass(frozen=True)
class SeagoingSpeedStatistics:
    """Contains speed statistics.

    Attributes:
        average_speed_in_knots: Average seagoing speed in knots
        std_speed_in_knots: Standard deviation speed in knots
        min_speed_in_knots: Minimum seagoing speed in knots
        max_speed_in_knots: Maximum seagoing speed in knots

    """
    average_speed_in_knots: Optional[float] = None
    std_speed_in_knots: Optional[float] = None
    min_speed_in_knots: Optional[float] = None
    max_speed_in_knots: Optional[float] = None


@dataclass(frozen=True)
class SeagoingSpeedStatisticsBreakdown:
    """Contains speed statistics for different parts of the Voyage.

    Attributes:
        voyage: Speed statistics for the voyage"
        laden: Speed statistics for the ballast part of the voyage
        ballast: Speed statistics for the laden part of the voyage

    """
    voyage: Optional[SeagoingSpeedStatistics] = None
    laden: Optional[SeagoingSpeedStatistics] = None
    ballast: Optional[SeagoingSpeedStatistics] = None


@dataclass(frozen=True)
class EmissionsEssentialStatistics:
    """Contains Emissions essential statistics.

    Attributes:
        emissions: Voyage emissions info
        consumptions: Voyage consumptions info
        distances: Voyage distances info
        duration: Voyage duration info

    """
    emissions: Optional[EmissionsBreakdown] = None
    consumptions: Optional[ConsumptionsBreakdown] = None
    distances: Optional[DistancesBreakdown] = None
    duration: Optional[DurationBreakdown] = None


@dataclass(frozen=True)
class EmissionsEstimation:
    """Contains info about the emissions estimation.

    Attributes:
        id: Voyage ID
        imo: Vessel IMO
        vessel_name: Vessel Name
        voyage_number: Voyage Number
        vessel_type_id: Vessel type id
        vessel_type: Vessel type
        vessel_class_id: Vessel class id
        vessel_class: Vessel class
        start_date: Start date of the Voyage
        end_date: End date of the Voyage
        quantity: Cargo quantity of the voyage
        deadweight: Vessel's deadweight
        transport_work_in_million_tonne_miles: Transport
        work measured in millions tonnes of cargo carried
        times the travelled distance in miles of the current voyage
        transport_work_in_million_dwt_miles: Transport work
        measured in millions tonnes when the cargo
        curried equals the DWT times the travelled
        distance in miles of the current voyage
        contains_eu_emissions: Declares whether
        voyage has European Union Related Emissions
        emissions: Emissions breakdown for the voyage
        consumptions: Consumptions breakdown for the voyage
        seagoing_speed_statistics: Seagoing
        Speed Statistics breakdown for the voyage
        duration: Duration breakdown for the voyage
        distances: Distance travelled breakdown for the voyage
        efficiency_metrics: Emissions Efficiency metrics for the voyage
        european_union_regulated: European Union Related Emissions

    """
    id: str
    imo: int
    vessel_name: str
    voyage_number: int
    vessel_type_id: int
    vessel_class_id: int
    start_date: str
    end_date: str
    deadweight: int
    emissions: EmissionsBreakdown
    vessel_type: Optional[str] = None
    vessel_class: Optional[str] = None
    quantity: Optional[float] = None
    transport_work_in_million_tonne_miles: Optional[float] = None
    transport_work_in_million_dwt_miles: Optional[float] = None
    contains_eu_emissions: Optional[bool] = None
    consumptions: Optional[ConsumptionsBreakdown] = None
    seagoing_speed_statistics: \
        Optional[SeagoingSpeedStatisticsBreakdown] = None
    duration: Optional[DurationBreakdown] = None
    distances: Optional[DistancesBreakdown] = None
    efficiency_metrics: Optional[Metrics] = None
    european_union_regulated: Optional[EmissionsEssentialStatistics] = None

    def __repr__(self) -> str:
        """Override of the default __repr__ function.

        Returns:
            Object string representation omitting None attributes

        """
        nodef_f_vals = (
            (f.name, attrgetter(f.name)(self))
            for f in dataclasses.fields(self)
            if attrgetter(f.name)(self) != f.default
        )

        nodef_f_repr = ", ".join(f"{name}={value}"
                                 for name, value
                                 in nodef_f_vals)
        return f"{self.__class__.__name__}({nodef_f_repr})"

    def to_dict(self) -> Dict[Any, Any]:
        """Cast EmissionsEstimation object to dict.

        Returns:
            Dict representation of EmissionsEstimation model

        """
        return dataclasses.asdict(
            self,
            dict_factory=lambda x: {
                _to_camel_case_with_special_keywords(k): v
                for (k, v) in x if v is not None
            })


@dataclass(frozen=True)
class Eexi:
    """Contains EEXI info.

    Attributes:
        value: Acquired EEXI value
        unit: EEXI unit
        required: EEXI required value based on IMO guidelines

    """
    value: Optional[float] = None
    unit: Optional[str] = None
    required: Optional[float] = None


@dataclass(frozen=True)
class Eiv:
    """Contains EIV info.

    Attributes:
        value: Acquired EIV value
        unit: EIV unit

    """
    value: Optional[float] = None
    unit: Optional[str] = None


@dataclass(frozen=True)
class Aer:
    """Contains AER info.

    Attributes:
        value: Annual metric value
        unit: Annual metric unit
        poseidon_principles_class: Poseidon Principles
        defined class based on the vessel's size
        poseidon_principles_alignment_in_percentage: The
        alignment delta in percentage, based on the acquired AER
        and the given alignment target from Poseidon Principles.
        Negative is aligned, positive is misaligned.
        poseidon_principles_year_target: The alignment target for
        the AER efficiency metric based on the Poseidon
        Principles guidelines for the year of the voyage

    """
    value: Optional[float] = None
    unit: Optional[str] = None
    poseidon_principles_class: Optional[str] = None
    poseidon_principles_alignment_in_percentage: Optional[float] = None
    poseidon_principles_year_target: Optional[float] = None


@dataclass(frozen=True)
class Cii:
    """Contains CII info.

    Attributes:
        value: Acquired CII value
        unit: CII unit
        rating: CII rating based on IMO guidelines
        target: CII target based on IMO guidelines
        target_year: The year of the CII target based on IMO guidelines

    """
    value: Optional[float] = None
    unit: Optional[str] = None
    rating: Optional[str] = None
    target: Optional[float] = None
    target_year: Optional[int] = None


@dataclass(frozen=True)
class VesselMetrics:
    """Contains Vessel emissions Metrics.

    Attributes:
        imo: Vessel IMO
        year: The year referenced for the calculated annual metrics
        vessel_type: The vessel type characterization of the vessel
        vessel_type_id: Vessel type ID
        vessel_class: The vessel class characterization of the vessel
        vessel_class_id: Vessel class ID
        eexi: EEXI Metrics
        eiv: EIV Metrics
        aer: AER Metrics
        cii: CII Metrics

    """
    imo: int
    year: Optional[int] = None
    vessel_type: Optional[str] = None
    vessel_type_id: Optional[int] = None
    vessel_class: Optional[str] = None
    vessel_class_id: Optional[int] = None
    eexi: Optional[Eexi] = None
    eiv: Optional[Eiv] = None
    aer: Optional[Aer] = None
    cii: Optional[Cii] = None

    def __repr__(self) -> str:
        """Override of the default __repr__ function.

        Returns:
            Object string representation omitting None attributes

        """
        nodef_f_vals = (
            (f.name, attrgetter(f.name)(self))
            for f in dataclasses.fields(self)
            if attrgetter(f.name)(self) != f.default
        )

        nodef_f_repr = ", ".join(f"{name}={value}"
                                 for name, value
                                 in nodef_f_vals)
        return f"{self.__class__.__name__}({nodef_f_repr})"

    def to_dict(self) -> Dict[Any, Any]:
        """Cast VesselMetrics object to dict.

        Returns:
            Dict representation of VesselMetrics object

        """
        return dataclasses.asdict(
            self,
            dict_factory=lambda x: {
                _to_camel_case_with_special_keywords(k): v
                for (k, v) in x if v is not None
            })


@dataclass(frozen=True)
class VesselClassEmissions:
    """Contains Vessel Class Emissions.

    Attributes:
        next_page_token: String. The key  to retrieve the next page
        data: List of Vessel Emissions for available vessels of this class

    """
    next_page_token: str
    data: List[EmissionsEstimation]

    def to_dict(self) -> Dict[Any, Any]:
        """Cast VesselClassEmissions object to dict.

        Returns:
            Dict representation of VesselClassEmissions object

        """
        return {
            "NextPageToken": self.next_page_token,
            "Data": [
                vessel_emissions.to_dict()
                for vessel_emissions in self.data
            ]
        }


@dataclass(frozen=True)
class VesselClassMetrics:
    """Contains Vessel Class Metrics.

    Attributes:
        next_page_token: String. The key that should be used
        as a parameter of the token to retrieve the next page
        data: List of Vessel Metrics for available vessels of this class

    """
    next_page_token: str
    data: List[VesselMetrics]

    def to_dict(self) -> Dict[Any, Any]:
        """Cast VesselClassMetrics object to dict.

        Returns:
            Dict representation of VesselClassMetrics object

        """
        return {
            "NextPageToken": self.next_page_token,
            "Data": [
                vessel_metrics.to_dict()
                for vessel_metrics in self.data
            ]
        }
