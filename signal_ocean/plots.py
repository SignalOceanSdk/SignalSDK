# noqa: D100

import pandas as pd
import plotly.express as px  # type: ignore
import plotly.figure_factory as ff  # type: ignore

from typing import Optional, Any, Dict


def styled_table(dataframe: pd.DataFrame,
                 font_family: Optional[str] = 'Calibri',
                 font_size: Optional[int] = 14,
                 table_width: Optional[int] = 900) -> Any:
    """Function to style dataframe table.

    Args:
        dataframe: The dataframe we want to style.
        font_family: Selected font family for the returned table.
        font_size: Selected font size for the returned table.
        table_width: Selected width for the returned table.

    Returns:
        A table graph presenting the given dataframe.
    """
    table = ff.create_table(dataframe, index=True)
    for i in range(len(table.layout.annotations)):
        table.layout.annotations[i].font.family = font_family
        table.layout.annotations[i].font.size = font_size
    table.layout.width = table_width
    return table.show()


def line_chart(dataframe: pd.DataFrame, x_axis_variable: str,
               y_axis_variable: str, line_filter: Optional[str] = None,
               hoverlabel: Optional[Dict[str, Any]] = dict(
                   bgcolor="blue", font_size=14, font_family="Calibri"
               ),
               chart_width: Optional[int] = 1000) -> Any:
    """Function to create line chart from dataframe.

    Args:
        dataframe: The given dataframe we want to create line chart from.
        x_axis_variable: The name of the column used as x-axis
        variable in the graph.
        y_axis_variable: The name of the column used as y-axis
        variable in the graph.
        line_filter: The name of the column used as line filter, in
        case of multiple line charts.
        hoverlabel: Style of the chart's hoverlabel.
        chart_width: Width of the chart.

    Returns:
        Line chart which displays information as a series of data points
        connected by straight line segments.
    """
    chart = px.line(dataframe, x=x_axis_variable, y=y_axis_variable,
                    color=line_filter, hover_data=dataframe.columns,
                    width=chart_width)
    chart.update_layout(
        hoverlabel=hoverlabel
    )
    return chart.show()
