from signal_ocean.historical_tonnage_list import VesselSubclass


def test_can_list_available_vessel_subclasses():
    subclasses = list(VesselSubclass)

    assert subclasses == [None, 'Dirty', 'Clean']
