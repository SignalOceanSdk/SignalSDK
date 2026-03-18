from signal_ocean.scraped_lineups import ScrapedLineup
from signal_ocean.util.pydantic_base import _to_pascal_case


def test_lineups_field_names():
    api_fields = [
        "LineupID",
        "MessageID",
        "ExternalMessageID",
        "ParsedPartID",
        "LineFrom",
        "LineTo",
        "InLineOrder",
        "Source",
        "UpdatedDate",
        "ReceivedDate",
        "IsDeleted",
        "LowConfidence",
        "ScrapedVesselName",
        "ScrapedIMO",
        "ScrapedDeadweight",
        "ScrapedYearBuilt",
        "IMO",
        "VesselName",
        "Deadweight",
        "YearBuilt",
        "LiquidCapacity",
        "VesselTypeID",
        "VesselType",
        "VesselClassID",
        "VesselClass",
        "CommercialOperatorID",
        "CommercialOperator",
        "ScrapedEta",
        "Eta",
        "ScrapedEtb",
        "Etb",
        "ScrapedEtd",
        "Etd",
        "ScrapedLocation",
        "LocationGeoID",
        "LocationName",
        "LocationTaxonomyID",
        "LocationTaxonomy",
        "OperationTypeID",
        "OperationType",
        "ScrapedQuantity",
        "Quantity",
        "QuantityUnit",
        "ScrapedCargoType",
        "CargoTypeID",
        "CargoType",
        "CargoGroupID",
        "CargoGroup",
        "ScrapedApiGravity",
        "ApiGravity",
        "ScrapedOrigin",
        "OriginGeoID",
        "OriginName",
        "OriginTaxonomyID",
        "OriginTaxonomy",
        "ScrapedDestination",
        "DestinationGeoID",
        "DestinationName",
        "DestinationTaxonomyID",
        "DestinationTaxonomy",
        "ScrapedSupplier",
        "SupplierID",
        "Supplier",
        "ScrapedCharterer",
        "ChartererID",
        "Charterer",
        "ScrapedBuyer",
        "BuyerID",
        "Buyer",
        "ScrapedPortAgent",
        "PortAgentID",
        "PortAgent",
        "VesselStatusID",
        "VesselStatus",
        "Content",
        "Subject",
        "Sender",
        "IsPrivate",
    ]
    alias_to_field = {}
    for name, info in ScrapedLineup.model_fields.items():
        if info.validation_alias is not None:
            alias_to_field[str(info.validation_alias)] = name
        else:
            alias_to_field[_to_pascal_case(name)] = name

    for api_field in api_fields:
        assert api_field in alias_to_field, (
            f"API field {api_field!r} not in model"
        )

    assert sorted(alias_to_field[f] for f in api_fields) == sorted(
        ScrapedLineup.model_fields
    )
