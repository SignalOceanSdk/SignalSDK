"""Models instantiated by the geos api."""
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Area:
    """Contains all details of an area.

    Attributes:
        area_id: The area identifier.
        area_name: The name of the area.
        location_taxonomy_id: GeoAsset (1), Port (2), Country (3),
            Level0 (4), Level1 (5), Level2 (6), Level3 (7),
            Invalid (-3), NotSet (-2), Unknown (-1).
        location_taxonomy_name: The name of the Location Taxonomy.
        parent_area_id: The parent area identifier.
        parent_area_name: The parent area name.
    """
    area_id: int
    location_taxonomy_id: int
    location_taxonomy_name: str
    area_name: Optional[str] = None
    parent_area_id: Optional[int] = None
    parent_area_name: Optional[str] = None


@dataclass(frozen=True)
class Country:
    """Contains all details of an country.

    Attributes:
        country_id: The country identifier.
        country_name: The name of the country.
        location_taxonomy_id: GeoAsset (1), Port (2),
            Country (3), Level0 (4), Level1 (5),
            Level2 (6), Level3 (7), Invalid (-3),
            NotSet (-2), Unknown (-1).
        location_taxonomy_name: The name of the Location Taxonomy.
        country_code: Two-letter country codes (ISO).
        country_code_numeric: Three-digit country codes (ISO).
        country_code_iso3: Three-letter country codes (ISO).
    """
    country_id: int
    country_name: str
    location_taxonomy_id: int
    location_taxonomy_name: str
    country_code: Optional[str] = None
    country_code_numeric: Optional[str] = None
    country_code_iso3: Optional[str] = None


@dataclass(frozen=True)
class GeoAsset:
    """Contains all details of a geo asset.

    Attributes:
        geo_asset_id: The geo asset identifier.
        location_taxonomy_id: GeoAsset (1), Port (2),
            Country (3), Level0 (4), Level1 (5),
            Level2 (6), Level3 (7), Invalid (-3),
            NotSet (-2), Unknown (-1).
        location_taxonomy_name: The name of the Location Taxonomy.
        geo_asset_name: The name of the geo asset.
        country_id: The country identifier.
        country_name: The parent area identifier.
        area_id_level0: The level0 area identifier.
        area_name_level0: The level0 area name.
        area_id_level1: The level1 area identifier.
        area_name_level1: The level1 area name.
        area_id_level2: The level2 area identifier.
        area_name_level2: The level2 area name.
        area_id_level3: The level3 area identifier.
        area_name_level3: The level3 area name.
        port_id: The port identifier.
        port_name: The port name.
        latitude: The position's latitude.
        longitide: he position's longitude.
    """
    geo_asset_id: int
    location_taxonomy_id: int
    location_taxonomy_name: str
    geo_asset_name: Optional[str] = None
    country_id: Optional[int] = None
    country_name: Optional[str] = None
    area_id_level0: Optional[int] = None
    area_name_level0: Optional[str] = None
    area_id_level1: Optional[int] = None
    area_name_level1: Optional[str] = None
    area_id_level2: Optional[int] = None
    area_name_level2: Optional[str] = None
    area_id_level3: Optional[int] = None
    area_name_level3: Optional[str] = None
    port_id: Optional[int] = None
    port_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass(frozen=True)
class Port:
    """Contains all details of a port.

    Attributes:
        port_id: The geo asset identifier.
        location_taxonomy_id: GeoAsset (1), Port (2), Country (3),
            Level0 (4), Level1 (5), Level2 (6),
            Level3 (7), Invalid (-3), NotSet (-2), Unknown (-1).
        location_taxonomy_name: The name of the Location Taxonomy.
        port_name: The name of the geo asset.
        unlocode: The Unlocode of the port.
        country_id: The country identifier.
        country_name: The parent area identifier.
        area_id_level0: The level0 area identifier.
        area_name_level0: The level0 area name.
        area_id_level1: The level1 area identifier.
        area_name_level1: The level1 area name.
        area_id_level2: The level2 area identifier.
        area_name_level2: The level2 area name.
        area_id_level3: The level3 area identifier.
        area_name_level3: The level3 area name.
        latitude: The position's latitude.
        longitide: he position's longitude.
    """
    port_id: int
    location_taxonomy_id: int
    location_taxonomy_name: str
    port_name: Optional[str] = None
    unlocode: Optional[str] = None
    country_id: Optional[int] = None
    country_name: Optional[str] = None
    area_id_level0: Optional[int] = None
    area_name_level0: Optional[str] = None
    area_id_level1: Optional[int] = None
    area_name_level1: Optional[str] = None
    area_id_level2: Optional[int] = None
    area_name_level2: Optional[str] = None
    area_id_level3: Optional[int] = None
    area_name_level3: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass(frozen=True)
class AreasPagedResponse:
    """Paged response for areas from the Geos API.

    Attributes:
        data: The structure that contains records retrieve for the current
            page.
    """
    data: Optional[Tuple[Area, ...]] = None


@dataclass(frozen=True)
class GeoAssetsPagedResponse:
    """Paged response for geo Assets from the Geos API.

    Attributes:
        data: The structure that contains records retrieve for the current
            page.
    """
    data: Optional[Tuple[GeoAsset, ...]] = None


@dataclass(frozen=True)
class CountriesPagedResponse:
    """Paged response for countries from the Geos API.

    Attributes:
        data: The structure that contains records retrieve for the current
            page.
    """
    data: Optional[Tuple[Country, ...]] = None


@dataclass(frozen=True)
class PortsPagedResponse:
    """Paged response for ports from the Geos API.

    Attributes:
        data: The structure that contains records retrieve for the current
            page.
    """
    data: Optional[Tuple[Port, ...]] = None
