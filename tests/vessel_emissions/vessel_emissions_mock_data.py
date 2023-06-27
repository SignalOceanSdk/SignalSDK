from signal_ocean.vessel_emissions.models import EmissionsEstimationModel, EmissionsBreakdown, Emissions, Metrics, \
    VesselMetrics, Eexi, Eiv, Aer, Cii, Consumptions, ConsumptionsBreakdown

__mock_emissions_response_1 = {
    "ID": "I8F9DC4VED7805D00",
    "IMO": 9412036,
    "VesselName": "Sea Hymn",
    "VoyageNumber": 143,
    "VesselTypeID": 1,
    "VesselType": "Tanker",
    "VesselClassID": 86,
    "VesselClass": "Aframax",
    "StartDate": "2021-01-24T11:59:59",
    "EndDate": "2021-02-05T14:31:12.812000",
    "Quantity": 71000,
    "Deadweight": 116337,
    "ContainsEuEmissions": True,
    "TransportWorkInMillionTonneMiles": 102.85628000000001,
    "TransportWorkInMillionDwtMiles": 168.53508516000002,
    "Emissions": {
        "Voyage": {
            "CO2InTons": 837.5087196481956,
            "COInTons": 0.7359510048818543,
            "CH4InTons": 0.015941177001051,
            "N2OInTons": 0.04245146957224711,
            "NMVOCInTons": 0.8183137527206179,
            "NOxInTons": 23.13202057801321,
            "SOxInTons": 51.94326251279127,
            "PMInTons": 5.1238549844792445
        },
        "Ballast": {
            "CO2InTons": 409.19323058978165,
            "COInTons": 0.3597114758091598,
            "CH4InTons": 0.00779158431355581,
            "N2OInTons": 0.02077755816948216,
            "NMVOCInTons": 0.3999679947625315,
            "NOxInTons": 11.32117200759659,
            "SOxInTons": 25.38835804676737,
            "PMInTons": 2.5091619607601823
        },
        "Laden": {
            "CO2InTons": 74.9966521789844,
            "COInTons": 0.06592767039954643,
            "CH4InTons": 0.001428036181939634,
            "N2OInTons": 0.003808096485172358,
            "NMVOCInTons": 0.07330585733956788,
            "NOxInTons": 2.074936572358288,
            "SOxInTons": 4.653160696438169,
            "PMInTons": 0.45987746806232016
        },
        "PortCall": {
            "CO2InTons": 252.0832,
            "COInTons": 0.2216,
            "CH4InTons": 0.0048000000000000004,
            "N2OInTons": 0.012800000000000002,
            "NMVOCInTons": 0.24639999999999998,
            "NOxInTons": 6.974399999999999,
            "SOxInTons": 15.64048,
            "PMInTons": 1.545767449464
        },
        "Stop": {
            "CO2InTons": 101.23563687942965,
            "COInTons": 0.08871185867314817,
            "CH4InTons": 0.0019215565055555556,
            "N2OInTons": 0.005065814917592594,
            "NMVOCInTons": 0.09863990061851852,
            "NOxInTons": 2.7615119980583334,
            "SOxInTons": 6.261263769585741,
            "PMInTons": 0.6090481061927422
        }
    },
    "EfficiencyMetrics": {
        "VoyageCii": 4.969343438804451,
        "VoyageCiiUnit": "g-CO2/capacity mile",
        "VoyageCiiRating": "D",
        "VoyageCiiTarget": 4.178777475053739,
        "VoyageCiiTargetYear": 2021,
        "CapacityEeoi": 39.74048276526212,
        "CapacityEeoiUnit": "g-CO2/capacity mile",
        "CapacityEeoiSeaCargoCharterYearTarget": 11.02,
        "CapacityEeoiSeaCargoCharterClass": "Oil Tanker 80000-119999 DWT",
        "CapacityEeoiSeaCargoCharterAlignmentInPercentage": 260.6214407011082,
        "Eeoi": 57.79110679327875,
        "EeoiUnit": "g-CO2/ton mile",
        "EeoiSeaCargoCharterYearTarget": 11.02,
        "EeoiSeaCargoCharterClass": "Oil Tanker 80000-119999 DWT",
        "EeoiSeaCargoCharterAlignmentInPercentage": 424.42020683556035,
        "kgCO2PerTonneCargo": 10.468858995602444,
        "kgCO2PerTonneDwt": 7.198988452927233
    }
}

__mock_emissions_1 = EmissionsEstimationModel(
    id="I8F9DC4VED7805D00",
    imo=9412036,
    vessel_name="Sea Hymn",
    voyage_number=143,
    vessel_type_id=1,
    vessel_type="Tanker",
    vessel_class_id=86,
    vessel_class="Aframax",
    start_date="2021-01-24T11:59:59",
    end_date="2021-02-05T14:31:12.812000",
    quantity=71000,
    deadweight=116337,
    contains_eu_emissions=True,
    transport_work_in_million_tonne_miles=102.85628000000001,
    transport_work_in_million_dwt_miles=168.53508516000002,
    emissions=EmissionsBreakdown(
        voyage=Emissions(
            co2_in_tons=837.5087196481956,
            coin_tons=0.7359510048818543,
            ch4_in_tons=0.015941177001051,
            n2_oin_tons=0.04245146957224711,
            nmvocin_tons=0.8183137527206179,
            nox_in_tons=23.13202057801321,
            sox_in_tons=51.94326251279127,
            pmin_tons=5.1238549844792445
        ),
        ballast=Emissions(
            co2_in_tons=409.19323058978165,
            coin_tons=0.3597114758091598,
            ch4_in_tons=0.00779158431355581,
            n2_oin_tons=0.02077755816948216,
            nmvocin_tons=0.3999679947625315,
            nox_in_tons=11.32117200759659,
            sox_in_tons=25.38835804676737,
            pmin_tons=2.5091619607601823
        ),

        laden=Emissions(
            co2_in_tons=74.9966521789844,
            coin_tons=0.06592767039954643,
            ch4_in_tons=0.001428036181939634,
            n2_oin_tons=0.003808096485172358,
            nmvocin_tons=0.07330585733956788,
            nox_in_tons=2.074936572358288,
            sox_in_tons=4.653160696438169,
            pmin_tons=0.45987746806232016
        ),
        port_call=Emissions(
            co2_in_tons=252.0832,
            coin_tons=0.2216,
            ch4_in_tons=0.0048000000000000004,
            n2_oin_tons=0.012800000000000002,
            nmvocin_tons=0.24639999999999998,
            nox_in_tons=6.974399999999999,
            sox_in_tons=15.64048,
            pmin_tons=1.545767449464
        ),
        stop=Emissions(
            co2_in_tons=101.23563687942965,
            coin_tons=0.08871185867314817,
            ch4_in_tons=0.0019215565055555556,
            n2_oin_tons=0.005065814917592594,
            nmvocin_tons=0.09863990061851852,
            nox_in_tons=2.7615119980583334,
            sox_in_tons=6.261263769585741,
            pmin_tons=0.6090481061927422
        )
    ),

    efficiency_metrics=Metrics(
        voyage_cii=4.969343438804451,
        voyage_cii_unit="g-CO2/capacity mile",
        voyage_cii_rating="D",
        voyage_cii_target=4.178777475053739,
        voyage_cii_target_year=2021,
        capacity_eeoi=39.74048276526212,
        capacity_eeoi_unit="g-CO2/capacity mile",
        capacity_eeoi_sea_cargo_charter_year_target=11.02,
        capacity_eeoi_sea_cargo_charter_class="Oil Tanker 80000-119999 DWT",
        capacity_eeoi_sea_cargo_charter_alignment_in_percentage=260.6214407011082,
        eeoi=57.79110679327875,
        eeoi_unit="g-CO2/ton mile",
        eeoi_sea_cargo_charter_year_target=11.02,
        eeoi_sea_cargo_charter_class="Oil Tanker 80000-119999 DWT",
        eeoi_sea_cargo_charter_alignment_in_percentage=424.42020683556035,
        kg_co2_per_tonne_cargo=10.468858995602444,
        kg_co2_per_tonne_dwt=7.198988452927233
    )
)

