"""Models instantiated by the scraped fixtures api."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

from signal_ocean.scraped_data.scraped_data_api import ScrapedDataResponse


@dataclass(frozen=True)
class ScrapedFixture:
    """Detailed information about a scraped fixture.

    Attributes:
        fixture_id: Integer. A unique identifier of the fixture line.
        message_id: Integer. A unique identifier of the message containing the
            specific fixture.
            A message can contain more than one fixture.
        parsed_part_id: Integer. A unique identifier for each email part.
            The email body and each attachment are considered different parsed
            parts. For an example the email body and its pdf attachment have
            same MessageID and different ParsedPartID.
        line_from: Nullable integer. The starting line from which the fixture
            is extracted. The email subject counts as  line 0 and the body
            content starts from line 1.
        line_to: Nullable integer. The final line from which the fixture is
            extracted. For single line fixtures LineFrom is equal to LineTo.
            For descriptive fixtures that span across multiple lines we have
            LineTo>LineFrom. These two numbers help the user identify which
            part of the text has been used to extract the fixture data.
        in_line_order: Nullable integer. This integer is used to list different
            fixtures extracted from the same line. It is the case for fixtures
            with different discharge options. A fixture with a discharge and an
            option like 'med-ukc' is interpreted in our system as 2 fixtures
            with same MessageID, same ParsedPartID, same LineNumber, same IMO,
            different FixtureID and an incremental InLineOrder number.
        source: String. It describes the source of the information.
            Our system allows the user to inject data in many different ways,
            namely through email (Source='Email'), through Slack channels
            (Source='Slack') or through manual contributions directly
            from our frontend platform TSOP (Source='User').
        updated_date: String, format YYYY-MM-DD HH:MM:SS, UTC timezone.
            Date on which the fixture has been reevaluated for the last time.
            In case of an email received by a broker one month ago and
            reprocessed through our engine today, this date will be today's.
        received_date: String, format YYYY-MM-DD HH:MM:SS, UTC timezone. Date
            on which the fixture has been injected into our system and
            processed.
        is_deleted: Boolean. This value is true if the fixture is marked as
            Deleted.
        scraped_vessel_name: String. The vessel name as reported in the fixture
            line, i.e. 'Signal Alpha', 'Cpt A Stellatos', 'Genco Tiberius'.
            'TBN' can also be found.
        scraped_deadweight: String. The dead weight of the vessel as reported
            in the fixture line, i.e. '150249', '167'.
        scraped_year_built: String. The year built of the vessel as reported in
            the fixture line, i.e. '2004', '09'.
        imo: Integer. The seven-digits number that uniquely identifies the ship
            reported in the fixture. It is the result of our internally
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
            VesselType and the value of its Deadweight (if Tanker or Dry),
            its LiquidCap (if LNG/LPG) or its TEU (if Containers).
            For example, an Aframax is a Tanker vessel with Deadweight within
            the range 82kt - 125kt, while a Capesize is a Dry vessel with
            Deadweight within the range 120kt-220kt. LR2 are defined as
            Aframax, as only Deadweight is used to define vessel classes.
        commercial_operator_id: Integer. Numeric ID corresponding to the
            current maritime company that commercially manages the vessel
            corresponding to the IMO mentioned above. Source: Signal's
            proprietary algorithm.
        commercial_operator: String. Name of the current maritime company
            associated to CommercialOperatorID. Source: our internal Companies
            Database.
        scraped_laycan: String. The laycan (latest day of cancellation) of the
            fixture as reported in the original text. It is often reported as a
            date range, e.g. '25-jan 27-jan', '31-1 feb',  '11-12 apr'.
            The string 'dnr' (date not reported) can also be found.
        laycan_from: Date, format YYYY-MM-DD. The mapped date corresponding to
            the beginning of the laycan date range.
        laycan_to: Date, format YYYY-MM-DD. The mapped date corresponding to
            the end of the laycan date range.
        scraped_load: String. The loading location reported in the original
            text of the fixture. It is very often shortened, very compact and
            can refer to terminals, ports, countries or wider areas. Examples:
            'singgi' for Singgi, 'rt' for Ras Tanura, 'waf' for West Africa.
        load_geo_id: Integer. It is the internal ID of the mapped loading
            location reported in the fixture. Our models convert and map a
            scraped string containing geo information to a specific entity of
            the Signal's proprietary geofencing structure. Each geo entity is
            identified by a taxonomy, an ID and a name. Examples: the string
            'bonny' is mapped to a geo asset with name 'Bonny', ID 3679 and
            taxonomy Port (TaxonomyID=2); the string 'nigeria' is mapped to a
            geoasset with name 'Nigeria', ID 171 and taxonomy Country
            (TaxonomyID=3); the string 'wafr' is mapped to a geoasset with name
            'Africa Atlantic Coast', ID 24772 and taxonomy Level0
            (TaxonomyID=4).
        load_name: String. The name of the Signal geo entity related to the
            reported loading location of the fixture. Examples: 'Bonny',
            'Nigeria', 'Africa Atlantic Coast', 'Arabian Gulf', 'Singapore',
            'East Coast Mexico'.
        load_taxonomy_id: Integer. An internal ID corresponding to each
            taxonomy, the level of geo details, from 1 to 7. A terminal
            (geoasset) has the lowest taxonomy (TaxonomyID=1), a port has
            TaxonomyID=2, while countries and wider areas have higher taxonomy
            (TaxonomyID>=3). Examples of Level 0 areas (TaxonomyID=4) include
            'Arabian Gulf', 'US Gulf' and 'East Mediterranean'. Level 1 areas
            (TaxonomyID=5) consist of multiple level 0 areas (TaxonomyID=4).
            For example, level 1 area 'Mediterranean' groups together
            the level 0 areas 'West Mediterranean', 'Central Mediterranean' and
            'East Mediterranean'. Level 2 areas (TaxonomyID=6) consist of
            multiple level 1 areas (TaxonomyID=4). For example, level 2 area
            'Mediterranean/UK Continent' groups together the 'Mediterranean'
            and 'UK Continent' level 1 areas. Level 3 areas (TaxonomyID=7) are
            the highest area grouping in our taxonomy and consist of multiple
            level 2 areas (TaxonomyID=6). Examples of such areas are
            'Pacific America' or 'Africa'. These group together level 2 areas.
            For instance, 'Pacific America' groups together the level 2 areas
            'West Coast North America', 'West Coast Mexico',
            'West Coast Central America' and 'West Coast South America'."
        load_taxonomy: String. The extended name identifying the TaxonomyID.
            Possible values are: GeoAsset-> 1, Port -> 2, Country-> 3,
            Level0-> 4, Level1->5, Level2->6, Level3->7.
        scraped_load2: String. The second loading location reported in the
            original text of the fixture. It is very often shortened, very
            compact and can refer to terminals, ports, countries or wider
            areas. Examples: 'singgi' for Singgi, 'rt' for Ras Tanura, 'waf'
            for West Africa."
        load_geo_id2: Integer. An internal ID corresponding to the mapped
            second loading location of the fixture. See LoadGeoID for more
            details.
        load_name2: String. The name of the Signal geo entity related to
            the reported second loading location of the fixture.
            Examples: 'Bonny', 'Nigeria', 'Africa Atlantic Coast',
            'Arabian Gulf', 'Singapore', 'East Coast Mexico'.
        load_taxonomy_id2: Integer. An internal ID corresponding to the
            taxonomy of the mapped discharging location. See LoadTaxonomyID for
            more details.
        load_taxonomy2: String. The extended name identifying the TaxonomyID.
            Possible values are: GeoAsset-> 1, Port -> 2, Country-> 3,
            Level0-> 4, Level1-> 5, Level2-> 6, Level3-> 7.
        scraped_discharge: String. The discharging port reported in the
            original text of the fixture. It is very often shortened, very
            compact and can refer to terminals, ports, countries or wider
            areas. For fixtures reporting multiple discharge options, this
            field contains only the first string. For example in the fixture
            'minerva aries subs mercuria 75 ulsd n. mangalore ukc-wafr-jpn
            14/jan 2.425m-2.375m-ws125' the field ScrapedDischarge contains
            'ukc' only."
        scraped_discharge_options: String. All the discharging options reported
            in the original text of the fixture. For example in the fixture
            'minerva aries subs mercuria 75 ulsd n. mangalore ukc-wafr-jpn
            14/jan 2.425m-2.375m-ws125' the field ScrapedDischargeOptions
            contains 'wafr-jpn'."
        discharge_geo_id: Integer. An internal ID corresponding to the mapped
            discharging location of the fixture. See LoadGeoID for more
            details.
        discharge_name: String. The name of the Signal geo entity related to
            the discharging location of the fixture. Examples: 'Indonesia',
            'Japan', 'Argentina'.
        discharge_taxonomy_id: Integer. An internal ID corresponding to the
            taxonomy of the mapped discharging location. See LoadTaxonomyID for
            more details.
        discharge_taxonomy: String. The extended name identifying the taxonomy
            of the mapped discharging location. Possible values are:
            GeoAsset-> 1, Port -> 2, Country-> 3, Level0->4, Level1->5,
            Level2->6, Level3->7.
        scraped_discharge2: String. The second discharging port reported in the
            original text of the fixture. It is very often shortened, very
            compact and can refer to terminals, ports, countries or wider
            areas. For example in the fixture 'al agaila 130 gabon+algeria/
            feast 14/01 rnr lord energy' the field ScrapedDischarge2 contains
            'algeria'."
        discharge_geo_id2: Integer. An internal ID corresponding to the mapped
            second discharging location of the fixture. See LoadGeoID for more
            details.
        discharge_name2: String. The name of the Signal geo entity related to
            the second discharging location of the fixture. Examples:
            'Algeria', 'Greece', 'France'.
        discharge_taxonomy_id2: Integer. An internal ID corresponding to the
            taxonomy of the mapped second discharging location. See
            LoadTaxonomyID for more details.
        discharge_taxonomy2: String. The extended name identifying the
            TaxonomyID. Possible values are: GeoAsset-> 1, Port -> 2,
            Country-> 3, Level0->4, Level1->5, Level2->6, Level3->7.
        scraped_charterer: String. The fixture charterer as reported in the
            original text.  Examples: 'atc', 'unipec', 'enoc', 'ioc', 'pbras'"
        charterer_id: Integer. Numeric ID corresponding to the chartering
            company that it is reported in the line. We use an internal mapper
            to find the correspondence between the reported string and our
            database.
        charterer: String. The company name corresponding to the ChartererID
            field.  Provided to better specify the company involved in the
            business. Source: our internal Company Database.
        scraped_cargo_type: String. The fixture cargo type as reported in the
            original text, often shortened. Examples: 'nhc', 'ulsd', 'ums',
            'nap', 'go'.
        cargo_type_id: Integer. It is an internal ID corresponding to the
            mapped cargo type of the fixture. A proprietary model is
            responsible to match the reported cargo type string to a specific
            cargo type in our hierarchy. Examples: 19-> Crude Oil, 16->Fueloil,
            9-> Naphtha, 135-> Unleaded Motor Spirit, 12-> Gasoil,
            60-> 'Ultra Low Sulphur Diesel (ULSD 10ppm)'.
        cargo_type: String. The extended name corresponding to the CargoTypeID
            field. Source: our internal CargoTypes database.
        cargo_group_id: Integer. Numeric ID corresponding to the high-level
            cargo type of the fixture cargo type. It is provided to group
            fixtures and facilitate analytics. Examples: 130000->Dirty,
            120000-> Clean, 110000->IMO.
        cargo_group: String. The extended name corresponding to the
            CargoGroupID field. Source: our internal CargoTypes database.
        scraped_quantity: String. The fixture quantity as reported in the
            original text, including ranges and buffer. Examples: '80',
            '75000/10', '270', '180/10'.
        quantity: Numeric. The mapped quantity measured in tonnes [t].
            Quantity would be equal to '180000', both for ScrapedQuantity
            '180/10' and '180000/5'.
        quantity_buffer: Numeric. The quantity buffer if reported in the
            fixture line, expressed as a fraction of 1.
            Examples: for ScrapedQuantity='75/10', QuantityBuffer=0.1.
            For ScrapedQuantity='180000/5', QuantityBuffer=0.05.
        quantity_from: Numeric. The lower limit of the quantity range measured
            in tonnes [t], computed as
            QuantityFrom=(1-QuantityBuffer)*Quantity.
            Examples: for ScrapedQuantity='170/10', QuantityFrom=153000.
            For ScrapedQuantity='150000/10', QuantityFrom=135000.
            If QuantityBuffer=-0, we have Quantity=QuantityFrom=QuantityTo.
        quantity_to: Numeric. The upper limit of the quantity range measured in
            tonnes [t], computed as QuantityFrom=(1+QuantityBuffer)*Quantity.
            Examples: for ScrapedQuantity='170/10', QuantityFrom=187000.
            For ScrapedQuantity='150000/10', QuantityFrom=165000.
            If QuantityBuffer=-0, we have Quantity=QuantityFrom=QuantityTo.
        scraped_rate: String. The fixture rate as reported in the original
            text, including its units or type. Examples: 'usd 240k', 'w100',
            '$18.95'. Values 'coa' and 'rnr' can also be found. For fixtures
            reporting multiple discharge options, this field contains only the
            rate for the first discharge.
        scraped_rate_options: String. All the rates corresponding to the
            discharging options reported in the original text of the fixture.
            For example in the fixture 'minerva aries subs mercuria 75 ulsd
            n. mangalore ukc-wafr-jpn 14/jan 2.425m-2.375m-ws125'
            the field ScrapedRateOptions contains '2.375m-ws125'.
        rate_value: Numeric. The mapped rate of the fixture. If lump sum, the
            rate is reported in USD. Example: for ScrapedRate='usd 240k',
            RateValue=240000.00 and RateType='LS'.
        rate_type: String. The type associated to the RateValue.
            Possible values are 'LS' for 'Lump Sum' (in usd), 'WS' for World
            Scale, 'PMT' for $/pmt, 'TCE' for Time Charter Equivalent or $/day.
        open_geo_id: Integer. An internal ID corresponding to the mapped open
            location. The fields starting with 'Open' (OpeGeoID, OpenGeoName,
            OpenTaxonomyID, OpenTaxonomy and OpenDate) are populated if a
            fixture is partial. Such a fixture is marked by the boolean
            'IsPartial' (see below) being true. In our system a fixture is
            partial if the discharge location is missing. There are two main
            sources of partial fixtures: the most common one is the case of a
            line in a tonnage list containing a subs indication and the second
            one is a fixture with no details contained in a fixture report.
            Example: a tonnage list line such as 'eagle san antonio mundra 04th
            subs' generates a partial fixture because only a limited number of
            fields is available. In this case we know the vessel name, the open
            location and the open date. There are no scraped fields
            corresponding to a partial fixture generated from a tonnage list,
            but only mapped ones. In the case of the example we have the vessel
            'eagle san antonio' mapped to IMO 9594822, 'mundra' mapped to
            OpenGeoID 3527 of taxonomy Port (TaxonomyID=2), '04th' napped to
            OpenDate '2022-02-04' as the tonnage list was received at the end
            of January. The status of this partial fixture is 'on subs'.
        open_geo_name: String. The name of the Signal geo entity related to the
            open location of the partial fixture. Examples: 'Singapore',
            'Japan', 'Argentina'.
        open_taxonomy_id: Integer. An internal ID corresponding to the taxonomy
            of the mapped open location. See LoadTaxonomyID for more details.
        open_taxonomy: String. The extended name identifying the taxonomy of
            the mapped open location. Possible values are: GeoAsset-> 1,
            Port -> 2, Country-> 3, Level0->4, Level1->5, Level2->6, Level3->7.
        open_date: Date, format YYYY-MM-DD. The mapped open date.
        scraped_delivery_date: String. The delivery date of the time charter
            fixture as reported in the original text. It if often reported as a
            date range, e.g. '16/18 Nov', '17/19'.
        delivery_date_from: Date, format YYYY-MM-DD. The mapped date
            corresponding to the beginning of the delivery date range.
        delivery_date_to: Date, format YYYY-MM-DD. The mapped date
            corresponding to the end of the delivery date range.
        scraped_delivery: String. The delivery location reported in the
            original text of the fixture. Very common in the case of time
            charter fixtures. The string can refer to waypoints, ports,
            countries or wider areas. Examples: 'Corpus Christi',
            'EC South America', 'PDM', 'E.Med'.
        delivery_geo_id: Integer. An internal ID corresponding to the mapped
            delivery location of the fixture. See LoadGeoID for more details.
        delivery_name: String. The name of the Signal geo entity related to the
            delivery location of the fixture. Examples: 'E.Med' matches to
            'East Mediterranean' (DeliveryGeoID=24737, DeliveryTaxonomyID=4,
            DeliveryTaxonomy='Level0'); 'PDM' matches to 'Ponta Da Madeira'
            (DeliveryGeoID=13013, DeliveryTaxonomyID=2,
            DeliveryTaxonomy='Port').
        delivery_taxonomy_id: Integer. An internal ID corresponding to the
            taxonomy of the mapped delivery location. Values from 1 to 7. See
            LoadTaxonomyID for more details.
        delivery_taxonomy: String. The extended name identifying the taxonomy
            of the mapped delivery location. Possible values are: GeoAsset-> 1,
            Port -> 2, Country-> 3, Level0->4, Level1->5, Level2->6, Level3->7.
        scraped_redelivery_from: String. The redelivery location reported in
            the original text of the fixture. Very common in the case of time
            charter fixtures. If the redelivery is reported as a geographical
            range, this field contains the first string. Otherwise the only
            delivery location reported. Example: In a dry fixture like
            ''Atrotos Heracles' 2014 81922 dwt dely Corpus Christi 6/10 Oct
            trip via US Gulf redel Skaw-Gibraltar $35,000 + $800,000 bb - XO
            Shipping' we have ScrapedRedeliveryFrom = 'Skaw' and
            ScrapedRedeliveryTo = 'Gibraltar'. For the fixture ''Gorgoypikoos'
            2005 76498 dwt dely Belawan 20/21 Sep trip via Indonesia redel N
            China $39,000 - cnr' we have ScrapedRedeliveryFrom = 'N China'.
        redelivery_from_geo_id: Integer. An internal ID corresponding to the
            mapped redelivery location of the fixture. See LoadGeoID for more
            details.
        redelivery_from_name: String. The name of the Signal geo entity related
            to the redelivery location of the fixture. Example: 'N China'
            matches to 'North China' (RedeliveryFromGeoID=24666,
            DeliveryTaxonomyID=4, DeliveryTaxonomy='Level0').
        redelivery_from_taxonomy_id: Integer. An internal ID corresponding to
            the taxonomy of the mapped redelivery location. Values from 1 to 7.
            See LoadTaxonomyID for more details.
        redelivery_from_taxonomy: String. The extended name identifying the
            taxonomy of the mapped redelivery location. Possible values are:
            GeoAsset-> 1, Port -> 2, Country-> 3, Level0->4, Level1->5,
            Level2->6, Level3->7.
        scraped_redelivery_to: String. If the redelivery is reported as a
            geographical range, this field contains the end of the range as
            reported in the original text of the fixture. Example: In a dry
            fixture like ''Atrotos Heracles' 2014 81922 dwt dely Corpus Christi
            6/10 Oct trip via US Gulf redel Skaw-Gibraltar $35,000 +
            $800,000 bb - XO Shipping' we have
            ScrapedRedeliveryTo = 'Gibraltar'.
        redelivery_to_geo_id: Integer. An internal ID corresponding to the
            mapped redelivery location of the fixture. See LoadGeoID for more
            details.
        redelivery_to_name: String. The name of the Signal geo entity related
            to the redelivery location of the fixture. Example: 'Gibraltar'
            matches to 'Gibraltar' (RedeliveryToGeoID=7345,
            DeliveryTaxonomyID=2, DeliveryTaxonomy='Port').
        redelivery_to_taxonomy_id: Integer. An internal ID corresponding to the
            taxonomy of the mapped redelivery location. Values from 1 to 7.
            See LoadTaxonomyID for more details.
        redelivery_to_taxonomy: String. The extended name identifying the
            taxonomy of the mapped redelivery location. Possible values are:
            GeoAsset-> 1, Port -> 2, Country-> 3, Level0->4, Level1->5,
            Level2->6, Level3->7.
        charter_type_id: Integer. An internal ID to distinguish fixtures
            reporting voyage charter and time charter agreements. Possible
            values are 0 and 1.
        charter_type: String. The extended name of the type of shipping
            contract reported in the fixture. Values currently supported are
            'Voyage'->0, 'Time charter'->1.
        fixture_status_id: Numeric ID corresponding to the different values of
            the FixtureStatus field. 0-> OnSubs, 1-> FullyFixed, 2 -> Failed,
            3 ->Cancelled , 4-> Available, -2 -> NotSet, -1 -> Unknown.
        fixture_status: String denoting the commercial status of a fixture if
            explicitly mentioned, like 'ffxd' for fully fixed or 'subs'/'-s-'
            for on subs.
        is_owners_option: Boolean. This value is true if 'o/o' (Owner's Option)
            or 'oos' is explicitly reported in the original text of the
            fixture.
        is_coa: Boolean. This value is true if 'COA' (Contract of
            Affreightment) or 'o/p' (Own Program) is explicitly reported in the
            original text of the fixture.
        content: String. The full content of the fixture. For a single line
            fixture it is the line content. Example of a dry fixture
            ''Atrotos Heracles' 2014 81922 dwt dely Corpus Christi 6/10 Oct
            trip via US Gulf redel Skaw-Gibraltar $35,000 + $800,000 bb - XO
            Shipping'. For multi line fixtures it is the collection of all the
            relevant parts of the text.
        sender: String. Our own mapping of the shipping company sending out the
            market report through email. This string helps grouping emails sent
            by the same organization, but from different domains. It is often
            the case for big organizations operating worldwide. For example
            Sender= 'SSY' for both domains 'ssysin.com' and 'ssy.co'.
        is_private: Boolean. A fixture is private if injected by a user into
            his own private account within TSOP. A user can provide private
            information through email forwarding, through manual contributions
            or through Slack. Private fixture information stay in the account,
            are accessible by the account users only (people within the same
            company) and are the most valuable ones.
        is_invalidated: Boolean. A fixture is invalidated whenever a user
            selects 'Ignore this fixture' from the Reported Fixtures dashboard
            in TSOP.
        is_partial: Boolean. A fixture is partial if the discharge field is
            missing. The two most common categories of partial fixtures are the
            fixtures generated by an 'on subs' indication in a tonnage list
            line and those included in a fixture report with vessel name,
            laycan and load port only. See OpenGeoID for more details.
    """

    # entity details
    fixture_id: int
    message_id: Optional[int] = None
    parsed_part_id: Optional[int] = None
    line_from: Optional[int] = None
    line_to: Optional[int] = None
    in_line_order: Optional[int] = None
    source: Optional[str] = None
    updated_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    is_deleted: Optional[bool] = False

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
    commercial_operator_id: Optional[int] = None
    commercial_operator: Optional[str] = None

    # laycan
    scraped_laycan: Optional[str] = None
    laycan_from: Optional[datetime] = None
    laycan_to: Optional[datetime] = None

    # load
    scraped_load: Optional[str] = None
    load_geo_id: Optional[int] = None
    load_name: Optional[str] = None
    load_taxonomy_id: Optional[int] = None
    load_taxonomy: Optional[str] = None

    # load 2
    scraped_load2: Optional[str] = None
    load_geo_id2: Optional[int] = None
    load_name2: Optional[str] = None
    load_taxonomy_id2: Optional[int] = None
    load_taxonomy2: Optional[str] = None

    # discharge
    scraped_discharge: Optional[str] = None
    scraped_discharge_options: Optional[str] = None
    discharge_geo_id: Optional[int] = None
    discharge_name: Optional[str] = None
    discharge_taxonomy_id: Optional[int] = None
    discharge_taxonomy: Optional[str] = None

    # discharge 2
    scraped_discharge2: Optional[str] = None
    discharge_geo_id2: Optional[int] = None
    discharge_name2: Optional[str] = None
    discharge_taxonomy_id2: Optional[int] = None
    discharge_taxonomy2: Optional[str] = None

    # charterer
    scraped_charterer: Optional[str] = None
    charterer_id: Optional[int] = None
    charterer: Optional[str] = None

    # cargo type
    scraped_cargo_type: Optional[str] = None
    cargo_type_id: Optional[int] = None
    cargo_type: Optional[str] = None
    cargo_group_id: Optional[int] = None
    cargo_group: Optional[str] = None

    # quantity
    scraped_quantity: Optional[str] = None
    quantity: Optional[float] = None
    quantity_buffer: Optional[float] = None
    quantity_from: Optional[float] = None
    quantity_to: Optional[float] = None

    # rate
    scraped_rate: Optional[str] = None
    scraped_rate_options: Optional[str] = None
    rate_value: Optional[float] = None
    rate_type: Optional[str] = None

    # open
    open_geo_id: Optional[int] = None
    open_geo_name: Optional[str] = None
    open_taxonomy_id: Optional[int] = None
    open_taxonomy: Optional[str] = None
    open_date: Optional[datetime] = None

    # delivery date
    scraped_delivery_date: Optional[str] = None
    delivery_date_from: Optional[datetime] = None
    delivery_date_to: Optional[datetime] = None

    # delivery
    scraped_delivery: Optional[str] = None
    delivery_geo_id: Optional[int] = None
    delivery_name: Optional[str] = None
    delivery_taxonomy_id: Optional[int] = None
    delivery_taxonomy: Optional[str] = None

    # redelivery from
    scraped_redelivery_from: Optional[str] = None
    redelivery_from_geo_id: Optional[int] = None
    redelivery_from_name: Optional[str] = None
    redelivery_from_taxonomy_id: Optional[int] = None
    redelivery_from_taxonomy: Optional[str] = None

    # redelivery to
    scraped_redelivery_to: Optional[str] = None
    redelivery_to_geo_id: Optional[int] = None
    redelivery_to_name: Optional[str] = None
    redelivery_to_taxonomy_id: Optional[int] = None
    redelivery_to_taxonomy: Optional[str] = None

    # charter type
    charter_type_id: Optional[int] = None
    charter_type: Optional[str] = None

    # fixture status
    fixture_status_id: Optional[int] = None
    fixture_status: Optional[str] = None

    # fixture indicators
    is_owners_option: Optional[bool] = False
    is_coa: Optional[bool] = False

    # content
    content: Optional[str] = None

    # sender
    sender: Optional[str] = None

    # debug info
    is_private: Optional[bool] = False
    is_invalidated: Optional[bool] = False
    is_partial: Optional[bool] = False


@dataclass(frozen=True)
class ScrapedFixturesResponse(ScrapedDataResponse[ScrapedFixture]):
    """Paged response for scraped fixtures from the Scraped Fixtures API.

    Attributes:
        next_page_token: String. The key that should be used as a parameter of
            the token to retrieve the next page.
        data: A tuple of ScrapedFixture objects retrieved for the current page.
    """

    next_page_token: Optional[str] = None
    data: Optional[Tuple[ScrapedFixture, ...]] = None
