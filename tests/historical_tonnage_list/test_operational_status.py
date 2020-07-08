from signal_ocean.historical_tonnage_list import OperationalStatus


def test_can_list_available_statuses():
    statuses = list(OperationalStatus)

    assert statuses == [
        'Ballast Fixed',
        'Repairs',
        'Waiting to Load',
        'Loading',
        'Laden',
        'Waiting to Discharge',
        'Discharging',
        'Active Storage',
        'Ballast Unfixed'
    ]
