from signal_ocean.vessel_emissions.models import Emissions, EmissionsEstimation, EmissionsBreakdown, \
    VesselClassEmissions, VesselClassMetrics, VesselMetrics, Aer, Cii, Metrics
from tests.vessel_emissions.vessel_emissions_mock_data import __mock_emissions_response_imo_all_args, \
    __mock_emissions_imo_all_args

__mock_emissions_response_vessel_class_no_args = {
    "NextPageToken": "eyJ2ZXNzZWxfY2xhc3NfaWQiOiA4NiwgImxhc3RfaWQiOiAiNjI1ZjUyZTlkMzMwZDA2MTBjOWFkZTEwIn0=",
    "Data": [{
        "ID": "I8FE002VED1BBCD00",
        "IMO": 9428994,
        "VesselName": "SKS Dee",
        "VoyageNumber": 52,
        "VesselTypeID": 1,
        "VesselType": "Tanker",
        "VesselClassID": 86,
        "VesselClass": "Aframax",
        "StartDate": "2017-12-14T03:23:33",
        "EndDate": "2018-01-17T23:56:25",
        "Quantity": 75000.0,
        "Deadweight": 119456,
        "ContainsEuEmissions": False,
        "TransportWorkInMillionTonneMiles": 435.21824999999995,
        "TransportWorkInMillionDwtMiles": 693.19241696,
        "Emissions": {
            "Voyage": {
                "CO2InTons": 2340.277087625018,
                "COInTons": 2.081481997406017,
                "CH4InTons": 0.045086252651393884,
                "N2OInTons": 0.12023000707038368,
                "NMVOCInTons": 2.3144276361048854,
                "NOxInTons": 69.74843285170633,
                "SOxInTons": 36.72763712859755,
                "PMInTons": 5.233317385611677
            },
            "Ballast": {
                "CO2InTons": 901.9591243208984,
                "COInTons": 0.8022176902032135,
                "CH4InTons": 0.0173765564664956,
                "N2OInTons": 0.04633748391065494,
                "NMVOCInTons": 0.8919965652801074,
                "NOxInTons": 26.881532853668695,
                "SOxInTons": 14.155087702244538,
                "PMInTons": 2.016957048111716
            },
            "Laden": {
                "CO2InTons": 1066.8937541930086,
                "COInTons": 0.9489133377583592,
                "CH4InTons": 0.02055407951823161,
                "N2OInTons": 0.05481087871528429,
                "NMVOCInTons": 1.0551094152692224,
                "NOxInTons": 31.797161014704297,
                "SOxInTons": 16.743524459547455,
                "PMInTons": 2.38578314591157
            },
            "PortCall": {
                "CO2InTons": 249.152,
                "COInTons": 0.2216,
                "CH4InTons": 0.0048000000000000004,
                "N2OInTons": 0.012800000000000002,
                "NMVOCInTons": 0.24639999999999998,
                "NOxInTons": 7.425599999999999,
                "SOxInTons": 3.91012,
                "PMInTons": 0.557152612464
            },
            "Stop": {
                "CO2InTons": 122.27220911111111,
                "COInTons": 0.10875096944444444,
                "CH4InTons": 0.002355616666666667,
                "N2OInTons": 0.006281644444444446,
                "NMVOCInTons": 0.12092165555555556,
                "NOxInTons": 3.6441389833333337,
                "SOxInTons": 1.9189049668055556,
                "PMInTons": 0.2734245791243902
            }
        }
    }, {
        "ID": "I8FE002VED1F08900",
        "IMO": 9428994,
        "VesselName": "SKS Dee",
        "VoyageNumber": 53,
        "VesselTypeID": 1,
        "VesselType": "Tanker",
        "VesselClassID": 86,
        "VesselClass": "Aframax",
        "StartDate": "2018-01-17T23:56:25",
        "EndDate": "2018-05-03T15:07:03",
        "Quantity": 90000.0,
        "Deadweight": 119456,
        "ContainsEuEmissions": False,
        "TransportWorkInMillionTonneMiles": 1726.4124,
        "TransportWorkInMillionDwtMiles": 2291.44799616,
        "Emissions": {
            "Voyage": {
                "CO2InTons": 8363.505735803703,
                "COInTons": 7.437847581420064,
                "CH4InTons": 0.1611086118719148,
                "N2OInTons": 0.4295252878914624,
                "NMVOCInTons": 8.270242076091627,
                "NOxInTons": 249.18061642097922,
                "SOxInTons": 130.78210278246783,
                "PMInTons": 18.641579700924957
            },
            "Ballast": {
                "CO2InTons": 510.0514108534562,
                "COInTons": 0.4536483457693532,
                "CH4InTons": 0.009826317958902958,
                "N2OInTons": 0.026203514557074554,
                "NMVOCInTons": 0.5044176552236852,
                "NOxInTons": 15.201313882422875,
                "SOxInTons": 8.004600495305342,
                "PMInTons": 1.14057473368848
            },
            "Laden": {
                "CO2InTons": 6908.1759625058,
                "COInTons": 6.143452682872935,
                "CH4InTons": 0.13307117724634518,
                "N2OInTons": 0.35475879555661,
                "NMVOCInTons": 6.830987098645719,
                "NOxInTons": 205.80670505522298,
                "SOxInTons": 107.94257489119026,
                "PMInTons": 15.38717762833648
            },
            "PortCall": {
                "CO2InTons": 700.7399999999999,
                "COInTons": 0.62325,
                "CH4InTons": 0.013500000000000002,
                "N2OInTons": 0.036000000000000004,
                "NMVOCInTons": 0.693,
                "NOxInTons": 20.8845,
                "SOxInTons": 10.9972125,
                "PMInTons": 1.566991722555
            },
            "Stop": {
                "CO2InTons": 244.53836244444443,
                "COInTons": 0.21749655277777774,
                "CH4InTons": 0.004711116666666666,
                "N2OInTons": 0.012562977777777777,
                "NMVOCInTons": 0.24183732222222215,
                "NOxInTons": 7.288097483333333,
                "SOxInTons": 3.837714895972223,
                "PMInTons": 0.5468356163450052
            }
        }
    }
    ]
}

