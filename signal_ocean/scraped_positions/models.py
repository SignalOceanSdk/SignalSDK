"""Models instantiated by the scraped positions api."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

from signal_ocean.scraped_data.scraped_data_api import ScrapedDataResponse


@dataclass(frozen=True)
class ScrapedPosition:
    """Detailed information about a scraped position.

    Attributes:
        position_id: Integer. A unique identifier of the position line.
        message_id: Integer. A unique identifier of the message containing the
            specific position. A message can contain more than one positions.
        external_message_id: String. It serves as a unique identifier for a
            message, supplied by any company that has integrated with Signal.
        parsed_part_id: Integer. A unique identifier for each email part. The
            email body and each attachment are considered different parsed
            parts. For an example the email body and its pdf attachment have
            same MessageID and different ParsedPartID.
        line_from: Nullable integer. The starting line from which the position
            is extracted. The email subject counts as  line 0 and the body
            content starts from line 1.
        line_to: Nullable integer. The final line from which the position is
            extracted. For single line positions LineFrom is equal to LineTo.
            For descriptive positions that span across multiple lines we have
            LineTo>LineFrom. These two numbers help the user identify which
            part of the text has been used to extract the position data.
        source: String. It describes the source of the information. Our system
            allows the user to inject data in many different ways, namely
            through email (Source='Email'), through Slack channels
            (Source='Slack') or through manual contributions directly from our
            frontend platform TSOP (Source='User').
        updated_date: String, format YYYY-MM-DD HH:MM:SS, UTC timezone. Date on
            which the position has been reevaluated for the last time. In case
            of an email received by a broker one month ago and reprocessed
            through our engine today, this date will be today's.
        received_date: String, format YYYY-MM-DD HH:MM:SS, UTC timezone. Date
            on which the position has been injected into our system and
            processed.
        is_deleted: Boolean. This value is true if the position is marked as
            Deleted.
        low_confidence: Boolean. This value is true when the data extraction
            process does not return as output some fields that we believe to
            be more important than others in business terms. These fields are
            called critical fields. The value is true if at least one of the
            critical fields is missing.For example missing charterer or laycan.
        scraped_vessel_name: String. The vessel name as reported in the
            position line, i.e. 'Signal Alpha', 'Cpt A Stellatos',
            'Genco Tiberius'. 'TBN' can also be found.
        scraped_deadweight: String. The dead weight of the vessel as
            reported in the position line, i.e. '150249', '167'.
        scraped_year_built: String. The year built of the vessel as reported in
            the position line, i.e. '2004', '09'.
        imo: Integer. The seven-digits number that uniquely identifies the ship
            reported in the position. It is the result of our internally
            developed Vessel Mapper model.
        vessel_name: String. It is the current vessel name corresponding to the
            IMO mentioned above. Provided to better specify the vessel and its
            particulars. Source: our internal Vessel Database.
        deadweight: Integer. The dead weight in tonnes [t] corresponding to the
            IMO mentioned above.
        year_built: Integer, YYYY format. The year the vessel was built.
            Source: our internal Vessel Database.
        liquid_capacity: Integer, measured in cbm [cbm]. The liquid capacity of
            the IMO mentioned above. Source: our internal Vessel Database.
        vessel_type_id: Integer. Numeric ID corresponding to the different
            values of the VesselType field. 1-> Tanker, 3-> Dry,
            4 -> Containers, 5 ->LNG (Liquified Natural gas),
            6-> LPG (Liquified Petroleum Gas).
        vessel_type: String. Description of the type of the vessel
            (VesselTypeID), based on the carried cargo. Main categories are
            Tankers, Dry (bulk carriers), Containers, LNG and LPG.
        vessel_class_id: Integer. It is an ID corresponding to the different
            vessel classes of a certain vessel type, as split according to our
            internal Vessel Database. For example 84->VLCC, 85->Suezmax,
            70->Capesize.
        vessel_class: String. Name of the vessel class the vessel belongs to.
            Assignment of a vessel to a certain VesselClass is based on the
            VesselType and the value of its Deadweight (if Tanker or Dry), its
            LiquidCap (if LNG/LPG) or its TEU (if Containers). For example, an
            Aframax is a Tanker vessel with Deadweight within the range
            82kt - 125kt, while a Capesize is a Dry vessel with Deadweight
            within the range 120kt-220kt. LR2 are defined as Aframax, as only
            Deadweight is used to define vessel classes.
        scraped_open_date: String. The open date of the position as reported in
            the original text. It is often reported as a date range, e.g.
            '13/16 April'.
        open_date_from: Date, format YYYY-MM-DD. The mapped date corresponding
            to the beginning of the open date range.
        open_date_to: Date, format YYYY-MM-DD. The mapped date corresponding to
            the end of the open date range.
        scraped_open_port: String. The open location reported in the original
            text of the position. It is very often shortened, very compact and
            can refer to terminals, ports, countries or wider areas. Examples:
            'singgi' for Singgi, 'rt' for Ras Tanura, 'waf' for West Africa.
        open_geo_id: Integer. It is the internal ID of the mapped open location
            reported in the position. Our models convert and map a scraped
            string containing geo information to a specific entity of the
            Signal's proprietary geofencing structure. Each geo entity is
            identified by a taxonomy, an ID and a name. Examples: the string
            'bonny' is mapped to a geo asset with name 'Bonny', ID 3679 and
            taxonomy Port (TaxonomyID=2); the string 'nigeria' is mapped to a
            geoasset with name 'Nigeria', ID 171 and taxonomy Country
            (TaxonomyID=3); the string 'wafr' is mapped to a geoasset with name
            'Africa Atlantic Coast', ID 24772 and taxonomy Level0
            (TaxonomyID=4).
        open_name: String. The name of the Signal geo entity related to the
            reported open location of the position.Examples: 'Bonny',
            'Nigeria', 'Africa Atlantic Coast', 'Arabian Gulf', 'Singapore',
            'East Coast Mexico'.
        open_taxonomy_id: Integer. An internal ID corresponding to each
            taxonomy, the level of geo details, from 1 to 7. A terminal
            (geoasset) has the lowest taxonomy (TaxonomyID=1), a port has
            TaxonomyID=2, while countries and wider areas have higher taxonomy
            (TaxonomyID>=3). Examples of Level 0 areas (TaxonomyID=4) include
            'Arabian Gulf', 'US Gulf' and 'East Mediterranean'. Level 1 areas
            (TaxonomyID=5) consist of multiple level 0 areas (TaxonomyID=4).
            For example, level 1 area 'Mediterranean' groups together the
            level 0 areas 'West Mediterranean', 'Central Mediterranean' and
            'East Mediterranean'. Level 2 areas (TaxonomyID=6) consist of
            multiple level 1 areas (TaxonomyID=4). For example, level 2 area
            'Mediterranean/UK Continent' groups together the 'Mediterranean'
            and 'UK Continent' level 1 areas. Level 3 areas (TaxonomyID=7) are
            the highest area grouping in our taxonomy and consist of multiple
            level 2 areas (TaxonomyID=6). Examples of such areas are
            'Pacific America' or 'Africa'. These group together level 2 areas.
            For instance, 'Pacific America' groups together the level 2 areas
            'West Coast North America', 'West Coast Mexico',
            'West Coast Central America' and 'West Coast South America'.
        open_taxonomy: String. The extended name identifying the TaxonomyID.
            Possible values are: GeoAsset-> 1, Port -> 2, Country-> 3,
            Level0->4, Level1->5, Level2->6, Level3->7.
        scraped_commercial_operator: String. The position commercial operator
            as reported in the original text. Examples: 'aet', 'thenamaris',
            'bpcl'
        commercial_operator_id: Integer. Numeric ID corresponding to the
            commercial operator company that it is reported in the line. We use
            an internal mapper to find the correspondence between the reported
            string and our database.
        commercial_operator: String. The company name corresponding to the
            CommercialOperator field. Provided to better specify the company
            involved in the business. Source: our internal Company Database.
        scraped_cargo_type: String. The position cargo type as reported in the
            original text, often shortened. Examples: 'nhc', 'ulsd', 'ums',
            'nap', 'go'.
        cargo_type_id: Integer. It is an internal ID corresponding to the
            mapped cargo type of the position. A proprietary model is
            responsible to match the reported cargo type string to a specific
            cargo type in our hierarchy. Examples: 19-> Crude Oil, 16->Fueloil,
            9-> Naphtha, 135-> Unleaded Motor Spirit, 12-> Gasoil,
            60-> 'Ultra Low Sulphur Diesel (ULSD 10ppm)'.
        cargo_type: String. The extended name corresponding to the CargoTypeID
            field. Source: our internal CargoTypes database.
        cargo_type_group_id: Integer. Numeric ID corresponding to the
            high-level cargo type of the position cargo type. It is provided to
            group positions and facilitate analytics. Examples: 130000->Dirty,
            120000-> Clean, 110000->IMO.
        cargo_type_group: String. The extended name corresponding to the
            CargoGroupID field. Source: our internal CargoTypes database.
        scraped_last_cargo_types: String. The position last cargo types as
            reported in the original text. Examples: 'ums/palm/go',
            'ums/ulsd/jet+nap', 'salt/limestone/coal'.
        last_cargo_types_ids: List of Lists. Contains the internal ID [Id] and
            TaxonomyID [TId] corresponding to the mapped cargo types report
            within last cargo types on position. Each list represents the cargo
            types of each voyage and contains dicts with [Id] and [TId] for
            every cargo type of the voyage. For example for
            ScrapedLastCargoTypes field that contains 'ums/ulsd/jet+nap'
            corresponding LastCargoTypesIDs field contains
            '[[{'Id': 135, 'TId': 0}], [{'Id': 60, 'TId': 0}],
                [{'Id': 14, 'TId': 1}, {'Id': 9, 'TId': 1}]]'
            First voyage: ScrapedLastCargoTypes='ums' corresponds to
                LastCargoTypesIDs=[{'Id': 135, 'TId': 0}]
            Second voyage: ScrapedLastCargoTypes='ulsd' corresponds to
                LastCargoTypesIDs=[{'Id': 60, 'TId': 0}]
            Third voyage: ScrapedLastCargoTypes='jet+nap' corresponds
                to LastCargoTypesIDs=[{'Id': 14, 'TId': 1},
                {'Id': 9, 'TId': 1}]]
        last_cargo_types: String. The extended names corresponding to each
            CargoTypeID on LastCargoTypeIDs. Voyages are separated with '/'.
            Cargo Types within same voyage are separated with '+'.
            Example:
            ScrapedLastCargoTypes='ums/ulsd/jet+nap'
            LastCargoTypesIDs=[[{'Id': 135, 'TId': 0}], [{'Id': 60, 'TId': 0}],
                [{'Id': 14, 'TId': 1}, {'Id': 9, 'TId': 1}]]
            LastCargoTypes='Unleaded Motor Spirit / Ultra Low Sulphur Diesel
                (ULSD 10ppm) / Jet + Naphtha'
        has_ballast: Boolean. This value is true when 'ballast', 'in ball' or
            'blst' explicitly reported in the original text of the position.
        has_dry_dock: Boolean. This value is true when 'dd', 'exdd' or 'xdd'
            explicitly reported in the original text of the position.
        has_if: Boolean. This value is true when 'if' or 'poss'
            explicitly reported in the original text of the position.
        has_on_hold: Boolean. This value is true when 'hold'
            explicitly reported in the original text of the position.
        has_on_subs: Boolean. This value is true when 'fxd', 'subs' or '-s-'
            explicitly reported in the original text of the position.
        has_prompt: Boolean. This value is true when 'ppt', 'prompt' or 'spot'
            explicitly reported in the original text of the position.
        has_uncertain: Boolean. This value is true when 'unc' or 'uncertain'
            explicitly reported in the original text of the position.
        is_position_list: Boolean. This value is true if the source of position
            is the company that commercially manages of the vessel.
        content: String. The full content of the position. For a single line
            position it is the line content. For multi line positions it is the
            collection of all the relevant parts of the text.
        subject: String. The email subject of the position. This field has
            content when Source="Email".
        sender: String. Our own mapping of the shipping company sending out the
            market report through email. This string helps grouping emails sent
            by the same organization, but from different domains. It is often
            the case for big organizations operating worldwide. For example
            Sender= 'SSY' for both domains 'ssysin.com' and 'ssy.co'.
        is_private: Boolean. A position is private if injected by a user into
            his own private account within TSOP. A user can provide private
            information through email forwarding or through Slack. Private
            position information stay in the account, are accessible by the
            account users only (people within the same company) and are the
            most valuable ones.
    """

    # entity details
    position_id: int
    message_id: Optional[int] = None
    external_message_id: Optional[str] = None
    parsed_part_id: Optional[int] = None
    line_from: Optional[int] = None
    line_to: Optional[int] = None
    source: Optional[str] = None
    updated_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    low_confidence: Optional[bool] = False

    # vessel
    scraped_vessel_name: Optional[str] = None
    scraped_deadweight: Optional[str] = None
    scraped_year_built: Optional[str] = None
    imo: Optional[int] = None
    vessel_name: Optional[str] = None
    deadweight: Optional[int] = None
    year_built: Optional[int] = None
    liquid_capacity: Optional[int] = None
    vessel_type_id: Optional[int] = None
    vessel_type: Optional[str] = None
    vessel_class_id: Optional[int] = None
    vessel_class: Optional[str] = None

    # open date
    scraped_open_date: Optional[str] = None
    open_date_from: Optional[datetime] = None
    open_date_to: Optional[datetime] = None

    # open port
    scraped_open_port: Optional[str] = None
    open_geo_id: Optional[int] = None
    open_name: Optional[str] = None
    open_taxonomy_id: Optional[int] = None
    open_taxonomy: Optional[str] = None

    # commercial operator
    scraped_commercial_operator: Optional[str] = None
    commercial_operator_id: Optional[int] = None
    commercial_operator: Optional[str] = None

    # cargo type
    scraped_cargo_type: Optional[str] = None
    cargo_type_id: Optional[int] = None
    cargo_type: Optional[str] = None
    cargo_type_group_id: Optional[int] = None
    cargo_type_group: Optional[str] = None

    # last cargoes
    scraped_last_cargo_types: Optional[str] = None
    last_cargo_types_ids: Optional[str] = None
    last_cargo_types: Optional[str] = None

    # position indicators
    has_ballast: Optional[bool] = False
    has_dry_dock: Optional[bool] = False
    has_if: Optional[bool] = False
    has_on_hold: Optional[bool] = False
    has_on_subs: Optional[bool] = False
    has_prompt: Optional[bool] = False
    has_uncertain: Optional[bool] = False
    is_position_list: Optional[bool] = False

    # content
    content: Optional[str] = None
    subject: Optional[str] = None

    # sender
    sender: Optional[str] = None

    # debug info
    is_private: Optional[bool] = False


@dataclass(frozen=True)
class ScrapedPositionsResponse(ScrapedDataResponse[ScrapedPosition]):
    """Paged response for scraped positions from the Scraped Positions API.

    Attributes:
        next_page_token: String. The key that should be used as a parameter of
            the token to retrieve the next page.
        data: A tuple of ScrapedPosition objects retrieved for the current
            page.
        next_request_token: String. The key that should be used as a parameter
            of the token to retrieve the next request.
    """

    next_page_token: Optional[str] = None
    data: Optional[Tuple[ScrapedPosition, ...]] = None
    next_request_token: Optional[str] = None
