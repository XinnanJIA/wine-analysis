import streamlit as sl
import plotly.graph_objects as go
from millify import millify


def plot_metric(
    label, value, series, prefix="", suffix="", show_graph=False, color_graph=""
):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 28,
                "font.color": "white",
            },
            title={
                "text": label,
                "font": {"size": 24, "color": "white"},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=series,
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        # plot_bgcolor="black",
        height=100,
    )

    sl.plotly_chart(fig, use_container_width=True)
