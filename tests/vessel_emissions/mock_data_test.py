from signal_ocean.vessel_emissions.models import EmissionsEstimation, EmissionsBreakdown, Emissions

__mock_emissions_estimation = {
    "ID": "I9783B354VED9AA1300",
    "IMO": 9929651,
    "VesselName": "C. Earnest",
    "VoyageNumber": 1,
    "VesselTypeID": 1,
    "VesselType": "Tanker",
    "VesselClassID": 84,
    "VesselClass": "VLCC",
    "StartDate": "2022-03-25T07:50:07",
    "EndDate": "2022-07-01T03:56:40",
    "Quantity": 255000.0,
    "Deadweight": 300000,
    "ContainsEuEmissions": False,
    "TransportWorkInMillionTonneMiles": 3363.3888,
    "TransportWorkInMillionDwtMiles": 3956.928,
    "Emissions": {
        "Voyage": {
            "CO2InTons": 8267.12013499702,
            "COInTons": 7.323807207272146,
            "CH4InTons": 0.15863842326221247,
            "N2OInTons": 0.420546309157253,
            "NMVOCInTons": 8.143439060793579,
            "NOxInTons": 206.27363014828046,
            "SOxInTons": 3.65880649262461,
            "PMInTons": 7.577564487857228
        },
        "Ballast": {
            "CO2InTons": 2702.096551708236,
            "COInTons": 2.4029646462846994,
            "CH4InTons": 0.05204977573179855,
            "N2OInTons": 0.13879940195146281,
            "NMVOCInTons": 2.6718884875656586,
            "NOxInTons": 68.06375673194857,
            "SOxInTons": 1.276890316773894,
            "PMInTons": 2.717479274728012
        },
        "Laden": {
            "CO2InTons": 3596.957553346655,
            "COInTons": 3.194539447561519,
            "CH4InTons": 0.06919580030819175,
            "N2OInTons": 0.18395071362940119,
            "NMVOCInTons": 3.552051082487176,
            "NOxInTons": 90.21590246870453,
            "SOxInTons": 1.6105886451366533,
            "PMInTons": 3.459371259486874
        },
        "PortCall": {
            "CO2InTons": 636.62,
            "COInTons": 0.5539999999999999,
            "CH4InTons": 0.012,
            "N2OInTons": 0.0305,
            "NMVOCInTons": 0.616,
            "NOxInTons": 14.9855,
            "SOxInTons": 0.08211252000000008,
            "PMInTons": 0.22008146580000001
        },
        "Stop": {
            "CO2InTons": 1331.4460299421296,
            "COInTons": 1.172303113425926,
            "CH4InTons": 0.025392847222222226,
            "N2OInTons": 0.06729619357638887,
            "NMVOCInTons": 1.3034994907407407,
            "NOxInTons": 33.00847094762731,
            "SOxInTons": 0.6892150107140629,
            "PMInTons": 1.1806324878423418
        }
    }
}


__mock_emissions_response_2 = [__mock_emissions_estimation] * 3

__mock_emissions_model = EmissionsEstimation(
        id='I9783B354VED9AA1300',
        imo=9929651,
        vessel_name='C. Earnest',
        voyage_number=1,
        vessel_type_id=1,
        vessel_type='Tanker',
        vessel_class_id=84,
        vessel_class='VLCC',
        start_date='2022-03-25T07:50:07',
        end_date='2022-07-01T03:56:40',
        quantity=255000.0,
        deadweight=300000,
        contains_eu_emissions=False,
        transport_work_in_million_tonne_miles=3363.3888,
        transport_work_in_million_dwt_miles=3956.928,
        emissions=(EmissionsBreakdown(
            voyage=Emissions(
                co2_in_tons=8267.12013499702,
                coin_tons=7.323807207272146,
                ch4_in_tons=0.15863842326221247,
                n2_oin_tons=0.420546309157253,
                nmvocin_tons=8.143439060793579,
                nox_in_tons=206.27363014828046,
                sox_in_tons=3.65880649262461,
                pmin_tons=7.577564487857228,
            ),
            ballast=Emissions(
                co2_in_tons=2702.096551708236,
                coin_tons=2.4029646462846994,
                ch4_in_tons=0.05204977573179855,
                n2_oin_tons=0.13879940195146281,
                nmvocin_tons=2.6718884875656586,
                nox_in_tons=68.06375673194857,
                sox_in_tons=1.276890316773894,
                pmin_tons=2.717479274728012,
            ),
            laden=Emissions(
                co2_in_tons=3596.957553346655,
                coin_tons=3.194539447561519,
                ch4_in_tons=0.06919580030819175,
                n2_oin_tons=0.18395071362940119,
                nmvocin_tons=3.552051082487176,
                nox_in_tons=90.21590246870453,
                sox_in_tons=1.6105886451366533,
                pmin_tons=3.459371259486874,
            ),
            port_call=Emissions(
                co2_in_tons=636.62,
                coin_tons=0.5539999999999999,
                ch4_in_tons=0.012,
                n2_oin_tons=0.0305,
                nmvocin_tons=0.616,
                nox_in_tons=14.9855,
                sox_in_tons=0.08211252000000008,
                pmin_tons=0.22008146580000001,
            ),
            stop=Emissions(
                co2_in_tons=1331.4460299421296,
                coin_tons=1.172303113425926,
                ch4_in_tons=0.025392847222222226,
                n2_oin_tons=0.06729619357638887,
                nmvocin_tons=1.3034994907407407,
                nox_in_tons=33.00847094762731,
                sox_in_tons=0.6892150107140629,
                pmin_tons=1.1806324878423418,
            )
        )
    )
)

__mock_emissions_2 = [__mock_emissions_model] * 3
