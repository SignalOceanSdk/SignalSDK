"""Request filters of the Supply API.

Field names are the API names in snake_case. A field left unset is not
sent. Filters do not check values: the API checks them and its error
message is raised to the caller.
"""
from typing import Any, List, Optional, Union

from pydantic import Field

from ._base import SupplyRequestModel


class FromToRange(SupplyRequestModel):
    """Inclusive range with `from` and `to` bounds.

    Attributes:
        from_: Lower bound, sent as `from`. A number, a date or a datetime.
        to: Upper bound. A number, a date or a datetime.
    """

    # Not `alias`: type checkers would then expect the keyword `from`.
    from_: Any = Field(
        None, validation_alias="from", serialization_alias="from"
    )
    to: Any = None


class MinMaxRange(SupplyRequestModel):
    """Inclusive range with `min` and `max` bounds.

    Attributes:
        min: Lower bound. A number, a date or a datetime.
        max: Upper bound. A number, a date or a datetime.
    """

    min: Any = None
    max: Any = None


class IncludeExcludeFilter(SupplyRequestModel):
    """Values to include and values to exclude.

    Attributes:
        values: Values to include.
        excluded: Values to exclude. A value cannot be in both lists.
    """

    values: Optional[List[Any]] = None
    excluded: Optional[List[Any]] = None


class HeadingRange(SupplyRequestModel):
    """Compass heading range in degrees, with `start` <= `end`.

    Attributes:
        start: First heading, 0 to 360.
        end: Last heading, 0 to 360.
    """

    start: float
    end: float


class GeoLocation(SupplyRequestModel):
    """A location for the location filters.

    Attributes:
        geo_id: The Signal geo identifier.
        location_taxonomy: The location level. See `LocationTaxonomy`.
    """

    geo_id: int
    location_taxonomy: int


class CommercialAvailabilityFilter(SupplyRequestModel):
    """Filters on open location, open date and commercial status.

    Location filters take `GeoLocation` values. A `*_relative_offset`
    range counts days from each snapshot day, or from today on live supply.
    An absolute date and its relative offset cannot be combined.

    Attributes:
        open_location: Where the vessel becomes available, from AIS and
            commercial data. Takes `GeoLocation` values: a port, an area
            (for example US Gulf) or a country.
        open_date: When the vessel becomes available for its next charter.
        open_date_relative_offset: Open date in days from the snapshot day.
            A negative value is in the past.
        availability_state: Charter market status: open for new business,
            under negotiation, or committed. See `AvailabilityState`.
        market_status: Whether the commercial operator markets the vessel:
            pushed, possibly pushed or not pushed. See `MarketStatus`.
        market_deployment: How the vessel is deployed: spot, program,
            contract or relet. See `MarketDeployment`.
        position_source_origin: How the position was found: entered by a
            user, from AIS, or calculated by the system. See
            `PositionSourceOrigin`.
        position_source_type: The channel that reported the position, for
            example email or a model prediction. See `PositionSourceType`.
        last_marketed_date: When the operator last marketed the vessel.
        last_marketed_date_relative_offset: Last marketed date in days from
            the snapshot day.
        latest_updated_date: When the commercial data of the vessel was last
            updated. Shows how recent the position is.
        latest_updated_date_relative_offset: Latest update in days from the
            snapshot day.
        forecasted_destination: The destination that the system predicts.
            Takes `GeoLocation` values. It is not the AIS destination.
    """

    open_location: Optional[IncludeExcludeFilter] = None
    open_date: Optional[FromToRange] = None
    open_date_relative_offset: Optional[FromToRange] = None
    availability_state: Optional[List[str]] = None
    market_status: Optional[IncludeExcludeFilter] = None
    market_deployment: Optional[List[str]] = None
    position_source_origin: Optional[IncludeExcludeFilter] = None
    position_source_type: Optional[IncludeExcludeFilter] = None
    last_marketed_date: Optional[FromToRange] = None
    last_marketed_date_relative_offset: Optional[FromToRange] = None
    latest_updated_date: Optional[FromToRange] = None
    latest_updated_date_relative_offset: Optional[FromToRange] = None
    forecasted_destination: Optional[IncludeExcludeFilter] = None