__mock_emissions_response_2 = [{
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
}, {
    "ID": "I9783B354VEDA484700",
    "IMO": 9929651,
    "VesselName": "C. Earnest",
    "VoyageNumber": 2,
    "VesselTypeID": 1,
    "VesselType": "Tanker",
    "VesselClassID": 84,
    "VesselClass": "VLCC",
    "StartDate": "2022-07-01T03:56:40",
    "EndDate": "2022-08-19T11:56:58",
    "Quantity": 243000.0,
    "Deadweight": 300000,
    "ContainsEuEmissions": True,
    "TransportWorkInMillionTonneMiles": 2663.0199899999993,
    "TransportWorkInMillionDwtMiles": 3287.6789999999996,
    "Emissions": {
        "Voyage": {
            "CO2InTons": 6790.670700343808,
            "COInTons": 6.00075557855251,
            "CH4InTons": 0.12998026523940456,
            "N2OInTons": 0.3418292808876354,
            "NMVOCInTons": 6.672320282289433,
            "NOxInTons": 167.71723833544547,
            "SOxInTons": 2.5029667643054117,
            "PMInTons": 5.491910237454452
        },
        "Ballast": {
            "CO2InTons": 2294.4994261479897,
            "COInTons": 2.033922574628233,
            "CH4InTons": 0.044056084648987,
            "N2OInTons": 0.11664283501361183,
            "NMVOCInTons": 2.261545678647999,
            "NOxInTons": 57.21500633160883,
            "SOxInTons": 0.958403504297451,
            "PMInTons": 2.0734079148878473
        },
        "Laden": {
            "CO2InTons": 3602.247828362485,
            "COInTons": 3.1873829764358512,
            "CH4InTons": 0.06904078649319534,
            "N2OInTons": 0.18208139089717165,
            "NMVOCInTons": 3.5440937066506937,
            "NOxInTons": 89.32744241471627,
            "SOxInTons": 1.401854206865687,
            "PMInTons": 3.056502367323505
        },
        "PortCall": {
            "CO2InTons": 558.76,
            "COInTons": 0.48474999999999996,
            "CH4InTons": 0.0105,
            "N2OInTons": 0.0265,
            "NMVOCInTons": 0.5389999999999999,
            "NOxInTons": 13.024000000000001,
            "SOxInTons": 0.045455145000000044,
            "PMInTons": 0.14173187967225
        },
        "Stop": {
            "CO2InTons": 335.1634458333333,
            "COInTons": 0.29470002748842594,
            "CH4InTons": 0.006383394097222222,
            "N2OInTons": 0.016605054976851854,
            "NMVOCInTons": 0.3276808969907407,
            "NOxInTons": 8.15078958912037,
            "SOxInTons": 0.09725390814227439,
            "PMInTons": 0.2202680755708518
        }
    }
}, {
    "ID": "I9783B354VEDA6FD400",
    "IMO": 9929651,
    "VesselName": "C. Earnest",
    "VoyageNumber": 3,
    "VesselTypeID": 1,
    "VesselType": "Tanker",
    "VesselClassID": 84,
    "VesselClass": "VLCC",
    "StartDate": "2022-08-19T11:56:58",
    "EndDate": "2022-10-20T19:57:36",
    "Quantity": 244000.0,
    "Deadweight": 300000,
    "ContainsEuEmissions": True,
    "TransportWorkInMillionTonneMiles": 2768.538680000001,
    "TransportWorkInMillionDwtMiles": 3403.941000000001,
    "Emissions": {
        "Voyage": {
            "CO2InTons": 7287.981934988181,
            "COInTons": 6.421559877615056,
            "CH4InTons": 0.13909515980393627,
            "N2OInTons": 0.36349511608940527,
            "NMVOCInTons": 7.140218203268728,
            "NOxInTons": 178.39278293464656,
            "SOxInTons": 2.354023568478281,
            "PMInTons": 5.252041044489147
        },
        "Ballast": {
            "CO2InTons": 2323.1676251257004,
            "COInTons": 2.054127767537052,
            "CH4InTons": 0.044493742257120265,
            "N2OInTons": 0.11716026570245411,
            "NMVOCInTons": 2.2840121025321736,
            "NOxInTons": 57.48132849580709,
            "SOxInTons": 0.8776506677968804,
            "PMInTons": 1.9201180476518667
        },
        "Laden": {
            "CO2InTons": 3369.772682721279,
            "COInTons": 2.9812166283071724,
            "CH4InTons": 0.06457508942181601,
            "N2OInTons": 0.17024663134759932,
            "NMVOCInTons": 3.3148545903198885,
            "NOxInTons": 83.52254298484644,
            "SOxInTons": 1.3031040025952028,
            "PMInTons": 2.8432465188636287
        },
        "PortCall": {
            "CO2InTons": 1041.9499999999998,
            "COInTons": 0.90025,
            "CH4InTons": 0.019500000000000003,
            "N2OInTons": 0.04875,
            "NMVOCInTons": 1.001,
            "NOxInTons": 23.96875,
            "SOxInTons": 0.01906183500000002,
            "PMInTons": 0.13732830267975002
        },
        "Stop": {
            "CO2InTons": 553.0916271412037,
            "COInTons": 0.4859654817708334,
            "CH4InTons": 0.010526328125,
            "N2OInTons": 0.027338219039351856,
            "NMVOCInTons": 0.5403515104166667,
            "NOxInTons": 13.420161453993055,
            "SOxInTons": 0.15420706308619805,
            "PMInTons": 0.3513481752939015
        }
    }
}, {
    "ID": "I9783B354VEDABEEE00",
    "IMO": 9929651,
    "VesselName": "C. Earnest",
    "VoyageNumber": 4,
    "VesselTypeID": 1,
    "VesselType": "Tanker",
    "VesselClassID": 84,
    "VesselClass": "VLCC",
    "StartDate": "2022-10-20T19:57:36",
    "EndDate": "2022-12-19T23:59:01",
    "Quantity": 261000.0,
    "Deadweight": 300000,
    "ContainsEuEmissions": True,
    "TransportWorkInMillionTonneMiles": 2822.670630000001,
    "TransportWorkInMillionDwtMiles": 3244.449000000001,
    "Emissions": {
        "Voyage": {
            "CO2InTons": 6005.753262313764,
            "COInTons": 5.300095555350624,
            "CH4InTons": 0.11480351383430959,
            "N2OInTons": 0.30104602915267803,
            "NMVOCInTons": 5.893247043494555,
            "NOxInTons": 147.72419461235071,
            "SOxInTons": 2.088167065012412,
            "PMInTons": 4.614608484276407
        },
        "Ballast": {
            "CO2InTons": 2033.9102649270355,
            "COInTons": 1.8032782058026067,
            "CH4InTons": 0.03906017774301676,
            "N2OInTons": 0.10345887585042686,
            "NMVOCInTons": 2.0050891241415267,
            "NOxInTons": 50.747239708940256,
            "SOxInTons": 0.8558024049116695,
            "PMInTons": 1.849998746533185
        },
        "Laden": {
            "CO2InTons": 3267.237442930711,
            "COInTons": 2.8855782971753325,
            "CH4InTons": 0.06250350102184836,
            "N2OInTons": 0.16417719815178825,
            "NMVOCInTons": 3.208513052454882,
            "NOxInTons": 80.55680788228776,
            "SOxInTons": 1.175733657296142,
            "PMInTons": 2.5872143845627553
        },
        "PortCall": {
            "CO2InTons": 558.76,
            "COInTons": 0.48474999999999996,
            "CH4InTons": 0.0105,
            "N2OInTons": 0.0265,
            "NMVOCInTons": 0.5389999999999999,
            "NOxInTons": 13.024000000000001,
            "SOxInTons": 0.045455145000000044,
            "PMInTons": 0.14173187967225
        },
        "Stop": {
            "CO2InTons": 145.84555445601853,
            "COInTons": 0.12648905237268518,
            "CH4InTons": 0.0027398350694444445,
            "N2OInTons": 0.006909955150462963,
            "NMVOCInTons": 0.14064486689814817,
            "NOxInTons": 3.3961470211226854,
            "SOxInTons": 0.011175857804600703,
            "PMInTons": 0.03566347350821582
        }
    }
}, {
    "ID": "I9783B354VEDB0E0800",
    "IMO": 9929651,
    "VesselName": "C. Earnest",
    "VoyageNumber": 5,
    "VesselTypeID": 1,
    "VesselType": "Tanker",
    "VesselClassID": 84,
    "VesselClass": "VLCC",
    "StartDate": "2022-12-19T23:59:01",
    "EndDate": "2023-03-14T07:56:46",
    "Quantity": 286000.0,
    "Deadweight": 300000,
    "ContainsEuEmissions": True,
    "TransportWorkInMillionTonneMiles": 5243.838600000005,
    "TransportWorkInMillionDwtMiles": 5500.530000000005,
    "Emissions": {
        "Voyage": {
            "CO2InTons": 10473.148881436808,
            "COInTons": 9.293915505042596,
            "CH4InTons": 0.20131224920669885,
            "N2OInTons": 0.5342452119368128,
            "NMVOCInTons": 10.334028792610539,
            "NOxInTons": 262.0306276979183,
            "SOxInTons": 4.555498066379615,
            "PMInTons": 9.813583360103838
        },
        "Ballast": {
            "CO2InTons": 1762.646008299334,
            "COInTons": 1.5622843800668604,
            "CH4InTons": 0.03384009487509446,
            "N2OInTons": 0.08957218709965897,
            "NMVOCInTons": 1.7371248702548487,
            "NOxInTons": 43.93690502581925,
            "SOxInTons": 0.7329528563691268,
            "PMInTons": 1.5864299040671905
        },
        "Laden": {
            "CO2InTons": 7709.014641945343,
            "COInTons": 6.854468866584533,
            "CH4InTons": 0.1484722498177155,
            "N2OInTons": 0.3956732635524317,
            "NMVOCInTons": 7.621575490642728,
            "NOxInTons": 194.0331733737773,
            "SOxInTons": 3.5928257533510264,
            "PMInTons": 7.686631841123893
        },
        "PortCall": {
            "CO2InTons": 547.31,
            "COInTons": 0.48474999999999996,
            "CH4InTons": 0.0105,
            "N2OInTons": 0.02775,
            "NMVOCInTons": 0.5389999999999999,
            "NOxInTons": 13.61275,
            "SOxInTons": 0.2214105450000002,
            "PMInTons": 0.48066123235725
        },
        "Stop": {
            "CO2InTons": 454.1782311921297,
            "COInTons": 0.3924122583912037,
            "CH4InTons": 0.008499904513888889,
            "N2OInTons": 0.021249761284722224,
            "NMVOCInTons": 0.436328431712963,
            "NOxInTons": 10.44779929832176,
            "SOxInTons": 0.008308911659461815,
            "PMInTons": 0.05986038255550291
        }
    }
}, {
    "ID": "I9783B354VEDB84AF00",
    "IMO": 9929651,
    "VesselName": "C. Earnest",
    "VoyageNumber": 6,
    "VesselTypeID": 1,
    "VesselType": "Tanker",
    "VesselClassID": 84,
    "VesselClass": "VLCC",
    "StartDate": "2023-03-14T07:56:46",
    "EndDate": "2023-04-30T11:55:24",
    "Quantity": 270000.0,
    "Deadweight": 300000,
    "ContainsEuEmissions": False,
    "TransportWorkInMillionTonneMiles": 2030.6241000000011,
    "TransportWorkInMillionDwtMiles": 2256.2490000000016,
    "Emissions": {
        "Voyage": {
            "CO2InTons": 5415.542294919199,
            "COInTons": 4.816674851312029,
            "CH4InTons": 0.10433230724863604,
            "N2OInTons": 0.27821948599636276,
            "NMVOCInTons": 5.355725105429983,
            "NOxInTons": 136.4318804454664,
            "SOxInTons": 2.549699007618982,
            "PMInTons": 5.449595395122589
        },
        "Ballast": {
            "CO2InTons": 454.30299397472027,
            "COInTons": 0.40406476153030285,
            "CH4InTons": 0.008752305303905477,
            "N2OInTons": 0.023339480810414606,
            "NMVOCInTons": 0.4492850056004811,
            "NOxInTons": 11.445097902407063,
            "SOxInTons": 0.2138910250931682,
            "PMInTons": 0.4571596654831368
        },
        "Laden": {
            "CO2InTons": 3270.058371662073,
            "COInTons": 2.908445186714597,
            "CH4InTons": 0.06299881270861944,
            "N2OInTons": 0.16799683388965184,
            "NMVOCInTons": 3.233939052375798,
            "NOxInTons": 82.38144741863803,
            "SOxInTons": 1.5395807346764205,
            "PMInTons": 3.290620601506647
        },
        "PortCall": {
            "CO2InTons": 1090.04,
            "COInTons": 0.9694999999999999,
            "CH4InTons": 0.021,
            "N2OInTons": 0.056,
            "NMVOCInTons": 1.0779999999999998,
            "NOxInTons": 27.461,
            "SOxInTons": 0.5132032500000004,
            "PMInTons": 1.0968942057885
        },
        "Stop": {
            "CO2InTons": 601.1409292824075,
            "COInTons": 0.5346649030671297,
            "CH4InTons": 0.011581189236111112,
            "N2OInTons": 0.0308831712962963,
            "NMVOCInTons": 0.5945010474537037,
            "NOxInTons": 15.144335124421296,
            "SOxInTons": 0.2830239978493926,
            "PMInTons": 0.6049209223443057
        }
    }
}, {
    "ID": "I9783B354VEDBD3C900",
    "IMO": 9929651,
    "VesselName": "C. Earnest",
    "VoyageNumber": 7,
    "VesselTypeID": 1,
    "VesselType": "Tanker",
    "VesselClassID": 84,
    "VesselClass": "VLCC",
    "StartDate": "2023-04-30T11:55:24",
    "EndDate": "2023-06-02T23:57:17",
    "Quantity": 278000.0,
    "Deadweight": 300000,
    "ContainsEuEmissions": False,
    "TransportWorkInMillionTonneMiles": 1929.7647999999995,
    "TransportWorkInMillionDwtMiles": 2082.4799999999996,
    "Emissions": {
        "Voyage": {
            "CO2InTons": 4150.61183795167,
            "COInTons": 3.6916243228635137,
            "CH4InTons": 0.07996298172267538,
            "N2OInTons": 0.2132346179271344,
            "NMVOCInTons": 4.104766395097336,
            "NOxInTons": 104.56492576601852,
            "SOxInTons": 1.9541553380841736,
            "PMInTons": 4.17671101567497
        },
        "Ballast": {
            "CO2InTons": 2825.5394821959203,
            "COInTons": 2.513082573106441,
            "CH4InTons": 0.05443500158353301,
            "N2OInTons": 0.1451600042227547,
            "NMVOCInTons": 2.794330081288028,
            "NOxInTons": 71.18283707073334,
            "SOxInTons": 1.330296177448777,
            "PMInTons": 2.8433065632888184
        },
        "Laden": {
            "CO2InTons": 522.7543433714909,
            "COInTons": 0.4649465486575359,
            "CH4InTons": 0.010071044375253486,
            "N2OInTons": 0.026856118334009294,
            "NMVOCInTons": 0.5169802779296788,
            "NOxInTons": 13.169569028039806,
            "SOxInTons": 0.2461187002035387,
            "PMInTons": 0.5260414391168767
        },
        "PortCall": {
            "CO2InTons": 545.02,
            "COInTons": 0.48474999999999996,
            "CH4InTons": 0.0105,
            "N2OInTons": 0.028,
            "NMVOCInTons": 0.5389999999999999,
            "NOxInTons": 13.7305,
            "SOxInTons": 0.2566016250000002,
            "PMInTons": 0.54844710289425
        },
        "Stop": {
            "CO2InTons": 257.2980123842592,
            "COInTons": 0.22884520109953704,
            "CH4InTons": 0.004956935763888889,
            "N2OInTons": 0.013218495370370372,
            "NMVOCInTons": 0.2544560358796296,
            "NOxInTons": 6.482019667245371,
            "SOxInTons": 0.12113883543185774,
            "PMInTons": 0.2589159103750245
        }
    }
}, {
    "ID": "I9783B354VEDBFB5600",
    "IMO": 9929651,
    "VesselName": "C. Earnest",
    "VoyageNumber": 8,
    "VesselTypeID": 1,
    "VesselType": "Tanker",
    "VesselClassID": 84,
    "VesselClass": "VLCC",
    "StartDate": "2023-06-02T23:57:17",
    "EndDate": "2023-09-07T14:03:35.429000",
    "Quantity": 270000.0,
    "Deadweight": 300000,
    "ContainsEuEmissions": False,
    "TransportWorkInMillionTonneMiles": 5303.950200000001,
    "TransportWorkInMillionDwtMiles": 5893.278000000001,
    "Emissions": {
        "Voyage": {
            "CO2InTons": 6924.895099830229,
            "COInTons": 6.150791988208722,
            "CH4InTons": 0.13323015136914199,
            "N2OInTons": 0.35425834658088906,
            "NMVOCInTons": 6.839147770282622,
            "NOxInTons": 173.73923906033772,
            "SOxInTons": 3.112042578215192,
            "PMInTons": 6.681894033383674
        },
        "Ballast": {
            "CO2InTons": 3897.7783129336012,
            "COInTons": 3.460108597926129,
            "CH4InTons": 0.07494820067710026,
            "N2OInTons": 0.19904668909225465,
            "NMVOCInTons": 3.847340968091147,
            "NOxInTons": 97.62331426410212,
            "SOxInTons": 1.7168546940916345,
            "PMInTons": 3.693743093708341
        },
        "Laden": {
            "CO2InTons": 2462.3235910632948,
            "COInTons": 2.18834677569926,
            "CH4InTons": 0.047401013192041735,
            "N2OInTons": 0.12619582415530103,
            "NMVOCInTons": 2.433252010524809,
            "NOxInTons": 61.887285525402284,
            "SOxInTons": 1.129276813264182,
            "PMInTons": 2.419806306470724
        },
        "PortCall": {
            "CO2InTons": 545.02,
            "COInTons": 0.48474999999999996,
            "CH4InTons": 0.0105,
            "N2OInTons": 0.028,
            "NMVOCInTons": 0.5389999999999999,
            "NOxInTons": 13.7305,
            "SOxInTons": 0.2566016250000002,
            "PMInTons": 0.54844710289425
        },
        "Stop": {
            "CO2InTons": 19.773195833333332,
            "COInTons": 0.017586614583333333,
            "CH4InTons": 0.00038093750000000004,
            "N2OInTons": 0.0010158333333333334,
            "NMVOCInTons": 0.019554791666666668,
            "NOxInTons": 0.49813927083333337,
            "SOxInTons": 0.00930944585937501,
            "PMInTons": 0.019897530310359846
        }
    }
}]

