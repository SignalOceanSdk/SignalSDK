"""The Supply API client."""
from datetime import date
from typing import Any, Dict, Optional, Tuple, Union

import requests

from ..connection import Connection
from .filters import LiveSupplyFilter, SupplyFilter
from .models import SupplySnapshot, SupplyTrend
from .templates import (
    SupplyTemplate,
    build_filter_body,
    find_template,
    get_supply_templates,
)


class SupplyAPI:
    """Retrieves vessel supply: daily counts, one day's vessels, live."""

    relative_url = "supply-api/v1/supply/"

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes the Supply API.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_supply_trend(
        self,
        start_date: date,
        end_date: date,
        template: Optional[str] = None,
        filters: Optional[SupplyFilter] = None,
    ) -> SupplyTrend:
        """Count the vessels that match the filters on each day of a range.

        Args:
            start_date: First day of the range.
            end_date: Last day of the range.
            template: A Baltic route code, for example `TD3C`. See
                `get_supply_templates`.
            filters: Filters. A field set here replaces the template's
                value for that field.

        Returns:
            One count per day, and the API's notes.
        """
        body = {
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            **_filter_body(template, filters),
        }
        data = self.__post("supply-trend", body)
        return SupplyTrend.model_validate(data)

    def get_historical_supply(
        self,
        day: date,
        template: Optional[str] = None,
        filters: Optional[SupplyFilter] = None,
        use_only_hub_ports: Optional[bool] = None,
    ) -> SupplySnapshot:
        """Get the vessels that matched the filters on one past day.

        Each subscription key can make a limited number of these calls per
        day.

        Args:
            day: The snapshot day.
            template: A Baltic route code, for example `TD3C`.
            filters: Filters. A field set here replaces the template's
                value for that field.
            use_only_hub_ports: True remaps each ETA basis port that is not
                a hub port to the hub port of its region. False uses the
                ports as given. None sends nothing, so the API default
                (False) applies.

        Returns:
            One record per vessel.
        """
        body = {
            "startDate": day.isoformat(),
            "endDate": day.isoformat(),
            **_filter_body(template, filters),
        }
        headers = None
        if use_only_hub_ports is not None:
            headers = {"UseOnlyHubPorts": str(use_only_hub_ports).lower()}
        data = self.__post("historical-raw-data", body, headers)
        return SupplySnapshot.model_validate(data)

    def get_live_supply(
        self,
        template: Optional[str] = None,
        filters: Optional[Union[SupplyFilter, LiveSupplyFilter]] = None,
        include_details: bool = False,
    ) -> SupplySnapshot:
        """Get the vessels that match the filters now.

        Args:
            template: A Baltic route code, for example `TD3C`.
            filters: Filters. Use `LiveSupplyFilter` for ETA calculations
                with routing restrictions.
            include_details: True adds your company's notes to each record.

        Returns:
            One record per vessel.
        """
        body: Dict[str, Any] = dict(_filter_body(template, filters))
        if include_details:
            body["includeDetails"] = True
        data = self.__post("supply", body)
        snapshot = SupplySnapshot.model_validate(data)
        return snapshot.model_copy(update={"include_details": include_details})

    def get_supply_templates(self) -> Tuple[SupplyTemplate, ...]:
        """Get the Baltic route templates.

        Returns:
            The templates. Pass a template's `code` as `template`.
        """
        return get_supply_templates()

    def __post(
        self,
        operation: str,
        body: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        response = self.__connection._make_post_request(
            self.relative_url + operation, body, headers=headers
        )
        _raise_for_status(response)
        return response.json()


def _filter_body(
    template: Optional[str],
    filters: Optional[Union[SupplyFilter, LiveSupplyFilter]],
) -> Dict[str, Any]:
    return build_filter_body(
        find_template(template) if template else None, filters
    )


def _raise_for_status(response: requests.Response) -> None:
    """Raise HTTPError with the API's own message for a non-2xx response."""
    if response.ok:
        return
    message = f"{response.status_code} {response.reason} for url: "
    message += str(response.url)
    detail = _error_detail(response)
    if detail:
        message += f": {detail}"
    raise requests.HTTPError(message, response=response)


def _error_detail(response: requests.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        body = None
    if not isinstance(body, dict):
        return response.text.strip()[:500]

    parts = [str(body[key]) for key in ("title", "detail", "message")
             if body.get(key)]
    errors = body.get("errors")
    if isinstance(errors, dict):
        for field, messages in errors.items():
            if isinstance(messages, list):
                messages = "; ".join(str(m) for m in messages)
            parts.append(f"{field}: {messages}")
    parts += [f"{key}: {body[key]}" for key in ("TrackingId", "traceId")
              if body.get(key)]
    return " | ".join(parts) if parts else response.text.strip()[:500]