class VoyageDetailsFilter(SupplyRequestModel):
    """Filters on voyage state, cargo, start port and charterer.

    `start_port` takes `GeoLocation` values; the id filters take integers.

    Attributes:
        voyage_state: The phase of the current voyage, for example ballast,
            laden, loading or discharging. See `VoyageState`.
        reported_last_cargo_type_id: Cargo type ids of the last reported
            cargoes, up to 3.
        cargo_type_id: Cargo type id on the current voyage.
        last_voyage_cargo_type_id: Cargo type ids of the previous voyage.
        start_port: The load port of the voyage leg.
        cargo_quantity: Cargo quantity in metric tonnes.
        charterer: Charterer company ids.
    """

    voyage_state: Optional[List[str]] = None
    reported_last_cargo_type_id: Optional[IncludeExcludeFilter] = None
    cargo_type_id: Optional[IncludeExcludeFilter] = None
    last_voyage_cargo_type_id: Optional[IncludeExcludeFilter] = None
    start_port: Optional[IncludeExcludeFilter] = None
    cargo_quantity: Optional[FromToRange] = None
    charterer: Optional[IncludeExcludeFilter] = None


class AisTrackingFilter(SupplyRequestModel):
    """Filters on AIS position, movement and destination.

    `ais_current_area` takes area ids as integers. `ais_closest_location`
    and `ais_destination` take `GeoLocation` values.

    Attributes:
        days_since_latest_ais: Maximum number of days since the last AIS
            message of the vessel. More than 7 days can mean that the AIS
            is off or out of coverage.
        ais_draught: Current AIS draught in metres. A deep draught usually
            means laden, a shallow draught usually means ballast.
        ais_heading: Compass headings in degrees, 0 to 360.
        ais_speed: Current AIS speed over ground in knots.
        ais_current_area: Area ids of the current AIS position.
        ais_closest_location: The named location nearest to the AIS
            position.
        ais_destination: The destination that the vessel reports on AIS.
        eta_to_ais_destination: ETA to the AIS destination, calculated by
            the system.
    """

    days_since_latest_ais: Optional[int] = None
    ais_draught: Optional[MinMaxRange] = None
    ais_heading: Optional[List[HeadingRange]] = None
    ais_speed: Optional[FromToRange] = None
    ais_current_area: Optional[IncludeExcludeFilter] = None
    ais_closest_location: Optional[IncludeExcludeFilter] = None
    ais_destination: Optional[IncludeExcludeFilter] = None
    eta_to_ais_destination: Optional[FromToRange] = None