__mock_emissions_2 = [
    EmissionsEstimationModel(
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
    ),
    EmissionsEstimationModel(
        id='I9783B354VEDA484700',
        imo=9929651,
        vessel_name='C. Earnest',
        voyage_number=2,
        vessel_type_id=1,
        vessel_type='Tanker',
        vessel_class_id=84,
        vessel_class='VLCC',
        start_date='2022-07-01T03:56:40',
        end_date='2022-08-19T11:56:58',
        quantity=243000.0,
        deadweight=300000,
        contains_eu_emissions=True,
        transport_work_in_million_tonne_miles=2663.0199899999993,
        transport_work_in_million_dwt_miles=3287.6789999999996,
        emissions=(EmissionsBreakdown(
            voyage=Emissions(
                co2_in_tons=6790.670700343808,
                coin_tons=6.00075557855251,
                ch4_in_tons=0.12998026523940456,
                n2_oin_tons=0.3418292808876354,
                nmvocin_tons=6.672320282289433,
                nox_in_tons=167.71723833544547,
                sox_in_tons=2.5029667643054117,
                pmin_tons=5.491910237454452,
            ),
            ballast=Emissions(
                co2_in_tons=2294.4994261479897,
                coin_tons=2.033922574628233,
                ch4_in_tons=0.044056084648987,
                n2_oin_tons=0.11664283501361183,
                nmvocin_tons=2.261545678647999,
                nox_in_tons=57.21500633160883,
                sox_in_tons=0.958403504297451,
                pmin_tons=2.0734079148878473,
            ),
            laden=Emissions(
                co2_in_tons=3602.247828362485,
                coin_tons=3.1873829764358512,
                ch4_in_tons=0.06904078649319534,
                n2_oin_tons=0.18208139089717165,
                nmvocin_tons=3.5440937066506937,
                nox_in_tons=89.32744241471627,
                sox_in_tons=1.401854206865687,
                pmin_tons=3.056502367323505,
            ),
            port_call=Emissions(
                co2_in_tons=558.76,
                coin_tons=0.48474999999999996,
                ch4_in_tons=0.0105,
                n2_oin_tons=0.0265,
                nmvocin_tons=0.5389999999999999,
                nox_in_tons=13.024000000000001,
                sox_in_tons=0.045455145000000044,
                pmin_tons=0.14173187967225,
            ),
            stop=Emissions(
                co2_in_tons=335.1634458333333,
                coin_tons=0.29470002748842594,
                ch4_in_tons=0.006383394097222222,
                n2_oin_tons=0.016605054976851854,
                nmvocin_tons=0.3276808969907407,
                nox_in_tons=8.15078958912037,
                sox_in_tons=0.09725390814227439,
                pmin_tons=0.2202680755708518,
            )
        )
        )
    )
    ,
    EmissionsEstimationModel(
        id='I9783B354VEDA6FD400',
        imo=9929651,
        vessel_name='C. Earnest',
        voyage_number=3,
        vessel_type_id=1,
        vessel_type='Tanker',
        vessel_class_id=84,
        vessel_class='VLCC',
        start_date='2022-08-19T11:56:58',
        end_date='2022-10-20T19:57:36',
        quantity=244000.0,
        deadweight=300000,
        contains_eu_emissions=True,
        transport_work_in_million_tonne_miles=2768.538680000001,
        transport_work_in_million_dwt_miles=3403.941000000001,
        emissions=(EmissionsBreakdown(
            voyage=Emissions(
                co2_in_tons=7287.981934988181,
                coin_tons=6.421559877615056,
                ch4_in_tons=0.13909515980393627,
                n2_oin_tons=0.36349511608940527,
                nmvocin_tons=7.140218203268728,
                nox_in_tons=178.39278293464656,
                sox_in_tons=2.354023568478281,
                pmin_tons=5.252041044489147,
            ),
            ballast=Emissions(
                co2_in_tons=2323.1676251257004,
                coin_tons=2.054127767537052,
                ch4_in_tons=0.044493742257120265,
                n2_oin_tons=0.11716026570245411,
                nmvocin_tons=2.2840121025321736,
                nox_in_tons=57.48132849580709,
                sox_in_tons=0.8776506677968804,
                pmin_tons=1.9201180476518667,
            ),
            laden=Emissions(
                co2_in_tons=3369.772682721279,
                coin_tons=2.9812166283071724,
                ch4_in_tons=0.06457508942181601,
                n2_oin_tons=0.17024663134759932,
                nmvocin_tons=3.3148545903198885,
                nox_in_tons=83.52254298484644,
                sox_in_tons=1.3031040025952028,
                pmin_tons=2.8432465188636287,
            ),
            port_call=Emissions(
                co2_in_tons=1041.9499999999998,
                coin_tons=0.90025,
                ch4_in_tons=0.019500000000000003,
                n2_oin_tons=0.04875,
                nmvocin_tons=1.001,
                nox_in_tons=23.96875,
                sox_in_tons=0.01906183500000002,
                pmin_tons=0.13732830267975002,
            ),
            stop=Emissions(
                co2_in_tons=553.0916271412037,
                coin_tons=0.4859654817708334,
                ch4_in_tons=0.010526328125,
                n2_oin_tons=0.027338219039351856,
                nmvocin_tons=0.5403515104166667,
                nox_in_tons=13.420161453993055,
                sox_in_tons=0.15420706308619805,
                pmin_tons=0.3513481752939015,
            )
        )
        )
    ),
    EmissionsEstimationModel(
        id='I9783B354VEDABEEE00',
        imo=9929651,
        vessel_name='C. Earnest',
        voyage_number=4,
        vessel_type_id=1,
        vessel_type='Tanker',
        vessel_class_id=84,
        vessel_class='VLCC',
        start_date='2022-10-20T19:57:36',
        end_date='2022-12-19T23:59:01',
        quantity=261000.0,
        deadweight=300000,
        contains_eu_emissions=True,
        transport_work_in_million_tonne_miles=2822.670630000001,
        transport_work_in_million_dwt_miles=3244.449000000001,
        emissions=(EmissionsBreakdown(
            voyage=Emissions(
                co2_in_tons=6005.753262313764,
                coin_tons=5.300095555350624,
                ch4_in_tons=0.11480351383430959,
                n2_oin_tons=0.30104602915267803,
                nmvocin_tons=5.893247043494555,
                nox_in_tons=147.72419461235071,
                sox_in_tons=2.088167065012412,
                pmin_tons=4.614608484276407,
            ),
            ballast=Emissions(
                co2_in_tons=2033.9102649270355,
                coin_tons=1.8032782058026067,
                ch4_in_tons=0.03906017774301676,
                n2_oin_tons=0.10345887585042686,
                nmvocin_tons=2.0050891241415267,
                nox_in_tons=50.747239708940256,
                sox_in_tons=0.8558024049116695,
                pmin_tons=1.849998746533185,
            ),
            laden=Emissions(
                co2_in_tons=3267.237442930711,
                coin_tons=2.8855782971753325,
                ch4_in_tons=0.06250350102184836,
                n2_oin_tons=0.16417719815178825,
                nmvocin_tons=3.208513052454882,
                nox_in_tons=80.55680788228776,
                sox_in_tons=1.175733657296142,
                pmin_tons=2.5872143845627553,
            ),
            port_call=Emissions(
                co2_in_tons=558.76,
                coin_tons=0.48474999999999996,
                ch4_in_tons=0.0105,
                n2_oin_tons=0.0265,
                nmvocin_tons=0.5389999999999999,
                nox_in_tons=13.024000000000001,
                sox_in_tons=0.045455145000000044,
                pmin_tons=0.14173187967225,
            ),
            stop=Emissions(
                co2_in_tons=145.84555445601853,
                coin_tons=0.12648905237268518,
                ch4_in_tons=0.0027398350694444445,
                n2_oin_tons=0.006909955150462963,
                nmvocin_tons=0.14064486689814817,
                nox_in_tons=3.3961470211226854,
                sox_in_tons=0.011175857804600703,
                pmin_tons=0.03566347350821582,
            )
        )
        )
    ),
    EmissionsEstimationModel(
        id='I9783B354VEDB0E0800',
        imo=9929651,
        vessel_name='C. Earnest',
        voyage_number=5,
        vessel_type_id=1,
        vessel_type='Tanker',
        vessel_class_id=84,
        vessel_class='VLCC',
        start_date='2022-12-19T23:59:01',
        end_date='2023-03-14T07:56:46',
        quantity=286000.0,
        deadweight=300000,
        contains_eu_emissions=True,
        transport_work_in_million_tonne_miles=5243.838600000005,
        transport_work_in_million_dwt_miles=5500.530000000005,
        emissions=(EmissionsBreakdown(
            voyage=Emissions(
                co2_in_tons=10473.148881436808,
                coin_tons=9.293915505042596,
                ch4_in_tons=0.20131224920669885,
                n2_oin_tons=0.5342452119368128,
                nmvocin_tons=10.334028792610539,
                nox_in_tons=262.0306276979183,
                sox_in_tons=4.555498066379615,
                pmin_tons=9.813583360103838,
            ),
            ballast=Emissions(
                co2_in_tons=1762.646008299334,
                coin_tons=1.5622843800668604,
                ch4_in_tons=0.03384009487509446,
                n2_oin_tons=0.08957218709965897,
                nmvocin_tons=1.7371248702548487,
                nox_in_tons=43.93690502581925,
                sox_in_tons=0.7329528563691268,
                pmin_tons=1.5864299040671905,
            ),
            laden=Emissions(
                co2_in_tons=7709.014641945343,
                coin_tons=6.854468866584533,
                ch4_in_tons=0.1484722498177155,
                n2_oin_tons=0.3956732635524317,
                nmvocin_tons=7.621575490642728,
                nox_in_tons=194.0331733737773,
                sox_in_tons=3.5928257533510264,
                pmin_tons=7.686631841123893,
            ),
            port_call=Emissions(
                co2_in_tons=547.31,
                coin_tons=0.48474999999999996,
                ch4_in_tons=0.0105,
                n2_oin_tons=0.02775,
                nmvocin_tons=0.5389999999999999,
                nox_in_tons=13.61275,
                sox_in_tons=0.2214105450000002,
                pmin_tons=0.48066123235725,
            ),
            stop=Emissions(
                co2_in_tons=454.1782311921297,
                coin_tons=0.3924122583912037,
                ch4_in_tons=0.008499904513888889,
                n2_oin_tons=0.021249761284722224,
                nmvocin_tons=0.436328431712963,
                nox_in_tons=10.44779929832176,
                sox_in_tons=0.008308911659461815,
                pmin_tons=0.05986038255550291,
            )
        )
        )
    ),
    EmissionsEstimationModel(
        id='I9783B354VEDB84AF00',
        imo=9929651,
        vessel_name='C. Earnest',
        voyage_number=6,
        vessel_type_id=1,
        vessel_type='Tanker',
        vessel_class_id=84,
        vessel_class='VLCC',
        start_date='2023-03-14T07:56:46',
        end_date='2023-04-30T11:55:24',
        quantity=270000.0,
        deadweight=300000,
        contains_eu_emissions=False,
        transport_work_in_million_tonne_miles=2030.6241000000011,
        transport_work_in_million_dwt_miles=2256.2490000000016,
        emissions=(EmissionsBreakdown(
            voyage=Emissions(
                co2_in_tons=5415.542294919199,
                coin_tons=4.816674851312029,
                ch4_in_tons=0.10433230724863604,
                n2_oin_tons=0.27821948599636276,
                nmvocin_tons=5.355725105429983,
                nox_in_tons=136.4318804454664,
                sox_in_tons=2.549699007618982,
                pmin_tons=5.449595395122589,
            ),
            ballast=Emissions(
                co2_in_tons=454.30299397472027,
                coin_tons=0.40406476153030285,
                ch4_in_tons=0.008752305303905477,
                n2_oin_tons=0.023339480810414606,
                nmvocin_tons=0.4492850056004811,
                nox_in_tons=11.445097902407063,
                sox_in_tons=0.2138910250931682,
                pmin_tons=0.4571596654831368,
            ),
            laden=Emissions(
                co2_in_tons=3270.058371662073,
                coin_tons=2.908445186714597,
                ch4_in_tons=0.06299881270861944,
                n2_oin_tons=0.16799683388965184,
                nmvocin_tons=3.233939052375798,
                nox_in_tons=82.38144741863803,
                sox_in_tons=1.5395807346764205,
                pmin_tons=3.290620601506647,
            ),
            port_call=Emissions(
                co2_in_tons=1090.04,
                coin_tons=0.9694999999999999,
                ch4_in_tons=0.021,
                n2_oin_tons=0.056,
                nmvocin_tons=1.0779999999999998,
                nox_in_tons=27.461,
                sox_in_tons=0.5132032500000004,
                pmin_tons=1.0968942057885,
            ),
            stop=Emissions(
                co2_in_tons=601.1409292824075,
                coin_tons=0.5346649030671297,
                ch4_in_tons=0.011581189236111112,
                n2_oin_tons=0.0308831712962963,
                nmvocin_tons=0.5945010474537037,
                nox_in_tons=15.144335124421296,
                sox_in_tons=0.2830239978493926,
                pmin_tons=0.6049209223443057,
            )
        )
        )
    ),
    EmissionsEstimationModel(
        id='I9783B354VEDBD3C900',
        imo=9929651,
        vessel_name='C. Earnest',
        voyage_number=7,
        vessel_type_id=1,
        vessel_type='Tanker',
        vessel_class_id=84,
        vessel_class='VLCC',
        start_date='2023-04-30T11:55:24',
        end_date='2023-06-02T23:57:17',
        quantity=278000.0,
        deadweight=300000,
        contains_eu_emissions=False,
        transport_work_in_million_tonne_miles=1929.7647999999995,
        transport_work_in_million_dwt_miles=2082.4799999999996,
        emissions=(EmissionsBreakdown(
            voyage=Emissions(
                co2_in_tons=4150.61183795167,
                coin_tons=3.6916243228635137,
                ch4_in_tons=0.07996298172267538,
                n2_oin_tons=0.2132346179271344,
                nmvocin_tons=4.104766395097336,
                nox_in_tons=104.56492576601852,
                sox_in_tons=1.9541553380841736,
                pmin_tons=4.17671101567497,
            ),
            ballast=Emissions(
                co2_in_tons=2825.5394821959203,
                coin_tons=2.513082573106441,
                ch4_in_tons=0.05443500158353301,
                n2_oin_tons=0.1451600042227547,
                nmvocin_tons=2.794330081288028,
                nox_in_tons=71.18283707073334,
                sox_in_tons=1.330296177448777,
                pmin_tons=2.8433065632888184,
            ),
            laden=Emissions(
                co2_in_tons=522.7543433714909,
                coin_tons=0.4649465486575359,
                ch4_in_tons=0.010071044375253486,
                n2_oin_tons=0.026856118334009294,
                nmvocin_tons=0.5169802779296788,
                nox_in_tons=13.169569028039806,
                sox_in_tons=0.2461187002035387,
                pmin_tons=0.5260414391168767,
            ),
            port_call=Emissions(
                co2_in_tons=545.02,
                coin_tons=0.48474999999999996,
                ch4_in_tons=0.0105,
                n2_oin_tons=0.028,
                nmvocin_tons=0.5389999999999999,
                nox_in_tons=13.7305,
                sox_in_tons=0.2566016250000002,
                pmin_tons=0.54844710289425,
            ),
            stop=Emissions(
                co2_in_tons=257.2980123842592,
                coin_tons=0.22884520109953704,
                ch4_in_tons=0.004956935763888889,
                n2_oin_tons=0.013218495370370372,
                nmvocin_tons=0.2544560358796296,
                nox_in_tons=6.482019667245371,
                sox_in_tons=0.12113883543185774,
                pmin_tons=0.2589159103750245,
            )
        )
        )
    ),
    EmissionsEstimationModel(
        id='I9783B354VEDBFB5600',
        imo=9929651,
        vessel_name='C. Earnest',
        voyage_number=8,
        vessel_type_id=1,
        vessel_type='Tanker',
        vessel_class_id=84,
        vessel_class='VLCC',
        start_date='2023-06-02T23:57:17',
        end_date='2023-09-07T14:03:35.429000',
        quantity=270000.0,
        deadweight=300000,
        contains_eu_emissions=False,
        transport_work_in_million_tonne_miles=5303.950200000001,
        transport_work_in_million_dwt_miles=5893.278000000001,
        emissions=(EmissionsBreakdown(
            voyage=Emissions(
                co2_in_tons=6924.895099830229,
                coin_tons=6.150791988208722,
                ch4_in_tons=0.13323015136914199,
                n2_oin_tons=0.35425834658088906,
                nmvocin_tons=6.839147770282622,
                nox_in_tons=173.73923906033772,
                sox_in_tons=3.112042578215192,
                pmin_tons=6.681894033383674,
            ),
            ballast=Emissions(
                co2_in_tons=3897.7783129336012,
                coin_tons=3.460108597926129,
                ch4_in_tons=0.07494820067710026,
                n2_oin_tons=0.19904668909225465,
                nmvocin_tons=3.847340968091147,
                nox_in_tons=97.62331426410212,
                sox_in_tons=1.7168546940916345,
                pmin_tons=3.693743093708341,
            ),
            laden=Emissions(
                co2_in_tons=2462.3235910632948,
                coin_tons=2.18834677569926,
                ch4_in_tons=0.047401013192041735,
                n2_oin_tons=0.12619582415530103,
                nmvocin_tons=2.433252010524809,
                nox_in_tons=61.887285525402284,
                sox_in_tons=1.129276813264182,
                pmin_tons=2.419806306470724,
            ),
            port_call=Emissions(
                co2_in_tons=545.02,
                coin_tons=0.48474999999999996,
                ch4_in_tons=0.0105,
                n2_oin_tons=0.028,
                nmvocin_tons=0.5389999999999999,
                nox_in_tons=13.7305,
                sox_in_tons=0.2566016250000002,
                pmin_tons=0.54844710289425,
            ),
            stop=Emissions(
                co2_in_tons=19.773195833333332,
                coin_tons=0.017586614583333333,
                ch4_in_tons=0.00038093750000000004,
                n2_oin_tons=0.0010158333333333334,
                nmvocin_tons=0.019554791666666668,
                nox_in_tons=0.49813927083333337,
                sox_in_tons=0.00930944585937501,
                pmin_tons=0.019897530310359846,
            )
        )
        )
    )
]

