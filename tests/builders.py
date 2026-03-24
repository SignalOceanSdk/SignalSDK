from signal_ocean import Port, VesselClass


def create_port(port_id=1, name='port name') -> Port:
    return Port(id=port_id, name=name)


def create_vessel_class(vessel_id=1, name='vessel class name') -> VesselClass:
    return VesselClass(id=vessel_id, name=name)
