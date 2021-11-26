"""Models instantiated by the voyages api."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple


@dataclass(frozen=True)
class VoyageEventDetail:
    """Detailed information about a voyage events.

    Voyage event details provides information a such as a jetty stay
    or ship-to-ship operation.

    Attributes:
        id: String. Uniquely identifies the event detail.
        event_id: String. Uniquely identifies the event that this event detail
            relates to.
        event_detail_type: String, denotes the type of the event detail. For
            instance, "StS" indicates that the event is a ship-to-ship
            operation, while "Jetty" describes that the event took place in a
            jetty.
        arrival_date: Date, format YYYY-MM-DD HH:MM:SS. The beginning of the
            specific event. The arrival date of an event is calculated based on
            the first AIS point within the event. In the case of missing AIS
            data, the arrival date is derived based on the last reported
            location of the vessel before the event and the time without
            reported AIS information.
        sailing_date: Date, format YYYY-MM-DD HH:MM:SS. The end of the specific
            event. The sailing date of an event is calculated based on the last
            AIS point within the event. In the case of missing AIS data, the
            sailing date is derived based on the next reported location of the
            vessel after the event and the time without reported AIS
            information.
        start_time_of_operation: Date, format YYYY-MM-DD HH:MM:SS. Timestamp
            indicating the beginning of the operation described by the event
            detail. This is the timestamp of the first AIS point the vessel is
            tracked within a jetty or that is captured performing a ship-to-
            ship operation.
        end_time_of_operation: Date, format YYYY-MM-DD HH:MM:SS. Timestamp
            indicating the end of the operation described by the event detail.
            This is the timestamp of the final AIS point the vessel is tracked
            within a jetty or that is captured performing a ship-to-ship
            operation.
        geo_asset_id: Numeric ID corresponding to the geo asset in which the
            event took place. Geo assets represent maritime facilities such as
            terminals, anchorages and lightering zones. Multiple geo assets are
            grouped under the same port.
        geo_asset_name: Name of the GeoAsset in which the event took place. Geo
            assets represent maritime facilities such as terminals, anchorages
            and lightering zones. Multiple geo assets are grouped under the
            same port.
        latitude: Numeric, decimal value representing the latitude of the
            location where the event took place. The location of the vessel is
            identified from AIS data within the duration of the event or, in
            the case of missing AIS data, from the location of the GeoAsset in
            which the event took place. If the event represents an operation in
            a jetty or a STS operation, the latitude reports the location of
            the first AIS within the jetty or STS operation.
        longitude: Numeric, decimal value representing the longitude of the
            location where the event took place. The location of the vessel is
            identified from AIS data within the duration of the event or, in
            the case of missing AIS data, from the location of the GeoAsset in
            which the event took place. If the event represents an operation in
            a jetty or a STS operation, the longitude reports the location of
            the first AIS within the jetty or STS operation.
        other_vessel_imo: Numeric, Containing the IMO of the second vessel in
            case of ship-to-ship operation.
        other_vessel_name: String, Containing the name of the second vessel in
            case of ship-to-ship operation.
    """
    id: Optional[str] = None
    event_id: Optional[str] = None
    event_detail_type: Optional[str] = None
    arrival_date: Optional[datetime] = None
    sailing_date: Optional[datetime] = None
    start_time_of_operation: Optional[datetime] = None
    end_time_of_operation: Optional[datetime] = None
    geo_asset_id: Optional[int] = None
    geo_asset_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    other_vessel_imo: Optional[int] = None
    other_vessel_name: Optional[str] = None


@dataclass(frozen=True)
class VoyageEvent:
    """An event associated with a voyage of a vessel.

    Voyage events describe the start of the voyage, a stop or a port call that
    took place during this voyage.

    Attributes:
        id: String. Uniquely identifies the event.
        port_id: Numeric ID corresponding to the port in which the event took
            place. A port may be associated with multiple geo assets
            representing different terminals and anchorages within this port.
        voyage_id: String. Uniquely identifies the voyage that this event
            relates to.
        event_type: String. It can take values "Stop", "Portcall" or
            "VoyageStart".
        event_horizon: String. It can take "Historical", "Current" or "Future"
            values, depending on whether the event is in the past with
            reference point the latest AIS point of the vessel (ArrivalDate
            and SailingDate both in the past), is current (ArrivalDate in the
            past and SailingDate in the future) or future (both ArrivalDate
            and SailingDate in the future).
        purpose: String. It will be "Stop" if EventType="Stop" and "Start" if
            EventType="VoyageStart". If the event is a portcall, that is an
            operational stop, this field specifies the type of operation, like
            "Load", "Discharge" or "Dry dock".
        event_date: Date, format YYYY-MM-DD HH:MM:SS. The timestamp of the
            specific event, for instantaneous events e.g. VoyageStart
        arrival_date: Date, format YYYY-MM-DD HH:MM:SS. The beginning of the
            specific event. The arrival date of an event is calculated based on
            the first AIS point within the event. In the case of missing AIS
            data, the arrival date is derived based on the last reported
            location of the vessel before the event and the time without
            reported AIS information. If an event is associated with multiple
            event details, the arrival date of the event reports the arrival
            date of the first event detail associated with this event.
        sailing_date: Date, format YYYY-MM-DD HH:MM:SS. The end of the specific
            event. The sailing date of an event is calculated based on the last
            AIS point within the event. In the case of missing AIS data, the
            sailing date is derived based on the next reported location of the
            vessel after the event and the time without reported AIS
            information. If an event is associated with multiple event details,
            the sailing date of the event reports the sailing date of the final
            event detail associated with this event.
        latitude: Numeric, decimal value representing the latitude of the
            location where the event took place.
        longitude: Numeric, decimal value representing the longitude of the
            location where the event took place.
        geo_asset_id: Numeric ID corresponding to the geo asset in which the
            event took place. Geo assets represent maritime facilities such as
            terminals, anchorages and lightering zones. Multiple geo assets are
            grouped under the same port.
        geo_asset_name: Name of the GeoAsset in which the event took place. Geo
            assets represent maritime facilities such as terminals, anchorages
            and lightering zones. Multiple geo assets are grouped under the
            same port.
        port_name: Name of the port in which the event took place. A port may
            be associated with multiple geo assets representing different
            terminals and anchorages within this port.
        country_id: Numeric ID corresponding to the country in which the event
            took place.
        country: Name of the country in which the event took place.
        area_idlevel0: Numeric ID corresponding to the level 0 area in which
            the event took place. Level 0 areas offer a detailed breakdown of
            the globe to the areas of maritime interest. Examples of level 0
            areas include "Arabian Gulf", "US Gulf" and "East Mediterranean".
        area_name_level0: Name of the area in which the event took place. Level
            0 areas offer a detailed breakdown of the globe to the areas of
            maritime interest. Examples of level 0 areas include "Arabian
            Gulf", "US Gulf" and "East Mediterranean".
        area_idlevel1: Numeric ID corresponding to the area in which the event
            took place. Level 1 areas consist of one or multiple level 0 areas.
            For example, level 1 area "Mediterranean" groups together the level
            0 areas "West Mediterranean", "Central Mediterranean" and "East
            Mediterranean".
        area_name_level1: Name of the area in which the event took place. Level
            1 areas consist of one or multiple level 0 areas. For example,
            level 1 area "Mediterranean" groups together the level 0 areas
            "West Mediterranean", "Central Mediterranean" and "East
            Mediterranean".
        area_idlevel2: Numeric ID corresponding to the area in which the event
            took place. Level 2 areas consist of one or multiple level 1 areas.
            For example, level 2 area "Mediterranean/UK Continent" groups
            together the "Mediterranean" and "UK Continent" level 1 areas.
        area_name_level2: Name of the area in which the event took place. Level
            2 areas consist of one or multiple level 1 areas. For example,
            level 2 area "Mediterranean/UK Continent" groups together the
            "Mediterranean" and "UK Continent" level 1 areas.
        area_idlevel3: Numeric ID corresponding to the area in which the event
            took place. Level 3 areas the highest area grouping in our
            taxonomy. Examples of such areas are "Pacific America" or "Africa".
            These group together level 2 areas. For instance, "Pacific America"
            groups together the level 2 areas "West Coast North America", "West
            Coast Mexico", "West Coast Central America" and "West Coast South
            America".
        area_name_level3: Name of the area in which the event took place. Level
            3 areas the highest area grouping in our taxonomy. Examples of such
            areas are "Pacific America" or "Africa". These group together level
            2 areas. For instance, "Pacific America" groups together the level
            2 areas "West Coast North America", "West Coast Mexico", "West
            Coast Central America" and "West Coast South America".
        low_ais_density: Boolean, indicating whether there is no tracked AIS
            data for a duration higher that the time required for an operation.
        event_details: Specific details regarding the voyage events, e.g. a
            ship-to-ship operation or a jetty stay.
    """

    id: Optional[str] = None
    port_id: Optional[int] = None
    voyage_id: Optional[str] = None
    event_type: Optional[str] = None
    event_horizon: Optional[str] = None
    purpose: Optional[str] = None
    event_date: Optional[datetime] = None
    arrival_date: Optional[datetime] = None
    sailing_date: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geo_asset_id: Optional[int] = None
    geo_asset_name: Optional[str] = None
    port_name: Optional[str] = None
    country_id: Optional[int] = None
    country: Optional[str] = None
    area_idlevel0: Optional[int] = None
    area_name_level0: Optional[str] = None
    area_idlevel1: Optional[int] = None
    area_name_level1: Optional[str] = None
    area_idlevel2: Optional[int] = None
    area_name_level2: Optional[str] = None
    area_idlevel3: Optional[int] = None
    area_name_level3: Optional[str] = None
    low_ais_density: Optional[bool] = None
    event_details: Optional[Tuple[VoyageEventDetail, ...]] = None


@dataclass(frozen=True)
class Voyage:
    """Contains information about a single voyage of a vessel.

    Attributes:
        imo: A seven-digits number that uniquely identifies a ship and does not
            change when the ship's owner, country of registry or name of the
            vessel changes.
        voyage_number: Numeric, a counter of the voyages for the same IMO.
        vessel_type_id: Numeric ID corresponding to the different values of the
            VesselType field.  1-> Tanker, 3-> Dry, 4 -> Containers, 5 ->LNG
            (Liquified Natural gas) , 6-> LPG (Liquified Petroleum Gas).
        vessel_class_id: Numeric ID corresponding to the different vessel
            classes of a certain vessel type.
        vessel_status_id: Numeric ID that takes the following values  1 ->
            Voyage, 2 -> Breaking, 3 -> Domestic Trade, 4-> FPSO, 5-> FPSO
            Conversion, 6-> Inactive, 7-> Storage Vessel, 9-> Conversion.
        commercial_operator_id: Numeric ID corresponding to the maritime
            company that manages the vessel commercially.
        deleted: Boolean. This will be true if the voyage has been deleted from
            our database.
        events: The events that took place during the voyage.
        id: String. Uniquely identifies the voyage.
        horizon: String. It can take "Historic", "Current" or "Future" values,
            depending on whether the voyage event is in the past (StartDate and
            EndDate both in the past), is current (StartDate in the past and
            EndDate in the future) or future (both StartDate and EndDate in the
            future). Note: the notions of "past", "current" and "future" are
            not derived by the current date, but by the comparison between the
            voyage dates and the latest received AIS for that specific vessel.
        latest_received_ais: Date, format YYYY-MM-DD HH:MM:SS. The most recent
        AIS update for the vessel. It is used to define the horizon of a voyage
            and its events.
        vessel_name: The vessel name corresponding to that IMO at the time of
            that voyage.
        vessel_type: Description of the type of the vessel, based on the
            carried cargo. Main categories are Tankers, Dry (bulk carriers),
            Containers, LNG and LPG.
        vessel_class: Name of the vessel class the vessel belongs to.
            Assignment of a vessel to a certain VesselClass is based on the
            VesselType and the value of its Deadweight (if Tanker or Dry), its
            LiquidCap (if LNG/LPG) or its TEU (if Containers).   For example,
            an Aframax is a Tanker vessel with Deadweight within the range 82kt
            - 125kt, while a Capesize is a Dry vessel with Deadweight within
            the range 120kt-220kt. LR2 are defined as Aframax, as only
            Deadweight is used to define vessel classes.
        trade: Additional attribute used to specify a Tanker vessel with finer
            granularity. It is derived by the last cargo carried by the vessel
            at the time of query.  For example, an LR2 with fueloil as last
            cargo has VesselClass=Aframax and Trade=Product.
        trade_id: For Tankers only. Numeric ID that takes the following values
            1 -> Crude, 2 -> Product, 3 -> Chemical.
        vessel_status: String identifying the status of a vessel. The active
            and most common status is the "Voyage" one, the one in which the
            vessel continuously sails and performs operations. The other
            statuses are used for specific purposes different than voyage.
        commercial_operator: Name of the maritime company that manages the
            vessel commercially.
        start_date: Date, format YYYY-MM-DD HH:MM:SS. The beginning of the
            specific voyage. The start of a voyage is set as the end of the
            previous voyage (if existing) or the first received AIS (for a new
            building). Voyages are consecutive and with no breaks in between,
            therefore a vessel is always in a voyage.
        first_load_arrival_date: Date, format YYYY-MM-DD HH:MM:SS. The time
            of arrival for the first load in the voyage. Indicates the
            transition from Ballast to Laden.
        end_date: Date, format YYYY-MM-DD HH:MM:SS. The end of the specific
            voyage. The end of a voyage is set as the sailing date (or
            completion date) from the port where the vessel discharged for the
            last time.
        charterer_id: Numeric ID corresponding to the company reported as
            charterer in at least one of the fixtures.
        charterer: String, name of the company reported as charterer in at
            least one of the fixtures.
        rate: Numeric, indicates the rate reported in at least one of the
            fixtures. If lump sum, the rate is reported in USD.
        rate_type: String, indicates the type of rate reported in at least one
            of the fixtures. Main types are "WS" for World Scale or "LS" for
            Lump Sum.
        ballast_bonus: .
        ballast_bonus_type: .
        cargo_type_id: Numeric ID corresponding to the type of cargo the vessel
            carries in this voyage. For example 19-> Crude Oil, 16->Fueloil,
            9-> Naphtha, 135-> Unleaded Motor Spirit, 12-> Gasoil.
        cargo_type: String, it corresponds to the estimated cargo type the
            vessel carries according to the specific voyage, AIS information,
            jetty the vessel may have visited or information coming from market
            reports.
        cargo_group_id: Numeric ID corresponding to the high-level cargo the
            vessel carries in this voyage, therefore called cargo group. For
            example 130000->Dirty, 120000-> Clean.
        cargo_group: String, it corresponds to the estimated high-level cargo
            the vessel carries in this voyage, according to AIS information and
            jetties the vessel may have visited or information coming from
            market reports.
        cargo_type_source: String, it specifies the source of CargoType and
            CargoGroup. If market reports are available this filed takes value
            "MarketInfo". If no market reports are available for this voyage,
            the cargo is estimated based on AIS and visited jetties. Market
            info are considered more accurate and reliable, whenever available.
        quantity: Numeric, measured in kilotonnes [kt]. It is the cargo
            quantity reported in at least one of the market reports.
        laycan_from: Date, format YYYY-MM-DD indicates the earliest reported
            Laycan From (latest day of cancellation) across all fixtures.
        laycan_to: Date, format YYYY-MM-DD indicates the latest reported Laycan
            To (latest day of cancellation) across all fixtures.
        fixture_status_id: Numeric ID corresponding to the different values of
            the FixtureStatus field.   0-> OnSubs, 1-> FullyFixed, 2 -> Failed,
            3 -> Cancelled , 4-> Available, 5-> PossFixed,
            -2 -> NotSet, -1 -> Unknown.
        fixture_status: String denoting the commercial status of a fixture if
            explicitly mentioned, like ffxd for fully fixed or subs for on
            subs.
        fixture_date: Date, format YYYY-MM-DD HH:MM:SS. Details the date of the
            first fixture reporting the specific voyage.
        fixture_is_coa: Boolean. Value is true if "COA" (Contract of
            Affreightment) is explicitly reported in at least one of the
            fixtures relative to the specific voyage.
        fixture_is_hold: Boolean. Value is true if "Hold" is explicitly
            reported in at least one of the fixtures relative to the specific
            voyage.
        is_implied_by_ais: Boolean. This will be true if the voyage is implied
            from AIS.
        has_manual_entries: Boolean. True if the fused matched fixture on a
            voyage contains at least one (partial or full) fixture input by a
            user. It indicates that there is additional information input by a
            user in addition to what received through market reports only.
        ballast_distance: Numeric. Travelled distance in nautical miles between
            the last discharge port of the previous voyage and the first load
            port of the current voyage. It is computed based on AIS data.
            It includes the whole period between the two port calls and non
            operational stops as well. Accuracy depends on AIS coverage.
        predicted_ballast_distance: Numeric, Computed distance of the ballast
            leg based on our distance model, in nautical miles. For current
            voyage, when vessel is ballast, it is the remaining distance
            between the vessel position and the first load port. For
            historical legs PredictedBallastDistance is empty.
        laden_distance: Numeric. Travelled distance in nautical miles between
            the first load port and the last discharge port of the same voyage.
            It is computed based on AIS data. Accuracy depends on AIS coverage.
        predicted_laden_distance: Numeric, Computed distance of the laden leg
            based on our distance model, in nautical miles. For current voyage,
            when vessel is laden, it is the remaining distance between the
            vessel position and the last discharge port. For historical legs
            PredictedLadenDistance is empty.
    """
    imo: int
    voyage_number: int
    vessel_type_id: Optional[int] = None
    vessel_class_id: Optional[int] = None
    vessel_status_id: Optional[int] = None
    commercial_operator_id: Optional[int] = None
    deleted: Optional[bool] = False
    events: Optional[Tuple[VoyageEvent, ...]] = None
    id: Optional[str] = None
    horizon: Optional[str] = None
    latest_received_ais: Optional[datetime] = None
    vessel_name: Optional[str] = None
    vessel_type: Optional[str] = None
    vessel_class: Optional[str] = None
    trade: Optional[str] = None
    trade_id: Optional[int] = None
    vessel_status: Optional[str] = None
    commercial_operator: Optional[str] = None
    start_date: Optional[datetime] = None
    first_load_arrival_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    charterer_id: Optional[int] = None
    charterer: Optional[str] = None
    rate: Optional[float] = None
    rate_type: Optional[str] = None
    ballast_bonus: Optional[float] = None
    ballast_bonus_type: Optional[str] = None
    cargo_type_id: Optional[int] = None
    cargo_type: Optional[str] = None
    cargo_group_id: Optional[int] = None
    cargo_group: Optional[str] = None
    cargo_type_source: Optional[str] = None
    quantity: Optional[float] = None
    laycan_from: Optional[datetime] = None
    laycan_to: Optional[datetime] = None
    fixture_status_id: Optional[int] = None
    fixture_status: Optional[str] = None
    fixture_date: Optional[datetime] = None
    fixture_is_coa: Optional[bool] = None
    fixture_is_hold: Optional[bool] = None
    is_implied_by_ais: Optional[bool] = None
    has_manual_entries: Optional[bool] = None
    ballast_distance: Optional[float] = None
    predicted_ballast_distance: Optional[float] = None
    laden_distance: Optional[float] = None
    predicted_laden_distance: Optional[float] = None


@dataclass(frozen=True)
class VoyageGeo:
    """Information about a geo asset object associated with a voyage.

    Attributes:
        id: Numeric ID of the geo asset. Geo assets represent maritime
            facilities such as terminals, anchorages and lightering zones.
            Multiple geo assets are grouped under the same port.
        name: Name of the geo asset. Geo assets represent maritime facilities
            such as terminals, anchorages and lightering zones. Multiple geo
            assets are grouped under the same port.
        port_id: Numeric ID corresponding to the port. A port may be associated
            with multiple geo assets representing different terminals and
            anchorages within this port.
        port_name: Name of the port. A port may be associated with multiple geo
            assets representing different terminals and anchorages within this
            port.
        country_id: Numeric ID corresponding to the country of the geo asset.
        country: Name of the country of the geo asset.
        area_idlevel0: Numeric ID corresponding to the level 0 area of the geo
            asset. Level 0 areas offer a detailed breakdown of the globe to the
            areas of maritime interest. Examples of level 0 areas include
            "Arabian Gulf", "US Gulf" and "East Mediterranean".
        area_name_level0: Name of the level 0 area of the geo asset. Level 0
            areas offer a detailed breakdown of the globe to the areas of
            maritime interest. Examples of level 0 areas include "Arabian
            Gulf", "US Gulf" and "East Mediterranean".
        area_idlevel1: Numeric ID corresponding to the level 1 area of the geo
            asset. Level 1 areas consist of one or multiple level 0 areas. For
            example, level 1 area "Mediterranean" groups together the level 0
            areas "West Mediterranean", "Central Mediterranean" and "East
            Mediterranean".
        area_name_level1: Name of the level 1 area of the geo asset. Level 1
            areas consist of one or multiple level 0 areas. For example, level
            1 area "Mediterranean" groups together the level 0 areas "West
            Mediterranean", "Central Mediterranean" and "East Mediterranean".
        area_idlevel2: Numeric ID corresponding to the level 2 area of the geo
            asset. Level 2 areas consist of one or multiple level 1 areas. For
            example, level 2 area "Mediterranean/UK Continent" groups together
            the "Mediterranean" and "UK Continent" level 1 areas.
        area_name_level2: Name of the level 2 area of the geo asset. Level 2
            areas consist of one or multiple level 1 areas. For example, level
            2 area "Mediterranean/UK Continent" groups together the
            "Mediterranean" and "UK Continent" level 1 areas.
        area_idlevel3: Numeric ID corresponding to the level 3 area of the geo
            asset. Level 3 areas the highest area grouping in our taxonomy.
            Examples of such areas are "Pacific America" or "Africa". These
            group together level 2 areas. For instance, "Pacific America"
            groups together the level 2 areas "West Coast North America", "West
            Coast Mexico", "West Coast Central America" and "West Coast South
            America".
        area_name_level3: Name of the level 3 area of the geo asset. Level 3
            areas the highest area grouping in our taxonomy. Examples of such
            areas are "Pacific America" or "Africa". These group together level
            2 areas. For instance, "Pacific America" groups together the level
            2 areas "West Coast North America", "West Coast Mexico", "West
            Coast Central America" and "West Coast South America".
    """
    id: Optional[int] = None
    name: Optional[str] = None
    port_id: Optional[int] = None
    port_name: Optional[str] = None
    country_id: Optional[int] = None
    country: Optional[str] = None
    area_idlevel0: Optional[int] = None
    area_name_level0: Optional[str] = None
    area_idlevel1: Optional[int] = None
    area_name_level1: Optional[str] = None
    area_idlevel2: Optional[int] = None
    area_name_level2: Optional[str] = None
    area_idlevel3: Optional[int] = None
    area_name_level3: Optional[str] = None


@dataclass(frozen=True)
class VoyagesFlat:
    """Voyages with additional information in flat format.

    Attributes:
        voyages: List of voyages.
        events: List of events that relate to the voyages.
        event_details: List of event details that relate to the events.
        geos: Geo asset data linked in events or event details.
    """
    voyages: Optional[Tuple[Voyage, ...]] = None
    events: Optional[Tuple[VoyageEvent, ...]] = None
    event_details: Optional[Tuple[VoyageEventDetail, ...]] = None
    geos: Optional[Tuple[VoyageGeo, ...]] = None


@dataclass(frozen=True)
class VoyagesPagedResponse:
    """Paged response for voyages in nested format from the Voyages API.

    Attributes:
        next_page_token: String. The key that should be used as a parameter of
            the token to retrieve the next page.
        next_request_token: String. Populated on the last page of incremental
            results and should be used in the next incremental update request.
        data: The structure that contains records retrieve for the current
            page.
    """
    next_page_token: Optional[str] = None
    next_request_token: Optional[str] = None
    data: Optional[Tuple[Voyage, ...]] = None


@dataclass(frozen=True)
class VoyagesFlatPagedResponse:
    """Paged response for voyages in flat format from the Voyages API.

    Attributes:
        next_page_token: String. The key that should be used as a parameter of
            the token to retrieve the next page.
        next_request_token: String. Populated on the last page of incremental
            results and should be used in the next incremental update request.
        data: The structure that contains records retrieve for the current
            page.
    """
    next_page_token: Optional[str] = None
    next_request_token: Optional[str] = None
    data: Optional[VoyagesFlat] = None
