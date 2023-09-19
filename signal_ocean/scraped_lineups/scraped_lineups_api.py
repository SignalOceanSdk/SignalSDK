"""Scraped Lineups API."""

from datetime import datetime
from typing import Optional, List, Tuple

from signal_ocean.scraped_data.scraped_data_api import ScrapedDataAPI
from signal_ocean.scraped_lineups.models import (
    ScrapedLineup,
    ScrapedLineupsResponse,
)


class ScrapedLineupsAPI(ScrapedDataAPI[ScrapedLineupsResponse, ScrapedLineup]):
    """Represents Signal's Scraped Lineups API."""

    relative_url = "scraped-lineups-api/v5.0/lineups"
    response_class = ScrapedLineupsResponse
    entity_ids_name = "lineup_ids"

    def get_lineups(
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
    ) -> Tuple[ScrapedLineup, ...]:
        """This function collects and returns the lineups by the given filters.

        Args:
            vessel_type: Format - int32. Available values
                Tanker = 1, Dry = 3, Container = 4, Lng = 5, Lpg = 6
            message_ids: List - Comma separated list of MessageIDs
            external_message_ids: List - Comma separated list of
                ExternalMessageIDs
            received_date_from: Format - date-time (as date-time in RFC3339).
                Earliest date the lineup received.
                Cannot be combined with 'Updated' dates
            received_date_to: Format - date-time (as date-time in RFC3339).
                Latest date the lineup received.
                Cannot be combined with 'Updated' dates
            updated_date_from: Format - date-time (as date-time in RFC3339).
                Earliest date the lineup updated.
                Cannot be combined with 'Received' dates
            updated_date_to: Format - date-time (as date-time in RFC3339).
                Latest date the lineup updated.
                Cannot be combined with 'Received' dates
            imos: List - Comma separated list of IMOs
            include_details: Boolean - Whether to include
                additional lineup details in the response.
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
                about the distribution of the lineup in the response.

        Returns:
            An Iterable of ScrapedLineup objects, as we have defined in
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

    def get_lineups_by_lineup_ids(
        self,
        lineup_ids: List[int],
        include_details: Optional[bool] = True,
        include_scraped_fields: Optional[bool] = True,
        include_vessel_details: Optional[bool] = True,
        include_labels: Optional[bool] = True,
        include_content: Optional[bool] = True,
        include_sender: Optional[bool] = True,
        include_debug_info: Optional[bool] = True,
    ) -> Tuple[ScrapedLineup, ...]:
        """This function collects and returns the lineups by the given lineup ids.

        Args:
            lineup_ids: List - Comma separated list of lineup ids
            include_details: Boolean - Whether to include
                additional lineup details in the response.
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
                about the distribution of the lineup in the response.

        Returns:
            An Iterable of ScrapedLineup objects, as we have defined in
            models.py Python file.
        """
        return self.get_data_by_entity_ids(
            lineup_ids=lineup_ids,
            include_details=include_details,
            include_scraped_fields=include_scraped_fields,
            include_vessel_details=include_vessel_details,
            include_labels=include_labels,
            include_content=include_content,
            include_sender=include_sender,
            include_debug_info=include_debug_info,
        )