__mock_emissions_vessel_class_no_args = VesselClassEmissions(
    next_page_token="eyJ2ZXNzZWxfY2xhc3NfaWQiOiA4NiwgImxhc3RfaWQiOiAiNjI1ZjUyZTlkMzMwZDA2MTBjOWFkZTEwIn0=",
    data=[
        EmissionsEstimation(
            id='I8FE002VED1BBCD00',
            imo=9428994,
            vessel_name='SKS Dee',
            voyage_number=52,
            vessel_type_id=1,
            vessel_type='Tanker',
            vessel_class_id=86,
            vessel_class='Aframax',
            start_date='2017-12-14T03:23:33',
            end_date='2018-01-17T23:56:25',
            quantity=75000.0,
            deadweight=119456,
            contains_eu_emissions=False,
            transport_work_in_million_tonne_miles=435.21824999999995,
            transport_work_in_million_dwt_miles=693.19241696,
            emissions=EmissionsBreakdown(
                voyage=Emissions(
                    co2_in_tons=2340.277087625018,
                    coin_tons=2.081481997406017,
                    ch4_in_tons=0.045086252651393884,
                    n2_oin_tons=0.12023000707038368,
                    nmvocin_tons=2.3144276361048854,
                    nox_in_tons=69.74843285170633,
                    sox_in_tons=36.72763712859755,
                    pmin_tons=5.233317385611677,
                ),
                ballast=Emissions(
                    co2_in_tons=901.9591243208984,
                    coin_tons=0.8022176902032135,
                    ch4_in_tons=0.0173765564664956,
                    n2_oin_tons=0.04633748391065494,
                    nmvocin_tons=0.8919965652801074,
                    nox_in_tons=26.881532853668695,
                    sox_in_tons=14.155087702244538,
                    pmin_tons=2.016957048111716,
                ),
                laden=Emissions(
                    co2_in_tons=1066.8937541930086,
                    coin_tons=0.9489133377583592,
                    ch4_in_tons=0.02055407951823161,
                    n2_oin_tons=0.05481087871528429,
                    nmvocin_tons=1.0551094152692224,
                    nox_in_tons=31.797161014704297,
                    sox_in_tons=16.743524459547455,
                    pmin_tons=2.38578314591157,
                ),
                port_call=Emissions(
                    co2_in_tons=249.152,
                    coin_tons=0.2216,
                    ch4_in_tons=0.0048000000000000004,
                    n2_oin_tons=0.012800000000000002,
                    nmvocin_tons=0.24639999999999998,
                    nox_in_tons=7.425599999999999,
                    sox_in_tons=3.91012,
                    pmin_tons=0.557152612464,
                ),
                stop=Emissions(
                    co2_in_tons=122.27220911111111,
                    coin_tons=0.10875096944444444,
                    ch4_in_tons=0.002355616666666667,
                    n2_oin_tons=0.006281644444444446,
                    nmvocin_tons=0.12092165555555556,
                    nox_in_tons=3.6441389833333337,
                    sox_in_tons=1.9189049668055556,
                    pmin_tons=0.2734245791243902,
                )
            )
        ),
        EmissionsEstimation(
            id='I8FE002VED1F08900',
            imo=9428994,
            vessel_name='SKS Dee',
            voyage_number=53,
            vessel_type_id=1,
            vessel_type='Tanker',
            vessel_class_id=86,
            vessel_class='Aframax',
            start_date='2018-01-17T23:56:25',
            end_date='2018-05-03T15:07:03',
            quantity=90000.0,
            deadweight=119456,
            contains_eu_emissions=False,
            transport_work_in_million_tonne_miles=1726.4124,
            transport_work_in_million_dwt_miles=2291.44799616,
            emissions=EmissionsBreakdown(
                voyage=Emissions(
                    co2_in_tons=8363.505735803703,
                    coin_tons=7.437847581420064,
                    ch4_in_tons=0.1611086118719148,
                    n2_oin_tons=0.4295252878914624,
                    nmvocin_tons=8.270242076091627,
                    nox_in_tons=249.18061642097922,
                    sox_in_tons=130.78210278246783,
                    pmin_tons=18.641579700924957,
                ),
                ballast=Emissions(
                    co2_in_tons=510.0514108534562,
                    coin_tons=0.4536483457693532,
                    ch4_in_tons=0.009826317958902958,
                    n2_oin_tons=0.026203514557074554,
                    nmvocin_tons=0.5044176552236852,
                    nox_in_tons=15.201313882422875,
                    sox_in_tons=8.004600495305342,
                    pmin_tons=1.14057473368848,
                ),
                laden=Emissions(
                    co2_in_tons=6908.1759625058,
                    coin_tons=6.143452682872935,
                    ch4_in_tons=0.13307117724634518,
                    n2_oin_tons=0.35475879555661,
                    nmvocin_tons=6.830987098645719,
                    nox_in_tons=205.80670505522298,
                    sox_in_tons=107.94257489119026,
                    pmin_tons=15.38717762833648,
                ),
                port_call=Emissions(
                    co2_in_tons=700.7399999999999,
                    coin_tons=0.62325,
                    ch4_in_tons=0.013500000000000002,
                    n2_oin_tons=0.036000000000000004,
                    nmvocin_tons=0.693,
                    nox_in_tons=20.8845,
                    sox_in_tons=10.9972125,
                    pmin_tons=1.566991722555,
                ),
                stop=Emissions(
                    co2_in_tons=244.53836244444443,
                    coin_tons=0.21749655277777774,
                    ch4_in_tons=0.004711116666666666,
                    n2_oin_tons=0.012562977777777777,
                    nmvocin_tons=0.24183732222222215,
                    nox_in_tons=7.288097483333333,
                    sox_in_tons=3.837714895972223,
                    pmin_tons=0.5468356163450052,
                )
            )
        )
    ]
)

