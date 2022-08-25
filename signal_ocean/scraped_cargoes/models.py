"""Models instantiated by the scraped cargoes api."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

from signal_ocean.scraped_data.scraped_data_api import ScrapedDataResponse


@dataclass(frozen=True)
class ScrapedCargo:
    """Detailed information about a scraped cargo.

    Attributes:
        cargo_id: Integer. A unique identifier of the cargo line.
        message_id: Integer. A unique identifier of the message containing the
            specific cargo. A message can contain more than one cargo.
        parsed_part_id: Integer. A unique identifier for each email part. The
            email body and each attachment are considered different parsed
            parts. For an example the email body and its pdf attachment have
            same MessageID and different ParsedPartID.
        line_from: Nullable integer. The starting line from which the cargo is
            extracted. The email subject counts as line 0 and the body content
            starts from line 1.
        line_to: Nullable integer. The final line from which the cargo is
            extracted. For single line cargoes LineFrom is equal to LineTo.
            For descriptive cargoes that span across multiple lines we have
            LineTo>LineFrom. These two numbers help the user identify which
            part of the text has been used to extract the cargo data.
        in_line_order: Nullable integer. This integer is used to list different
            cargoes extracted from the same line. It is the case for cargoes
            with different discharge options. A cargo with a discharge and
            an option like 'med-ukc' is interpreted in our system as 2 cargoes
            with same MessageID, same ParsedPartID, same LineNumber,  different
            CargoID and an incremental InLineOrder number.
        source: String. It describes the source of the information. Our system
            allows the user to inject data in many different ways, namely
            through email (Source='Email'), through Slack channels
            (Source='Slack') or through manual contributions directly from our
            frontend platform TSOP (Source='User').
        updated_date: String, format YYYY-MM-DD HH:MM:SS, UTC timezone. Date on
            which the cargo has been reevaluated for the last time. In case of
            an email received by a broker one month ago and reprocessed through
            our engine today, this date will be today's.
        received_date: String, format YYYY-MM-DD HH:MM:SS, UTC timezone. Date
            on which the cargo has been injected into our system and processed.
        is_deleted: Boolean. This value is true if the cargo is marked as
            Deleted.
        scraped_laycan: String. The laycan (latest day of cancellation) of the
            cargo as reported in the original text. It if often reported as a
            date range, e.g. '25-jan 27-jan', '31-1 feb', '11-12 apr'. The
            string 'dnr' (date not reported) can also be found.
        laycan_from: Date, format YYYY-MM-DD. The mapped date corresponding to
            the beginning of the laycan date range.
        laycan_to: Date, format YYYY-MM-DD. The mapped date corresponding to
            the end of the laycan date range.
        scraped_load: String. The loading location reported in the original
            text of the cargo. It is very often shortened, very compact and can
            refer to terminals, ports, countries or wider areas. Examples:
            'singgi' for Singgi, 'rt' for Ras Tanura, 'waf' for West Africa.
        load_geo_id: Integer. It is the internal ID of the mapped loading
            location reported in the cargo. Our models convert and map a
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
            reported loading location of the cargo. Examples: 'Bonny',
            'Nigeria', 'Africa Atlantic Coast', 'Arabian Gulf', 'Singapore',
            'East Coast Mexico'.
        load_taxonomy_id: Integer. An internal ID corresponding to each
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
        load_taxonomy: String. The extended name identifying the TaxonomyID.
            Possible values are: GeoAsset-> 1, Port -> 2, Country-> 3,
            Level0->4, Level1->5, Level2->6, Level3->7.
        scraped_load2: String. The second loading location reported in the
            original text of the cargo. It is very often shortened, very
            compact and can refer to terminals, ports, countries or wider
            areas. Examples: 'singgi' for Singgi, 'rt' for Ras Tanura, 'waf'
            for West Africa.
        load_geo_id2: Integer. An internal ID corresponding to the mapped
            second loading location of the cargo. See LoadGeoID for more
            details.
        load_name2: String. The name of the Signal geo entity related to
            the reported second loading location of the cargo. Examples:
            'Bonny', 'Nigeria', 'Africa Atlantic Coast', 'Arabian Gulf',
            'Singapore', 'East Coast Mexico'.
        load_taxonomy_id2: Integer. An internal ID corresponding to the
            taxonomy of the mapped discharging location. See LoadTaxonomyID for
            more details.
        load_taxonomy2: String. The extended name identifying the TaxonomyID.
            Possible values are: GeoAsset-> 1, Port -> 2, Country-> 3,
            Level0->4, Level1->5, Level2->6, Level3->7.
        scraped_discharge: String. The discharging port reported in the
            original text of the cargo. It is very often shortened, very
            compact and can refer to terminals, ports, countries or wider
            areas. For cargoes reporting multiple discharge options, this field
            contains only the first string. For example in the cargo
            'mercuria 75 ulsd n. mangalore ukc-wafr-jpn 14/jan
            2.425m-2.375m-ws125' the field ScrapedDischarge contains 'ukc'
            only.
        scraped_discharge_options: String. All the discharging options reported
            in the original text of the cargo. For example in the cargo
            'minerva aries subs mercuria 75 ulsd n. mangalore ukc-wafr-jpn
            14/jan 2.425m-2.375m-ws125' the field ScrapedDischargeOptions
            contains 'wafr-jpn'.
        discharge_geo_id: Integer. An internal ID corresponding to the mapped
            discharging location of the cargo. See LoadGeoID for more details.
        discharge_name: String. The name of the Signal geo entity related to
            the discharging location of the cargo. Examples: 'Indonesia',
            'Japan', 'Argentina'.
        discharge_taxonomy_id: Integer. An internal ID corresponding to the
            taxonomy of the mapped discharging location. See LoadTaxonomyID for
            more details.
        discharge_taxonomy: String. The extended name identifying the taxonomy
            of the mapped discharging location. Possible values are:
            GeoAsset-> 1, Port -> 2, Country-> 3, Level0->4, Level1->5,
            Level2->6, Level3->7.
        scraped_discharge2: String. The second discharging port reported in the
            original text of the cargo. It is very often shortened, very
            compact and can refer to terminals, ports, countries or wider
            areas. For example in the cargo 'al agaila 130 gabon+algeria/
            feast 14/01 rnr lord energy' the field ScrapedDischarge2 contains
            'algeria'.
        discharge_geo_id2: Integer. An internal ID corresponding to the mapped
            second discharging location of the cargo. See LoadGeoID for more
            details.
        discharge_name2: String. The name of the Signal geo entity related to
            the second discharging location of the cargo. Examples:
            'Algeria', 'Greece', 'France'.
        discharge_taxonomy_id2: Integer. An internal ID corresponding to the
            taxonomy of the mapped second discharging location. See
            LoadTaxonomyID for more details.
        discharge_taxonomy2: String. The extended name identifying the
            TaxonomyID. Possible values are: GeoAsset-> 1, Port -> 2,
            Country-> 3, Level0->4, Level1->5, Level2->6, Level3->7.
        scraped_charterer: String. The cargo charterer as reported in the
            original text. Examples: 'atc', 'unipec', 'enoc', 'ioc', 'pbras'
        charterer_id: Integer. Numeric ID corresponding to the chartering
            company that it is reported in the line. We use an internal mapper
            to find the correspondence between the reported string and our
            database.
        charterer: String. The company name corresponding to the ChartererID
            field. Provided to better specify the company involved in the
            business. Source: our internal Company Database.
        scraped_cargo_type: String. The cargo type of the cargo as reported in
            the original text, often shortened. Examples: 'nhc', 'ulsd', 'ums',
            'nap', 'go'.
        cargo_type_id: Integer. It is an internal ID corresponding to the
            mapped cargo type of the cargo. A proprietary model is responsible
            to match the reported cargo string to a specific cargo type in our
            hierarchy. Examples: 19-> Crude Oil, 16->Fueloil, 9-> Naphtha,
            135-> Unleaded Motor Spirit, 12-> Gasoil,
            60-> 'Ultra Low Sulphur Diesel (ULSD 10ppm)'.
        cargo_type: String. The extended name corresponding to the CargoTypeID
            field. Source: our internal CargoTypes database.
        cargo_type_group_id: Integer. Numeric ID corresponding to the
            high-level cargo type of the reported cargo type. It is provided to
            group cargoes and facilitate analytics. Examples: 130000->Dirty,
            120000-> Clean, 110000->IMO.
        cargo_type_group: String. The extended name corresponding to the
            CargoGroupID field. Source: our internal CargoTypes database.
        scraped_quantity: String. The cargo quantity as reported in the
            original text, including ranges and buffer. Also, it's common to
            report the required vessel class which indicates the size of
            suitable vessels. Examples: '80', '75000/10', '270', '180/10',
            'VLCC', 'Kmx/Ppmx'.
        quantity: Numeric. The mapped quantity measured in tonnes [t].
            Quantity would be equal to '180000', both for ScrapedQuantity
            '180/10' and '180000/5'.
        quantity_buffer: Numeric. The quantity buffer if reported in the cargo
            line, expressed as a fraction of 1. Examples: for
            ScrapedQuantity='75/10', QuantityBuffer=0.1.
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
        size_from: Numeric. The lower limit of the size range measured in
            tonnes [t]. Examples: for ScrapedQuantity='VLCC', SizeFrom=200000.
            For ScrapedQuantity='Kmx/Ppmx', SizeFrom=80000.
        size_to: Numeric. The upper limit of the size range measured in
            tonnes [t]. Examples: for ScrapedQuantity='VLCC', SizeTo=350000.
            For ScrapedQuantity='Kmx/Ppmx', SizeTo=110000.
        scraped_delivery_date: String. The delivery date of the time charter
            cargo as reported in the original text. It if often reported as a
            date range, e.g. '16/18 Nov', '17/19'.
        delivery_date_from: Date, format YYYY-MM-DD. The mapped date
            corresponding to the beginning of the delivery date range.
        delivery_date_to: Date, format YYYY-MM-DD. The mapped date
            corresponding to the end of the delivery date range.
        scraped_delivery_from: String. The delivery location reported in the
            original text of the cargo. Very common in the case of time charter
            cargoes. If the delivery is reported as a geographical range,
            this field contains the first string. Otherwise the only delivery
            location reported. Example: In a dry cargo like
            ''Acct IVS Supramax/ultramax Del South Africa/West Africa 1 tct to
            Cont 10 March onw 3.75 adcom pus' we have
            ScrapedRedeliveryFrom = 'South Africa' and
            ScrapedRedeliveryTo = 'West Africa'. For the cargo
            ''Nova Marine Carriers SA 25/32k dwt Dely
            W Med 29/31 March  Redely UK  3,75 adc pus' we have
            ScrapedRedeliveryFrom = 'W Med'.
        delivery_from_geo_id: Integer. An internal ID corresponding to the
            mapped delivery location of the cargo. See LoadGeoID for more
            details.
        delivery_from_name: String. The name of the Signal geo entity related
            to the delivery location of the cargo. Examples: 'E.Med' matches
            to 'East Mediterranean' (DeliveryFromGeoID=24737,
            DeliveryFromTaxonomyID=4, DeliveryFromTaxonomy='Level0'); 'PDM'
            matches to 'Ponta Da Madeira' (DeliveryFromGeoID=13013,
            DeliveryFromTaxonomyID=2, DeliveryFromTaxonomy='Port').
        delivery_from_taxonomy_id: Integer. An internal ID corresponding to the
            taxonomy of the mapped delivery to location. See LoadTaxonomyID for
            more details.
        delivery_from_taxonomy: String. The extended name identifying the
            taxonomy of the mapped delivery location. Possible values are:
            GeoAsset-> 1, Port -> 2, Country-> 3, Level0->4, Level1->5,
            Level2->6, Level3->7.
        scraped_delivery_to: String. If the delivery is reported as a
            geographical range, this field contains the end of the range as
            reported in the original text of the cargo. Example: In a dry cargo
            like ''Acct IVS Supramax/ultramax Del South Africa/West Africa 1
            tct to Cont 10 March onw 3.75 adcom pus' we have
            ScrapedDeliveryTo = 'West Africa'.
        delivery_to_geo_id: Integer. An internal ID corresponding to the mapped
            delivery location of the cargo. See LoadGeoID for more details.
        delivery_to_name: String. The name of the Signal geo entity related to
            the delivery location of the cargo. Example: 'West Africa'
            matches to 'West Africa' (DeliveryToGeoID=37,
            DeliveryToTaxonomyID=5, DeliveryToTaxonomy='Level1')
        delivery_to_taxonomy_id: Integer. An internal ID corresponding to the
            taxonomy of the mapped delivery to location. See LoadTaxonomyID for
            more details.
        delivery_to_taxonomy: String. The extended name identifying the
            taxonomy of the mapped delivery location. Possible values are:
            GeoAsset-> 1, Port -> 2, Country-> 3, Level0->4, Level1->5,
            Level2->6, Level3->7.
        scraped_redelivery_from: String. The redelivery location reported in
            the original text of the cargo. Very common in the case of time
            charter cargoes. If the redelivery is reported as a geographical
            range, this field contains the first string. Otherwise the only
            delivery location reported. Example: In a dry cargo like
            ''dely Corpus Christi 6/10 Oct trip via US Gulf redel
            Skaw-Gibraltar $35,000 + $800,000 bb - XO Shipping' we have
            ScrapedRedeliveryFrom = 'Skaw' and
            ScrapedRedeliveryTo = 'Gibraltar'. For the cargo ''dely Belawan
            20/21 Sep trip via Indonesia redel N China $39,000 - cnr'
            we have ScrapedRedeliveryFrom = 'N China'."
        redelivery_from_geo_id: Integer. An internal ID corresponding to the
            mapped redelivery location of the cargo. See LoadGeoID for more
            details.
        redelivery_from_name: String. The name of the Signal geo entity related
            to the redelivery location of the cargo.
            Example: 'N China' matches to 'North China'
            (RedeliveryFromGeoID=24666, DeliveryTaxonomyID=4,
            DeliveryTaxonomy='Level0').
        redelivery_from_taxonomy_id: Integer. An internal ID corresponding to
            the taxonomy of the mapped redelivery location. Values from 1 to 7.
            See LoadTaxonomyID for more details.
        redelivery_from_taxonomy: String. The extended name identifying the
            taxonomy of the mapped redelivery location. Possible values are:
            GeoAsset-> 1, Port -> 2, Country-> 3, Level0->4, Level1->5,
            Level2->6, Level3->7.
        scraped_redelivery_to: String. If the redelivery is reported as a
            geographical range, this field contains the end of the range as
            reported in the original text of the cargo. Example: In a dry cargo
            like ''dely Corpus Christi 6/10 Oct trip via US Gulf redel
            Skaw-Gibraltar $35,000 + $800,000 bb - XO Shipping' we have
            ScrapedRedeliveryTo = 'Gibraltar'.
        redelivery_to_geo_id: Integer. An internal ID corresponding to the
            mapped redelivery location of the cargo. See LoadGeoID for more
            details.
        redelivery_to_name: String. The name of the Signal geo entity related
            to the redelivery location of the cargo. Example: 'Gibraltar'
            matches to 'Gibraltar' (RedeliveryToGeoID=7345,
            DeliveryTaxonomyID=2, DeliveryTaxonomy='Port').
        redelivery_to_taxonomy_id: Integer. An internal ID corresponding to the
            taxonomy of the mapped redelivery location. Values from 1 to 7.
            See LoadTaxonomyID for more details.
        redelivery_to_taxonomy: String. The name of the Signal geo entity
            related to the redelivery location of the cargo. Example:
            'Gibraltar' matches to 'Gibraltar' (RedeliveryToGeoID=7345,
            DeliveryTaxonomyID=2, DeliveryTaxonomy='Port').
        charter_type_id: Integer. An internal ID to distinguish cargoes
            reporting voyage charter and time charter agreements. Possible
            values are 0 and 1.
        charter_type: String. The extended name of the type of shipping
            contract reported in the cargo. Values currently supported are
            'Voyage'->0, 'Time charter'->1.
        cargo_status_id: Numeric ID corresponding to the different values of
            the CargoStatus field. 0-> OnSubs, 1-> FullyFixed, 2 -> Failed,
            3 ->Cancelled , 4-> Available, -2 -> NotSet, -1 -> Unknown.
        cargo_status: String denoting the commercial status of a cargo if
            explicitly mentioned, like 'ffxd' for fully fixed or 'subs'/'-s-'
            for on subs.
        content: String. The full content of the cargo. For a single line cargo
            it is the line content. For multi line cargoes it is the collection
            of all the relevant parts of the text.
        sender: String. Our own mapping of the shipping company sending out the
            market report through email. This string helps grouping emails sent
            by the same organization, but from different domains. It is often
            the case for big organizations operating worldwide. For example
            Sender= 'SSY' for both domains 'ssysin.com' and 'ssy.co'.
        is_private: Boolean. A cargo is private if injected by a user into his
            own private account within TSOP. A user can provide private
            information through email forwarding, through manual contributions
            or through Slack. Private cargo information stay in the account,
            are accessible by the account users only (people within the same
            company) and are the most valuable ones.
    """

    # entity details
    cargo_id: int
    message_id: Optional[int] = None
    parsed_part_id: Optional[int] = None
    line_from: Optional[int] = None
    line_to: Optional[int] = None
    in_line_order: Optional[int] = None
    source: Optional[str] = None
    updated_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    is_deleted: Optional[bool] = False

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
    cargo_type_group_id: Optional[int] = None
    cargo_type_group: Optional[str] = None

    # quantity
    scraped_quantity: Optional[str] = None
    quantity: Optional[float] = None
    quantity_buffer: Optional[float] = None
    quantity_from: Optional[float] = None
    quantity_to: Optional[float] = None
    size_from: Optional[float] = None
    size_to: Optional[float] = None

    # delivery date
    scraped_delivery_date: Optional[str] = None
    delivery_date_from: Optional[datetime] = None
    delivery_date_to: Optional[datetime] = None

    # delivery from
    scraped_delivery_from: Optional[str] = None
    delivery_from_geo_id: Optional[int] = None
    delivery_from_name: Optional[str] = None
    delivery_from_taxonomy_id: Optional[int] = None
    delivery_from_taxonomy: Optional[str] = None

    # delivery to
    scraped_delivery_to: Optional[str] = None
    delivery_to_geo_id: Optional[int] = None
    delivery_to_name: Optional[str] = None
    delivery_to_taxonomy_id: Optional[int] = None
    delivery_to_taxonomy: Optional[str] = None

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

    # cargo status
    cargo_status_id: Optional[int] = None
    cargo_status: Optional[str] = None

    # content
    content: Optional[str] = None

    # sender
    sender: Optional[str] = None

    # debug info
    is_private: Optional[bool] = False


@dataclass(frozen=True)
class ScrapedCargoesResponse(ScrapedDataResponse[ScrapedCargo]):
    """Paged response for scraped cargoes from the Scraped Cargoes API.

    Attributes:
        next_page_token: String. The key that should be used as a parameter of
            the token to retrieve the next page.
        data: A tuple of ScrapedCargo objects retrieved for the current page.
    """

    next_page_token: Optional[str] = None
    data: Optional[Tuple[ScrapedCargo, ...]] = None