class VesselParticularsFilter(SupplyRequestModel):
    """Filters on vessel characteristics, ownership and sanctions.

    Attributes:
        commercial_operator: Company ids of the commercial operator, the
            company that decides the employment of the vessel.
        liquid_capacity: Liquid capacity in cubic metres.
        ice_class: Ice class names.
        cranes_ton_capacity: Crane capacity in tonnes.
        length_overall: Length overall (LOA) in metres.
        breadth_extreme: Breadth in metres.
        air_draught: Air draught in metres.
        ballast_parallel_body_length: Parallel body length in ballast, in
            metres.
        bow_to_center_manifold: Bow to center manifold, in metres.
        class_renewal_date: Class renewal date.
        built_country_code: ISO codes of the build country.
        built_country_name: Names of the build country.
        crude_oil_washing: Crude oil washing system.
        delivery_date: Delivery date.
        flag_code: ISO codes of the flag state.
        heating_coils_fitted: Heating coils fitted.
        inert_gas_system: Inert gas system.
        lightship_tonnes: Lightship weight in tonnes.
        main_engine_manufacturer_id: Main engine manufacturer ids.
        main_engine_manufacturer: Main engine manufacturer names.
        main_engine_kw: Main engine power in kW.
        main_engine_rpm: Main engine RPM.
        moulded_depth: Moulded depth in metres.
        parallel_body_length: Parallel body length in metres.
        reduced_gross_tonnage: Reduced gross tonnage.
        shipyard_built_id: Ids of the shipyard that built the vessel.
        stern_line: Stern line fitted.
        water_line_to_manifold: Waterline to manifold, in metres.
        built_for_trade_ids: Ids of the trades that the vessel was built
            for.
        bale_capacity: Bale capacity in cubic metres.
        co2_fitted: CO2 system fitted.
        grain_capacity: Grain capacity in cubic metres.
        neo_panama_locks: Fits the Neo-Panamax locks.
        number_of_holds: Number of holds.
        australian_ladder: Australian ladder fitted.
        log_fitted: Log fitted.
        open_hatch: Open hatch design.
        a60_bulkhead: A60 bulkhead.
        gross_registered_tonnage: Gross registered tonnage (GRT).
        net_registered_tonnage: Net registered tonnage (NRT).
        head_owner_id: Company ids of the head owner, the owner at the top
            of the ownership structure.
        ballast_water_treatment: Ballast water treatment system.
        draught: Draught in metres.
        geared: Has cranes or other cargo gear. A geared vessel can load and
            discharge without port cranes.
        classification_register_id: Classification society ids.
        vessel_age: Vessel age in years. An alternative to `year_built`.
        coating: Tank coating. See `Coating`.
        imo_type: IMO ship type. See `ImoType`.
        crane_max_out_reach: Maximum crane outreach in metres.
        crane_lifting_capacity: Crane lifting capacity in tonnes.
        number_of_cranes: Number of cranes.
        box_shaped_holds: Box-shaped holds.
        hold_length: Hold length in metres.
        hold_height: Hold height in metres.
        hold_breadth: Hold breadth in metres.
        number_of_hatches: Number of hatches.
        has_hatches: Has hatches.
        hatch_length: Hatch length in metres.
        hatch_breadth: Hatch breadth in metres.
        number_of_grabs: Number of grabs.
        has_grabs: Has grabs.
        grab_lifting_capacity: Grab lifting capacity in tonnes.
        grab_max_lifting_weight: Maximum grab lifting weight in tonnes.
        scrubbers: Exhaust gas scrubbers fitted. A vessel with scrubbers can
            burn high-sulphur fuel oil.
        year_built: Year built.
        number_of_bow_thrusters: Number of bow thrusters.
        number_of_bow_chain_stoppers: Number of bow chain stoppers.
        propulsion_type: Propulsion type ids.
        gas_containment_type: Gas containment type ids, for LNG and LPG
            vessels.
        summer_tpc: Summer tonnes per centimetre immersion (TPC).
        design_model: Names of the vessel design model.
        sanction_status: Sanction status ids. Use it to find or remove
            sanctioned vessels.
        trade: The sub-segment of the vessel within its class. Includes
            the manual changes of your company.
    """

    commercial_operator: Optional[IncludeExcludeFilter] = None
    liquid_capacity: Optional[MinMaxRange] = None
    ice_class: Optional[List[str]] = None
    cranes_ton_capacity: Optional[MinMaxRange] = None
    length_overall: Optional[MinMaxRange] = None
    breadth_extreme: Optional[MinMaxRange] = None
    air_draught: Optional[MinMaxRange] = None
    ballast_parallel_body_length: Optional[MinMaxRange] = None
    bow_to_center_manifold: Optional[MinMaxRange] = None
    class_renewal_date: Optional[MinMaxRange] = None
    built_country_code: Optional[IncludeExcludeFilter] = None
    built_country_name: Optional[IncludeExcludeFilter] = None
    crude_oil_washing: Optional[bool] = None
    delivery_date: Optional[MinMaxRange] = None
    flag_code: Optional[IncludeExcludeFilter] = None
    heating_coils_fitted: Optional[bool] = None
    inert_gas_system: Optional[bool] = None
    lightship_tonnes: Optional[MinMaxRange] = None
    main_engine_manufacturer_id: Optional[IncludeExcludeFilter] = None
    main_engine_manufacturer: Optional[List[str]] = None
    main_engine_kw: Optional[MinMaxRange] = None
    main_engine_rpm: Optional[MinMaxRange] = None
    moulded_depth: Optional[MinMaxRange] = None
    parallel_body_length: Optional[MinMaxRange] = None
    reduced_gross_tonnage: Optional[MinMaxRange] = None
    shipyard_built_id: Optional[IncludeExcludeFilter] = None
    stern_line: Optional[bool] = None
    water_line_to_manifold: Optional[MinMaxRange] = None
    built_for_trade_ids: Optional[List[int]] = None
    bale_capacity: Optional[MinMaxRange] = None
    co2_fitted: Optional[bool] = None
    grain_capacity: Optional[MinMaxRange] = None
    neo_panama_locks: Optional[bool] = None
    number_of_holds: Optional[MinMaxRange] = None
    australian_ladder: Optional[bool] = None
    log_fitted: Optional[bool] = None
    open_hatch: Optional[bool] = None
    a60_bulkhead: Optional[bool] = None
    gross_registered_tonnage: Optional[MinMaxRange] = None
    net_registered_tonnage: Optional[MinMaxRange] = None
    head_owner_id: Optional[IncludeExcludeFilter] = None
    ballast_water_treatment: Optional[bool] = None
    draught: Optional[MinMaxRange] = None
    geared: Optional[bool] = None
    classification_register_id: Optional[IncludeExcludeFilter] = None
    vessel_age: Optional[MinMaxRange] = None
    coating: Optional[str] = None
    imo_type: Optional[str] = None
    crane_max_out_reach: Optional[MinMaxRange] = None
    crane_lifting_capacity: Optional[MinMaxRange] = None
    number_of_cranes: Optional[MinMaxRange] = None
    box_shaped_holds: Optional[bool] = None
    hold_length: Optional[MinMaxRange] = None
    hold_height: Optional[MinMaxRange] = None
    hold_breadth: Optional[MinMaxRange] = None
    number_of_hatches: Optional[MinMaxRange] = None
    has_hatches: Optional[bool] = None
    hatch_length: Optional[MinMaxRange] = None
    hatch_breadth: Optional[MinMaxRange] = None
    number_of_grabs: Optional[MinMaxRange] = None
    has_grabs: Optional[bool] = None
    grab_lifting_capacity: Optional[MinMaxRange] = None
    grab_max_lifting_weight: Optional[MinMaxRange] = None
    scrubbers: Optional[bool] = None
    year_built: Optional[MinMaxRange] = None
    number_of_bow_thrusters: Optional[MinMaxRange] = None
    number_of_bow_chain_stoppers: Optional[MinMaxRange] = None
    propulsion_type: Optional[IncludeExcludeFilter] = None
    gas_containment_type: Optional[IncludeExcludeFilter] = None
    summer_tpc: Optional[MinMaxRange] = None
    design_model: Optional[IncludeExcludeFilter] = None
    sanction_status: Optional[IncludeExcludeFilter] = None
    trade: Optional[IncludeExcludeFilter] = None


