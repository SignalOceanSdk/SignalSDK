from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


@dataclass(frozen=True)
class Emissions:
    """
    Contains the reported emissions per gas type

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
    co2_in_tons: float
    coin_tons: float
    ch4_in_tons: float
    n2_oin_tons: float
    nmvocin_tons: float
    nox_in_tons: float
    sox_in_tons: float
    pmin_tons: float


@dataclass(frozen=True)
class EmissionsBreakdown:
    """
    Contains emissions breakdown for different parts of the Voyage

    Attributes:
        voyage: Vessel Emissions for the voyage
        ballast: Vessel Emissions for the ballast part of the voyage
        laden: Vessel Emissions for the laden part of the voyage
        port_call: Vessel Emissions for the port calls of the voyage
        stop: Vessel Emissions for the stops of the voyage
    """
    voyage: Emissions
    ballast: Optional[Emissions]
    laden: Optional[Emissions]
    port_call: Optional[Emissions]
    stop: Optional[Emissions]


@dataclass(frozen=True)
class Consumptions:
    """
    Contains the reported consumptions per gas type

    Attributes:
    hfo_in_tons: HFO vessel consumption in tons
    lfo_in_tons: LFO vessel consumption in tons
    mgo_in_tons: MGO vessel consumption in tons
    lng_in_tons: LNG vessel consumption in tons
    lpg_propane_in_tons: LPG Propane vessel consumption in tons
    lpg_butane_in_tons: LPG Butane vessel consumption in tons
    total_in_tons: Total vessel consumption in tons

    """
    hfo_in_tons: Optional[float]
    lfo_in_tons: Optional[float]
    mgo_in_tons: Optional[float]
    lng_in_tons: Optional[float]
    lpg_propane_in_tons: Optional[float]
    lpg_butane_in_tons: Optional[float]
    total_in_tons: float


@dataclass(frozen=True)
class ConsumptionsBreakdown:
    """
    Contains consumptions breakdown for different parts of the Voyage

    Attributes:
        voyage: Vessel Consumptions for the voyage
        ballast: Vessel Consumptions for the ballast part of the voyage
        laden: Vessel Consumptions for the laden part of the voyage
        port_call: Vessel Consumptions for the port calls of the voyage
        stop: Vessel Consumptions for the stops of the voyage
    """
    voyage: Consumptions
    ballast: Optional[Consumptions]
    laden: Optional[Consumptions]
    port_call: Optional[Consumptions]
    stop: Optional[Consumptions]


@dataclass(frozen=True)
class Duration:
    """
    Contains voyage duration information

    Attributes:
        in_hours: Duration in Hours
        in_days: Duration in Days
    """
    in_hours: float
    in_days: float


@dataclass(frozen=True)
class DurationBreakdown:
    """
    Contains duration breakdown for the different parts of the voyage

    Attributes:
        voyage: Duration of the voyage
        ballast: Duration of the ballast part of the voyage
        laden: Duration of the laden part of the voyage
        port_call: Duration of the port calls of the voyage
        stop: Duration of the stops of the voyage
    """
    voyage: Duration
    ballast: Optional[Duration]
    laden: Optional[Duration]
    port_call: Optional[Duration]
    stop: Optional[Duration]


@dataclass(frozen=True)
class Distance:
    distance_travelled: float


@dataclass(frozen=True)
class DistancesBreakdown:
    voyage: Distance
    ballast: Distance
    laden: Distance


@dataclass(frozen=True)
class Metrics:
    voyage_cii: float
    voyage_cii_unit: str
    voyage_cii_rating: str
    voyage_cii_target: float
    voyage_cii_target_year: int
    capacity_eeoi: float
    capacity_eeoi_unit: str
    capacity_eeoi_sea_cargo_charter_year_target: float
    capacity_eeoi_sea_cargo_charter_class: str
    capacity_eeoi_sea_cargo_charter_alignment_in_percentage: float
    eeoi: Optional[float]
    eeoi_unit: Optional[str]
    eeoi_sea_cargo_charter_year_target: Optional[float]
    eeoi_sea_cargo_charter_class: Optional[str]
    eeoi_sea_cargo_charter_alignment_in_percentage: Optional[float]
    kg_co2_per_tonne_cargo: Optional[float]
    kg_co2_per_tonne_dwt: Optional[float]


@dataclass(frozen=True)
class SeagoingSpeedStatistics:
    average_speed_in_knots: Optional[float]
    std_speed_in_knots: Optional[float]
    min_speed_in_knots: Optional[float]
    max_speed_in_knots: Optional[float]


@dataclass(frozen=True)
class SeagoingSpeedStatisticsBreakdown:
    voyage: SeagoingSpeedStatistics
    laden: SeagoingSpeedStatistics
    ballast: SeagoingSpeedStatistics


@dataclass(frozen=True)
class EmissionsEssentialStatistics:
    emissions: Optional[EmissionsBreakdown]
    consumptions: Optional[ConsumptionsBreakdown]
    distances: Optional[DistancesBreakdown]
    duration: Optional[DurationBreakdown]


@dataclass(frozen=True)
class EmissionsEstimationModel:
    id: Optional[str] = None
    imo: Optional[int] = None
    vessel_name: Optional[str] = None
    voyage_number: Optional[int] = None
    vessel_type_id: Optional[int] = None
    vessel_type: Optional[str] = None
    vessel_class_id: Optional[int] = None
    vessel_class: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    quantity: Optional[float] = None
    deadweight: Optional[int] = None
    transport_work_in_million_tonne_miles: Optional[float] = None
    transport_work_in_million_dwt_miles: Optional[float] = None
    contains_eu_emissions: Optional[bool] = None
    emissions: Optional[EmissionsBreakdown] = None
    consumptions: Optional[ConsumptionsBreakdown] = None
    seagoing_speed_statistics: Optional[SeagoingSpeedStatisticsBreakdown] = None
    duration: Optional[DurationBreakdown] = None
    distances: Optional[DistancesBreakdown] = None
    efficiency_metrics: Optional[Metrics] = None
    european_union_regulated: Optional[EmissionsEssentialStatistics] = None


@dataclass(frozen=True)
class Eexi:
    value: Optional[float] = None
    unit: Optional[str] = None
    required: Optional[float] = None


@dataclass(frozen=True)
class Eiv:
    value: Optional[float] = None
    unit: Optional[str] = None


@dataclass(frozen=True)
class Aer:
    value: Optional[float] = None
    unit: Optional[str] = None
    poseidon_principles_class: Optional[str] = None
    poseidon_principles_alignment_in_percentage: Optional[float] = None
    poseidon_principles_year_target: Optional[float] = None


@dataclass(frozen=True)
class Cii:
    value: Optional[float] = None
    unit: Optional[str] = None
    rating: Optional[str] = None
    target: Optional[float] = None
    target_year: Optional[int] = None


@dataclass(frozen=True)
class VesselMetrics:
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


@dataclass(frozen=True)
class VesselClassEmissions:
    next_page_token: str
    data: List[EmissionsEstimationModel]


@dataclass(frozen=True)
class VesselClassMetrics:
    next_page_token: str
    data: List[VesselMetrics]
