"""Scraped Fixtures API."""

from datetime import datetime
from typing import Optional, List, Tuple

from signal_ocean.scraped_data.scraped_data_api import ScrapedDataAPI
from signal_ocean.scraped_fixtures.models import (
    ScrapedFixture,
    ScrapedFixturesResponse,
)


class ScrapedFixturesAPI(
    ScrapedDataAPI[ScrapedFixturesResponse, ScrapedFixture]
):
    """Represents Signal's Scraped Fixtures API."""

    relative_url = "scraped-fixtures-api/v5.0/fixtures"
    response_class = ScrapedFixturesResponse
    entity_ids_name = "fixture_ids"

    def get_fixtures(
        self,
        vessel_type: int,
        message_ids: Optional[List[int]] = None,
        external_message_ids: Optional[List[str]] = None,
        received_date_from: Optional[datetime] = None,
        received_date_to: Optional[datetime] = None,
        updated_date_from: Optional[datetime] = None,
        updated_date_to: Optional[datetime] = None,
        imos: Optional[List[int]] = None,
        include_details: Optional[bool] = True,
        include_scraped_fields: Optional[bool] = True,
        include_vessel_details: Optional[bool] = True,
        include_labels: Optional[bool] = True,
        include_content: Optional[bool] = True,
        include_sender: Optional[bool] = True,
        include_debug_info: Optional[bool] = True,
    ) -> Tuple[ScrapedFixture, ...]:
        """This function collects and returns the fixtures by the given filters.

        Args:
            vessel_type: Format - int32. Available values
                Tanker = 1, Dry = 3, Container = 4, Lng = 5, Lpg = 6
            message_ids: List - Comma separated list of MessageIDs
            external_message_ids: List - Comma separated list of
                ExternalMessageIDs
            received_date_from: Format - date-time (as date-time in RFC3339).
                Earliest date the fixture received.
                Cannot be combined with 'Updated' dates
            received_date_to: Format - date-time (as date-time in RFC3339).
                Latest date the fixture received.
                Cannot be combined with 'Updated' dates
            updated_date_from: Format - date-time (as date-time in RFC3339).
                Earliest date the fixture updated.
                Cannot be combined with 'Received' dates
            updated_date_to: Format - date-time (as date-time in RFC3339).
                Latest date the fixture updated.
                Cannot be combined with 'Received' dates
            imos: List - Comma separated list of IMOs
            include_details: Boolean - Whether to include
                additional fixture details in the response.
            include_scraped_fields: Boolean - Whether to include the relative
                scraped fields in the response.
            include_vessel_details: Boolean - Whether to include some vessel
                details in the response.
            include_labels: Boolean - Whether to include the relative labels in
                the response.
            include_content: Boolean - Whether to include the original message
                line (untouched) in the response.
            include_sender: Boolean - Whether to include some of the message
                sender details in the response.
            include_debug_info: Boolean - Whether to include some information
                about the distribution of the fixture in the response.

        Returns:
            An Iterable of ScrapedFixture objects, as we have defined in
            models.py Python file.
        """
        return self.get_data(
            vessel_type=vessel_type,
            message_ids=message_ids,
            external_message_ids=external_message_ids,
            received_date_from=received_date_from,
            received_date_to=received_date_to,
            updated_date_from=updated_date_from,
            updated_date_to=updated_date_to,
            imos=imos,
            include_details=include_details,
            include_scraped_fields=include_scraped_fields,
            include_vessel_details=include_vessel_details,
            include_labels=include_labels,
            include_content=include_content,
            include_sender=include_sender,
            include_debug_info=include_debug_info,
        )

    def get_fixtures_by_fixture_ids(
        self,
        fixture_ids: List[int],
        include_details: Optional[bool] = True,
        include_scraped_fields: Optional[bool] = True,
        include_vessel_details: Optional[bool] = True,
        include_labels: Optional[bool] = True,
        include_content: Optional[bool] = True,
        include_sender: Optional[bool] = True,
        include_debug_info: Optional[bool] = True,
    ) -> Tuple[ScrapedFixture, ...]:
        """This function collects and returns the fixtures by the given fixture ids.

        Args:
            fixture_ids: List - Comma separated list of fixture ids
            include_details: Boolean - Whether to include
                additional fixture details in the response.
            include_scraped_fields: Boolean - Whether to include the relative
                scraped fields in the response.
            include_vessel_details: Boolean - Whether to include some vessel
                details in the response.
            include_labels: Boolean - Whether to include the relative labels in
                the response.
            include_content: Boolean - Whether to include the original message
                line (untouched) in the response.
            include_sender: Boolean - Whether to include some of the message
                sender details in the response.
            include_debug_info: Boolean - Whether to include some information
                about the distribution of the fixture in the response.

        Returns:
            An Iterable of ScrapedFixture objects, as we have defined in
            models.py Python file.
        """
        return self.get_data_by_entity_ids(
            fixture_ids=fixture_ids,
            include_details=include_details,
            include_scraped_fields=include_scraped_fields,
            include_vessel_details=include_vessel_details,
            include_labels=include_labels,
            include_content=include_content,
            include_sender=include_sender,
            include_debug_info=include_debug_info,
        )
