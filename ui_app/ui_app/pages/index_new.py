"""The overview page of the app."""

import reflex as rx

from ..components.sales_dashboard import sales_dashboard_content
from ..states.sales_dashboard import SalesDashboardState
from ..templates.template import template


@template(route="/", title="Sales Dashboard - Overview")
def index() -> rx.Component:
    """The overview page with sales dashboard."""
    return sales_dashboard_content()


@rx.page(route="/", title="Sales Dashboard - Overview", on_load=SalesDashboardState.load_data)
def index_page() -> rx.Component:
    """The overview page with sales dashboard."""
    return index()
