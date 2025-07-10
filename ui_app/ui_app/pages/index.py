"""The overview page of the app."""

import datetime

import reflex as rx

from .. import styles
from ..components.card import card
from ..components.notification import notification
from ..templates import template
from ..views.acquisition_view import acquisition
from ..views.charts import (
    StatsState,
    area_toggle,
    orders_chart,
    pie_chart,
    revenue_chart,
    timeframe_select,
    users_chart,
)
from ..views.stats_cards import stats_cards
from .profile import ProfileState


def _time_data() -> rx.Component:
    return rx.hstack(
        rx.tooltip(
            rx.icon("info", size=20),
            content=f"{(datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%b %d, %Y')} - {datetime.datetime.now().strftime('%b %d, %Y')}",
        ),
        rx.text("Last 30 days", size="4", weight="medium"),
        align="center",
        spacing="2",
        display=["none", "none", "flex"],
    )


def tab_content_header() -> rx.Component:
    return rx.hstack(
        _time_data(),
        area_toggle(),
        align="center",
        width="100%",
        spacing="4",
    )


@template(route="/", title="Overview")
def index() -> rx.Component:
    """The overview page.

    Returns:
        The overview page component.

    """
    return rx.vstack(
        rx.flex(
            stats_cards(),
            spacing="3",
            flex_direction=["column", "column", "row"],
            width="100%",
        ),
        rx.flex(
            card(
                rx.vstack(
                    tab_content_header(),
                    revenue_chart(),
                    spacing="4",
                ),
                padding="0px",
            ),
            card(pie_chart()),
            spacing="3",
            flex_direction=["column", "column", "column", "row"],
            width="100%",
        ),
        rx.flex(
            card(users_chart()),
            card(orders_chart()),
            spacing="3",
            flex_direction=["column", "column", "column", "row"],
            width="100%",
        ),
        acquisition(),
        notification(icon="bell", color="blue", count=2),
        spacing="8",
        width="100%",
    )
