from signal_ocean.vessel_consumptions.models import (
    Consumption,
    VesselConsumptions,
    AdvertisedConsumptionAtSea,
    AdvertisedConsumptionInPort,
    AdvertisedConsumptions,
    AdvertisedConsumptionsPage,
)

# --- GET vessels/{imo}/consumptions ---

__mock_consumptions_response = {
    "IMO": 9412036,
    "IdleConsumption": 3.5,
    "LoadPortConsumption": 5.0,
    "DischargePortConsumption": 4.5,
    "AuxiliaryIdleConsumption": 1.2,
    "AuxiliaryBallastConsumption": 1.5,
    "AuxiliaryLadenConsumption": 1.8,
    "LadenConsumptions": [
        {
            "Speed": 12.5,
            "SpeedProfileId": 1,
            "SpeedProfile": "Eco",
            "Consumption": 30.0
        },
        {
            "Speed": 14.0,
            "SpeedProfileId": 2,
            "SpeedProfile": "Full",
            "Consumption": 45.0
        }
    ],
    "BallastConsumptions": [
        {
            "Speed": 12.0,
            "SpeedProfileId": 1,
            "SpeedProfile": "Eco",
            "Consumption": 25.0
        }
    ]
}

__mock_consumptions = VesselConsumptions(
    imo=9412036,
    idle_consumption=3.5,
    load_port_consumption=5.0,
    discharge_port_consumption=4.5,
    auxiliary_idle_consumption=1.2,
    auxiliary_ballast_consumption=1.5,
    auxiliary_laden_consumption=1.8,
    laden_consumptions=[
        Consumption(speed=12.5, speed_profile_id=1,
                    speed_profile="Eco", consumption=30.0),
        Consumption(speed=14.0, speed_profile_id=2,
                    speed_profile="Full", consumption=45.0),
    ],
    ballast_consumptions=[
        Consumption(speed=12.0, speed_profile_id=1,
                    speed_profile="Eco", consumption=25.0),
    ]
)

__mock_consumptions_minimal_response = {
    "IMO": 9412036,
    "IdleConsumption": 2.0,
}

__mock_consumptions_minimal = VesselConsumptions(
    imo=9412036,
    idle_consumption=2.0,
)

# --- GET vessels/{imo}/advertisedConsumptions ---

__mock_advertised_consumptions_response = {
    "IMO": 9412036,
    "UpdatedDate": "2024-06-15T10:30:00",
    "BallastConsumptions": [
        {
            "MainFuelTypeId": 1,
            "MainFuelType": "VLSFO",
            "MainFuelConsumption": 28.5,
            "AuxFuelTypeId": 2,
            "AuxFuelType": "MGO",
            "AuxFuelConsumption": 1.5,
            "Speed": 13.0,
            "SpeedProfileId": 1,
            "SpeedProfile": "Eco"
        }
    ],
    "LadenConsumptions": [
        {
            "MainFuelTypeId": 1,
            "MainFuelType": "VLSFO",
            "MainFuelConsumption": 35.0,
            "AuxFuelTypeId": 2,
            "AuxFuelType": "MGO",
            "AuxFuelConsumption": 2.0,
            "Speed": 14.5,
            "SpeedProfileId": 2,
            "SpeedProfile": "Full"
        }
    ],
    "IdleConsumptions": [
        {
            "MainFuelTypeId": 1,
            "MainFuelType": "VLSFO",
            "MainFuelConsumption": 3.0,
            "AuxFuelTypeId": 2,
            "AuxFuelType": "MGO",
            "AuxFuelConsumption": 1.0,
            "OperationalContextId": 1,
            "OperationalContext": "Idle"
        }
    ],
    "WorkingConsumptions": [
        {
            "MainFuelTypeId": 1,
            "MainFuelType": "VLSFO",
            "MainFuelConsumption": 5.0,
            "AuxFuelTypeId": 2,
            "AuxFuelType": "MGO",
            "AuxFuelConsumption": 2.5,
            "OperationalContextId": 2,
            "OperationalContext": "Loading"
        }
    ]
}

__mock_advertised_consumptions = AdvertisedConsumptions(
    imo=9412036,
    updated_date="2024-06-15T10:30:00",
    ballast_consumptions=[
        AdvertisedConsumptionAtSea(
            main_fuel_type_id=1, main_fuel_type="VLSFO",
            main_fuel_consumption=28.5,
            aux_fuel_type_id=2, aux_fuel_type="MGO",
            aux_fuel_consumption=1.5,
            speed=13.0, speed_profile_id=1, speed_profile="Eco"
        )
    ],
    laden_consumptions=[
        AdvertisedConsumptionAtSea(
            main_fuel_type_id=1, main_fuel_type="VLSFO",
            main_fuel_consumption=35.0,
            aux_fuel_type_id=2, aux_fuel_type="MGO",
            aux_fuel_consumption=2.0,
            speed=14.5, speed_profile_id=2, speed_profile="Full"
        )
    ],
    idle_consumptions=[
        AdvertisedConsumptionInPort(
            main_fuel_type_id=1, main_fuel_type="VLSFO",
            main_fuel_consumption=3.0,
            aux_fuel_type_id=2, aux_fuel_type="MGO",
            aux_fuel_consumption=1.0,
            operational_context_id=1, operational_context="Idle"
        )
    ],
    working_consumptions=[
        AdvertisedConsumptionInPort(
            main_fuel_type_id=1, main_fuel_type="VLSFO",
            main_fuel_consumption=5.0,
            aux_fuel_type_id=2, aux_fuel_type="MGO",
            aux_fuel_consumption=2.5,
            operational_context_id=2, operational_context="Loading"
        )
    ]
)

__mock_advertised_consumptions_minimal_response = {
    "IMO": 9876543,
    "UpdatedDate": "2024-01-01T00:00:00",
}

__mock_advertised_consumptions_minimal = AdvertisedConsumptions(
    imo=9876543,
    updated_date="2024-01-01T00:00:00",
)

# --- GET vessels/advertisedConsumptions (paginated) ---

__mock_advertised_consumptions_page_response = {
    "NextPageToken": "abc123",
    "Data": [
        {
            "IMO": 9412036,
            "UpdatedDate": "2024-06-15T10:30:00",
            "BallastConsumptions": [
                {
                    "MainFuelTypeId": 1,
                    "MainFuelType": "VLSFO",
                    "MainFuelConsumption": 28.5,
                    "Speed": 13.0,
                }
            ],
        },
        {
            "IMO": 9876543,
            "UpdatedDate": "2024-01-01T00:00:00",
        }
    ]
}

__mock_advertised_consumptions_page = AdvertisedConsumptionsPage(
    next_page_token="abc123",
    data=[
        AdvertisedConsumptions(
            imo=9412036,
            updated_date="2024-06-15T10:30:00",
            ballast_consumptions=[
                AdvertisedConsumptionAtSea(
                    main_fuel_type_id=1, main_fuel_type="VLSFO",
                    main_fuel_consumption=28.5,
                    speed=13.0,
                )
            ],
        ),
        AdvertisedConsumptions(
            imo=9876543,
            updated_date="2024-01-01T00:00:00",
        )
    ]
)

__mock_advertised_consumptions_page_empty_response = {
    "NextPageToken": None,
    "Data": []
}

__mock_advertised_consumptions_page_empty = AdvertisedConsumptionsPage(
    next_page_token=None,
    data=[]
)
