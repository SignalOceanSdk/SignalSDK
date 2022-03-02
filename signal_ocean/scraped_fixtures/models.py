"""Models instantiated by the scraped fixtures api."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ScrapedFixture:
    """Detailed information about a scraped fixtures.

    Attributes:
        fixture_id: Integer. A unique identifier of the fixture line.
        message_id: Integer. A unique identifier of the message containing
            the specific fixture. A message can contain more than one fixture.
        updated_date: String, format YYYY-MM-DD HH:MM:SS, UTC timezone. Date
            on which the fixture has been reevaluated for the last time. In
            case of an email received by a broker one month ago and reprocessed
            through our engine today, this date will be today's.
        received_date: String, format YYYY-MM-DD HH:MM:SS, UTC timezone.
            Date on which the fixture has been injected into our system
            and processed.
        reported_fixture_date: String, format YYYY-MM-DD. Only occasionally
            reported. Some tanker market reports summarize the fixtures of the
            week by splitting them per day. This day is generally reported in
            the text as a header. If present and if correctly extracted, the
            field
            ReportedFixtureDate refers to that date.
        imo: Integer. The seven-digits number that uniquely identifies the ship
            reported in the fixture.
        vessel_class_id: Integer. It is an ID corresponding to the different
            vessel classes of a certain vessel type, as split according to our
            internal. Vessel Database.
            For example 84->VLCC, 85->Suezmax, 70->Capesize."
        laycan_from: Date, format YYYY-MM-DD. The mapped date corresponding to
            the beginning of the laycan date range.
        laycan_to: Date, format YYYY-MM-DD. The mapped date corresponding to
            the end of the laycan date range.
        load_geo_id: Integer. It is the internal ID of the mapped loading
            location
            reported in the fixture. Our models convert and map a scraped
            string
            containing geo information to a specific entity of the Signal's
            proprietary
            geofencing structure. Each geo entity is identified by a taxonomy,
            an ID and a name.
        load_taxonomy_id: Integer. An internal ID corresponding to each
            taxonomy,the level of geo details, from 1 to 7
        discharge_geo_id: Integer. An internal ID corresponding to the mapped
            discharging location of the fixture.See LoadGeoID for more details.
        discharge_taxonomy_id: Integer. An internal ID corresponding to the
            taxonomy of the mapped discharging location. See LoadTaxonomyID for
            more details.
        charterer_id: Integer. Numeric ID corresponding to the
            chartering company that it is reported in the line. We use an
            internal mapper to find the correspondence between the reported
            string and our database.
        cargo_type_id: "Integer. It is an internal
            ID corresponding to the mapped cargo type of the fixture. A
            proprietary model is responsible to match the reported cargo string
            to a specific cargo type in our hierarchy.
        cargo_group_id: Integer. Numeric ID corresponding to the
            high-level cargo of the fixture cargo.
            It is provided to group fixtures and facilitate analytics.
        quantity: Numeric. The mapped quantity measured in tonnes [t].
            Quantity would be equal to "180000", both for ScrapedQuantity
            "180/10" and "180000/5".
        quantity_buffer: "Numeric. The quantity
            buffer if reported in the fixture line, expressed as a fraction of
            1.
        quantity_from: Numeric. The lower limit of the quantity range
            measured in tonnes [t], computed as
            QuantityFrom=(1-QuantityBuffer)*Quantity.
        quantity_to: "Numeric. The upper limit of the quantity range measured
            in tonnes [t],computed as QuantityFrom=(1+QuantityBuffer)*Quantity.
        rate_value: "Numeric. The mapped rate of the fixture. If lump sum,
            the rate is reported in USD.
        rate_type: String. The type associated to the RateValue.
        open_geo_id: "Integer. An internal ID
            corresponding to the mapped open location. The fields starting with
            ""Open"" (OpeGeoID, OpenGeoName, OpenTaxonomyID, OpenTaxonomy and
            OpenDate) are populated if a fixture is partial. Such a fixture is
            marked by the boolean ""IsPartial"" (see below) being true. In our
            system a fixture is partial if the discharge location is missing.
        partial fixtures: the most common one is the case of a line in a
            tonnage list containing a subs indication
            and the second one is a fixture with no details contained in a
            fixture report.
        open_taxonomy_id: Integer. An internal ID
            corresponding to the taxonomy of the mapped open location. See
            LoadTaxonomyID for more details.
        open_date: Date, format YYYY-MM-DD.The mapped open date.
            delivery_date_from: Date, format YYYY-MM-DD. The mapped date
            corresponding to the beginning of the delivery date
            range.
        delivery_date_to: Date, format YYYY-MM-DD. The mapped date
            corresponding to the end of the delivery date range.
        delivery_geo_id: Integer. An internal ID corresponding
            to the mapped delivery location of the fixture.
            See LoadGeoID for more details.
        delivery_taxonomy_id: Integer. An internal ID corresponding to the
            taxonomy of the mapped delivery location. Values from 1 to 7. See
            LoadTaxonomyID for more details.
        redelivery_from_geo_id: Integer. An internal ID corresponding to the
            mapped redelivery location of the fixture. See LoadGeoID for more
            details.
        redelivery_from_taxonomy_id: Integer. An internal ID corresponding to
            the taxonomy of the mapped redelivery location. Values from 1 to 7.
            See LoadTaxonomyID for more details.
        redelivery_to_geo_id: Integer. An internal ID corresponding to the
            mapped redelivery location of the fixture. See LoadGeoID for more
            details.
        redelivery_to_taxonomy_id: Integer. An internal ID
            corresponding to the taxonomy of the mapped redelivery location.
            Values from 1 to 7. See LoadTaxonomyID for more details.
        charter_type_id: Integer. An internal ID to distinguish fixtures
            reporting voyage charter and time charter agreements.
            Possible values are 0 and 1.
        fixture_status_id: Numeric ID corresponding to the
            different values of the FixtureStatus field. 0-> OnSubs,
            1-> FullyFixed, 2 -> Failed, 3 ->Cancelled , 4-> Available,
            -2 -> NotSet, -1 -> Unknown.
        is_owners_option: Boolean. This value is
            true if "o/o" (Owner's Option) or "oos" is explicitly reported in
            the original text of the fixture.
        is_coa: Boolean. This value is true if
            "COA" (Contract of Affreightment) or "o/p" (Own Program) is
            explicitly reported in the original text of the fixture.

        Include details
        parsed_part_id: Integer. A unique identifier for each
            email part. The email body and each attachment are considered
            different parsed parts. For an example the email body and its pdf
            attachment have same MessageID and different ParsedPartID.
        line_from:Nullable integer. The starting line from which the fixture
            is extracted. The email subject counts as  line 0 and the body
            content starts from line 1.
        line_to: Nullable integer. The final line
            from which the fixture is extracted. For single line fixtures
            LineFrom is equal to LineTo. For descriptive fixtures that span
            across multiple lines we have LineTo>LineFrom. These two numbers
            help the user identify which part of the text has been used to
            extract the fixture data.
        in_line_order: Nullable integer. This integer is used
            to list different fixtures extracted from the same line. It is the
            case for fixtures with different discharge options.A fixture with a
            discharge and an option like "med-ukc" is interpreted in our system
            as 2 fixtures with same MessageID, same ParsedPartID,
            same LineNumber, same IMO, different FixtureID and an incremental
            InLineOrder number.
        source: String. It describes the source of the
            information. Our system allows the user to inject data in many
            different ways, namely through email (Source="Email"), through
            Slack channels (Source="Slack") or through manual contributions
            directly from our frontend platform TSOP (Source="User").

        Include scraped fields
        scraped_vessel_name: String. The vessel name
            as reported in the fixture line, i.e. "Signal Alpha", "Cpt A
            Stellatos", "Genco Tiberius". "TBN" can also be found.
        scraped_deadweight: String. The dead weight of the vessel as reported
            in the fixture line, i.e. "150249", "167".
        scraped_year_build:
            String. The year built of the vessel as reported in the fixture
            line, i.e. "2004", "09".
        scraped_laycan: String. The laycan (latest day of
            cancellation) of the fixture as reported in the original text.It if
            often reported as a date range, e.g. "25-jan 27-jan", "31-1 feb",
            "11-12 apr".The string "dnr" (date not reported) can also be found.
        scraped_load: "String. The loading location reported in the original
            text of the fixture. It is very often shortened, very compact and
            can refer to terminals, ports, countries or wider areas.
        scraped_discharge: "String. The discharging port reported in
            the original text of the fixture. It is very often shortened,
            very compact and can refer to terminals, ports, countries or wider
            areas.
        scraped_discharge_options: "String. All the discharging
            options reported in the original text of the fixture.
        scraped_charterer: String. The fixture charterer as reported in the
            original text.
        scraped_cargo_type: "String. The fixture cargo as reported in the
            original text, often shortened.
        scraped_quantity: "String. The fixture quantity as
            reported in the original text, including ranges and buffer.
        scraped_rate: String. The
            fixture rate as reported in the original text, including its units
            or type.
        scraped_rate_options:"String. All the rates corresponding to
            the discharging options reported in the original text of the
            fixture.
        scraped_delivery_date: String. The delivery date of the time charter
            fixture as reported in the original text.
            It if often reported as a date range, e.g. "16/18 Nov", "17/19".
        scraped_delivery: String. The delivery location
            reported in the original text of the fixture. Very common in the
            case of time charter fixtures.
            The string can refer to waypoints, ports, countries or wider areas.
        scraped_redelivery_from: "String. The
            redelivery location reported in the original text of the fixture.
            Very common in the case of time charter fixtures. If the redelivery
            is reported as a geographical range, this field contains the first
            string. Otherwise the only delivery location reported.
        scraped_redelivery_to: "String. If the redelivery is reported as a
            geographical range, this field contains the end of the range as
            reported in the original text of the fixture.


        Include vessel details
        vessel_name: String. It is the vessel name
            corresponding to the IMO mentioned above. Provided to better
            specify the vessel and its particulars.
        deadweight: Integer. The dead weight in tonnes [t] corresponding to
            the IMO mentioned above.
        year_build: Integer, YYYY format. The year
            the vessel was built.
        liquid_capacity: Integer, measured in cbm [cbm]. The liquid capacity
            of the IMO mentioned above.
        vessel_type_id: "Integer. Numeric ID corresponding to the different
            values of the VesselType field. 1->Tanker, 3-> Dry, 4 ->Containers,
            5 ->LNG (Liquified Natural gas) , 6-> LPG (Liquified Petroleum Gas)
        vessel_type: String. Description of the type of the vessel (
            VesselTypeID), based on the carried cargo. Main categories are
            Tankers, Dry (bulk carriers), Containers, LNG and LPG.
        vessel_class: "String. Name of the vessel class the vessel belongs to.
            Assignment of a vessel to a certain VesselClass is based on the
            VesselType and the value of its Deadweight (if Tanker or Dry), its
            LiquidCap (if LNG/LPG) or its TEU (if Containers).
        commercial_operator_id: Integer.
            Numeric ID corresponding to the maritime company that commercially
            manages the vessel corresponding to the IMO mentioned above.
        commercial_operator: "String. Name of
            the maritime company associated to CommercialOperatorID.



        Include labels
        load_name: "String. The name of the Signal geo entity
            related to the reported loading location of the fixture.
        load_taxonomy: "String. The
            extended name identifying the TaxonomyID.
        Possible values are:
            GeoAsset-> 1, Port -> 2, Country-> 3, Level0->4, Level1->5,
            Level2->6, Level3->7. "
        discharge_name: String. The name of the Signal geo entity related to
            the discharging location of the fixture.
        discharge_taxonomy:
            "String. The extended name identifying the taxonomy of the mapped
            discharging location. Possible values are: GeoAsset-> 1, Port -> 2,
            Country-> 3, Level0->4, Level1->5, Level2->6, Level3->7. "
        charterer: String. The company name corresponding to the ChartererID
            field.
            Provided to better specify the company involved in the business.
        cargo_type: String. The
            extended name corresponding to the CargoTypeID field.
        cargo_group: String. The extended name
            corresponding to the CargoGroupID field.
        open_taxonomy: "String. The extended name identifying the taxonomy
            of the mapped open location. Possible values
            are: GeoAsset-> 1, Port -> 2, Country-> 3, Level0->4, Level1->5,
            Level2->6, Level3->7. "
        redelivery_from_name: "String. The name of
            the Signal geo entity related to the redelivery location of the
            fixture.
        delivery_name: "String. The name of the Signal geo entity
            related to the delivery location of the fixture.
        open_geo_name:
            String. The name of the Signal geo entity related to the open
            location of the partial fixture.
        redelivery_from_taxonomy:"String. The extended name
            identifying the taxonomy of the mapped redelivery location.Possible
            values are: GeoAsset-> 1, Port -> 2, Country-> 3, Level0->4,
            Level1->5, Level2->6, Level3->7. "
        redelivery_to_name: "String. The
            name of the Signal geo entity related to the redelivery location of
            the fixture.
        redelivery_to_taxonomy: "String. The extended name
            identifying the taxonomy of the mapped redelivery location.Possible
            values are: GeoAsset-> 1, Port -> 2, Country-> 3, Level0->4,
            Level1->5, Level2->6, Level3->7. "
        charterer_type: "String. The
            extended name of the type of shipping contract reported in the
            fixture. Values currently supported are ""Voyage""->0, ""Time
            charter""->1."
        fixture_status: String denoting the commercial status
            of a fixture if explicitly mentioned, like "ffxd" for fully fixed
            or "subs"/"-s-" for on subs.

        Include content
        content: String. The full content of the fixture. For
            a single line fixture it is the line content.

        include sender
        sender: String. The full address of the email's
            sender. Examples from our public reports are: "tanker@braemar.com",
            "galtanker@galbraiths.co.uk". These public reports are marked by a
            blue [PUBLIC] tag in the TSOP Emails Dashboard.
        sender_name: String.
            The sender's name as setup in the sender's email client.
        sender_domain: String.The sender's domain.
        mapped_sender: Optional[str] = String. Our own mapping of the
            shipping company sending out the market report through email.  This
            string helps grouping emails sent by the same organization,but from
            different domains. It is often the case for big organizations
            operating worldwide.

        # include debug info
        is_private: Boolean. A fixture is private if injected by
            a user into his own private account within TSOP. A user can provide
            private information through email forwarding, through manual
            contributions or through Slack. Private fixture information stay in
            the account,are accessible by the account users only (people within
            the same company) and are the most valuable ones.
        is_shared: Boolean.
            A fixture is "Shared" if provided by a source to a list of
            subscribers. In some cases the source is a brokerage company and
            the subscribers are commercial operators only.
        is_invalidated: Boolean. A fixture is invalidated whenever a user
            selects "Ignore this fixture" from the Reported Fixtures dashboard
            in TSOP.
        is_partial: Boolean. A
            fixture is partial if the discharge field is missing. The two most
            common categories of partial fixtures are the fixtures generated by
            an "on subs" indication in a tonnage list line and those included
            in a fixture report with vessel name, laycan and load port only.

    """

    fixture_id: int
    message_id: int
    updated_date: datetime
    received_date: datetime
    reported_fixture_date: Optional[str] = None
    imo: Optional[int] = None
    vessel_class_id: Optional[int] = None
    laycan_from: Optional[datetime] = None
    laycan_to: Optional[datetime] = None
    load_geo_id: Optional[int] = None
    load_taxonomy_id: Optional[int] = None
    discharge_geo_id: Optional[int] = None
    discharge_taxonomy_id: Optional[int] = None
    charterer_id: Optional[int] = None
    cargo_type_id: Optional[int] = None
    cargo_group_id: Optional[int] = None
    quantity: Optional[float] = None
    quantity_buffer: Optional[float] = None
    quantity_from: Optional[float] = None
    quantity_to: Optional[float] = None
    rate_value: Optional[float] = None
    rate_type: Optional[str] = None
    open_geo_id: Optional[int] = None
    open_taxonomy_id: Optional[int] = None
    open_date: Optional[datetime] = None
    delivery_date_from: Optional[datetime] = None
    delivery_date_to: Optional[datetime] = None
    delivery_geo_id: Optional[int] = None
    delivery_taxonomy_id: Optional[int] = None
    redelivery_from_geo_id: Optional[int] = None
    redelivery_from_taxonomy_id: Optional[int] = None
    redelivery_to_geo_id: Optional[int] = None
    redelivery_to_taxonomy_id: Optional[int] = None
    charter_type_id: Optional[int] = None
    fixture_status_id: Optional[int] = None
    is_owners_option: Optional[bool] = False
    is_coa: Optional[bool] = False

    # include details
    parsed_part_id: Optional[int] = None
    line_from: Optional[int] = None
    line_to: Optional[int] = None
    in_line_order: Optional[int] = None
    source: Optional[str] = None

    # include scraped fields
    scraped_vessel_name: Optional[str] = None
    scraped_deadweight: Optional[str] = None
    scraped_year_build: Optional[str] = None
    scraped_laycan: Optional[str] = None
    scraped_load: Optional[str] = None
    scraped_discharge: Optional[str] = None
    scraped_discharge_options: Optional[str] = None
    scraped_charterer: Optional[str] = None
    scraped_cargo_type: Optional[str] = None
    scraped_quantity: Optional[str] = None
    scraped_rate: Optional[str] = None
    scraped_rate_options: Optional[str] = None
    scraped_delivery_date: Optional[str] = None
    scraped_delivery: Optional[str] = None
    scraped_redelivery_from: Optional[str] = None
    scraped_redelivery_to: Optional[str] = None

    # Include vessel details
    vessel_name: Optional[str] = None
    deadweight: Optional[int] = None
    year_build: Optional[int] = None
    liquid_capacity: Optional[int] = None
    vessel_type_id: Optional[int] = None
    vessel_type: Optional[str] = None
    vessel_class: Optional[str] = None
    commercial_operator_id: Optional[int] = None
    commercial_operator: Optional[str] = None

    # include labels
    load_name: Optional[str] = None
    load_taxonomy: Optional[str] = None
    discharge_name: Optional[str] = None
    discharge_taxonomy: Optional[str] = None
    charterer: Optional[str] = None
    cargo_type: Optional[str] = None
    cargo_group: Optional[str] = None
    open_taxonomy: Optional[str] = None
    redelivery_from_name: Optional[str] = None
    delivery_name: Optional[str] = None
    open_geo_name: Optional[str] = None
    redelivery_from_taxonomy: Optional[str] = None
    redelivery_to_name: Optional[str] = None
    redelivery_to_taxonomy: Optional[str] = None
    charterer_type: Optional[str] = None
    fixture_status: Optional[str] = None

    # include content
    content: Optional[str] = None

    # include sender
    sender: Optional[str] = None
    sender_name: Optional[str] = None
    sender_domain: Optional[str] = None
    mapped_sender: Optional[str] = None

    # include debug info
    is_public: Optional[bool] = False
    is_private: Optional[bool] = False
    is_shared: Optional[bool] = False
    is_invalidated: Optional[bool] = False
    is_partial: Optional[bool] = False