__mock_emissions_response_3 = {
    "ID": "I8F9DC4VED7805D00",
    "IMO": 9412036,
    "VesselName": "Sea Hymn",
    "VoyageNumber": 143,
    "VesselTypeID": 1,
    "VesselType": "Tanker",
    "VesselClassID": 86,
    "VesselClass": "Aframax",
    "StartDate": "2021-01-24T11:59:59",
    "EndDate": "2021-02-05T14:31:12.812000",
    "Quantity": 71000.0,
    "Deadweight": 116337,
    "ContainsEuEmissions": true,
    "TransportWorkInMillionTonneMiles": 102.85628000000001,
    "TransportWorkInMillionDwtMiles": 168.53508516000002,
    "Emissions": {
        "Voyage": {
            "CO2InTons": 837.5087196481956,
            "COInTons": 0.7359510048818543,
            "CH4InTons": 0.015941177001051,
            "N2OInTons": 0.04245146957224711,
            "NMVOCInTons": 0.8183137527206179,
            "NOxInTons": 23.13202057801321,
            "SOxInTons": 0.5194326251279129,
            "PMInTons": 0.7876209259839941
        },
        "Ballast": {
            "CO2InTons": 409.19323058978165,
            "COInTons": 0.3597114758091598,
            "CH4InTons": 0.00779158431355581,
            "N2OInTons": 0.02077755816948216,
            "NMVOCInTons": 0.3999679947625315,
            "NOxInTons": 11.32117200759659,
            "SOxInTons": 0.25388358046767373,
            "PMInTons": 0.3908711003278056
        },
        "Laden": {
            "CO2InTons": 74.9966521789844,
            "COInTons": 0.06592767039954643,
            "CH4InTons": 0.001428036181939634,
            "N2OInTons": 0.003808096485172358,
            "NMVOCInTons": 0.07330585733956788,
            "NOxInTons": 2.074936572358288,
            "SOxInTons": 0.04653160696438169,
            "PMInTons": 0.07163858482177292
        },
        "PortCall": {
            "CO2InTons": 252.0832,
            "COInTons": 0.2216,
            "CH4InTons": 0.0048000000000000004,
            "N2OInTons": 0.012800000000000002,
            "NMVOCInTons": 0.24639999999999998,
            "NOxInTons": 6.974399999999999,
            "SOxInTons": 0.1564048,
            "PMInTons": 0.24079586462400004
        },
        "Stop": {
            "CO2InTons": 101.23563687942965,
            "COInTons": 0.08871185867314817,
            "CH4InTons": 0.0019215565055555556,
            "N2OInTons": 0.005065814917592594,
            "NMVOCInTons": 0.09863990061851852,
            "NOxInTons": 2.7615119980583334,
            "SOxInTons": 0.06261263769585741,
            "PMInTons": 0.08431537621041556
        }
    },
    "Consumptions": {
        "Voyage": {
            "LFOInTons": 259.85270696196113,
            "MGOInTons": 5.833576388888889,
            "TotalInTons": 265.68628335085003
        },
        "Ballast": {
            "LFOInTons": 129.8597385592635,
            "TotalInTons": 129.8597385592635
        },
        "Laden": {
            "LFOInTons": 23.800603032327235,
            "TotalInTons": 23.800603032327235
        },
        "PortCall": {
            "LFOInTons": 80.0,
            "TotalInTons": 80.0
        },
        "Stop": {
            "LFOInTons": 26.19236537037037,
            "MGOInTons": 5.833576388888889,
            "TotalInTons": 32.02594175925926
        }
    },
    "SeagoingSpeedStatistics": {
        "Voyage": {
            "AverageSpeedInKnots": 12.338028169014084,
            "StdSpeedInKnots": 0.38073845435382875,
            "MinSpeedInKnots": 11.7,
            "MaxSpeedInKnots": 13.6
        },
        "Ballast": {
            "AverageSpeedInKnots": 12.341935483870968,
            "StdSpeedInKnots": 0.3919469632475068,
            "MinSpeedInKnots": 11.7,
            "MaxSpeedInKnots": 13.6
        },
        "Laden": {
            "AverageSpeedInKnots": 12.311111111111112,
            "StdSpeedInKnots": 0.3100179206289712,
            "MinSpeedInKnots": 11.8,
            "MaxSpeedInKnots": 12.8
        }
    },
    "Duration": {
        "Voyage": {
            "InHours": 290.52050333333335,
            "InDays": 12.105020972222224
        },
        "Ballast": {
            "InHours": 107.35055555555554,
            "InDays": 4.472939814814815
        },
        "Laden": {
            "InHours": 14.755052222222222,
            "InDays": 0.6147938425925926
        },
        "PortCall": {
            "InHours": 58.611666666666665,
            "InDays": 2.442152777777778
        },
        "Stop": {
            "InHours": 109.8032288888889,
            "InDays": 4.575134537037037
        }
    },
    "Distances": {
        "Voyage": {
            "DistanceTravelled": 1448.6800000000003
        },
        "Ballast": {
            "DistanceTravelled": 1267.5300000000002
        },
        "Laden": {
            "DistanceTravelled": 181.14999999999998
        }
    },
    "EfficiencyMetrics": {
        "VoyageCii": 4.969343438804451,
        "VoyageCiiUnit": "g-CO2/capacity mile",
        "VoyageCiiRating": "D",
        "VoyageCiiTarget": 4.178777475053739,
        "VoyageCiiTargetYear": 2021,
        "CapacityEeoi": 39.74048276526212,
        "CapacityEeoiUnit": "g-CO2/capacity mile",
        "CapacityEeoiSeaCargoCharterYearTarget": 11.02,
        "CapacityEeoiSeaCargoCharterClass": "Oil Tanker 80000-119999 DWT",
        "CapacityEeoiSeaCargoCharterAlignmentInPercentage": 260.6214407011082,
        "Eeoi": 65.11674004876478,
        "EeoiUnit": "g-CO2/ton mile",
        "EeoiSeaCargoCharterYearTarget": 11.02,
        "EeoiSeaCargoCharterClass": "Oil Tanker 80000-119999 DWT",
        "EeoiSeaCargoCharterAlignmentInPercentage": 490.8960077020398,
        "kgCO2PerTonneCargo": 11.795897459833741,
        "kgCO2PerTonneDwt": 7.198988452927233
    },
    "EuropeanUnionRegulated": {
        "Emissions": {
            "Voyage": {
                "CO2InTons": 427.8956764925594,
                "COInTons": 0.37587048240638204,
                "CH4InTons": 0.008141598896889143,
                "N2OInTons": 0.02165259462781549,
                "NMVOCInTons": 0.41793541004030926,
                "NOxInTons": 11.799233592666035,
                "SOxInTons": 0.26528857232253483,
                "PMInTons": 0.39634881071439554
            },
            "Ballast": {
                "CO2InTons": 409.19323058978165,
                "COInTons": 0.3597114758091598,
                "CH4InTons": 0.00779158431355581,
                "N2OInTons": 0.02077755816948216,
                "NMVOCInTons": 0.3999679947625315,
                "NOxInTons": 11.32117200759659,
                "SOxInTons": 0.25388358046767373,
                "PMInTons": 0.3908711003278056
            },
            "Stop": {
                "CO2InTons": 18.70244590277778,
                "COInTons": 0.016159006597222223,
                "CH4InTons": 0.00035001458333333335,
                "N2OInTons": 0.0008750364583333332,
                "NMVOCInTons": 0.017967415277777777,
                "NOxInTons": 0.4780615850694444,
                "SOxInTons": 0.011404991854861112,
                "PMInTons": 0.005477710386589924
            }
        },
        "Consumptions": {
            "Voyage": {
                "LFOInTons": 129.8597385592635,
                "MGOInTons": 5.833576388888889,
                "TotalInTons": 135.6933149481524
            },
            "Ballast": {
                "LFOInTons": 129.8597385592635,
                "TotalInTons": 129.8597385592635
            },
            "Stop": {
                "MGOInTons": 5.833576388888889,
                "TotalInTons": 5.833576388888889
            }
        },
        "Distances": {
            "Voyage": {
                "DistanceTravelled": 1267.5300000000002
            },
            "Ballast": {
                "DistanceTravelled": 1267.5300000000002
            },
            "Laden": {
                "DistanceTravelled": 0.0
            }
        },
        "Duration": {
            "Voyage": {
                "InHours": 127.35138888888888,
                "InDays": 5.306307870370371
            },
            "Ballast": {
                "InHours": 107.35055555555554,
                "InDays": 4.472939814814815
            },
            "Stop": {
                "InHours": 20.000833333333333,
                "InDays": 0.8333680555555556
            }
        }
    }
}

