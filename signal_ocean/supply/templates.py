"""Baltic route templates for the Supply API.

A template is a set of filters that matches one Baltic Exchange route. Pass
its route code as `template` to any `SupplyAPI` method. Filters that you
pass too replace the template's value for the same field only.

Date windows are stored as offsets in days, so a template gives the same
window relative to each snapshot day on the historical endpoints and
relative to today on live supply.
"""
from typing import Any, Dict, List, Optional, Tuple, Union

from ._base import SupplyResponseModel
from .constants import (
    AvailabilityState,
    DefiningSize,
    EtaCalculationBasis,
    LocationTaxonomy,
    MarketDeployment,
    MarketStatus,
    VesselClass,
    VesselSubclass,
    VesselType,
    VoyageState,
)
from .filters import (
    AisTrackingFilter,
    CommercialAvailabilityFilter,
    EtaConfiguration,
    FromToRange,
    GeoLocation,
    HeadingRange,
    IncludeExcludeFilter,
    LiveSupplyFilter,
    MinMaxRange,
    SupplyFilter,
    VesselParticularsFilter,
    VoyageDetailsFilter,
)


class SupplyTemplate(SupplyResponseModel):
    """A Baltic route template.

    Attributes:
        code: The route code, for example `TD3C`.
        name: The template name.
        description: What the template selects.
        segment: `Tanker` or `Dry`.
        list_type: The kind of list the template was designed for.
        filters: The filters the template sends.
    """

    code: str
    name: str
    description: str
    segment: str
    list_type: str
    filters: SupplyFilter


def _geo(taxonomy: int, ids: Tuple[int, ...]) -> List[GeoLocation]:
    return [GeoLocation(geo_id=i, location_taxonomy=taxonomy) for i in ids]


def _level0(*ids: int) -> List[GeoLocation]:
    return _geo(LocationTaxonomy.LEVEL0, ids)


def _countries(*ids: int) -> List[GeoLocation]:
    return _geo(LocationTaxonomy.COUNTRY, ids)


def _ports(*ids: int) -> List[GeoLocation]:
    return _geo(LocationTaxonomy.PORT, ids)


def _headings(*ranges: Tuple[float, float]) -> List[HeadingRange]:
    return [HeadingRange(start=start, end=end) for start, end in ranges]


def _eta(
    code: str, basis_port_id: int, basis: str, max_days: int
) -> List[EtaConfiguration]:
    return [
        EtaConfiguration(
            id=code,
            basis_port_id=basis_port_id,
            eta_calculation_basis=basis,
            speed=13.0,
            sea_margin=0.0,
            eta_relative_offset=MinMaxRange(min=0, max=max_days),
        )
    ]


