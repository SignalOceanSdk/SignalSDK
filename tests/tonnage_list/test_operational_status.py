from signal_ocean.tonnage_list import OperationalStatus


def test_can_list_available_statuses() -> None:
    statuses = list(OperationalStatus)

    assert statuses == [
        "Ballast Fixed",
        "Repairs",
        "Waiting to Load",
        "Loading",
        "Laden",
        "Waiting to Discharge",
        "Discharging",
        "Active Storage",
        "Ballast Unfixed",
        "Ballast Fixed (implied)",
    ]
