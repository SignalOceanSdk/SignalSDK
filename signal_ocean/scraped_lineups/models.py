"""Models instantiated by the scraped lineups api."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

from signal_ocean.scraped_data.scraped_data_api import ScrapedDataResponse


@dataclass(frozen=True)
class ScrapedLineup:
    """Detailed information about a scraped lineup.

    Attributes:
        lineup_id: Integer. A unique identifier of the lineup line.
        message_id: Integer. A unique identifier of the message containing the
            specific lineup. A message can contain more than one lineup.
        external_message_id: String. It serves as a unique identifier for a
            message, supplied by any company that has integrated with Signal.
        parsed_part_id: Integer. A unique identifier for each email part. The
            email body and each attachment are considered different parsed
            parts. For an example the email body and its pdf attachment have
            same MessageID and different ParsedPartID.
        line_from: Nullable integer. The starting line from which the lineup
            is extracted. The email subject counts as line 0 and the body
            content starts from line 1.
        line_to: Nullable integer. The final line from which the lineup is
            extracted. For single line lineups LineFrom is equal to LineTo.
            For descriptive lineups that span across multiple lines we have
            LineTo>LineFrom. These two numbers help the user identify which
            part of the text has been used to extract the lineup data.
        in_line_order: Nullable integer. This integer is used to list different
            cargoes extracted from the same line. It is the case for lineups
            with multiple cargoes or buyers. A lineup with two cargoes like
            'gasoil + fuel oil' is interpreted in our system as 2 lineups with
            same MessageID, same ParsedPartID, same LineNumber,  same IMO,
            different LineupID and an incremental InLineOrder number.
        source: String. It describes the source of the information. Our system
            allows the user to inject data in many different ways, namely
            through email (Source='Email'), through Slack channels
            (Source='Slack') or through manual contributions directly from
            our frontend platform TSOP (Source='User').
        updated_date: String, format YYYY-MM-DD HH:MM:SS, UTC timezone.
            Date on which the lineup has been reevaluated for the last time.
            In case of an email received by a broker one month ago and
            reprocessed through our engine today, this date will be today's.
        received_date: String, format YYYY-MM-DD HH:MM:SS, UTC timezone.
            Date on which the lineup has been injected into our system
            and processed.
        is_deleted: Boolean. This value is true if the lineup is marked as
            Deleted.
        low_confidence: Boolean. This value is true when the data extraction
            process does not return as output some fields that we believe to
            be more important than others in business terms. These fields are
            called critical fields. The value is true if at least one of the
            critical fields is missing.For example missing charterer or laycan.
        scraped_vessel_name: String. The vessel name as reported in the lineup
            line, i.e. 'Signal Alpha', 'Cpt A Stellatos', 'Genco Tiberius'.
            'TBN' can also be found.
        scraped_imo: String. Vessel's IMO as reported in the lineup line,
            i.e. '9412036', '9439670', '9331555'.
        scraped_deadweight: String. The dead weight of the vessel as reported
            in the lineup line, i.e. '150249', '167'.
        scraped_year_built: String. The year built of the vessel as reported
            in the lineup line, i.e. '2004', '09'.
        imo: Integer. The seven-digits number that uniquely identifies the
            ship reported in the lineup. It is the result of our internally
            developed Vessel Mapper model.
        vessel_name: String. It is the current vessel name corresponding to
            the IMO mentioned above. Provided to better specify the vessel and
            its particulars. Source: our internal Vessel Database.
        deadweight: Integer. The dead weight in tonnes [t] corresponding to
            the IMO mentioned above.
        year_built: Integer, YYYY format. The year the vessel was built.
            Source: our internal Vessel Database.
        liquid_capacity: Integer, measured in cbm [cbm]. The liquid capacity
            of the IMO mentioned above. Source: our internal Vessel Database.
        vessel_type_id: Integer. Numeric ID corresponding to the different
            values of the VesselType field. 1-> Tanker, 3-> Dry,
            4 -> Containers, 5 ->LNG (Liquified Natural gas),
            6-> LPG (Liquified Petroleum Gas).
        vessel_type: String. Description of the type of the vessel
            (VesselTypeID), based on the carried cargo. Main categories are
            Tankers, Dry (bulk carriers), Containers, LNG and LPG.
        vessel_class_id: Integer. It is an ID corresponding to the different
            vessel classes of a certain vessel type, as split according
            to our internal Vessel Database.
            For example 84->VLCC, 85->Suezmax, 70->Capesize.
        vessel_class: String. Name of the vessel class the vessel belongs to.
            Assignment of a vessel to a certain VesselClass is based on the
            VesselType and the value of its Deadweight (if Tanker or Dry),
            its LiquidCap (if LNG/LPG) or its TEU (if Containers).
            For example, an Aframax is a Tanker vessel with Deadweight within
            the range 82kt - 125kt, while a Capesize is a Dry vessel with
            Deadweight within the range 120kt-220kt. LR2 are defined
            as Aframax, as only Deadweight is used to define vessel classes.
        commercial_operator_id: Integer. Numeric ID corresponding to the
            current maritime company that commercially manages the vessel
            corresponding to the IMO mentioned above.
            Source: Signal's proprietary algorithm.
        commercial_operator: String. Name of the current maritime company
            associated to CommercialOperatorID.
            Source: our internal Companies Database.
        scraped_eta: String. The estimated time of arrival of the lineup as
            reported in the original text.
        eta: Date, format YYYY-MM-DD. The mapped date corresponding to the
            estimated time of arrival date.
        scraped_etb: String. The estimated time of berthing of the lineup as
            reported in the original text. Strings tba (to be announced) and
            tbc (to be confirmed) can also be found.
        etb: Date, format YYYY-MM-DD. The mapped date corresponding to the
            estimated time of berthing date.
        scraped_etd: String. The estimated time of departure of the lineup as
            reported in the original text. Strings tba (to be announced) and
            tbc (to be confirmed) can also be found.
        etd: Date, format YYYY-MM-DD. The mapped date corresponding to the
            estimated time of departure date.
        scraped_location: String. The location reported in the original text
            of the lineup. Also, It could be reported in the subject of email.
        location_geo_id: Integer. It is the internal ID of the mapped location
            reported in the lineup. Our models convert and map a scraped string
            containing geo information to a specific entity of the Signal's
            proprietary geofencing structure. Each geo entity is identified by
            a taxonomy, an ID and a name. Examples: the string 'turkmenbashi'
            is mapped to a geo asset with name 'Turkmenbashi Refinery', ID
            5086 and taxonomy GoeAsset (TaxonomyID=1); the string 'murmansk' is
            mapped to a geoasset with name 'Murmansk', ID 3761 and taxonomy
            Port (TaxonomyID=2); the string 'congo' is mapped to a geoasset
            with name 'Congo', ID 49 and taxonomy Country (TaxonomyID=3).
        location_name: String. The name of the Signal geo entity related to
            the reported location of the lineup. Examples: 'Qingdao',
            'Nigeria', 'Yangpu', 'Quanzhou'.
        location_taxonomy_id: Integer. An internal ID corresponding to each
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
             West Coast North America', 'West Coast Mexico',
            'West Coast Central America' and 'West Coast South America'.
        location_taxonomy: String. The extended name identifying the
            TaxonomyID. Possible values are: GeoAsset-> 1, Port -> 2,
            Country-> 3, Level0->4, Level1->5, Level2->6, Level3->7.
        operation_type_id: Interger. Numeric ID corresponding to the different
            values of the OperationType field. 1-> Loading, 2-> Discharge,
            3 -> Waypoint, -2 -> NotSet, -1 -> Unknown.
        operation_type: String. Denotes the operation type of the lineup if
            explicitly mentioned, like 'loading' for load.
        scraped_quantity: String. The quantity as reported in the original
            text of the lineup.
        quantity: Integer. The mapped quantity measured in the corresponding
            value of QuantityUnit filed.
        quantity_unit: String. Denotes the quantity unit of the lineup.
            1-> Tonnes, 2-> Barrels, -2 -> NotSet, -1 -> Unknown.
        scraped_cargo_type: String. The cargo type of the cargo as reported in
            the original text, often shortened. Examples: 'nhc', 'ulsd',
            'ums', 'nap', 'go'.
        cargo_type_id: Integer. It is an internal ID corresponding to the
            mapped cargo type of the cargo. A proprietary model is responsible
            to match the reported cargo string to a specific cargo type in our
            hierarchy. Examples: 19-> Crude Oil, 16->Fueloil, 9-> Naphtha,
            135-> Unleaded Motor Spirit, 12-> Gasoil,
            60-> 'Ultra Low Sulphur Diesel (ULSD 10ppm)'.
        cargo_type: String. The extended name corresponding to the CargoTypeID
            field. Source: our internal CargoTypes database.
        cargo_group_id: Integer. Numeric ID corresponding to the high-level
            cargo type of the reported cargo type. It is provided to group
            cargoes and facilitate analytics. Examples: 130000->Dirty,
            120000->Clean, 110000->IMO.
        cargo_group: String. The extended name corresponding to the
            CargoGroupID field. Source: our internal CargoTypes database.
        scraped_api_gravity: String. The API gravity reported in the original
            text on the lineup.
        api_gravity: Numeric. The mapped value corresponding to the API
            gravity.
        scraped_origin: String. The origin location reported in the original
            text of the lineup.
        origin_geo_id: Integer. An internal ID corresponding to the mapped
            origin location of the lineup. See LocationGeoID for more details.
        origin_name: String. The name of the Signal geo entity related to the
            reported origin location of the lineup. Examples: 'Fuel Pier',
            'Port Of Arzew Terminal 2', 'CPC (Novorossiysk) SBM',
            'Sheskharis Oil Terminal'.
        origin_taxonomy_id: Integer. An internal ID corresponding to the
            taxonomy of the mapped origin location. See LocationTaxonomyID
            for more details.
        origin_taxonomy: String. The extended name identifying the TaxonomyID.
            Possible values are: GeoAsset-> 1, Port -> 2, Country-> 3,
            Level0->4, Level1->5, Level2->6, Level3->7.
        scraped_destination: String. The destination location reported in the
            original text of the lineup. Strings tba (to be announced) and tbn
            (to be nominated) can also be found
        destination_geo_id: Integer. An internal ID corresponding to the
            mapped destination location of the lineup. See LocationGeoID for
            more details.
        destination_name: String. The name of the Signal geo entity related to
            the reported destination location of the lineup. Examples:
            'Fuel Pier', 'Port Of Arzew Terminal 2',
            'CPC (Novorossiysk) SBM', 'Sheskharis Oil Terminal'.
        destination_taxonomy_id: Integer. An internal ID corresponding to the
            taxonomy of the mapped destination location.
            See LocationTaxonomyID for more details.
        destination_taxonomy: String. The extended name identifying the
            TaxonomyID. Possible values are: GeoAsset-> 1, Port -> 2,
            Country-> 3, Level0->4, Level1->5, Level2->6, Level3->7.
        scraped_supplier: String. The supplier as reported in the original
            text of the lineup.
        supplier_id: Integer. Numeric ID corresponding to the supplier company
            that it is reported in the line. We use an internal mapper to find
            the correspondence between the reported string and our database.
        supplier: String. The company name corresponding to the SupplierID
            field. Provided to better specify the company involved in the
            business. Source: our internal Company Database.
        scraped_charterer: String. The charterer as reported in the original
            text of the lineup.
        charterer_id: Integer. Numeric ID corresponding to the chartering
            company that it is reported in the line. We use an internal mapper
            to find the correspondence between the reported string and our
            database.
        charterer: String. The company name corresponding to the ChartererID
            field. Provided to better specify the company involved in the
            business. Source: our internal Company Database.
        scraped_buyer: String. The buyer as reported in the original text of
            the lineup.
        buyer_id: Integer. Numeric ID corresponding to the buyer company that
            it is reported in the line. We use an internal mapper to find the
            correspondence between the reported string and our database.
        buyer: String. The company name corresponding to the BuyerID field.
            Provided to better specify the company involved in the business.
            Source: our internal Company Database.
        scraped_port_agent: String. The port agent as reported in the original
            text of the lineup.
        port_agent_id: Integer. Numeric ID corresponding to the port agent
            company that it is reported in the line.
        port_agent: String. The company name corresponding to the PortAgentID
            field. Provided to better specify the company involved in the
            business. Source: our internal Company Database.
        vessel_status_id: Integer. Numeric ID corresponding to the different
            values of the VesselStatus field. 1-> Expected, 2-> Arrived,
            3-> At anchor, 4-> At berth, 5-> Sailed, 6-> Failed,
            7-> Cancelled, 8-> Substituted, -2 -> NotSet, -1 -> Unknown.
        vessel_status: String denoting the vessel status of a lineup if
            explicitly mentioned, like 'expected for expected or 'waiting' for
            at anchor.
        content: String. The full content of the lineup. For a single line
            lineup it is the line content. For multi line lineups it is the
            collection of all the relevant parts of the text.
        subject: String. The email subject of the lineup. This field has
            content when Source='Email'.
        sender: String. Our own mapping of the shipping company sending out the
            market report through email. This string helps grouping emails
            sent by the same organization, but from different domains. It is
            often the case for big organizations operating worldwide. For
            example Sender= 'SSY' for both domains 'ssysin.com' and 'ssy.co'.
        is_private: Boolean. A lineup is private if injected by a user into
            his own private account within TSOP. A user can provide private
            information through email forwarding or through Slack.
            Private lineup information stay in the account, are accessible by
            the account users only (people within the same company) and are
            the most valuable ones.
    """

    # entity details
    lineup_id: int
    message_id: Optional[int] = None
    external_message_id: Optional[str] = None
    parsed_part_id: Optional[int] = None
    line_from: Optional[int] = None
    line_to: Optional[int] = None
    in_line_order: Optional[int] = None
    source: Optional[str] = None
    updated_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    low_confidence: Optional[bool] = False

    # vessel
    scraped_vessel_name: Optional[str] = None
    scraped_imo: Optional[str] = None
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
    commercial_operator_id: Optional[int] = None
    commercial_operator: Optional[str] = None

    # eta
    scraped_eta: Optional[str] = None
    eta: Optional[datetime] = None

    # etb
    scraped_etb: Optional[str] = None
    etb: Optional[datetime] = None

    # etd
    scraped_etd: Optional[str] = None
    etd: Optional[datetime] = None

    # location
    scraped_location: Optional[str] = None
    location_geo_id: Optional[int] = None
    location_name: Optional[str] = None
    location_taxonomy_id: Optional[int] = None
    location_taxonomy: Optional[str] = None

    # operation_type
    operation_type_id: Optional[int] = None
    operation_type: Optional[str] = None

    # quantity
    scraped_quantity: Optional[str] = None
    quantity: Optional[float] = None
    quantity_unit: Optional[str] = None

    # cargo type
    scraped_cargo_type: Optional[str] = None
    cargo_type_id: Optional[int] = None
    cargo_type: Optional[str] = None
    cargo_group_id: Optional[int] = None
    cargo_group: Optional[str] = None

    # api_gravity
    scraped_api_gravity: Optional[str] = None
    api_gravity: Optional[int] = None

    # origin
    scraped_origin: Optional[str] = None
    origin_geo_id: Optional[int] = None
    origin_name: Optional[str] = None
    origin_taxonomy_id: Optional[int] = None
    origin_taxonomy: Optional[str] = None

    # destination
    scraped_destination: Optional[str] = None
    destination_geo_id: Optional[int] = None
    destination_name: Optional[str] = None
    destination_taxonomy_id: Optional[int] = None
    destination_taxonomy: Optional[str] = None

    # supplier
    scraped_supplier: Optional[str] = None
    supplier_id: Optional[int] = None
    supplier: Optional[str] = None

    # charterer
    scraped_charterer: Optional[str] = None
    charterer_id: Optional[int] = None
    charterer: Optional[str] = None

    # buyer
    scraped_buyer: Optional[str] = None
    buyer_id: Optional[int] = None
    buyer: Optional[str] = None

    # port agent
    scraped_port_agent: Optional[str] = None
    port_agent_id: Optional[int] = None
    port_agent: Optional[str] = None

    # vessel status
    vessel_status_id: Optional[int] = None
    vessel_status: Optional[str] = None

    # content
    content: Optional[str] = None
    subject: Optional[str] = None

    # sender
    sender: Optional[str] = None

    # debug info
    is_private: Optional[bool] = False


@dataclass(frozen=True)
class ScrapedLineupsResponse(ScrapedDataResponse[ScrapedLineup]):
    """Paged response for scraped lineups from the Scraped Lineups API.

    Attributes:
        next_page_token: String. The key that should be used as a parameter of
            the token to retrieve the next page.
        data: A tuple of ScrapedLineup objects retrieved for the current page.
        next_request_token: String. The key that should be used as a parameter
            of the token to retrieve the next request.
    """

    next_page_token: Optional[str] = None
    data: Optional[Tuple[ScrapedLineup, ...]] = None
    next_request_token: Optional[str] = None