_TEMPLATES: Tuple[SupplyTemplate, ...] = (
    SupplyTemplate(
        code="TD1",
        name="VLCC US Gulf Supply 30 Days (TD1)",
        description="US Gulf crude supply to Loop, available next 30 days",
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=200000, to=549999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.CRUDE],
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    excluded=_level0(24719, 24739, 24741)
                ),
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(24767, 24778, 24772, 24777)
                ),
            ),
            eta_configuration=_eta(
                "TD1", 3858, EtaCalculationBasis.EARLIEST_OPEN_DATE, 30
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=15),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TD3C",
        name="VLCC Arabian Gulf Supply 18 Days (TD3C)",
        description=(
            "Arabian Gulf crude supply to Fujairah, available next 18 days"
        ),
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=200000, to=549999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.CRUDE],
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    excluded=_level0(
                        24719, 24739, 24741, 24776, 24772, 25007, 24709
                    )
                ),
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(
                        24767, 24772, 24776, 24746, 24676, 24733, 24671, 24600
                    )
                ),
            ),
            eta_configuration=_eta(
                "TD3C", 3153, EtaCalculationBasis.EARLIEST_OPEN_DATE, 18
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=15),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TD15",
        name="VLCC West Africa Supply 20 Days (TD15)",
        description=(
            "West Africa crude supply to Bonny, available next 20 days"
        ),
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=200000, to=549999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.CRUDE],
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    excluded=_level0(24719, 24739, 24741, 24742, 24598, 24768)
                ),
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(
                        24767, 24746, 24676, 24733, 24671, 24600, 24747, 24740,
                        24583, 24584, 24737,
                    )
                ),
            ),
            eta_configuration=_eta(
                "TD15", 3679, EtaCalculationBasis.EARLIEST_OPEN_DATE, 20
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=15),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TD23",
        name="Suezmax US Gulf Supply 20 Days (TD23)",
        description="US Gulf crude supply to Houston, available next 20 days",
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=125000, to=199999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.CRUDE],
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    excluded=_level0(24719, 24739, 24741, 24742, 24598, 24768)
                ),
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(
                        24767, 24778, 24772, 24777, 24737, 24583, 24584
                    )
                ),
            ),
            eta_configuration=_eta(
                "TD23", 3853, EtaCalculationBasis.EARLIEST_OPEN_DATE, 20
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TD20",
        name="Suezmax West Africa Supply 20 Days (TD20)",
        description=(
            "West Africa crude supply to Bonny, available next 20 days"
        ),
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=125000, to=199999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.CRUDE],
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    excluded=_level0(
                        24719, 24739, 24741, 24742, 24598, 24768, 24676, 24733,
                        24671, 24600,
                    )
                ),
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(
                        24767, 24746, 24676, 24733, 24671, 24600, 24747, 24740,
                        24583, 24584, 24737,
                    )
                ),
            ),
            eta_configuration=_eta(
                "TD20", 3679, EtaCalculationBasis.EARLIEST_OPEN_DATE, 20
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TD6",
        name="Suezmax Black Sea Supply 20 Days (TD6)",
        description="Black Sea crude supply to Novo, available next 20 days",
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=125000, to=199999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.CRUDE],
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    excluded=_level0(
                        24719, 24739, 24741, 24742, 24598, 24768, 24676, 24733,
                        24671, 24600, 24769, 24767, 24746, 24747, 24777,
                    )
                ),
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(
                        24767, 24746, 24676, 24733, 24671, 24600, 24747, 24772,
                        24777,
                    )
                ),
            ),
            eta_configuration=_eta(
                "TD6", 3763, EtaCalculationBasis.EARLIEST_OPEN_DATE, 20
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=15),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TD25",
        name="Aframax US Gulf Supply 10 Days (TD25)",
        description="US Gulf crude supply to Houston, available next 10 days",
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=82000, to=124999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.CRUDE],
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    excluded=_level0(24719, 24739, 24741, 24742, 24598, 24768)
                ),
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            eta_configuration=_eta(
                "TD25", 3853, EtaCalculationBasis.EARLIEST_OPEN_DATE, 10
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TD19",
        name="Aframax Mediterranean Supply 10 Days (TD19)",
        description=(
            "Mediterranean crude supply to Ceyhan, available next 10 days"
        ),
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=82000, to=124999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.CRUDE],
            commercial_availability=CommercialAvailabilityFilter(
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(
                        24747, 24746, 24767, 24676, 24733, 24777, 24740, 24671,
                        24594,
                    )
                ),
            ),
            eta_configuration=_eta(
                "TD19", 3812, EtaCalculationBasis.EARLIEST_OPEN_DATE, 10
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TD7",
        name="Aframax Continent Supply 10 Days (TD7)",
        description=(
            "Continent crude supply to Amsterdam, available next 10 days"
        ),
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=82000, to=124999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.CRUDE],
            commercial_availability=CommercialAvailabilityFilter(
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(24676, 24733, 24671, 24600, 24746, 24594)
                ),
            ),
            eta_configuration=_eta(
                "TD7", 3688, EtaCalculationBasis.EARLIEST_OPEN_DATE, 10
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TD8",
        name="Aframax Arabian Gulf Supply 15 Days (TD8)",
        description=(
            "Arabian Gulf crude supply to Fujairah, available next 15 days"
        ),
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=82000, to=124999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.CRUDE],
            commercial_availability=CommercialAvailabilityFilter(
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(
                        24737, 24738, 24712, 24583, 24584, 24676, 24733, 24746,
                        24671, 24600, 24767, 24772,
                    )
                ),
            ),
            eta_configuration=_eta(
                "TD8", 3153, EtaCalculationBasis.EARLIEST_OPEN_DATE, 15
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TC14",
        name="MR2 US Gulf Supply 7 Days (TC14)",
        description="US Gulf clean supply to Houston, available next 7 days",
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=42000, to=59999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.PRODUCT],
            commercial_availability=CommercialAvailabilityFilter(
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            eta_configuration=_eta(
                "TC14", 3853, EtaCalculationBasis.EARLIEST_OPEN_DATE, 7
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TC2",
        name="MR2 Continent Supply 10 Days (TC2)",
        description=(
            "Continent clean supply to Rotterdam, available next 10 days"
        ),
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=42000, to=59999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.PRODUCT],
            commercial_availability=CommercialAvailabilityFilter(
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(24676, 24733, 24671, 24746, 24600, 24594)
                ),
            ),
            eta_configuration=_eta(
                "TC2", 3689, EtaCalculationBasis.EARLIEST_OPEN_DATE, 10
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TC12",
        name="MR2 Far East Supply 10 Days (TC12)",
        description="Far East clean supply to Chiba, available next 10 days",
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=42000, to=59999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.PRODUCT],
            commercial_availability=CommercialAvailabilityFilter(
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(24714, 24777, 24764)
                ),
            ),
            eta_configuration=_eta(
                "TC12", 3570, EtaCalculationBasis.EARLIEST_OPEN_DATE, 10
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TC6",
        name="MR1 Mediterranean Supply 10 Days (TC6)",
        description="Med clean supply to Lavera, available next 10 days",
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=25000, to=41999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.PRODUCT],
            commercial_availability=CommercialAvailabilityFilter(
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            eta_configuration=_eta(
                "TC6", 3412, EtaCalculationBasis.EARLIEST_OPEN_DATE, 10
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TC1",
        name="LR2 Arabian Gulf Supply Next 30 Days",
        description=(
            "Arabian Gulf clean supply to Ruwais, available next 30 days"
        ),
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=100000, to=124999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.PRODUCT],
            commercial_availability=CommercialAvailabilityFilter(
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_current_area=IncludeExcludeFilter(
                    excluded=[
                        24673, 24740, 24747, 24676, 24733, 24600, 24671, 24746,
                        24767, 25007, 24709, 24758, 24757, 24756, 24594, 24755,
                    ]
                ),
            ),
            eta_configuration=_eta(
                "TC1", 3160, EtaCalculationBasis.EARLIEST_OPEN_DATE, 30
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="TC5",
        name="LR1 Arabian Gulf Supply Next 30 Days",
        description=(
            "Arabian Gulf clean supply to Ruwais, available next 30 days"
        ),
        segment="Tanker",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_type=VesselType.TANKER,
            size=FromToRange(from_=60000, to=81999),
            defining_size=DefiningSize.DEADWEIGHT,
            vessel_subclass=[VesselSubclass.PRODUCT],
            commercial_availability=CommercialAvailabilityFilter(
                availability_state=[
                    AvailabilityState.AVAILABLE,
                    AvailabilityState.CANCELLED,
                    AvailabilityState.FAILED,
                ],
                market_status=IncludeExcludeFilter(
                    values=[MarketStatus.PUSHED, MarketStatus.POSS_PUSHED]
                ),
                market_deployment=[
                    MarketDeployment.SPOT,
                    MarketDeployment.RELET,
                ],
            ),
            ais_tracking=AisTrackingFilter(
                ais_current_area=IncludeExcludeFilter(
                    excluded=[
                        24673, 24740, 24747, 24676, 24733, 24600, 24671, 24746,
                        24767, 25007, 24709, 24758, 24757, 24756, 24594, 24755,
                    ]
                ),
            ),
            eta_configuration=_eta(
                "TC5", 3160, EtaCalculationBasis.EARLIEST_OPEN_DATE, 30
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20),
                sanction_status=IncludeExcludeFilter(values=[0]),
            ),
        ),
    ),
    SupplyTemplate(
        code="C3",
        name="Capesize Brazil 40 days ballasters (C3)",
        description=(
            "Capesize vessels ballasting from Singapore with ETA to Tubarao "
            "within the next 40 days"
        ),
        segment="Dry",
        list_type="TrackingListAis",
        filters=SupplyFilter(
            vessel_class=VesselClass.CAPESIZE,
            voyage_details=VoyageDetailsFilter(
                voyage_state=[
                    VoyageState.BALLAST_UNFIXED,
                    VoyageState.BALLAST_FIXED,
                ]
            ),
            ais_tracking=AisTrackingFilter(
                days_since_latest_ais=5,
                ais_heading=_headings(
                    (157.5, 202.5),
                    (202.5, 247.5),
                    (247.5, 292.5),
                    (292.5, 337.5),
                ),
                ais_speed=FromToRange(from_=3.0, to=30.0),
                ais_current_area=IncludeExcludeFilter(
                    values=[
                        24769, 24767, 24772, 24776, 24779, 24771, 24702, 24655,
                        24770, 24728, 24725, 24729, 24715, 24666, 24726, 24730,
                    ]
                ),
                ais_destination=IncludeExcludeFilter(
                    excluded=_countries(20, 108, 210, 56, 55, 129)
                    + _level0(
                        24772, 24737, 24778, 24583, 24584, 24738, 24712, 25007,
                        24709, 24758, 24757, 24594, 24755, 24756, 24673,
                    )
                ),
            ),
            eta_configuration=_eta(
                "C3", 12770, EtaCalculationBasis.LATEST_AIS_LOCATION, 40
            ),
        ),
    ),
    SupplyTemplate(
        code="C5",
        name="Capesize W Australia 15 days ballasters (C5)",
        description=(
            "Capesize vessels ballasting from China with ETA to Port Hedland "
            "within the next 15 days"
        ),
        segment="Dry",
        list_type="TrackingListAis",
        filters=SupplyFilter(
            vessel_class=VesselClass.CAPESIZE,
            voyage_details=VoyageDetailsFilter(
                voyage_state=[
                    VoyageState.BALLAST_UNFIXED,
                    VoyageState.BALLAST_FIXED,
                ]
            ),
            ais_tracking=AisTrackingFilter(
                days_since_latest_ais=5,
                ais_heading=_headings(
                    (67.5, 112.5),
                    (112.5, 157.5),
                    (157.5, 202.5),
                    (202.5, 247.5),
                    (247.5, 292.5),
                ),
                ais_speed=FromToRange(from_=3.0, to=30.0),
                ais_current_area=IncludeExcludeFilter(
                    values=[
                        24666, 24715, 24725, 24726, 24729, 24730, 24702, 24704,
                        24773, 24714, 24728, 24770, 24655,
                    ]
                ),
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(
                        24739, 24767, 24769, 24772, 24776, 24655, 24781, 24780
                    )
                ),
            ),
            eta_configuration=_eta(
                "C5", 3210, EtaCalculationBasis.LATEST_AIS_LOCATION, 15
            ),
        ),
    ),
    SupplyTemplate(
        code="C7",
        name="Capesize Atlantic ballasters (C7)",
        description=(
            "Capesize vessels ballasting through the Atlantic with "
            "destination to Caribs, US or Canada"
        ),
        segment="Dry",
        list_type="TrackingListAis",
        filters=SupplyFilter(
            vessel_class=VesselClass.CAPESIZE,
            voyage_details=VoyageDetailsFilter(
                voyage_state=[
                    VoyageState.BALLAST_UNFIXED,
                    VoyageState.BALLAST_FIXED,
                ]
            ),
            ais_tracking=AisTrackingFilter(
                days_since_latest_ais=5,
                ais_heading=_headings(
                    (67.5, 112.5),
                    (112.5, 157.5),
                    (157.5, 202.5),
                    (202.5, 247.5),
                    (247.5, 292.5),
                ),
                ais_speed=FromToRange(from_=3.0, to=30.0),
                ais_current_area=IncludeExcludeFilter(
                    values=[
                        24740, 24747, 24676, 24733, 24671, 24746, 24600, 25007,
                        24709, 24758, 24757, 24673, 24756, 24755, 24594, 24712,
                        24738,
                    ]
                ),
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(
                        24767, 24769, 24772, 24776, 24779, 24756, 24755, 24594,
                        24757, 24758, 24709, 25007, 24712, 24738, 24737, 24583,
                        24584, 24673,
                    )
                ),
            ),
        ),
    ),
    SupplyTemplate(
        code="P6",
        name="Panamax ECSA 40 days ballasters (P6)",
        description=(
            "Panamax vessels ballasting from Singapore with ETA to Santos "
            "within the next 40 days (excl North Brazil)."
        ),
        segment="Dry",
        list_type="TrackingListAis",
        filters=SupplyFilter(
            vessel_type=VesselType.DRY,
            size=FromToRange(from_=67000, to=84999),
            defining_size=DefiningSize.DEADWEIGHT,
            voyage_details=VoyageDetailsFilter(
                voyage_state=[
                    VoyageState.BALLAST_FIXED,
                    VoyageState.BALLAST_UNFIXED,
                ]
            ),
            ais_tracking=AisTrackingFilter(
                days_since_latest_ais=5,
                ais_heading=_headings(
                    (157.5, 202.5),
                    (202.5, 247.5),
                    (247.5, 292.5),
                    (292.5, 337.5),
                ),
                ais_speed=FromToRange(from_=3.0, to=30.0),
                ais_current_area=IncludeExcludeFilter(
                    values=[
                        24769, 24767, 24772, 24776, 24779, 24771, 24702, 24655,
                        24770, 24728, 24725, 24729, 24715, 24666, 24726, 24730,
                    ]
                ),
                ais_destination=IncludeExcludeFilter(
                    excluded=_ports(
                        3248, 9079, 3253, 9076, 3244, 3235, 13013, 3241
                    )
                    + _countries(20, 108, 210, 56, 55, 129)
                    + _level0(
                        24772, 24737, 24778, 24583, 24584, 24738, 24712, 25007,
                        24709, 24758, 24757, 24594, 24755, 24756, 24673,
                    )
                ),
            ),
            eta_configuration=_eta(
                "P6", 3245, EtaCalculationBasis.LATEST_AIS_LOCATION, 40
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20)
            ),
        ),
    ),
    SupplyTemplate(
        code="P1",
        name="Panamax Atlantic ballasters (P1)",
        description=(
            "Panamax ballasters with destination to Caribs, US or Canada "
            "Atlantic Coast"
        ),
        segment="Dry",
        list_type="TrackingListAis",
        filters=SupplyFilter(
            vessel_type=VesselType.DRY,
            size=FromToRange(from_=67000, to=84999),
            defining_size=DefiningSize.DEADWEIGHT,
            voyage_details=VoyageDetailsFilter(
                voyage_state=[
                    VoyageState.BALLAST_FIXED,
                    VoyageState.BALLAST_UNFIXED,
                ]
            ),
            ais_tracking=AisTrackingFilter(
                days_since_latest_ais=5,
                ais_speed=FromToRange(from_=3.0, to=30.0),
                ais_current_area=IncludeExcludeFilter(
                    values=[
                        24676, 24733, 24671, 24746, 24600, 24747, 24740, 24673,
                        24757, 24756, 24594, 24755, 24758, 24709, 25007,
                    ]
                ),
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(
                        24767, 24772, 24769, 24776, 24712, 24738, 24737, 24583,
                        24584, 24756, 24594, 24755, 24757, 24758, 24709, 25007,
                        24673,
                    )
                ),
            ),
        ),
    ),
    SupplyTemplate(
        code="P3",
        name="Panamax WCNA 20 days ballasters (P3)",
        description=(
            "Panamax vessels ballasting from Far East with ETA to Vancouver "
            "(Canada) within the next 20 days"
        ),
        segment="Dry",
        list_type="TrackingListAis",
        filters=SupplyFilter(
            vessel_class=VesselClass.PANAMAX_DRY,
            voyage_details=VoyageDetailsFilter(
                voyage_state=[
                    VoyageState.BALLAST_FIXED,
                    VoyageState.BALLAST_UNFIXED,
                ]
            ),
            ais_tracking=AisTrackingFilter(
                days_since_latest_ais=5,
                ais_heading=_headings(
                    (0.0, 22.5),
                    (22.5, 67.5),
                    (67.5, 112.5),
                    (112.5, 157.5),
                    (157.5, 202.5),
                ),
                ais_speed=FromToRange(from_=3.0, to=30.0),
                ais_current_area=IncludeExcludeFilter(
                    values=[
                        24719, 24739, 24741, 24782, 24714, 24730, 24715, 24666,
                        24726,
                    ]
                ),
                ais_destination=IncludeExcludeFilter(
                    excluded=_level0(
                        24714, 24730, 24715, 24666, 24726, 24729, 24725, 24728,
                        24704, 24781, 24708, 24702, 24773, 24774, 24655, 24770,
                        24771, 24767, 24769, 24776, 24772, 24779, 24737, 24738,
                        24712, 25007, 24709, 24764, 24777, 24778, 24598, 24768,
                    )
                ),
            ),
            eta_configuration=_eta(
                "P3", 3267, EtaCalculationBasis.LATEST_AIS_LOCATION, 20
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20)
            ),
        ),
    ),
    SupplyTemplate(
        code="P5",
        name="Panamax Marketed SE Asia open 7 days (P5)",
        description=(
            "Panamax marketed vessels opening in the South East Asia within "
            "the next 7 days"
        ),
        segment="Dry",
        list_type="TonnageListOpen",
        filters=SupplyFilter(
            vessel_class=VesselClass.PANAMAX_DRY,
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    values=_level0(24702, 24655, 24770, 24728)
                ),
                open_date_relative_offset=FromToRange(from_=-5, to=7),
                latest_updated_date_relative_offset=FromToRange(
                    from_=-5, to=0
                ),
            ),
        ),
    ),
    SupplyTemplate(
        code="S5",
        name="Supramax Marketed ECSA ETA 20days (S5)",
        description=(
            "Supramax marketed vessels available to load in Santos within 20 "
            "days"
        ),
        segment="Dry",
        list_type="TonnageListEta",
        filters=SupplyFilter(
            vessel_class=VesselClass.SUPRAMAX,
            commercial_availability=CommercialAvailabilityFilter(
                latest_updated_date_relative_offset=FromToRange(
                    from_=-5, to=0
                ),
            ),
            voyage_details=VoyageDetailsFilter(
                voyage_state=[
                    VoyageState.BALLAST_FIXED,
                    VoyageState.BALLAST_UNFIXED,
                    VoyageState.DISCHARGING,
                    VoyageState.WAIT_TO_DISCHARGE,
                ]
            ),
            ais_tracking=AisTrackingFilter(
                ais_current_area=IncludeExcludeFilter(
                    values=[24746, 24772, 24767, 24769, 24776, 25007]
                ),
            ),
            eta_configuration=_eta(
                "S5", 3245, EtaCalculationBasis.EARLIEST_OPEN_DATE, 20
            ),
        ),
    ),
    SupplyTemplate(
        code="S2",
        name="Supramax Marketed Far East open 10days (S2)",
        description=(
            "Supramax marketed vessels opening in N China, S Korea, Japan or "
            "Russian Pacific within the next 10 days"
        ),
        segment="Dry",
        list_type="TonnageListOpen",
        filters=SupplyFilter(
            vessel_class=VesselClass.SUPRAMAX,
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    values=_level0(24666, 24715, 24730, 24714)
                ),
                open_date_relative_offset=FromToRange(from_=0, to=10),
                latest_updated_date_relative_offset=FromToRange(
                    from_=-5, to=0
                ),
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20)
            ),
        ),
    ),
    SupplyTemplate(
        code="S10",
        name="Supramax Marketed South China open 10days (S10)",
        description=(
            "Supramax marketed vessels opening in Singapore, Malaysia, "
            "Thailand, Vietnam or Phillipines within the next 10 days"
        ),
        segment="Dry",
        list_type="TonnageListOpen",
        filters=SupplyFilter(
            vessel_class=VesselClass.SUPRAMAX,
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    values=_level0(24702, 24655, 24770, 24728)
                ),
                open_date_relative_offset=FromToRange(from_=0, to=10),
                latest_updated_date_relative_offset=FromToRange(
                    from_=-5, to=0
                ),
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20)
            ),
        ),
    ),
    # The name says 20 days; the template's own window is 10 days.
    SupplyTemplate(
        code="HS4",
        name="Handy Marketed USG open 20 days (HS4)",
        description=(
            "Handysize marketed vessels opening in USG, ECM and Caribs within "
            "the next 20 days"
        ),
        segment="Dry",
        list_type="TonnageListOpen",
        filters=SupplyFilter(
            vessel_class=VesselClass.HANDYSIZE,
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    values=_level0(24676, 24733, 24600, 24671, 24746)
                ),
                open_date_relative_offset=FromToRange(from_=0, to=10),
                latest_updated_date_relative_offset=FromToRange(
                    from_=-5, to=0
                ),
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20)
            ),
        ),
    ),
    SupplyTemplate(
        code="HS5",
        name="Handy Marketed SE Asia open 10 days (HS5)",
        description=(
            "Handysize marketed vessels opening in Singapore, Malaysia, "
            "Thailand, Vietnam or Phillipines within the next 10 days"
        ),
        segment="Dry",
        list_type="TonnageListOpen",
        filters=SupplyFilter(
            vessel_class=VesselClass.HANDYSIZE,
            commercial_availability=CommercialAvailabilityFilter(
                open_location=IncludeExcludeFilter(
                    values=_level0(24702, 24655, 24770, 24728)
                ),
                open_date_relative_offset=FromToRange(from_=0, to=10),
                latest_updated_date_relative_offset=FromToRange(
                    from_=-5, to=0
                ),
            ),
            vessel_particulars=VesselParticularsFilter(
                vessel_age=MinMaxRange(max=20)
            ),
        ),
    ),
)

