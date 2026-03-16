"""The models for vessel consumptions api."""
from typing import Optional, List, Dict, Any

from pydantic import Field, AliasChoices
from pydantic_core import PydanticUndefined

from signal_ocean.util.pydantic_base import SignalBaseModel


def _to_camel_case(s: str) -> str:
    _to_camelcase = s.split('_')
    _to_camelcase = [word.capitalize() for word in _to_camelcase]
    return ''.join(_to_camelcase)


class Consumption(SignalBaseModel):
    """Contains consumption data for a specific speed.

    Attributes:
        speed: Vessel speed
        speed_profile_id: Speed profile identifier
        speed_profile: Speed profile name
        consumption: Consumption value

    """
    speed: float
    speed_profile_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices('SpeedProfileId', 'SpeedProfileID',
                                      'speed_profile_id'),
    )
    speed_profile: Optional[str] = None
    consumption: Optional[float] = None


class VesselConsumptions(SignalBaseModel):
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
        nodef_f_vals = []
        for name, field_info in self.__class__.model_fields.items():
            value = getattr(self, name)
            default = field_info.default
            if default is PydanticUndefined or value != default:
                nodef_f_vals.append(f"{name}={value}")
        return f"{self.__class__.__name__}({', '.join(nodef_f_vals)})"

    def to_dict(self) -> Dict[Any, Any]:
        """Cast VesselConsumptions object to dict.

        Returns:
            Dict representation of VesselConsumptions model

        """
        def _convert(data):
            if isinstance(data, dict):
                return {_to_camel_case(k): _convert(v) for k, v in data.items() if v is not None}
            elif isinstance(data, list):
                return [_convert(item) for item in data]
            return data
        return _convert(self.model_dump())


class AdvertisedConsumptionAtSea(SignalBaseModel):
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
    main_fuel_type_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices('MainFuelTypeId', 'MainFuelTypeID',
                                      'main_fuel_type_id'),
    )
    main_fuel_type: Optional[str] = None
    main_fuel_consumption: float = 0.0
    aux_fuel_type_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices('AuxFuelTypeId', 'AuxFuelTypeID',
                                      'aux_fuel_type_id'),
    )
    aux_fuel_type: Optional[str] = None
    aux_fuel_consumption: Optional[float] = None
    speed: float = 0.0
    speed_profile_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices('SpeedProfileId', 'SpeedProfileID',
                                      'speed_profile_id'),
    )
    speed_profile: Optional[str] = None


class AdvertisedConsumptionInPort(SignalBaseModel):
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
    main_fuel_type_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices('MainFuelTypeId', 'MainFuelTypeID',
                                      'main_fuel_type_id'),
    )
    main_fuel_type: Optional[str] = None
    main_fuel_consumption: float = 0.0
    aux_fuel_type_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices('AuxFuelTypeId', 'AuxFuelTypeID',
                                      'aux_fuel_type_id'),
    )
    aux_fuel_type: Optional[str] = None
    aux_fuel_consumption: Optional[float] = None
    operational_context_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices('OperationalContextId',
                                      'OperationalContextID',
                                      'operational_context_id'),
    )
    operational_context: Optional[str] = None


class AdvertisedConsumptions(SignalBaseModel):
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
        nodef_f_vals = []
        for name, field_info in self.__class__.model_fields.items():
            value = getattr(self, name)
            default = field_info.default
            if default is PydanticUndefined or value != default:
                nodef_f_vals.append(f"{name}={value}")
        return f"{self.__class__.__name__}({', '.join(nodef_f_vals)})"

    def to_dict(self) -> Dict[Any, Any]:
        """Cast AdvertisedConsumptions object to dict.

        Returns:
            Dict representation of AdvertisedConsumptions model

        """
        def _convert(data):
            if isinstance(data, dict):
                return {_to_camel_case(k): _convert(v) for k, v in data.items() if v is not None}
            elif isinstance(data, list):
                return [_convert(item) for item in data]
            return data
        return _convert(self.model_dump())


class AdvertisedConsumptionsPage(SignalBaseModel):
    """Contains a page of advertised consumptions.

    Attributes:
        next_page_token: The key to retrieve the next page
        data: List of advertised consumptions

    """
    next_page_token: Optional[str] = None
    data: List[AdvertisedConsumptions] = Field(default_factory=list)

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
