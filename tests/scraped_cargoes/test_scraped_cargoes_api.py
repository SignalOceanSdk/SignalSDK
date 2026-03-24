from signal_ocean.util.pydantic_base import _to_pascal_case

from signal_ocean.scraped_cargoes import ScrapedCargo


def test_cargoes_field_names():
    api_fields = [
        "CargoID",
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
        "ScrapedLaycan",
        "LaycanFrom",
        "LaycanTo",
        "ScrapedLoad",
        "LoadGeoID",
        "LoadName",
        "LoadTaxonomyID",
        "LoadTaxonomy",
        "ScrapedLoad2",
        "LoadGeoID2",
        "LoadName2",
        "LoadTaxonomyID2",
        "LoadTaxonomy2",
        "ScrapedDischarge",
        "ScrapedDischargeOptions",
        "DischargeGeoID",
        "DischargeName",
        "DischargeTaxonomyID",
        "DischargeTaxonomy",
        "ScrapedDischarge2",
        "DischargeGeoID2",
        "DischargeName2",
        "DischargeTaxonomyID2",
        "DischargeTaxonomy2",
        "ScrapedCharterer",
        "ChartererID",
        "Charterer",
        "ScrapedCargoType",
        "CargoTypeID",
        "CargoType",
        "CargoTypeGroupID",
        "CargoTypeGroup",
        "ScrapedQuantity",
        "Quantity",
        "QuantityBuffer",
        "QuantityFrom",
        "QuantityTo",
        "SizeFrom",
        "SizeTo",
        "ScrapedDeliveryDate",
        "DeliveryDateFrom",
        "DeliveryDateTo",
        "ScrapedDeliveryFrom",
        "DeliveryFromGeoID",
        "DeliveryFromName",
        "DeliveryFromTaxonomyID",
        "DeliveryFromTaxonomy",
        "ScrapedDeliveryTo",
        "DeliveryToGeoID",
        "DeliveryToName",
        "DeliveryToTaxonomyID",
        "DeliveryToTaxonomy",
        "ScrapedRedeliveryFrom",
        "RedeliveryFromGeoID",
        "RedeliveryFromName",
        "RedeliveryFromTaxonomyID",
        "RedeliveryFromTaxonomy",
        "ScrapedRedeliveryTo",
        "RedeliveryToGeoID",
        "RedeliveryToName",
        "RedeliveryToTaxonomyID",
        "RedeliveryToTaxonomy",
        "CharterTypeID",
        "CharterType",
        "CargoStatusID",
        "CargoStatus",
        "Content",
        "Subject",
        "Sender",
        "IsPrivate",
    ]
    alias_to_field = {}
    for name, info in ScrapedCargo.model_fields.items():
        if info.validation_alias is not None:
            alias_to_field[str(info.validation_alias)] = name
        else:
            alias_to_field[_to_pascal_case(name)] = name

    for api_field in api_fields:
        assert api_field in alias_to_field, (
            f"API field {api_field!r} not in model"
        )

    assert sorted(alias_to_field[f] for f in api_fields) == sorted(
        ScrapedCargo.model_fields
    )