__mock_emissions_response_vessel_class_one_arg = {
    "NextPageToken": "eyJ2ZXNzZWxfY2xhc3NfaWQiOiA4NiwgImxhc3RfaWQiOiAiNjI1ZjUyZTlkMzMwZDA2MTBjOWFkZTEwIn0=",
    "Data": [{
        "ID": "I8FE002VED1BBCD00",
        "IMO": 9428994,
        "VesselName": "SKS Dee",
        "VoyageNumber": 52,
        "VesselTypeID": 1,
        "VesselType": "Tanker",
        "VesselClassID": 86,
        "VesselClass": "Aframax",
        "StartDate": "2017-12-14T03:23:33",
        "EndDate": "2018-01-17T23:56:25",
        "Quantity": 75000.0,
        "Deadweight": 119456,
        "ContainsEuEmissions": False,
        "TransportWorkInMillionTonneMiles": 435.21824999999995,
        "TransportWorkInMillionDwtMiles": 693.19241696,
        "Emissions": {
            "Voyage": {
                "CO2InTons": 2340.277087625018,
                "COInTons": 2.081481997406017,
                "CH4InTons": 0.045086252651393884,
                "N2OInTons": 0.12023000707038368,
                "NMVOCInTons": 2.3144276361048854,
                "NOxInTons": 69.74843285170633,
                "SOxInTons": 36.72763712859755,
                "PMInTons": 5.233317385611677
            },
            "Ballast": {
                "CO2InTons": 901.9591243208984,
                "COInTons": 0.8022176902032135,
                "CH4InTons": 0.0173765564664956,
                "N2OInTons": 0.04633748391065494,
                "NMVOCInTons": 0.8919965652801074,
                "NOxInTons": 26.881532853668695,
                "SOxInTons": 14.155087702244538,
                "PMInTons": 2.016957048111716
            },
            "Laden": {
                "CO2InTons": 1066.8937541930086,
                "COInTons": 0.9489133377583592,
                "CH4InTons": 0.02055407951823161,
                "N2OInTons": 0.05481087871528429,
                "NMVOCInTons": 1.0551094152692224,
                "NOxInTons": 31.797161014704297,
                "SOxInTons": 16.743524459547455,
                "PMInTons": 2.38578314591157
            },
            "PortCall": {
                "CO2InTons": 249.152,
                "COInTons": 0.2216,
                "CH4InTons": 0.0048000000000000004,
                "N2OInTons": 0.012800000000000002,
                "NMVOCInTons": 0.24639999999999998,
                "NOxInTons": 7.425599999999999,
                "SOxInTons": 3.91012,
                "PMInTons": 0.557152612464
            },
            "Stop": {
                "CO2InTons": 122.27220911111111,
                "COInTons": 0.10875096944444444,
                "CH4InTons": 0.002355616666666667,
                "N2OInTons": 0.006281644444444446,
                "NMVOCInTons": 0.12092165555555556,
                "NOxInTons": 3.6441389833333337,
                "SOxInTons": 1.9189049668055556,
                "PMInTons": 0.2734245791243902
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
    }, {
        "ID": "I8FE002VED1F08900",
        "IMO": 9428994,
        "VesselName": "SKS Dee",
        "VoyageNumber": 53,
        "VesselTypeID": 1,
        "VesselType": "Tanker",
        "VesselClassID": 86,
        "VesselClass": "Aframax",
        "StartDate": "2018-01-17T23:56:25",
        "EndDate": "2018-05-03T15:07:03",
        "Quantity": 90000.0,
        "Deadweight": 119456,
        "ContainsEuEmissions": False,
        "TransportWorkInMillionTonneMiles": 1726.4124,
        "TransportWorkInMillionDwtMiles": 2291.44799616,
        "Emissions": {
            "Voyage": {
                "CO2InTons": 8363.505735803703,
                "COInTons": 7.437847581420064,
                "CH4InTons": 0.1611086118719148,
                "N2OInTons": 0.4295252878914624,
                "NMVOCInTons": 8.270242076091627,
                "NOxInTons": 249.18061642097922,
                "SOxInTons": 130.78210278246783,
                "PMInTons": 18.641579700924957
            },
            "Ballast": {
                "CO2InTons": 510.0514108534562,
                "COInTons": 0.4536483457693532,
                "CH4InTons": 0.009826317958902958,
                "N2OInTons": 0.026203514557074554,
                "NMVOCInTons": 0.5044176552236852,
                "NOxInTons": 15.201313882422875,
                "SOxInTons": 8.004600495305342,
                "PMInTons": 1.14057473368848
            },
            "Laden": {
                "CO2InTons": 6908.1759625058,
                "COInTons": 6.143452682872935,
                "CH4InTons": 0.13307117724634518,
                "N2OInTons": 0.35475879555661,
                "NMVOCInTons": 6.830987098645719,
                "NOxInTons": 205.80670505522298,
                "SOxInTons": 107.94257489119026,
                "PMInTons": 15.38717762833648
            },
            "PortCall": {
                "CO2InTons": 700.7399999999999,
                "COInTons": 0.62325,
                "CH4InTons": 0.013500000000000002,
                "N2OInTons": 0.036000000000000004,
                "NMVOCInTons": 0.693,
                "NOxInTons": 20.8845,
                "SOxInTons": 10.9972125,
                "PMInTons": 1.566991722555
            },
            "Stop": {
                "CO2InTons": 244.53836244444443,
                "COInTons": 0.21749655277777774,
                "CH4InTons": 0.004711116666666666,
                "N2OInTons": 0.012562977777777777,
                "NMVOCInTons": 0.24183732222222215,
                "NOxInTons": 7.288097483333333,
                "SOxInTons": 3.837714895972223,
                "PMInTons": 0.5468356163450052
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
    ]
}

__mock_emissions_vessel_class_one_arg = VesselClassEmissions(
    next_page_token="eyJ2ZXNzZWxfY2xhc3NfaWQiOiA4NiwgImxhc3RfaWQiOiAiNjI1ZjUyZTlkMzMwZDA2MTBjOWFkZTEwIn0=",
    data=[
        EmissionsEstimation(
            id='I8FE002VED1BBCD00',
            imo=9428994,
            vessel_name='SKS Dee',
            voyage_number=52,
            vessel_type_id=1,
            vessel_type='Tanker',
            vessel_class_id=86,
            vessel_class='Aframax',
            start_date='2017-12-14T03:23:33',
            end_date='2018-01-17T23:56:25',
            quantity=75000.0,
            deadweight=119456,
            contains_eu_emissions=False,
            transport_work_in_million_tonne_miles=435.21824999999995,
            transport_work_in_million_dwt_miles=693.19241696,
            emissions=EmissionsBreakdown(
                voyage=Emissions(
                    co2_in_tons=2340.277087625018,
                    coin_tons=2.081481997406017,
                    ch4_in_tons=0.045086252651393884,
                    n2_oin_tons=0.12023000707038368,
                    nmvocin_tons=2.3144276361048854,
                    nox_in_tons=69.74843285170633,
                    sox_in_tons=36.72763712859755,
                    pmin_tons=5.233317385611677,
                ),
                ballast=Emissions(
                    co2_in_tons=901.9591243208984,
                    coin_tons=0.8022176902032135,
                    ch4_in_tons=0.0173765564664956,
                    n2_oin_tons=0.04633748391065494,
                    nmvocin_tons=0.8919965652801074,
                    nox_in_tons=26.881532853668695,
                    sox_in_tons=14.155087702244538,
                    pmin_tons=2.016957048111716,
                ),
                laden=Emissions(
                    co2_in_tons=1066.8937541930086,
                    coin_tons=0.9489133377583592,
                    ch4_in_tons=0.02055407951823161,
                    n2_oin_tons=0.05481087871528429,
                    nmvocin_tons=1.0551094152692224,
                    nox_in_tons=31.797161014704297,
                    sox_in_tons=16.743524459547455,
                    pmin_tons=2.38578314591157,
                ),
                port_call=Emissions(
                    co2_in_tons=249.152,
                    coin_tons=0.2216,
                    ch4_in_tons=0.0048000000000000004,
                    n2_oin_tons=0.012800000000000002,
                    nmvocin_tons=0.24639999999999998,
                    nox_in_tons=7.425599999999999,
                    sox_in_tons=3.91012,
                    pmin_tons=0.557152612464,
                ),
                stop=Emissions(
                    co2_in_tons=122.27220911111111,
                    coin_tons=0.10875096944444444,
                    ch4_in_tons=0.002355616666666667,
                    n2_oin_tons=0.006281644444444446,
                    nmvocin_tons=0.12092165555555556,
                    nox_in_tons=3.6441389833333337,
                    sox_in_tons=1.9189049668055556,
                    pmin_tons=0.2734245791243902,
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
        ),
        EmissionsEstimation(
            id='I8FE002VED1F08900',
            imo=9428994,
            vessel_name='SKS Dee',
            voyage_number=53,
            vessel_type_id=1,
            vessel_type='Tanker',
            vessel_class_id=86,
            vessel_class='Aframax',
            start_date='2018-01-17T23:56:25',
            end_date='2018-05-03T15:07:03',
            quantity=90000.0,
            deadweight=119456,
            contains_eu_emissions=False,
            transport_work_in_million_tonne_miles=1726.4124,
            transport_work_in_million_dwt_miles=2291.44799616,
            emissions=EmissionsBreakdown(
                voyage=Emissions(
                    co2_in_tons=8363.505735803703,
                    coin_tons=7.437847581420064,
                    ch4_in_tons=0.1611086118719148,
                    n2_oin_tons=0.4295252878914624,
                    nmvocin_tons=8.270242076091627,
                    nox_in_tons=249.18061642097922,
                    sox_in_tons=130.78210278246783,
                    pmin_tons=18.641579700924957,
                ),
                ballast=Emissions(
                    co2_in_tons=510.0514108534562,
                    coin_tons=0.4536483457693532,
                    ch4_in_tons=0.009826317958902958,
                    n2_oin_tons=0.026203514557074554,
                    nmvocin_tons=0.5044176552236852,
                    nox_in_tons=15.201313882422875,
                    sox_in_tons=8.004600495305342,
                    pmin_tons=1.14057473368848,
                ),
                laden=Emissions(
                    co2_in_tons=6908.1759625058,
                    coin_tons=6.143452682872935,
                    ch4_in_tons=0.13307117724634518,
                    n2_oin_tons=0.35475879555661,
                    nmvocin_tons=6.830987098645719,
                    nox_in_tons=205.80670505522298,
                    sox_in_tons=107.94257489119026,
                    pmin_tons=15.38717762833648,
                ),
                port_call=Emissions(
                    co2_in_tons=700.7399999999999,
                    coin_tons=0.62325,
                    ch4_in_tons=0.013500000000000002,
                    n2_oin_tons=0.036000000000000004,
                    nmvocin_tons=0.693,
                    nox_in_tons=20.8845,
                    sox_in_tons=10.9972125,
                    pmin_tons=1.566991722555,
                ),
                stop=Emissions(
                    co2_in_tons=244.53836244444443,
                    coin_tons=0.21749655277777774,
                    ch4_in_tons=0.004711116666666666,
                    n2_oin_tons=0.012562977777777777,
                    nmvocin_tons=0.24183732222222215,
                    nox_in_tons=7.288097483333333,
                    sox_in_tons=3.837714895972223,
                    pmin_tons=0.5468356163450052,
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
    ]
)


__mock_emissions_response_vessel_class_all_args = {
    "NextPageToken": "eyJ2ZXNzZWxfY2xhc3NfaWQiOiA4NiwgImxhc3RfaWQiOiAiNjI1ZjUyZTlkMzMwZDA2MTBjOWFkZTEwIn0=",
    "Data": __mock_emissions_response_imo_all_args
}

__mock_emissions_vessel_class_all_args = VesselClassEmissions(
    next_page_token="eyJ2ZXNzZWxfY2xhc3NfaWQiOiA4NiwgImxhc3RfaWQiOiAiNjI1ZjUyZTlkMzMwZDA2MTBjOWFkZTEwIn0=",
    data=__mock_emissions_imo_all_args
)


__mock_vessel_class_metrics_response_1 = {
    "NextPageToken": "eyJ2ZXNzZWxfY2xhc3NfaWQiOiA4NiwgImxhc3RfaWQiOiAiNjI3MjQwYjQyZmUzMjg2N2MwZTk3NDkyIn0=",
    "Data": [{
        "IMO": 7370868,
        "Year": 2018,
        "VesselType": "Tanker",
        "VesselTypeID": 1,
        "VesselClass": "Aframax",
        "VesselClassID": 86,
        "Aer": {
            "Value": 104.93873496233248,
            "Unit": "g-CO2/dwt mile",
            "PoseidonPrinciplesClass": "Oil Tanker 120000-199999 DWT",
            "PoseidonPrinciplesAlignmentInPercentage": 3032.499551114402,
            "PoseidonPrinciplesYearTarget": 3.35
        },
        "Cii": {
            "Value": 104.93873496233248,
            "Unit": "g-CO2/capacity mile",
            "Rating": "E",
            "Target": 4.155390768552234,
            "TargetYear": 2018
        }
    }, {
        "IMO": 7370868,
        "Year": 2019,
        "VesselType": "Tanker",
        "VesselTypeID": 1,
        "VesselClass": "Aframax",
        "VesselClassID": 86,
        "Aer": {
            "Value": 104.93873496233248,
            "Unit": "g-CO2/dwt mile",
            "PoseidonPrinciplesClass": "Oil Tanker 120000-199999 DWT",
            "PoseidonPrinciplesAlignmentInPercentage": 3109.135625759403,
            "PoseidonPrinciplesYearTarget": 3.27
        },
        "Cii": {
            "Value": 104.93873496233248,
            "Unit": "g-CO2/capacity mile",
            "Rating": "E",
            "Target": 4.155390768552234,
            "TargetYear": 2019
        }
    }
    ]
}

__mock_vessel_class_metrics_1 = VesselClassMetrics(
    next_page_token="eyJ2ZXNzZWxfY2xhc3NfaWQiOiA4NiwgImxhc3RfaWQiOiAiNjI3MjQwYjQyZmUzMjg2N2MwZTk3NDkyIn0=",
    data=[
        VesselMetrics(
            imo=7370868,
            year=2018,
            vessel_type="Tanker",
            vessel_type_id=1,
            vessel_class="Aframax",
            vessel_class_id=86,
            aer=Aer(
                value=104.93873496233248,
                unit="g-CO2/dwt mile",
                poseidon_principles_class="Oil Tanker 120000-199999 DWT",
                poseidon_principles_alignment_in_percentage=3032.499551114402,
                poseidon_principles_year_target=3.35
            ),
            cii=Cii(
                value=104.93873496233248,
                unit="g-CO2/capacity mile",
                rating="E",
                target=4.155390768552234,
                target_year=2018
            )
        ),
        VesselMetrics(
            imo=7370868,
            year=2019,
            vessel_type="Tanker",
            vessel_type_id=1,
            vessel_class="Aframax",
            vessel_class_id=86,
            aer=Aer(
                value=104.93873496233248,
                unit="g-CO2/dwt mile",
                poseidon_principles_class="Oil Tanker 120000-199999 DWT",
                poseidon_principles_alignment_in_percentage=3109.135625759403,
                poseidon_principles_year_target=3.27
            ),
            cii=Cii(
                value=104.93873496233248,
                unit="g-CO2/capacity mile",
                rating="E",
                target=4.155390768552234,
                target_year=2019
            )
        )
    ]
)
