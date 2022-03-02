from typing import Optional, List, Iterable
from datetime import date
from .._internals import format_iso_date, QueryString

from signal_ocean.util.request_helpers import get_multiple

from .models import ScrapedFixture
from ..connection import Connection


class ScrapedFixturesAPI:
    """Represents Signal's Scraped Fixtures API."""

    relative_url = "scraped-fixtures-api/api/public/v1/fixtures"

    page_size = 1000
    page_number = 1

    def __init__(
        self, connection: Optional[Connection] = None, max_pages: int = 10000
    ):
        """Initializes the Scraped Fixturess API.

        Args: connection: API connection configuration. If not provided,
        the default connection method is used. max_pages: max_pages to
        return. We use this parameter to avoid memory leaks
        """
        self.__connection = connection or Connection()
        self.max_pages = max_pages

    def get_fixtures(
        self,
        received_date_from: date,
        vessel_type: int,
        received_date_to: Optional[date] = None,
        updated_date_from: Optional[date] = None,
        updated_date_to: Optional[date] = None,
        include_fixture_details: Optional[bool] = True,
        include_scraped_fields: Optional[bool] = True,
        include_vessel_details: Optional[bool] = True,
        include_labels: Optional[bool] = True,
        include_content: Optional[bool] = True,
        include_sender: Optional[bool] = True,
        include_debug_info: Optional[bool] = True,
        port_id: Optional[int] = None,
        vessel_class_id: Optional[int] = None,
    ) -> Iterable[ScrapedFixture]:
        """This function returns the all the scraped fixtures for a specific
        selected port.

        Attributes: received_date_from: Format - date-time (as date-time in
        RFC3339). Earliest date the fixture received. Cannot be combined with
        'Updated' dates received_date_to: Format - date-time (as date-time in
        RFC3339). Latest date the fixture received. Cannot be combined with
        'Updated' dates vessel_type: Format - int32. Available values ►
        Tanker = 1, Dry = 3, Container = 4, Lng = 5, Lpg = 6
        updated_date_from: Format - date-time (as date-time in RFC3339).
        Earliest date the fixture updated. Cannot be combined with 'Received'
        dates updated_date_to: Format - date-time (as date-time in RFC3339).
        Latest date the fixture updated. Cannot be combined with 'Received'
        dates include_fixture_details: Boolean. Whether to include additional
        fixture details in the response. include_scraped_fields: Boolean.
        Whether to include the relative scraped fields in the response.
        include_vessel_details: Boolean. Whether to include some vessel
        details in the response. include_labels: Boolean. Whether to include
        the relative labels in the response. include_content: Whether to
        include the original message line (untouched) in the response.
        include_sender: Boolean. Whether to include some of the message
        sender details in the response. include_debug_info: Boolean. Whether
        to include some information about the distribution of the fixture in
        the response. port_id: Integer. The port id vessel_class_id: Integer.
        It is an ID corresponding to the different vessel classes of a
        certain vessel type, as split according to our internal Vessel
        Database. For example 84->VLCC, 85->Suezmax, 70->Capesize.

        Returns: An Iterable of ScrapedFixture objects, as we have defined in
        models.py.
        """

        more_fixtues = True

        results: List[ScrapedFixture] = []
        while more_fixtues and self.page_number < self.max_pages:

            query_string: QueryString = {
                "PageNumber": self.page_number,
                "PageSize": self.page_size,
                "ReceivedDateFrom": format_iso_date(received_date_from),
                "ReceivedDateTo": format_iso_date(received_date_to),
                "VesselType": vessel_type,
                "UpdatedDateFrom": format_iso_date(updated_date_from),
                "UpdatedDateTo": format_iso_date(updated_date_to),
                "IncludeFixtureDetails": include_fixture_details,
                "IncludeScrapedFields": include_scraped_fields,
                "IncludeVesselDetails": include_vessel_details,
                "IncludeLabels": include_labels,
                "IncludeContent": include_content,
                "IncludeSender": include_sender,
                "IncludeDebugInfo": include_debug_info,
            }

            fixtures = get_multiple(
                connection=self.__connection,
                relative_url=self.relative_url,
                cls=ScrapedFixture,
                query_string=query_string,
            )

            if len(fixtures) == 0:
                more_fixtues = False

            self.page_number = self.page_number + 1

            filtered_fixtures: List[ScrapedFixture] = []
            if port_id and vessel_class_id:
                filtered_fixtures = [
                    fixture
                    for fixture in fixtures
                    if (fixture.load_geo_id == port_id)
                    and (fixture.vessel_class_id == vessel_class_id)
                ]
            elif port_id:
                filtered_fixtures = [
                    fixture
                    for fixture in fixtures
                    if fixture.load_geo_id == port_id
                ]
            elif vessel_class_id:
                filtered_fixtures = [
                    fixture
                    for fixture in fixtures
                    if fixture.vessel_class_id == vessel_class_id
                ]
            else:
                results += fixtures

            if len(filtered_fixtures) > 0:
                results += filtered_fixtures

        self.page_number = 1
        return results
