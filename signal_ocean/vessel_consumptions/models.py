"""The models for vessel consumptions api."""
import dataclasses
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from operator import attrgetter


def _to_camel_case(s: str) -> str:
    _to_camelcase = s.split('_')
    _to_camelcase = [word.capitalize() for word in _to_camelcase]
    return ''.join(_to_camelcase)


@dataclass(frozen=True)
class Consumption:
    """Contains consumption data for a specific speed.

    Attributes:
        speed: Vessel speed
        speed_profile_id: Speed profile identifier
        speed_profile: Speed profile name
        consumption: Consumption value

    """
    speed: float
    speed_profile_id: Optional[int] = None
    speed_profile: Optional[str] = None
    consumption: Optional[float] = None


@dataclass(frozen=True)
class VesselConsumptions:
    """Contains vessel consumptions data.

    Attributes:
        imo: Vessel IMO
        idle_consumption: Idle consumption value
        load_port_consumption: Load port consumption value
        discharge_port_consumption: Discharge port consumption value
        auxiliary_idle_consumption: Auxiliary idle consumption value
        auxiliary_ballast_consumption: Auxiliary ballast consumption value
        auxiliary_laden_consumption: Auxiliary laden consumption value
        laden_consumptions: List of laden consumptions
        ballast_consumptions: List of ballast consumptions

    """
    imo: int
    idle_consumption: Optional[float] = None
    load_port_consumption: Optional[float] = None
    discharge_port_consumption: Optional[float] = None
    auxiliary_idle_consumption: Optional[float] = None
    auxiliary_ballast_consumption: Optional[float] = None
    auxiliary_laden_consumption: Optional[float] = None
    laden_consumptions: Optional[List[Consumption]] = None
    ballast_consumptions: Optional[List[Consumption]] = None

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
        """Cast VesselConsumptions object to dict.

        Returns:
            Dict representation of VesselConsumptions model

        """
        return dataclasses.asdict(
            self,
            dict_factory=lambda x: {
                _to_camel_case(k): v
                for (k, v) in x if v is not None
            })


@dataclass(frozen=True)
class AdvertisedConsumptionAtSea:
    """Contains advertised consumption at sea data.

    Attributes:
        main_fuel_type_id: Main fuel type identifier
        main_fuel_type: Main fuel type name
        main_fuel_consumption: Main fuel consumption value
        aux_fuel_type_id: Auxiliary fuel type identifier
        aux_fuel_type: Auxiliary fuel type name
        aux_fuel_consumption: Auxiliary fuel consumption value
        speed: Vessel speed
        speed_profile_id: Speed profile identifier
        speed_profile: Speed profile name

    """
    main_fuel_type_id: Optional[int] = None
    main_fuel_type: Optional[str] = None
    main_fuel_consumption: float = 0.0
    aux_fuel_type_id: Optional[int] = None
    aux_fuel_type: Optional[str] = None
    aux_fuel_consumption: Optional[float] = None
    speed: float = 0.0
    speed_profile_id: Optional[int] = None
    speed_profile: Optional[str] = None


@dataclass(frozen=True)
class AdvertisedConsumptionInPort:
    """Contains advertised consumption in port data.

    Attributes:
        main_fuel_type_id: Main fuel type identifier
        main_fuel_type: Main fuel type name
        main_fuel_consumption: Main fuel consumption value
        aux_fuel_type_id: Auxiliary fuel type identifier
        aux_fuel_type: Auxiliary fuel type name
        aux_fuel_consumption: Auxiliary fuel consumption value
        operational_context_id: Operational context identifier
        operational_context: Operational context name

    """
    main_fuel_type_id: Optional[int] = None
    main_fuel_type: Optional[str] = None
    main_fuel_consumption: float = 0.0
    aux_fuel_type_id: Optional[int] = None
    aux_fuel_type: Optional[str] = None
    aux_fuel_consumption: Optional[float] = None
    operational_context_id: Optional[int] = None
    operational_context: Optional[str] = None


@dataclass(frozen=True)
class AdvertisedConsumptions:
    """Contains advertised consumptions data for a vessel.

    Attributes:
        imo: Vessel IMO
        updated_date: Date of last update
        ballast_consumptions: List of advertised ballast consumptions at sea
        laden_consumptions: List of advertised laden consumptions at sea
        idle_consumptions: List of advertised idle consumptions in port
        working_consumptions: List of advertised working consumptions in port

    """
    imo: int
    updated_date: str
    ballast_consumptions: Optional[List[AdvertisedConsumptionAtSea]] = None
    laden_consumptions: Optional[List[AdvertisedConsumptionAtSea]] = None
    idle_consumptions: Optional[List[AdvertisedConsumptionInPort]] = None
    working_consumptions: Optional[List[AdvertisedConsumptionInPort]] = None

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
        """Cast AdvertisedConsumptions object to dict.

        Returns:
            Dict representation of AdvertisedConsumptions model

        """
        return dataclasses.asdict(
            self,
            dict_factory=lambda x: {
                _to_camel_case(k): v
                for (k, v) in x if v is not None
            })


@dataclass(frozen=True)
class AdvertisedConsumptionsPage:
    """Contains a page of advertised consumptions.

    Attributes:
        next_page_token: The key to retrieve the next page
        data: List of advertised consumptions

    """
    next_page_token: Optional[str] = None
    data: List[AdvertisedConsumptions] = dataclasses.field(
        default_factory=list
    )

    def to_dict(self) -> Dict[Any, Any]:
        """Cast AdvertisedConsumptionsPage object to dict.

        Returns:
            Dict representation of AdvertisedConsumptionsPage object

        """
        return {
            "NextPageToken": self.next_page_token,
            "Data": [
                advertised_consumptions.to_dict()
                for advertised_consumptions in self.data
            ]
        }
