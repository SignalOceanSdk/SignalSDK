# noqa: D100

import pandas as pd

from typing import Tuple

from .models import FreightPricing
from .._internals import snake_to_camel_case


def create_dataframe(
        api_response: Tuple[FreightPricing, ...]
) -> pd.DataFrame:
    """Create dataframe from Freight Rates API's response.

    Args:
        api_response: Data from Freight Rates API which we want
        to convert to dataframe.

    Returns:
        Dataframe populated with data from Freight Rates API's response
    """
    response_dict = vars(api_response[0])
    response_dict['freight_cost'] = response_dict['costs'].freight_cost
    response_dict['canal_costs'] = response_dict['costs'].canal
    response_dict['other_port_expenses'] = \
        response_dict['costs'].other_port_expenses
    response_dict['load_ports'] = [lp.name for lp in
                                   response_dict['load_ports']]
    response_dict['discharge_ports'] = [dp.name for dp in
                                        response_dict['discharge_ports']]
    response_dict.pop('costs')
    df = pd.DataFrame([response_dict])
    for column_name, _ in df.items():
        df = df.rename(
            columns={column_name: snake_to_camel_case(str(column_name))})
    return df
