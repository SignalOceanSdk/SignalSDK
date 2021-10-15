from signal_ocean.tonnage_list import VesselSubclass


def test_can_list_available_vessel_subclasses() -> None:
    subclasses = list(VesselSubclass)

    assert subclasses == [None, "Dirty", "Clean"]
