"""The vessels api."""
from typing import Optional, Tuple
from urllib.parse import urljoin
from datetime import date
from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_multiple, get_single
from signal_ocean.vessels.models import (VesselClass, VesselType,
                                         Vessel, VesselPagedResponse,
                                         FieldHistory,
                                         VesselFieldResponse,
                                         DifferenceByField)


class VesselsAPI:
    """Represents Signal's Vessels API."""

    relative_url = "vessels-api/v2/"
    default_pit = str(date.today())

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes VesselsAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_vessel_classes(self) -> Tuple[VesselClass, ...]:
        """Retrieves all available vessel classes.

        Returns:
            A tuple of all available vessel classes.
        """
        url = urljoin(VesselsAPI.relative_url, "vesselClasses")
        return get_multiple(self.__connection, url, VesselClass)

    def get_vessel_types(self) -> Tuple[VesselType, ...]:
        """Retrieves all available vessel types.

        Returns:
            A tuple of all available vessel types.
        """
        url = urljoin(VesselsAPI.relative_url, "vesselTypes")
        return get_multiple(self.__connection, url, VesselType)

    def get_vessel(self, imo: int) -> Optional[Vessel]:
        """Retrieves a vessel by its IMO.

        Args:
            imo: IMO of the vessel to retrieve.

        Returns:
            A vessel or None if no vessel with the specified IMO has
                been found.
        """
        url = urljoin(VesselsAPI.relative_url, f"vessels/{imo}")
        return get_single(self.__connection, url, Vessel,
                          rename_keys={"STSTCoating": "stst_coating",
                                       "BWTS": "bwts",
                                       "GHG": "ghg"})

    def get_vessels(self, name: Optional[str] = None) -> Tuple[Vessel, ...]:
        """Retrieves all available vessels.

        Args:
                name: String to filter and return only companies the name
                        of which contains the provided string. If None, all
                        companies are returned.

        Returns:
            A tuple of all available vessels.
        """
        endpoint = (
            "vessels/all" if name is None else f"vessels/searchByName/{name}"
        )
        url = urljoin(VesselsAPI.relative_url, endpoint)
        return get_multiple(self.__connection, url, Vessel,
                            rename_keys={"STSTCoating": "stst_coating",
                                         "BWTS": "bwts",
                                         "GHG": "ghg"})

    def get_vessels_by_vessel_class(
        self, vesselClass: int
    ) -> Optional[Tuple[Vessel, ...]]:
        """Retrieves all vessels of a specific vessel class.

        Args:
                vesselClass: Vessel Class of the vessels to retrieve.

        Returns:
            A tuple of all available vessels.
        """
        endpoint = f"vessels?vesselClass={vesselClass}"
        url = urljoin(VesselsAPI.relative_url, endpoint)
        response = get_single(self.__connection, url, VesselPagedResponse,
                              rename_keys={"STSTCoating": "stst_coating",
                                           "BWTS": "bwts",
                                           "GHG": "ghg"})
        return response if response is None else response.items

    def get_vessels_name_history(
            self, imo: Optional[int] = None
    ) -> Tuple[VesselFieldResponse, ...]:
        """Retrieves all vessel names changes.

        Args:
                imo: IMO of the vessel to retrieve.

        Returns:
            A tuple of all vessel names changes.
        """
        return self.__get_history(FieldHistory.Name, imo)

    def get_vessels_commOp_history(
            self, imo: Optional[int] = None
    ) -> Tuple[VesselFieldResponse, ...]:
        """Retrieves all commOp changes.

        Args:
                imo: IMO of the vessel to retrieve.

        Returns:
            A tuple of all commOp changes.
        """
        return self.__get_history(FieldHistory.CommOp, imo)

    def __get_history(
            self,
            field: FieldHistory,
            imo: Optional[int] = None
    ) -> Tuple[VesselFieldResponse, ...]:
        endpoint = "vessels"
        if field == FieldHistory.Name:
            if imo is None:
                endpoint += "/nameHistory"
            else:
                endpoint += f"/{imo}/history/names"
        elif field == FieldHistory.CommOp:
            if imo is None:
                endpoint += "/commOpHistory"
            else:
                endpoint += f"/{imo}/history/commOps"

        url = urljoin(VesselsAPI.relative_url, endpoint)

        if imo is not None:
            historyChanges = get_multiple(self.__connection,
                                          url,
                                          DifferenceByField)
            fieldResponse = VesselFieldResponse(imo=imo,
                                                history=historyChanges)
            response = (fieldResponse, )  # type:Tuple[VesselFieldResponse,...]
        else:
            history = get_multiple(self.__connection, url, VesselFieldResponse)
            response = history

        return response
