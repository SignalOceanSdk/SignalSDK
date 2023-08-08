from signal_ocean.vessel_valuations.models import Valuation, HistoricalValuation, PageValuations

__mock_valuation_imo = {
    "imo": 9414254,
    "valuationPrice": 20.382829,
    "scrapPrice": 4.637992,
    "updatedDate": "2023-07-31T13:00:04.67"
}

__mock_valuation_imo_response = Valuation(
    imo=9414254,
    valuation_price=20.382829,
    scrap_price=4.637992,
    updated_date="2023-07-31T13:00:04.67"
)

__mock_historical_valuations_no_args = [{
    "imo": 9414254,
    "valueFrom": "2016-01-01T00:00:00",
    "valuationPrice": 21.670405,
    "scrapPrice": 2.372692
}, {
    "imo": 9414254,
    "valueFrom": "2016-01-08T00:00:00",
    "valuationPrice": 21.642829,
    "scrapPrice": 2.372692
}, {
    "imo": 9414254,
    "valueFrom": "2016-01-15T00:00:00",
    "valuationPrice": 21.615253,
    "scrapPrice": 2.372692
}
    ]

__mock_response_historical_valuations_no_args = [
    HistoricalValuation(
        imo=9414254,
        value_from="2016-01-01T00:00:00",
        valuation_price=21.670405,
        scrap_price=2.372692
    ),
    HistoricalValuation(
        imo=9414254,
        value_from="2016-01-08T00:00:00",
        valuation_price=21.642829,
        scrap_price=2.372692
    ),
    HistoricalValuation(
        imo=9414254,
        value_from="2016-01-15T00:00:00",
        valuation_price=21.615253,
        scrap_price=2.372692
    ),
]

__mock_valuation_page = {
    "page": 1,
    "pageSize": 100,
    "total": 20820,
    "valuations": [{
        "imo": 5024738,
        "valuationPrice": 3.178215,
        "scrapPrice": 3.178215,
        "updatedDate": "2023-07-31T13:00:04.67"
    }
    ]
}

__mock_response_valuation_page = PageValuations(
    page=1,
    page_size=100,
    total=20820,
    valuations=[
        Valuation(
            imo=5024738,
            valuation_price=3.178215,
            scrap_price=3.178215,
            updated_date="2023-07-31T13:00:04.67"
        )
    ]
)

__mock_valuations_list = {
    "imo": 9180803,
    "valuationPrice": 10.514177,
    "scrapPrice": 5.947302,
    "updatedDate": "2023-07-31T13:00:04.67"
}


__mock_response_valuations_list = [Valuation(
        imo=9180803,
        valuation_price=10.514177,
        scrap_price=5.947302,
        updated_date="2023-07-31T13:00:04.67"
    )]
