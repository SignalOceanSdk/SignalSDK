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
        geo_asset_type_id: Refinery (1), Storage (2),
            Anchorage (3), SPM_SBM (4), Terminal (5), Dock (6), Platform (7),
            Scrapyard (8), FPSO (9), Shipyard (10), SBM (11), FSO (12),
            Plant (13), Lightering (14), MOPU (15), Port (16), Waypoint (17)
        geo_asset_type_name: The name of the geo asset type.
        country_id: Numeric ID of the country.
        country_name: Name of the country.
        area_id_level0: Numeric ID corresponding to the level 0 area the geo
            asset belongs to. Level 0 areas offer a detailed breakdown of the
            globe to the areas of maritime interest. Examples of level 0 areas
            include "Arabian Gulf", "US Gulf" and "East Mediterranean".
        area_name_level0: Name of the area the geo asset belongs to. Level 0
            areas offer a detailed breakdown of the globe to the areas of
            maritime interest. Examples of level 0 areas include "Arabian
            Gulf", "US Gulf" and "East Mediterranean".
        area_id_level1: Numeric ID corresponding to the level 1 area the geo
            asset belongs to. Level 1 areas consist of one or multiple level
            0 areas. For example, level 1 area "Mediterranean" groups
            together the level 0 areas "West Mediterranean", "Central
            Mediterranean" and "East Mediterranean".
        area_name_level1: Name of the area the geo asset belongs to. Level 1
            areas consist of one or multiple level 0 areas. For example, level
            1 area "Mediterranean" groups together the level 0 areas "West
            Mediterranean", "Central Mediterranean" and "East Mediterranean".
        area_id_level2: Numeric ID corresponding to the level 2 area the geo
            asset belongs to. Level 2 areas consist of one or multiple level 1
            areas. For example, level 2 area "Mediterranean/UK Continent"
            groups together the "Mediterranean" and "UK Continent" level 1
            areas.
        area_name_level2: Name of the area the geo asset belongs to. Level 2
            areas consist of one or multiple level 1 areas. For example, level
            2 area "Mediterranean/UK Continent" groups together the
            "Mediterranean" and "UK Continent" level 1 areas.
        area_id_level3: Numeric ID corresponding to the level 3 area the geo
            asset belongs to. Level 3 areas the highest area grouping in our
            taxonomy. Examples of such areas are "Pacific America" or "Africa".
            These group together level 2 areas. For instance, "Pacific America"
            groups together the level 2 areas "West Coast North America",
            "West Coast Mexico", "West Coast Central America" and "West Coast
            South America".
        area_name_level3: Name of the area the geo asset belongs to. Level 3
            areas the highest area grouping in our taxonomy. Examples of such
            areas are "Pacific America" or "Africa". These group together level
            2 areas. For instance, "Pacific America" groups together the level
            2 areas "West Coast North America", "West Coast Mexico", "West
            Coast Central America" and "West Coast South America".
        port_id: The port identifier.
        port_name: The port name.
        latitude: The geo asset position's latitude.
        longitide: The geo asset position's longitude.
        vessel_class_associations: A list of Vessel Class IDs. Vessel Class
            Associations indicate which Vessel Classes have been observed
            operating at a specific GeoAsset, including all of its berths.
            Available Vessel Classes for Tanker: 84-> VLCC, 85-> Suezmax, 86
            -> Aframax, 87-> Panamax, 88-> MR2, 89-> MR1, 90-> Small, for Dry:
            69-> VLOC, 70-> Capesize, 72-> Post Panamax, 74-> Panamax, 75->
            Supramax, 76-> Handymax, 77-> Handysize, 92-> Small, for Container:
            78-> ULCV, 79-> New Panamax, 80-> Post Panamax, 81-> Panamax, 82->
            Feedermax, 83-> Feeder, 95-> Small, for LNG: 91-> LNG, for LPG: 60
            -> VLGC, 61-> Midsize/LGC, 62-> Handy, 63-> Small.
    """
    geo_asset_id: int
    location_taxonomy_id: int
    location_taxonomy_name: str
    geo_asset_name: Optional[str] = None
    geo_asset_type_id: Optional[int] = None
    geo_asset_type_name: Optional[str] = None
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
    vessel_class_associations: Optional[Tuple[int, ...]] = None


@dataclass(frozen=True)
class Port:
    """Contains all details of a port.

    Attributes:
        port_id: Numeric ID of the port.
        location_taxonomy_id: GeoAsset (1), Port (2), Country (3),
            Level0 (4), Level1 (5), Level2 (6),
            Level3 (7), Invalid (-3), NotSet (-2), Unknown (-1).
        location_taxonomy_name: The name of the Location Taxonomy.
        port_name: Name of the port.
        unlocode: The Unlocode of the port.
        country_id: The country identifier.
        country_name: The parent area identifier.
        area_id_level0: Numeric ID corresponding to the level 0 area the port
            belongs to. Level 0 areas offer a detailed breakdown of the
            globe to the areas of maritime interest. Examples of level 0 areas
            include "Arabian Gulf", "US Gulf" and "East Mediterranean".
        area_name_level0: Name of the area the port belongs to. Level 0
            areas offer a detailed breakdown of the globe to the areas of
            maritime interest. Examples of level 0 areas include "Arabian
            Gulf", "US Gulf" and "East Mediterranean".
        area_id_level1: Numeric ID corresponding to the level 1 area the port
            belongs to. Level 1 areas consist of one or multiple level
            0 areas. For example, level 1 area "Mediterranean" groups
            together the level 0 areas "West Mediterranean", "Central
            Mediterranean" and "East Mediterranean".
        area_name_level1: Name of the area the port belongs to. Level 1
            areas consist of one or multiple level 0 areas. For example, level
            1 area "Mediterranean" groups together the level 0 areas "West
            Mediterranean", "Central Mediterranean" and "East Mediterranean".
        area_id_level2: Numeric ID corresponding to the level 2 area the port
            belongs to. Level 2 areas consist of one or multiple level 1
            areas. For example, level 2 area "Mediterranean/UK Continent"
            groups together the "Mediterranean" and "UK Continent" level 1
            areas.
        area_name_level2: Name of the area the port belongs to. Level 2
            areas consist of one or multiple level 1 areas. For example, level
            2 area "Mediterranean/UK Continent" groups together the
            "Mediterranean" and "UK Continent" level 1 areas.
        area_id_level3: Numeric ID corresponding to the level 3 area the port
            belongs to. Level 3 areas the highest area grouping in our
            taxonomy. Examples of such areas are "Pacific America" or "Africa".
            These group together level 2 areas. For instance, "Pacific America"
            groups together the level 2 areas "West Coast North America",
            "West Coast Mexico", "West Coast Central America" and "West Coast
            South America".
        area_name_level3: Name of the area the port belongs to. Level 3
            areas the highest area grouping in our taxonomy. Examples of such
            areas are "Pacific America" or "Africa". These group together level
            2 areas. For instance, "Pacific America" groups together the level
            2 areas "West Coast North America", "West Coast Mexico", "West
            Coast Central America" and "West Coast South America".
        latitude: The port position's latitude.
        longitide: The port position's longitude.
        vessel_class_associations: A list of Vessel Class IDs. Vessel Class
            Associations indicate which Vessel Classes have been observed
            operating at a specific GeoAsset, including all of its berths.
            Available Vessel Classes for Tanker: 84-> VLCC, 85-> Suezmax, 86
            -> Aframax, 87-> Panamax, 88-> MR2, 89-> MR1, 90-> Small, for Dry:
            69-> VLOC, 70-> Capesize, 72-> Post Panamax, 74-> Panamax, 75->
            Supramax, 76-> Handymax, 77-> Handysize, 92-> Small, for Container:
            78-> ULCV, 79-> New Panamax, 80-> Post Panamax, 81-> Panamax, 82->
            Feedermax, 83-> Feeder, 95-> Small, for LNG: 91-> LNG, for LPG: 60
            -> VLGC, 61-> Midsize/LGC, 62-> Handy, 63-> Small.
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
    vessel_class_associations: Optional[Tuple[int, ...]] = None


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
