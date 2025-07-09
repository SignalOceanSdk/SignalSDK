"""The vessels api."""
from typing import Optional, Tuple
from urllib.parse import urljoin
from datetime import date
from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_multiple, get_single
from signal_ocean.vessels.models import (VesselClass, VesselType,
                                         Vessel, SingleVesselPagedResponse,
                                         VesselPagedResponse,
                                         FieldHistory,
                                         VesselFieldResponse,
                                         VesselHistoryPagedResponse,
                                         VesselHistoryPerIMOPagedResponse)


class VesselsAPI:
    """Represents Signal's Vessels API."""

    relative_url = "vessels-api/v3/"
    default_pit = str(date.today())

    rename_keys = {"STSTCoating": "stst_coating",
                   "BWTS": "bwts",
                   "GHG": "ghg",
                   "VCM": "vcm",
                   "IMOType1": "imo_type_1",
                   "IMOType2": "imo_type_2",
                   "IMOType3": "imo_type_3"}

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

    def get_vessel(self,
                   imo: int,
                   includeVesselSanctions: bool = False
                   ) -> Optional[Vessel]:
        """Retrieves a vessel by its IMO.

        Args:
            imo: IMO of the vessel to retrieve.

        Returns:
            A vessel or None if no vessel with the specified IMO has
                been found.
        """
        url = urljoin(VesselsAPI.relative_url,
                      f"vessels/{imo}" +
                      f"?includeVesselSanctions={includeVesselSanctions}"
                      )
        response = get_single(self.__connection,
                              url,
                              SingleVesselPagedResponse,
                              rename_keys=VesselsAPI.rename_keys)
        return response if response is None else response.data

    def get_vessels(self,
                    name: Optional[str] = None,
                    includeVesselSanctions: bool = False
                    ) -> Tuple[Vessel, ...]:
        """Retrieves all available vessels.

        Args:
                name: String to filter and return only companies the name
                        of which contains the provided string. If None, all
                        companies are returned.

        Returns:
            A tuple of all available vessels.
        """
        endpoint = (
            ("vessels"
             if name is None else
             f"vessels/searchByName/{name}") +
            f"?includeVesselSanctions={includeVesselSanctions}"
        )
        url = urljoin(VesselsAPI.relative_url, endpoint)

        hasNextPage = True
        nextPageToken: Optional[str] = ""
        vessels: Tuple[Vessel, ...] = ()
        while(hasNextPage):
            specific_url = url + (nextPageToken
                                  if nextPageToken == ""
                                  else f"&token={nextPageToken}")
            response = get_single(self.__connection,
                                  specific_url,
                                  VesselPagedResponse,
                                  rename_keys=VesselsAPI.rename_keys)
            vessels = vessels + (response.data if response else ())
            nextPageToken = response.next_page_token if response else None
            hasNextPage = nextPageToken is not None

        return vessels

    def get_vessels_by_vessel_class(
        self, vesselClass: int,  includeVesselSanctions: bool = False
    ) -> Optional[Tuple[Vessel, ...]]:
        """Retrieves all vessels of a specific vessel class.

        Args:
                vesselClass: Vessel Class of the vessels to retrieve.

        Returns:
            A tuple of all available vessels.
        """
        endpoint = f"vessels?vesselClass={vesselClass}"
        endpoint += f"&includeVesselSanctions={includeVesselSanctions}"
        url = urljoin(VesselsAPI.relative_url, endpoint)
        vessels: Tuple[Vessel, ...] = ()
        hasNextPage = True
        nextPageToken: Optional[str] = ""
        while(hasNextPage):
            specific_url = url + (nextPageToken
                                  if nextPageToken == ""
                                  else f"&token={nextPageToken}")
            response = get_single(self.__connection,
                                  specific_url,
                                  VesselPagedResponse,
                                  rename_keys=VesselsAPI.rename_keys)
            vessels = vessels + (response.data if response else ())
            nextPageToken = response.next_page_token if response else None
            hasNextPage = nextPageToken is not None

        return vessels if len(vessels) > 0 else None

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

    def get_vessels_flag_history(
            self, imo: Optional[int] = None
    ) -> Tuple[VesselFieldResponse, ...]:
        """Retrieves all flag changes.

        Args:
                imo: IMO of the vessel to retrieve.

        Returns:
            A tuple of all flag changes.
        """
        return self.__get_history(FieldHistory.Flag, imo)

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
        elif field == FieldHistory.Flag:
            if imo is None:
                endpoint += "/flagHistory"
            else:
                endpoint += f"/{imo}/history/flags"

        url = urljoin(VesselsAPI.relative_url, endpoint)

        if imo is not None:
            response = get_single(self.__connection,
                                  url,
                                  VesselHistoryPerIMOPagedResponse)
            fieldResponse = VesselFieldResponse(imo=imo,
                                                history=response.data
                                                if response
                                                else ())
            historyResponse: Tuple[VesselFieldResponse, ...] = (
                fieldResponse, )
        else:
            next_page_token: Optional[str] = ""
            hasNextPage = True
            historyResponse = ()
            while(hasNextPage):
                specific_url = url + (next_page_token
                                      if next_page_token == ""
                                      else f"?token={next_page_token}")
                multipleHistoryResponse = get_single(
                    self.__connection,
                    specific_url,
                    VesselHistoryPagedResponse)
                historyResponse = historyResponse + (
                    multipleHistoryResponse.data
                    if multipleHistoryResponse
                    else ())
                if multipleHistoryResponse:
                    next_page_token = multipleHistoryResponse.next_page_token
                else:
                    next_page_token = None
                hasNextPage = next_page_token is not None
        return historyResponse
