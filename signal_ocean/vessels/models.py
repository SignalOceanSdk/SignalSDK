"""Models instantiated by the vessels api."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class VesselClass:
    """Vessel class characteristics.

    Detailed characteristics of each vessel class, including its defining
    measurement and the range that corresponds to this vessel class.

    Attributes:
        id: The vessel class id e.g. 81 (refers to Panamax), 86 (Aframax), 85
            (Suezmax).
        vessel_type_id: Numeric ID corresponding to the different values of the
            VesselType field.  1-> Tanker, 3-> Dry, 4 -> Containers, 5
            ->LNG(Liquified Natural gas) , 6-> LPG(Liquified Petroleum Gas).
        from_size: The minimum value that corresponds to this vessel class
            (Deadweight/TEU/CubicSize).
        to_size: The maximum value that corresponds to this vessel class
            (Deadweight/TEU/CubicSize).
        name: The vessel class e.g. Panamax, Aframax, Suezmax.
        vessel_type: Description of the type of the vessel, based on the
            carried cargo. Main categories are Tankers, Dry (bulk carriers),
            Containers, LNG and LPG.
        defining_size: The attribute(DeadWeight, TEU, CubicSize) that defines
            the size of the vesselClass.
        size: The units of the DefiningSize attribute.  DeadWeight->
            kt(kilotons), TEU-> TEU, CubicSize-> cbm(cubic meters).
    """

    id: int
    vessel_type_id: int
    from_size: int
    to_size: int
    name: Optional[str] = None
    vessel_type: Optional[str] = None
    defining_size: Optional[str] = None
    size: Optional[str] = None


@dataclass(frozen=True)
class VesselType:
    """A vessel type.

    Attributes:
        id: The vessel type id, e.g. 1 -> Tanker, 3 -> Dry, 4 -> Containers,
            5 -> LNG (Liquified Natural gas),
            6-> LPG (Liquified Petroleum Gas).
        name: The vessel type name, e.g. Tanker, Dry, Containers,
            LNG (Liquified Natural gas), LPG (Liquified Petroleum Gas).
    """

    id: int
    name: str


@dataclass(frozen=True)
class Vessel:
    """Contains all details of a vessel.

    Attributes:
        imo: A seven-digits number that uniquely identifies a ship and does
            not change when the ship's owner, country of registry or name of
            the vessel changes.
        vessel_type_id: Numeric ID corresponding to the different values of
            the VesselType field.  1 -> Tanker, 3 -> Dry, 4 -> Containers,
            5 -> LNG(Liquified Natural gas), 6 -> LPG(Liquified Petroleum
            Gas), -2 -> NotSet, -1 -> Unknown
        built_for_trade_id: Numeric ID corresponding to the different values
            of the BuiltForTrade field.  1 -> Crude, 2 -> Product,
            3 -> Chemical, -2 -> NotSet, -1 -> Unknown
        trade_id: Numeric ID that takes the same values as the BuiltForTradeID
            field.  1 -> Crude, 2 -> Product, 3 -> Chemical,
            -2 -> NotSet, -1 -> Unknown
        vessel_class_id: 60-> VLGCLpg, 61-> MidsizeLpg, 62-> HandyLpg,
            63-> SmallLpg, 69-> VLOC, 70-> Capesize, 72-> PostPanamaxDry,
            74-> PanamaxDry, 75-> Supramax, 76-> Handymax, 77-> Handysize,
            78-> ULCV, 79-> NewPanamaxContainer, 80-> PostPanamaxContainer,
            81-> PanamaxContainer, 82-> FeedermaxContainer,
            83-> FeederContainer, 84-> VLCC, 85-> Suezmax, 86-> Aframax,
            87-> PanamaxTanker, 88-> MR2, 89-> MR1, 90-> Small, 91-> LNGLng,
            92-> SmallDry, 94-> ULCC, 95-> SmallContainer
        commercial_operator_id: Numeric ID corresponding to the maritime
            company that manages the vessel commercially.
        deadweight: Numeric, measured in tonnes [t], often shortened as DWT,
            denotes the total carrying capacity of the vessel including cargo,
            ballast water, stores, provisions, crew and so on.
        breadth_extreme: Numeric, measured in meters [m], denotes the width of
            a ship over the outside of all planking or plating at the widest
            frame.
        gross_rated_tonnage: Numeric, measured in register tons, often
            shortened as GRT, denotes the sum of all the closed and/or closable
            spaces.
        reduced_gross_tonnage: Numeric, measured in register tons, often
            shortened as RGT, denotes a measure applicable for open-top
            container ships and tankers with a double hull (ships equipped with
            segregated ballast tanks).This quantity can be used to compute
            various tonnage-based fees.
        net_rated_tonnage: Numeric, measured in register tons, often shortened
            as NRT, denotes the difference between the GRT and the sum of all
            spaces which are not used for the purpose for which the ship is
            built.
        draught: Numeric, measured in meters [m], denotes the distance between
            the ship’s keel and the waterline of the vessel. As the
            instantaneous draught of a vessel is a function of the vessel's
            loading status, this vessel characteristics refers to the maximum
            draught of the vessel.
        length_overall: Numeric, measured in meters [m], denotes the vessel's
            maximum length between the extremes points, forward and aft.
        moulded_depth: Numeric, measured in meters [m], denotes the vertical
            distance between the moulded base line and the top of the beams of
            the uppermost continuous deck.
        year_built: Numeric, year format, the year the vessel was built.
        geared: Boolean, denotes whether the vessel has cranes installed for
            handling its cargo or not.
        clean_dirty_willing: Boolean, indicates whether a tanker vessel is
            ‘willing’ to compete in the market complementary to the one shown
            in Trade. For example an LR willing dirty will have Trade=Product
            and CleanDirtyWilling=true.
        main_engine_manufacturer_id: Numeric ID corresponding to the different
            values of the MainEngine field.  1-> MAN B&W, 2-> Wartsila, 3->
            Mitsubishi.
        classification_register_id: The id of the classification register.
            Default value: -2.
        updated_date: Date, format YYYY-MM-DD HH:MM:SS, corresponding to the
            latest update.
        interline_coating: interline coating
        vessel_name: The current vessel name corresponding to that IMO.
        call_sign: Alphanumeric code that uniquely identifies a vessel and is
            used for radio communication with land based operators or stations
            and between the vessels.
        vessel_type: Description of the type of the vessel, based on the
            carried cargo.  Main categories are Tankers, Dry (bulk carriers),
            Containers, LNG and LPG.
        built_for_trade: Additional attribute to specify a Tanker vessel with
            finer granularity.  This classification is derived by the vessel
            characteristics only. It indicates the initial cargo the vessel was
            designed for, here called "trade". For example, an LR2 is a vessel
            of VesselClass Aframax and BuiltForTrade Clean.
        trade: Time-dependent version of the attribute BuiltForTrade. It is
            specified by the last cargo carried by the vessel at the time of
            query. For example, an LR2 with fueloil as last cargo has
            BuiltForTrade = Crude and Trade = Product.
        vessel_class: Name of the vessel class the vessel belongs to.
            Assignment of a vessel to a certain VesselClass is based on the
            VesselType and the value of its Deadweight (if Tanker or Dry), its
            LiquidCap (if LNG/LPG) or its TEU (if Containers).  For example, an
            Aframax is a Tanker vessel with Deadweight within the range 82kt -
            125kt, while a Capesize is a Dry vessel with Deadweight within the
            range 120kt-220kt. LR2 are defined as Aframax, as only Deadweight
            is used to define vessel classes.
        flag_code: ISO 3166-1 alpha-2 code representing the vessel's country of
            registration.
        flag: The country where the vessel has been registered and whose law is
            subject to.
        commercial_operator: Name of the maritime company that manages the
            vessel commercially.
        built_country_code: Two letters code representing the country where the
            vessel was built.
        built_country_name: String, the name of the country where the vessel
            was built.
        scrapped_date: Date, with format YYYY-MM-DD, indicates when the vessel
            was scrapped. If the vessel is active, ScrappedDate is null.
        shipyard_built_id: Numeric ID corresponding to the geo location where
            the vessel was built, for example the specific shipyard.
        shipyard_built_name: String, the name of the shipyard where the vessel
            was built, e.g. Hyundai Heavy Industries Co.
        ice_class: Alphanumeric code that denotes the vessel's additional level
            of strengthening as well as other arrangements that make navigation
            through frozen seas possible. For example 1A, 1D, etc.
        cranes_ton_capacity: Numeric, measured in tonnes [t], denotes the
            capacity of the vessel's cranes whenever applicable.
        teu: Numeric, measured in TEU (Twenty-Foot Equivalent Unit), denotes a
            volumetric measure of a container's cargo carrying capacity. Used
            for Containers, that is vessels with VesselType=4.
        te_u14: Numeric, denotes the capacity of the vessel measured in twenty-
            foot equivalent units (TEU) loaded at 14 tons.
        reefers: Numeric, denotes the capacity of the vessel measured in
            refrigerated twenty-foot equivalent units (TEU), i.e., the maximum
            number of refrigerated containers that could be carried.
        panama_canal_net_tonnage: Numeric, measured in register tons,
            volumetric measure derived by the NRT (NetRatedTonnage) and
            modified for Panama Canal purposes. Often used to compute tonnage-
            based fees.
        cubic_size: Numeric, measured in cubic meters [cbm] denotes the
            carrying capacity of Gas vessels (LNG, LPG). For tankers it is the
            volume of cargo tanks.
        scrubbers_date: Date, format YYYY-MM-DD HH:MM:SS, best estimate of the
            scrubbers installation date.
        summer_tpc: Numeric, measured in [metric tonnes/cm], acronym of Summer
            Tonnes Per Centimeter, denotes the cargo in metric tonnes (10^3 kg)
            needed to further increase the vessel's salt water draught by one
            centimeter.
        lightship_tonnes: The weight of the vessels without any cargo or
            bunkers. It is an important parameter to estimate the scrap value
            of the vessel as it represents the amount of steel that can be
            recycled.
        main_engine_manufacturer: String denoting the brand of the vessel's
            main engine.
        delivery_date: Date, with format YYYY-MM-DD, indicates when the vessel
            was delivered to the owner and commenced its first voyage.
        classification_register: The name of the organization that issued the
            vessel's classification certificate. Default value: Not set.
        number_of_holds: Numeric, the number of separate enclosed spaces within
            a ship designed for storing cargo.
        grain_capacity: This is the space available for a liquid-type cargo,
            like bulk grain, which can flow into every corner.
        bale_capacity: This is the space available for solid cargo. Bale space
            is usually about 7–10% less than grain space.
        gear_details: This value indicates the crane details of the vessel
        main_engine_kw: This value indicates the main engine's power in KW
        main_engine_rpm: This value indicates the main engine's revolutions
            per minute (RPM)
        air_draught: This value indicates the distance from the top of a
            vessel's highest point to its waterline
        deck_teu: This value indicates the number of containers that can be
            stacked on the deck of the vessel
        under_deck_teu: This value indicates the number of containers that can
            be carried in the vessel's holds ("under deck")
        suez_canal_net_tonnage: Numeric, measured in register tons, volumetric
            measure derived by the NRT (NetRatedTonnage) and modified for Suez
            Canal purposes. Often used to compute tonnage-based fees
        class_renewal_date: This value indicates the latest date of the
            vessel's “Class Renewal”, which is the official survey that all
            seagoing vessels that travel international must do every 5 years
        mewis_duct: The date the Becker Mewis Duct equipment was installed
        inert_gas_system: Boolean, indicates whether a vessel has inert gas
            system, which is a system of preventing any explosion in the cargo
            tanks of a tanker
        imo_type_1: The safest type of tanker, for most severe cargoes
        imo_type_2: Can carry more polluting cargoes than ImoRating3
        imo_type_3: Can carry cargoes that are not very polluting but need
            special containment(ex: edibles)
        stst_coating: STSS coating
        epoxy_coating: Epoxy coating
        zinc_coating: Zinc coating
        marineline_coating: Marineline coating
        crude_oil_washing: Crude Oil Washing system
        beneficial_owner_id: Numeric ID corresponding to the beneficial owner
            of the vessel
        beneficial_owner: Name of the beneficial owner of the vessel
    """

    imo: int
    vessel_type_id: int
    built_for_trade_id: int
    trade_id: int
    vessel_class_id: int
    commercial_operator_id: int
    deadweight: int
    breadth_extreme: int
    gross_rated_tonnage: int
    reduced_gross_tonnage: int
    net_rated_tonnage: int
    draught: float
    length_overall: float
    moulded_depth: float
    year_built: int
    geared: bool
    clean_dirty_willing: bool
    main_engine_manufacturer_id: int
    classification_register_id: int
    updated_date: datetime
    interline_coating: Optional[int] = None
    vessel_name: Optional[str] = None
    call_sign: Optional[str] = None
    vessel_type: Optional[str] = None
    built_for_trade: Optional[str] = None
    trade: Optional[str] = None
    vessel_class: Optional[str] = None
    flag_code: Optional[str] = None
    flag: Optional[str] = None
    commercial_operator: Optional[str] = None
    built_country_code: Optional[str] = None
    built_country_name: Optional[str] = None
    scrapped_date: Optional[datetime] = None
    shipyard_built_id: Optional[int] = None
    shipyard_built_name: Optional[str] = None
    ice_class: Optional[str] = None
    cranes_ton_capacity: Optional[int] = None
    teu: Optional[int] = None
    te_u14: Optional[int] = None
    reefers: Optional[int] = None
    panama_canal_net_tonnage: Optional[int] = None
    cubic_size: Optional[int] = None
    scrubbers_date: Optional[datetime] = None
    summer_tpc: Optional[float] = None
    lightship_tonnes: Optional[int] = None
    main_engine_manufacturer: Optional[str] = None
    delivery_date: Optional[datetime] = None
    classification_register: Optional[str] = None
    number_of_holds: Optional[int] = None
    grain_capacity: Optional[int] = None
    bale_capacity: Optional[int] = None
    gear_details: Optional[str] = None
    main_engine_kw: Optional[int] = None
    main_engine_rpm: Optional[int] = None
    air_draught: Optional[float] = None
    deck_teu: Optional[int] = None
    under_deck_teu: Optional[int] = None
    suez_canal_net_tonnage: Optional[int] = None
    class_renewal_date: Optional[datetime] = None
    mewis_duct: Optional[datetime] = None
    inert_gas_system: Optional[str] = None
    imo_type_1: Optional[str] = None
    imo_type_2: Optional[str] = None
    imo_type_3: Optional[str] = None
    stst_coating: Optional[int] = None
    epoxy_coating: Optional[int] = None
    zinc_coating: Optional[int] = None
    marineline_coating: Optional[int] = None
    crude_oil_washing: Optional[str] = None
    beneficial_owner_id: Optional[int] = None
    beneficial_owner: Optional[str] = None
