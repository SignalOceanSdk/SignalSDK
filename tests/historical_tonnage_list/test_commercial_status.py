from signal_ocean.historical_tonnage_list import CommercialStatus


def test_can_list_available_statuses():
    statuses = list(CommercialStatus)

    assert statuses == ['On Subs', 'Failed', 'Cancelled', 'Available', 'Poss Fixed']
