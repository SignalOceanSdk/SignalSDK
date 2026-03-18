from signal_ocean.util.pydantic_base import _to_pascal_case

from signal_ocean.scraped_positions import ScrapedPosition


def test_positions_field_names():
    api_fields = [
        "PositionID",
        "MessageID",
        "ExternalMessageID",
        "ParsedPartID",
        "LineFrom",
        "LineTo",
        "Source",
        "UpdatedDate",
        "ReceivedDate",
        "IsDeleted",
        "LowConfidence",
        "ScrapedVesselName",
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
        "ScrapedOpenDate",
        "OpenDateFrom",
        "OpenDateTo",
        "ScrapedOpenPort",
        "OpenGeoID",
        "OpenName",
        "OpenTaxonomyID",
        "OpenTaxonomy",
        "ScrapedCommercialOperator",
        "CommercialOperatorID",
        "CommercialOperator",
        "ScrapedCargoType",
        "CargoTypeID",
        "CargoType",
        "CargoTypeGroupID",
        "CargoTypeGroup",
        "ScrapedLastCargoTypes",
        "LastCargoTypesIds",
        "LastCargoTypes",
        "HasBallast",
        "HasDryDock",
        "HasIf",
        "HasOnHold",
        "HasOnSubs",
        "HasPrompt",
        "HasUncertain",
        "IsPositionList",
        "Content",
        "Subject",
        "Sender",
        "IsPrivate",
    ]
    alias_to_field = {}
    for name, info in ScrapedPosition.model_fields.items():
        if info.validation_alias is not None:
            alias_to_field[str(info.validation_alias)] = name
        else:
            alias_to_field[_to_pascal_case(name)] = name

    for api_field in api_fields:
        assert api_field in alias_to_field, (
            f"API field {api_field!r} not in model"
        )

    assert sorted(alias_to_field[f] for f in api_fields) == sorted(
        ScrapedPosition.model_fields
    )
