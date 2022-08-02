"""Models instantiated by the voyages api."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple


@dataclass(frozen=True)
class MatchedFixture:
    """Contains information about a single fixture.

    Attributes:
        fixture_status_id: Numeric ID corresponding to the different values of
            the FixtureStatus field. 0-> OnSubs, 1-> FullyFixed,
            2-> Failed, 3-> Cancelled , 4-> Available, 5-> PossFixed,
            -2-> NotSet, -1-> Unknown.
        fixture_status: String denoting the commercial status of a fixture if
            explicitly mentioned, like ffxd for fully fixed or subs for on
            subs.
        charter_type_id: Numeric ID corresponding to the different values of
            the ChartererType field. 0-> Voyage, 1-> Time charter
        charter_type: String denoting the type of the charter
        charterer_id: Numeric ID corresponding to the company reported as
            charterer in at least one of the fixtures.
        charterer: String, name of the company reported as charterer in at
            least one of the fixtures.
        laycan_from: Date, format YYYY-MM-DD indicates the earliest reported
            Laycan From (latest day of cancellation) across all fixtures.
        laycan_to: Date, format YYYY-MM-DD indicates the latest reported
            Laycan To (latest day of cancellation) across all fixtures.
        load_geo_id: Numeric ID corresponding to the id of the load geo asset
        load_name: String, name of the load geo asset
        load_taxonomy_id: 1-> GeoAsset, 2->  Port, 3-> Country, 4-> Level0,
            5-> Level1, 6-> Level2, 7-> Level3, -3-> Invalid, -2-> NotSet,
            -1-> Unknown
        load_taxonomy: String, the taxonomy of the load geo asset
        load_geo_id2:  Numeric ID corresponding to the id of the load geo
            asset
        load_name: String, name of the load geo asset
        load_name2: String, the taxonomy of the second load geo asset
        load_taxonomy_id2: 1-> GeoAsset, 2->  Port, 3-> Country, 4-> Level0,
            5-> Level1, 6-> Level2, 7-> Level3, -3-> Invalid, -2-> NotSet,
            -1-> Unknown
        load_taxonomy2: String, the taxonomy of the load geo asset
        discharge_geo_id: Numeric ID corresponding to the id of the discharge
            geo asset
        discharge_name: String, name of the discharge geo asset
        discharge_taxonomy_id: 1-> GeoAsset, 2->  Port, 3-> Country,
            4-> Level0, 5-> Level1, 6-> Level2, 7-> Level3, -3-> Invalid,
            -2-> NotSet, -1-> Unknown
        discharge_taxonomy: String, the taxonomy of the discharge geo asset
        discharge_geo_id2: Numeric ID corresponding to the id of the discharge
            geo
        discharge_name2: String, name of the discharge geo asset
        discharge_taxonomy_id2: 1-> GeoAsset, 2->  Port, 3-> Country,
            4-> Level0, 5-> Level1, 6-> Level2, 7-> Level3, -3-> Invalid,
            -2-> NotSet, -1-> Unknown
        discharge_taxonomy2: String, the taxonomy of the discharge geo asset
        cargo_type_id: numeric ID corresponding to the type of cargo the
            vessel carries in this voyage. For example 19-> Crude Oil,
            16->Fueloil, 9-> Naphtha, 135-> Unleaded Motor Spirit, 12-> Gasoil
        cargo_type: String, it corresponds to the estimated cargo type the
            vessel carries according to the specific voyage, AIS information,
            jetty the vessel may have visited or information coming from
            market reports.
        cargo_group_id: Numeric ID corresponding to the high-level cargo the
            vessel carries in this voyage, therefore called cargo group.
            For example 130000->Dirty, 120000-> Clean
        cargo_group: String, it corresponds to the estimated high-level cargo
            the vessel carries in this voyage, according to AIS information
            and jetties the vessel may have visited or information coming from
            market reports.
        quantity: Numeric, measured in kilotonnes [kt]. It is the cargo
            quantity reported in at least one of the market reports.
        quantity_buffer: Buffer on the agreed quantity.
        rate: Numeric, indicates the rate reported in at least one of the
            fixtures. If lump sum, the rate is reported in USD.
        rate_type: String, indicates the type of rate reported in at least
            one of the fixtures. Main types are "WS" for World Scale, "LS"
            for Lump Sum, "TCE" ($/day) for Time Charter Equivalent.
        ballast_bonus_value: Numeric, indicates the incentive or compensation
            paid to the ship owner for delivering the ship to the agreed
            delivery place. Derived from market info whenever available.
        ballast_bonus_type: String, indicates the currency of the ballast
            bonus, "$"(dollars).
        delivery_geo_id: Numeric ID corresponding to the id of the delivery
            geo asset
        delivery_name: String, name of the delivery geo asset
        delivery_taxonomy_id: 1-> GeoAsset, 2->  Port, 3-> Country,
            4-> Level0, 5-> Level1, 6-> Level2, 7-> Level3, -3-> Invalid,
            -2-> NotSet, -1-> Unknown
        delivery_taxonomy: String, the taxonomy of the delivery geo asset
        delivery_date_from: The start date of the delivery
        delivery_date_to: The end date of the delivery
        redelivery_from_geo_id: Numeric ID corresponding to the id of the
            redelivery from geo
        redelivery_from_name: String, name of the  redelivery from geo asset
        redelivery_from_taxonomy_id: 1-> GeoAsset, 2->  Port, 3-> Country,
            4-> Level0, 5-> Level1, 6-> Level2, 7-> Level3, -3-> Invalid,
            -2-> NotSet, -1-> Unknown
        redelivery_from_taxonomy: String, the taxonomy of the redelivery from
            geo asset
        redelivery_to_geo_id: Numeric ID corresponding to the id of the
            redelivery to geo asset
        redelivery_to_name: String, name of the  redelivery to geo asset
        redelivery_to_taxonomy_id: 1-> GeoAsset, 2->  Port, 3-> Country,
            4-> Level0, 5-> Level1, 6-> Level2, 7-> Level3, -3-> Invalid,
            -2-> NotSet, -1-> Unknown
        redelivery_to_taxonomy: String, the taxonomy of the redelivery to geo
            asset
        user_entries: The number of the user entries for the voyage
        full_fixtures: The number of full fixtures for the voyage
        partial_fixtures: The number of partial fixtures for the voyage
        is_coa: Boolean. Value is true if "COA" (Contract of Affreightment)
            is explicitly reported in at least one of the fixtures relative
            to the specific voyage
        is_owners_option: Boolean, indicating if owners option is agreed
        is_hold: Boolean. Value is true if "Hold" is explicitly reported in
            at least one of the fixtures relative to the specific voyage
        is_fio: Boolean, is free in and out. If true, charterer pays for
            loading and unloading
        sources: A list of the sources

    """

    fixture_status_id: Optional[int] = None
    fixture_status: Optional[str] = None
    charter_type_id: Optional[int] = None
    charter_type: Optional[str] = None
    fixture_date: Optional[datetime] = None
    charterer_id: Optional[int] = None
    charterer: Optional[str] = None
    laycan_from: Optional[datetime] = None
    laycan_to: Optional[datetime] = None
    load_geo_id: Optional[int] = None
    load_name: Optional[str] = None
    load_taxonomy_id: Optional[int] = None
    load_taxonomy: Optional[str] = None
    load_geo_id2: Optional[int] = None
    load_name2: Optional[str] = None
    load_taxonomy_id2: Optional[int] = None
    load_taxonomy2: Optional[str] = None
    discharge_geo_id: Optional[int] = None
    discharge_name: Optional[str] = None
    discharge_taxonomy_id: Optional[int] = None
    discharge_taxonomy: Optional[str] = None
    discharge_geo_id2: Optional[int] = None
    discharge_name2: Optional[str] = None
    discharge_taxonomy_id2: Optional[int] = None
    discharge_taxonomy2: Optional[str] = None
    cargo_type_id: Optional[int] = None
    cargo_type: Optional[str] = None
    cargo_group_id: Optional[int] = None
    cargo_group: Optional[str] = None
    quantity: Optional[int] = None
    quantity_buffer: Optional[int] = None
    rate: Optional[int] = None
    rate_type: Optional[str] = None
    ballast_bonus_value: Optional[int] = None
    ballast_bonus_type: Optional[str] = None
    delivery_geo_id: Optional[int] = None
    delivery_name: Optional[str] = None
    delivery_taxonomy_id: Optional[int] = None
    delivery_taxonomy: Optional[str] = None
    delivery_date_from: Optional[datetime] = None
    delivery_date_to: Optional[datetime] = None
    redelivery_from_geo_id: Optional[int] = None
    redelivery_from_name: Optional[str] = None
    redelivery_from_taxonomy_id: Optional[int] = None
    redelivery_from_taxonomy: Optional[str] = None
    redelivery_to_geo_id: Optional[int] = None
    redelivery_to_name: Optional[str] = None
    redelivery_to_taxonomy_id: Optional[int] = None
    redelivery_to_taxonomy: Optional[str] = None
    user_entries: Optional[int] = None
    full_fixtures: Optional[int] = None
    partial_fixtures: Optional[int] = None
    is_coa: Optional[bool] = None
    is_owners_option: Optional[bool] = None
    is_hold: Optional[bool] = None
    is_fio: Optional[bool] = None
    sources: Optional[Tuple[str, ...]] = None


@dataclass(frozen=True)
class Fixture:
    """Fixture information.

    Attributes:
        next_page_token: String. The key that should be used as a parameter
            of the token to retrieve the next page.
        is_matched: Boolean. This will be true if the market data item is
            matched to the corresponding voyage.
        is_load_matched: Boolean. This will be true if the load of the market
            data item is matched to the corresponding voyage.
        is_discharge_matched: Boolean. This will be true if the load of the
            market data item is matched to the corresponding voyage.
        fixture_status_id: 0-> OnSubs, 1-> FullyFixed, 2-> Failed,
            3-> Cancelled, 4-> Available, -2-> NotSet, -1-> Unknown
        fixture_status: String, based on the status of the market data item.
            Potential values are OnSubs, FullyFixed, Failed, Cancelled,
            Available
    """

    fixture_id: Optional[int] = None
    is_matched: Optional[bool] = None
    is_load_matched: Optional[bool] = None
    is_discharge_matched: Optional[bool] = None
    fixture_status_id: Optional[int] = None
    fixture_status: Optional[str] = None


@dataclass(frozen=True)
class VoyagesMarketData:
    """Contains information about a single fixture.

    Attributes:
        id: String. Uniquely identifies the market data result.
        voyage_id: String. Uniquely identifies the voyage.
        imo: A seven-digits number that uniquely identifies a ship and does
            not change when the ship's owner, country of registry or name of
            the vessel changes.
        voyage_number: Numeric, a counter of the voyages for the same IMO.
        vessel_name: The vessel name corresponding to that IMO at the time
            of that voyage.
        vessel_type_id: 0-> Empty, 1-> Tanker, 3-> Dry, 4-> Container,
            5-> Lng, 6-> Lpg, -2-> NotSet, -1-> Unknown
        vessel_type: Description of the type of the vessel, based on the
            carried cargo. Main categories are Tankers, Dry (bulk carriers),
            Containers, LNG and LPG.
        vessel_class_id: 60-> VLGCLpg, 61-> MidsizeLpg, 62-> HandyLpg,
            63-> SmallLpg, 69-> VLOC, 70-> Capesize, 72-> PostPanamaxDry,
            74-> PanamaxDry, 75-> Supramax, 76-> Handymax, 77-> Handysize,
            78-> ULCV, 79-> NewPanamaxContainer, 80-> PostPanamaxContainer,
            81-> PanamaxContainer, 82-> FeedermaxContainer,
            83-> FeederContainer, 84-> VLCC, 85-> Suezmax, 86-> Aframax,
            87-> PanamaxTanker, 88-> MR2, 89-> MR1, 90-> Small, 91-> LNGLng,
            92-> SmallDry, 94-> ULCC, 95-> SmallContainer
        vessel_class: Name of the vessel class the vessel belongs to.
            Assignment of a vessel to a certain VesselClass is based on the
            VesselType and the value of its Deadweight (if Tanker or Dry),
            its LiquidCap (if LNG/LPG) or its TEU (if Containers). For
            example, an Aframax is a Tanker vessel with Deadweight within the
            range 82kt - 125kt, while a Capesize is a Dry vessel with
            Deadweight within the range 120kt-220kt. LR2 are defined as
            Aframax, as only Deadweight is used to define vessel classes.
        trade_id: 1-> Crude, 2-> Product, 3-> Chemical, -2-> NotSet,
            -1-> Unknown
        trade: Additional attribute used to specify a Tanker vessel with finer
            granularity. It is derived by the last cargo carried by the vessel
            at the time of query. For example, an LR2 with fueloil as last
            cargo has VesselClass=Aframax and Trade=Product.
        commercial_operator_id: Numeric ID corresponding to the maritime
            company that manages the vessel commercially.
        commercial_operator: Name of the maritime company that manages the
            vessel commercially.
        deadweight: Numeric, measured in tonnes [t], often shortened as DWT,
            denotes the total carrying capacity of the vessel including cargo,
            ballast water, stores, provisions, crew and so on.
        year_built: Numeric, year format, the year the vessel was built.
        matched_fixture: Nested object containing additional information on
            the matched fixture.
        fixtures: Nested object containing information on fixtures for a given
            IMO and voyage.


    """

    id: Optional[str] = None
    voyage_id: Optional[str] = None
    imo: Optional[int] = None
    voyage_number: Optional[int] = None
    vessel_name: Optional[str] = None
    vessel_type_id: Optional[int] = None
    vessel_type: Optional[str] = None
    vessel_class_id: Optional[int] = None
    vessel_class: Optional[str] = None
    trade_id: Optional[int] = None
    trade: Optional[str] = None
    commercial_operator_id: Optional[int] = None
    commercial_operator: Optional[str] = None
    deadweight: Optional[int] = None
    year_built: Optional[int] = None
    matched_fixture: Optional[MatchedFixture] = None
    fixtures: Optional[Tuple[Fixture, ...]] = None


@dataclass(frozen=True)
class VoyagesMarketDataPagedResponse:
    """Paged response in nested format from the VoyagesMarketData API.

    Attributes:
        next_page_token: String. The key that should be used as a parameter
            of the token to retrieve the next page.
        next_request_token: String. Populated on the last page of
            incremental results and should be used in the next incremental
            update request.
        data: The structure that contains records retrieve for the current
            page.
    """

    next_page_token: Optional[str] = None
    next_request_token: Optional[str] = None
    data: Optional[Tuple[VoyagesMarketData, ...]] = None