class _EtaConfigurationFields(SupplyRequestModel):
    basis_port_id: int
    speed: Optional[float] = None
    sea_margin: Optional[float] = None
    eta_calculation_basis: Optional[str] = None
    eta: Optional[MinMaxRange] = None
    eta_relative_offset: Optional[MinMaxRange] = None
    id: Optional[str] = None


class EtaConfiguration(_EtaConfigurationFields):
    """A custom ETA calculation, for supply trend and historical supply.

    Attributes:
        basis_port_id: The port to calculate the ETA to.
        speed: Speed in knots. The API uses 12 when not set.
        sea_margin: Extra time in percent, for example 10 for 10%.
        eta_calculation_basis: See `EtaCalculationBasis`.
        eta: Absolute ETA range. Cannot be combined with
            `eta_relative_offset`.
        eta_relative_offset: ETA range in days from the snapshot day.
        id: Identifier returned in each vessel's `eta_details`.
    """


class EtaConfigurationWithRestrictions(_EtaConfigurationFields):
    """A custom ETA calculation with routing restrictions, for live supply.

    Attributes:
        restrictions: See `Restrictions`. The other attributes are the same
            as in `EtaConfiguration`.
    """

    restrictions: Optional[str] = None


class _SupplyFilterFields(SupplyRequestModel):
    vessel_class: Optional[Union[int, str]] = None
    vessel_type: Optional[Union[int, str]] = None
    size: Optional[FromToRange] = None
    defining_size: Optional[str] = None
    vessel_subclass: Optional[List[str]] = None
    add_willing_to_switch_subclass: Optional[bool] = None
    imo: Optional[List[int]] = None
    search_text: Optional[str] = None
    commercial_availability: Optional[CommercialAvailabilityFilter] = None
    voyage_details: Optional[VoyageDetailsFilter] = None
    ais_tracking: Optional[AisTrackingFilter] = None
    vessel_particulars: Optional[VesselParticularsFilter] = None


class SupplyFilter(_SupplyFilterFields):
    """Filters for supply trend, historical supply and live supply.

    Give either `vessel_class`, or all of `vessel_type`, `defining_size`
    and `size`. The API refuses a request with neither, or with both.

    Attributes:
        vessel_class: Class name (see `VesselClass`) or class id.
        vessel_type: Type name (see `VesselType`) or type id.
        size: Size range, in the unit of `defining_size`.
        defining_size: See `DefiningSize`.
        vessel_subclass: See `VesselSubclass`.
        add_willing_to_switch_subclass: Also include vessels willing to
            switch into `vessel_subclass`.
        imo: IMO numbers.
        search_text: Text to find in vessel or company names.
        commercial_availability: See `CommercialAvailabilityFilter`.
        voyage_details: See `VoyageDetailsFilter`.
        ais_tracking: See `AisTrackingFilter`.
        vessel_particulars: See `VesselParticularsFilter`.
        eta_configuration: Custom ETA calculations.
    """

    eta_configuration: Optional[List[EtaConfiguration]] = None


class LiveSupplyFilter(_SupplyFilterFields):
    """Filters for live supply, where ETA calculations take restrictions.

    The attributes are the same as in `SupplyFilter`, except that
    `eta_configuration` also accepts `EtaConfigurationWithRestrictions`.
    """

    eta_configuration: Optional[
        List[Union[EtaConfiguration, EtaConfigurationWithRestrictions]]
    ] = None
