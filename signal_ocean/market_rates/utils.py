# noqa: D100

import pandas as pd

from typing import Tuple, Union

from .models import MarketRate, Route, VesselClass
from .._internals import snake_to_camel_case


def create_dataframe(
        api_response: Tuple[Union[MarketRate, Route, VesselClass], ...]
) -> pd.DataFrame:
    """Create dataframe from Market Rates API's response.

    Args:
        api_response: Data from Market Rates API which we want
        to convert to dataframe.

    Returns:
        Dataframe populated with data from Market Rates API's response
    """
    df = pd.DataFrame([vars(x) for x in api_response])
    for column_name, _ in df.iteritems():
        df = df.rename(
            columns={column_name: snake_to_camel_case(str(column_name))})
    return df
