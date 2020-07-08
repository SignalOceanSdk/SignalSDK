from signal_ocean.historical_tonnage_list import MarketDeployment


def test_can_list_available_market_deployments():
    market_deployments = list(MarketDeployment)

    assert market_deployments == ['Spot', 'Program', 'Relet', 'Contract']