__mock_emissions_3 = EmissionsEstimationModel(
    id='I8F9DC4VED7805D00',
    imo=9412036,
    vessel_name='Sea Hymn',
    voyage_number=143,
    vessel_type_id=1,
    vessel_type='Tanker',
    vessel_class_id=86,
    vessel_class='Aframax',
    start_date='2021-01-24T11:59:59',
    end_date='2021-02-05T14:31:12.812000',
    quantity=71000.0,
    deadweight=116337,
    contains_eu_emissions=True,
    transport_work_in_million_tonne_miles=102.85628000000001,
    transport_work_in_million_dwt_miles=168.53508516000002,
    emissions=(EmissionsBreakdown(
        voyage=Emissions(
            co2_in_tons=837.5087196481956,
            coin_tons=0.7359510048818543,
            ch4_in_tons=0.015941177001051,
            n2_oin_tons=0.04245146957224711,
            nmvocin_tons=0.8183137527206179,
            nox_in_tons=23.13202057801321,
            sox_in_tons=0.5194326251279129,
            pmin_tons=0.7876209259839941,
        ),
        ballast=Emissions(
            co2_in_tons=409.19323058978165,
            coin_tons=0.3597114758091598,
            ch4_in_tons=0.00779158431355581,
            n2_oin_tons=0.02077755816948216,
            nmvocin_tons=0.3999679947625315,
            nox_in_tons=11.32117200759659,
            sox_in_tons=0.25388358046767373,
            pmin_tons=0.3908711003278056,
        ),
        laden=Emissions(
            co2_in_tons=74.9966521789844,
            coin_tons=0.06592767039954643,
            ch4_in_tons=0.001428036181939634,
            n2_oin_tons=0.003808096485172358,
            nmvocin_tons=0.07330585733956788,
            nox_in_tons=2.074936572358288,
            sox_in_tons=0.04653160696438169,
            pmin_tons=0.07163858482177292,
        ),
        port_call=Emissions(
            co2_in_tons=252.0832,
            coin_tons=0.2216,
            ch4_in_tons=0.0048000000000000004,
            n2_oin_tons=0.012800000000000002,
            nmvocin_tons=0.24639999999999998,
            nox_in_tons=6.974399999999999,
            sox_in_tons=0.1564048,
            pmin_tons=0.24079586462400004,
        ),
        stop=Emissions(
            co2_in_tons=101.23563687942965,
            coin_tons=0.08871185867314817,
            ch4_in_tons=0.0019215565055555556,
            n2_oin_tons=0.005065814917592594,
            nmvocin_tons=0.09863990061851852,
            nox_in_tons=2.7615119980583334,
            sox_in_tons=0.06261263769585741,
            pmin_tons=0.08431537621041556,
        )
    )
    )
    ,
    consumptions=(ConsumptionsBreakdown(
        voyage=Consumptions(
            lfoin_tons=259.85270696196113,
            mgoin_tons=5.833576388888889,
            total_in_tons=265.68628335085003,
        ),
        ballast=Consumptions(
            lfoin_tons=129.8597385592635,
            total_in_tons=129.8597385592635,
        ),
        laden=Consumptions(
            lfoin_tons=23.800603032327235,
            total_in_tons=23.800603032327235,
        ),
        port_call=Consumptions(
            lfoin_tons=80.0,
            total_in_tons=80.0,
        ),
        stop=Consumptions(
            lfoin_tons=26.19236537037037,
            mgoin_tons=5.833576388888889,
            total_in_tons=32.02594175925926,
        )
    )
    )
)

