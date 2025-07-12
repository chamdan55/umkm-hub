"""Sales dashboard components."""

from typing import Dict, Any, List
import reflex as rx

from ..components.card import card
from ..components.notification import notification
from ..states.sales_dashboard import SalesDashboardState


def stats_card(title: str, value: str, icon: str, color: str = "blue") -> rx.Component:
    """Create a stats card component."""
    return card(
        rx.hstack(
            rx.icon(icon, size=24, color=f"var(--{color}-9)"),
            rx.vstack(
                rx.text(title, size="2", color="var(--gray-11)"),
                rx.text(value, size="4", weight="bold", color="var(--gray-12)"),
                align="start",
                spacing="1",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        style={"padding": "1rem"},
    )


def sales_filters() -> rx.Component:
    """Create the sales filters section."""
    return rx.hstack(
        rx.vstack(
            rx.text("Product", size="2", weight="bold"),
            rx.select(
                SalesDashboardState.product_options,
                value=SalesDashboardState.selected_product,
                on_change=SalesDashboardState.set_selected_product,
                placeholder="Select product...",
                width="200px",
            ),
            spacing="1",
            align="start",
        ),
        rx.vstack(
            rx.text("Period", size="2", weight="bold"),
            rx.select(
                ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
                value=SalesDashboardState.selected_period,
                on_change=SalesDashboardState.set_selected_period,
                placeholder="Select period...",
                width="200px",
            ),
            spacing="1",
            align="start",
        ),
        spacing="6",
        align="start",
    )


def daily_revenue_chart() -> rx.Component:
    """Create the daily revenue line chart."""
    return rx.vstack(
        rx.heading("Daily Revenue", size="4"),
        rx.recharts.line_chart(
            rx.recharts.line(
                data_key="revenue",
                stroke="#8884d8",
                stroke_width=2,
                dot={"fill": "#8884d8", "stroke": "#8884d8", "strokeWidth": 2, "r": 4},
                active_dot={"r": 6, "fill": "#8884d8"},
            ),
            rx.recharts.x_axis(
                data_key="date",
                tick_formatter=rx.Var.create("(value) => new Date(value).toLocaleDateString()"),
                angle=-45,
                text_anchor="end",
            ),
            rx.recharts.y_axis(
                tick_formatter=rx.Var.create("(value) => 'Rp ' + value.toLocaleString()"),
            ),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.tooltip(
                formatter=rx.Var.create("(value, name) => ['Rp ' + value.toLocaleString(), 'Revenue']"),
                label_formatter=rx.Var.create("(value) => new Date(value).toLocaleDateString()"),
            ),
            rx.recharts.legend(),
            data=SalesDashboardState.daily_revenue_data,
            width="100%",
            height=400,
        ),
        spacing="4",
        align="start",
        width="100%",
    )


def product_sales_chart() -> rx.Component:
    """Create the product sales pie chart."""
    return rx.vstack(
        rx.heading("Sales by Product", size="4"),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=SalesDashboardState.product_sales_data,
                data_key="revenue",
                name_key="product",
                cx="50%",
                cy="50%",
                outer_radius=150,
                fill="#8884d8",
                label=True,
            ),
            rx.recharts.tooltip(
                formatter=rx.Var.create("(value, name) => ['Rp ' + value.toLocaleString(), 'Revenue']"),
            ),
            rx.recharts.legend(),
            width="100%",
            height=400,
        ),
        spacing="4",
        align="start",
        width="100%",
    )


def top_products_table() -> rx.Component:
    """Create the top products table."""
    return rx.vstack(
        rx.heading("Top Products", size="4"),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Product"),
                    rx.table.column_header_cell("Revenue"),
                    rx.table.column_header_cell("Quantity"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    SalesDashboardState.formatted_top_products,
                    lambda item: rx.table.row(
                        rx.table.cell(item["product"]),
                        rx.table.cell(item["revenue"]),
                        rx.table.cell(item["quantity"]),
                    ),
                ),
            ),
            variant="surface",
            size="1",
            width="100%",
        ),
        spacing="4",
        align="start",
        width="100%",
    )


def quick_insights() -> rx.Component:
    """Create the quick insights section."""
    return rx.vstack(
        rx.heading("Quick Insights", size="4"),
        rx.vstack(
            rx.hstack(
                rx.icon("trending-up", size=16, color="var(--green-9)"),
                rx.text(
                    f"Revenue Growth: {SalesDashboardState.revenue_growth:.1f}%",
                    size="2",
                    weight="medium",
                ),
                align="center",
                spacing="2",
            ),
            rx.hstack(
                rx.icon("shopping-cart", size=16, color="var(--blue-9)"),
                rx.text(
                    f"Orders Growth: {SalesDashboardState.orders_growth:.1f}%",
                    size="2",
                    weight="medium",
                ),
                align="center",
                spacing="2",
            ),
            spacing="3",
            align="start",
        ),
        spacing="4",
        align="start",
        width="100%",
    )


def sales_dashboard_content() -> rx.Component:
    """Main sales dashboard content."""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading("Sales Dashboard", size="6"),
            rx.button(
                "Refresh Data",
                on_click=SalesDashboardState.load_data,
                variant="outline",
                size="2",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        
        # Filters
        card(
            rx.vstack(
                rx.heading("Filters", size="4"),
                sales_filters(),
                spacing="4",
                align="start",
                width="100%",
            ),
            style={"padding": "1.5rem"},
        ),
        
        # Stats Cards
        rx.grid(
            stats_card(
                "Total Revenue",
                f"Rp {SalesDashboardState.total_revenue:,.0f}",
                "dollar-sign",
                "green",
            ),
            stats_card(
                "Total Orders",
                f"{SalesDashboardState.total_orders:,}",
                "shopping-cart",
                "blue",
            ),
            stats_card(
                "Average Order Value",
                f"Rp {SalesDashboardState.average_order_value:,.0f}",
                "trending-up",
                "purple",
            ),
            stats_card(
                "Items Sold",
                f"{SalesDashboardState.items_sold:,}",
                "package",
                "orange",
            ),
            columns="4",
            spacing="4",
            width="100%",
        ),
        
        # Charts Section
        rx.grid(
            card(
                daily_revenue_chart(),
                style={"padding": "1.5rem"},
            ),
            card(
                product_sales_chart(),
                style={"padding": "1.5rem"},
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),
        
        # Bottom Section
        rx.grid(
            card(
                top_products_table(),
                style={"padding": "1.5rem"},
            ),
            card(
                quick_insights(),
                style={"padding": "1.5rem"},
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),
        
        spacing="6",
        align="start",
        width="100%",
        padding="2rem",
    )
