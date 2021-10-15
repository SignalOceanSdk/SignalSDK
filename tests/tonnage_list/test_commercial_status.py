from signal_ocean.tonnage_list import CommercialStatus


def test_can_list_available_statuses() -> None:
    statuses = list(CommercialStatus)

    assert statuses == [
        "On Subs",
        "Failed",
        "Cancelled",
        "Available",
        "Poss Fixed",
    ]