_BY_CODE = {template.code.casefold(): template for template in _TEMPLATES}

_SIZE_BAND = ("vesselType", "size", "definingSize")

_DATE_PAIRS = (
    ("openDate", "openDateRelativeOffset"),
    ("lastMarketedDate", "lastMarketedDateRelativeOffset"),
    ("latestUpdatedDate", "latestUpdatedDateRelativeOffset"),
)


def get_supply_templates() -> Tuple[SupplyTemplate, ...]:
    """Return the Baltic route templates.

    Returns:
        The templates, tankers first, then dry bulk.
    """
    return tuple(template.model_copy(deep=True) for template in _TEMPLATES)


def find_template(code: str) -> SupplyTemplate:
    """Return the template with a route code; case and spaces are ignored.

    Args:
        code: The route code, for example `TD3C`.

    Returns:
        The template.

    Raises:
        ValueError: The code is not a template route code.
    """
    template = _BY_CODE.get(code.strip().casefold())
    if template is None:
        valid = ", ".join(t.code for t in _TEMPLATES)
        raise ValueError(
            f"Unknown supply template '{code}'. Valid codes: {valid}"
        )
    return template.model_copy(deep=True)


def build_filter_body(
    template: Optional[SupplyTemplate],
    filters: Optional[Union[SupplyFilter, LiveSupplyFilter]],
) -> Dict[str, Any]:
    """Merge a template and user filters into the filter part of a request.

    A user field replaces the template value of that field only, and a
    user field set to None removes it. The API refuses a vessel class
    together with a size band, and an absolute date together with its
    relative offset, so the user's choice removes the template's other one.

    Args:
        template: The template, or None.
        filters: The user filters, or None.

    Returns:
        The request body fields, with camelCase names and no null values.
    """
    base = _dump(template.filters) if template else {}
    user = _dump(filters) if filters else {}

    if "vesselClass" in user:
        for key in _SIZE_BAND:
            base.pop(key, None)
    if any(key in user for key in _SIZE_BAND):
        base.pop("vesselClass", None)

    user_commercial = user.get("commercialAvailability")
    base_commercial = base.get("commercialAvailability")
    if isinstance(user_commercial, dict) and isinstance(base_commercial, dict):
        for absolute, relative in _DATE_PAIRS:
            if absolute in user_commercial:
                base_commercial.pop(relative, None)
            if relative in user_commercial:
                base_commercial.pop(absolute, None)

    return _without_none(_merge(base, user))


def _dump(filters: Union[SupplyFilter, LiveSupplyFilter]) -> Dict[str, Any]:
    return filters.model_dump(mode="json", by_alias=True, exclude_unset=True)


def _merge(base: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in user.items():
        if value is None:
            merged.pop(key, None)
        elif isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _without_none(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _without_none(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_without_none(item) for item in value]
    return value