__mock_metrics_response = [
    {
        "IMO": 9412036,
        "Year": 2022,
        "VesselType": "Tanker",
        "VesselTypeID": 1,
        "VesselClass": "Aframax",
        "VesselClassID": 86,
        "Eexi": {
            "Value": 5.515052548670922,
            "Unit": "g-CO2/ton mile",
            "Required": 3.288153751950862
        },
        "Eiv": {
            "Value": 4.69363738382239,
            "Unit": "g-CO2/ton mile"
        },
        "Aer": {
            "Value": 3.78004183987603,
            "Unit": "g-CO2/dwt mile",
            "PoseidonPrinciplesClass": "Oil Tanker 80000-119999 DWT",
            "PoseidonPrinciplesAlignmentInPercentage": 6.780842934351123,
            "PoseidonPrinciplesYearTarget": 3.54
        },
        "Cii": {
            "Value": 3.78004183987603,
            "Unit": "g-CO2/capacity mile",
            "Rating": "B",
            "Target": 4.136136888573598,
            "TargetYear": 2022
        }
    }]

__mock_metrics_1 = [VesselMetrics(
    imo=9412036,
    year=2022,
    vessel_type="Tanker",
    vessel_type_id=1,
    vessel_class="Aframax",
    vessel_class_id=86,
    eexi=Eexi(
        value=5.515052548670922,
        unit="g-CO2/ton mile",
        required=3.288153751950862
    ),
    eiv=Eiv(
        value=4.69363738382239,
        unit="g-CO2/ton mile"
    ),
    aer=Aer(
        value=3.78004183987603,
        unit="g-CO2/dwt mile",
        poseidon_principles_class="Oil Tanker 80000-119999 DWT",
        poseidon_principles_alignment_in_percentage=6.780842934351123,
        poseidon_principles_year_target=3.54
    ),
    cii=Cii(
        value=3.78004183987603,
        unit="g-CO2/capacity mile",
        rating="B",
        target=4.136136888573598,
        target_year=2022
    )
)
]
