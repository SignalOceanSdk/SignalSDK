from signal_ocean.tonnage_list import MarketDeployment


def test_can_list_available_market_deployments() -> None:
    market_deployments = list(MarketDeployment)

    assert market_deployments == ["Spot", "Program", "Relet", "Contract"]
