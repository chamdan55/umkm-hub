"""Sales dashboard components."""

from typing import Dict, Any, List
import reflex as rx

from ..components.card import card
from ..components.notification import notification
from ..states.sales_dashboard import SalesDashboardState


def stats_card(title: str, value: str, icon: str, color: str = "blue") -> rx.Component:
    """Create a stats card component with enhanced styling."""
    color_schemes = {
        "green": {
            "bg": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
            "icon_bg": "rgba(16, 185, 129, 0.1)",
            "text": "#ffffff"
        },
        "blue": {
            "bg": "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
            "icon_bg": "rgba(59, 130, 246, 0.1)",
            "text": "#ffffff"
        },
        "purple": {
            "bg": "linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)",
            "icon_bg": "rgba(139, 92, 246, 0.1)",
            "text": "#ffffff"
        },
        "orange": {
            "bg": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
            "icon_bg": "rgba(245, 158, 11, 0.1)",
            "text": "#ffffff"
        }
    }
    
    scheme = color_schemes.get(color, color_schemes["blue"])
    
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon(icon, size=28, color=scheme["text"]),
                padding="12px",
                border_radius="12px",
                background=scheme["icon_bg"],
                backdrop_filter="blur(10px)",
            ),
            rx.vstack(
                rx.text(title, size="2", color=scheme["text"], opacity="0.9", weight="medium"),
                rx.text(value, size="5", weight="bold", color=scheme["text"]),
                align="start",
                spacing="1",
                flex="1",
            ),
            justify="between",
            align="center",
            width="100%",
            padding="20px",
        ),
        background=scheme["bg"],
        border_radius="16px",
        box_shadow="0 4px 20px rgba(0,0,0,0.1)",
        border="1px solid rgba(255,255,255,0.1)",
        transition="all 0.3s ease",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": "0 8px 30px rgba(0,0,0,0.15)"
        },
        width="100%",
        min_height="120px",
    )


def sales_filters() -> rx.Component:
    """Create the sales filters section with enhanced styling."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.icon("filter", size=18, color="var(--blue-9)"),
                    rx.text("Filter by Product", size="3", weight="bold", color="var(--gray-12)"),
                    align="center",
                    spacing="2",
                ),
                rx.select(
                    SalesDashboardState.product_options,
                    value=SalesDashboardState.selected_product,
                    on_change=SalesDashboardState.set_selected_product,
                    placeholder="Select product...",
                    width="250px",
                    size="3",
                ),
                spacing="2",
                align="start",
            ),
            rx.vstack(
                rx.hstack(
                    rx.icon("calendar", size=18, color="var(--purple-9)"),
                    rx.text("Filter by Period", size="3", weight="bold", color="var(--gray-12)"),
                    align="center",
                    spacing="2",
                ),
                rx.select(
                    ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
                    value=SalesDashboardState.selected_period,
                    on_change=SalesDashboardState.set_selected_period,
                    placeholder="Select period...",
                    width="250px",
                    size="3",
                ),
                spacing="2",
                align="start",
            ),
            spacing="8",
            align="start",
            width="100%",
        ),
        background="linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
        border_radius="16px",
        padding="24px",
        border="1px solid var(--gray-6)",
        box_shadow="0 2px 10px rgba(0,0,0,0.05)",
    )


def daily_revenue_chart() -> rx.Component:
    """Create the daily revenue line chart with enhanced styling."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("trending-up", size=20, color="var(--blue-9)"),
                rx.heading("Daily Revenue Trend", size="4", color="var(--gray-12)"),
                align="center",
                spacing="2",
            ),
            rx.recharts.line_chart(
                rx.recharts.line(
                    data_key="revenue",
                    stroke="#3b82f6",
                    stroke_width=3,
                    dot={"fill": "#3b82f6", "stroke": "#ffffff", "strokeWidth": 2, "r": 5},
                    active_dot={"r": 7, "fill": "#1d4ed8", "stroke": "#ffffff", "strokeWidth": 2},
                ),
                rx.recharts.x_axis(
                    data_key="date",
                    tick_formatter=rx.Var.create("(value) => new Date(value).toLocaleDateString()"),
                    angle=-45,
                    text_anchor="end",
                    tick={"fontSize": 12, "fill": "#64748b"},
                ),
                rx.recharts.y_axis(
                    tick_formatter=rx.Var.create("(value) => 'Rp ' + value.toLocaleString()"),
                    tick={"fontSize": 12, "fill": "#64748b"},
                ),
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    stroke="#e2e8f0",
                    opacity=0.6,
                ),
                rx.recharts.tooltip(
                    formatter=rx.Var.create("(value, name) => ['Rp ' + value.toLocaleString(), 'Revenue']"),
                    label_formatter=rx.Var.create("(value) => new Date(value).toLocaleDateString()"),
                    content_style={
                        "backgroundColor": "#ffffff",
                        "border": "1px solid #e2e8f0",
                        "borderRadius": "8px",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.1)"
                    },
                ),
                data=SalesDashboardState.daily_revenue_data,
                width="100%",
                height=400,
                margin={"top": 20, "right": 30, "left": 20, "bottom": 60},
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        background="linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
        border_radius="16px",
        padding="24px",
        border="1px solid var(--gray-6)",
        box_shadow="0 4px 20px rgba(0,0,0,0.08)",
        width="100%",
    )


def product_sales_chart() -> rx.Component:
    """Create the product sales pie chart with enhanced styling."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("pie-chart", size=20, color="var(--purple-9)"),
                rx.heading("Sales Volume by Product", size="4", color="var(--gray-12)"),
                align="center",
                spacing="2",
            ),
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    data=SalesDashboardState.product_sales_data,
                    data_key="quantity",
                    name_key="product",
                    cx="50%",
                    cy="50%",
                    outer_radius=140,
                    inner_radius=50,
                    fill="#8884d8",
                    label=True,
                    label_line=False,
                    stroke="#ffffff",
                    stroke_width=2,
                ),
                rx.recharts.tooltip(
                    formatter=rx.Var.create("(value, name) => [value.toLocaleString() + ' units', 'Quantity Sold']"),
                    content_style={
                        "backgroundColor": "#ffffff",
                        "border": "1px solid #e2e8f0",
                        "borderRadius": "8px",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.1)"
                    },
                ),
                width="100%",
                height=400,
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        background="linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
        border_radius="16px",
        padding="24px",
        border="1px solid var(--gray-6)",
        box_shadow="0 4px 20px rgba(0,0,0,0.08)",
    )


def top_products_table() -> rx.Component:
    """Create the top products table with enhanced styling."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("crown", size=20, color="var(--orange-9)"),
                rx.heading("Top Performing Products", size="4", color="var(--gray-12)"),
                align="center",
                spacing="2",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell(
                            "Rank",
                            style={"background": "var(--gray-2)", "font_weight": "600", "color": "var(--gray-12)", "width": "60px"}
                        ),
                        rx.table.column_header_cell(
                            "Product",
                            style={"background": "var(--gray-2)", "font_weight": "600", "color": "var(--gray-12)"}
                        ),
                        rx.table.column_header_cell(
                            "Revenue",
                            style={"background": "var(--gray-2)", "font_weight": "600", "color": "var(--gray-12)"}
                        ),
                        rx.table.column_header_cell(
                            "Quantity",
                            style={"background": "var(--gray-2)", "font_weight": "600", "color": "var(--gray-12)"}
                        ),
                        style={"border_bottom": "2px solid var(--gray-6)"}
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        SalesDashboardState.formatted_top_products_with_rank,
                        lambda item: rx.table.row(
                            rx.table.cell(
                                rx.box(
                                    rx.text(item["rank"], size="2", weight="bold", color="white"),
                                    background=rx.cond(
                                        item["rank"] == "1",
                                        "var(--yellow-9)",
                                        rx.cond(
                                            item["rank"] == "2",
                                            "var(--gray-9)",
                                            rx.cond(
                                                item["rank"] == "3",
                                                "var(--orange-9)",
                                                "var(--blue-9)"
                                            )
                                        )
                                    ),
                                    border_radius="50%",
                                    width="28px",
                                    height="28px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                ),
                                padding="12px",
                                text_align="center",
                            ),
                            rx.table.cell(
                                rx.text(item["product"], weight="medium", color="var(--gray-12)"),
                                padding="12px",
                            ),
                            rx.table.cell(
                                rx.text(item["revenue"], weight="bold", color="var(--green-9)"),
                                padding="12px",
                            ),
                            rx.table.cell(
                                rx.text(item["quantity"], color="var(--gray-11)"),
                                padding="12px",
                            ),
                            style={
                                "border_bottom": "1px solid var(--gray-4)",
                                "_hover": {"background": "var(--gray-1)"}
                            }
                        ),
                    ),
                ),
                variant="surface",
                size="2",
                width="100%",
                style={"border_radius": "12px", "overflow": "hidden"}
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        background="linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
        border_radius="16px",
        padding="24px",
        border="1px solid var(--gray-6)",
        box_shadow="0 4px 20px rgba(0,0,0,0.08)",
    )


def quick_insights() -> rx.Component:
    """Create the quick insights section with enhanced styling - full width horizontal layout."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("zap", size=20, color="var(--yellow-9)"),
                rx.heading("Quick Insights", size="4", color="var(--gray-12)"),
                align="center",
                spacing="2",
            ),
            rx.hstack(
                rx.box(
                    rx.hstack(
                        rx.box(
                            rx.icon("trending-up", size=18, color="white"),
                            background="linear-gradient(135deg, #10b981 0%, #059669 100%)",
                            border_radius="10px",
                            padding="8px",
                        ),
                        rx.vstack(
                            rx.text("Revenue Growth", size="2", color="var(--gray-11)", weight="medium"),
                            rx.text(
                                f"{SalesDashboardState.revenue_growth:.1f}%",
                                size="4",
                                weight="bold",
                                color=rx.cond(
                                    SalesDashboardState.revenue_growth >= 0,
                                    "var(--green-9)",
                                    "var(--red-9)"
                                ),
                            ),
                            align="start",
                            spacing="1",
                        ),
                        align="center",
                        spacing="3",
                    ),
                    background="rgba(16, 185, 129, 0.05)",
                    border_radius="12px",
                    padding="16px",
                    border="1px solid rgba(16, 185, 129, 0.1)",
                    flex="1",
                ),
                rx.box(
                    rx.hstack(
                        rx.box(
                            rx.icon("shopping-cart", size=18, color="white"),
                            background="linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
                            border_radius="10px",
                            padding="8px",
                        ),
                        rx.vstack(
                            rx.text("Orders Growth", size="2", color="var(--gray-11)", weight="medium"),
                            rx.text(
                                f"{SalesDashboardState.orders_growth:.1f}%",
                                size="4",
                                weight="bold",
                                color=rx.cond(
                                    SalesDashboardState.orders_growth >= 0,
                                    "var(--green-9)",
                                    "var(--red-9)"
                                ),
                            ),
                            align="start",
                            spacing="1",
                        ),
                        align="center",
                        spacing="3",
                    ),
                    background="rgba(59, 130, 246, 0.05)",
                    border_radius="12px",
                    padding="16px",
                    border="1px solid rgba(59, 130, 246, 0.1)",
                    flex="1",
                ),
                spacing="6",
                align="stretch",
                width="100%",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        background="linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
        border_radius="16px",
        padding="24px",
        border="1px solid var(--gray-6)",
        box_shadow="0 4px 20px rgba(0,0,0,0.08)",
        width="100%",
    )


def sales_dashboard_content() -> rx.Component:
    """Main sales dashboard content with enhanced styling."""
    return rx.box(
        rx.vstack(
            # Header with gradient background
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("bar-chart-3", size=32, color="white"),
                            rx.heading("Sales Dashboard", size="7", color="white", weight="bold"),
                            align="center",
                            spacing="3",
                        ),
                        rx.text(
                            "Monitor your business performance in real-time",
                            size="3",
                            color="rgba(255,255,255,0.8)",
                            weight="medium",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    rx.button(
                        rx.icon("refresh-cw", size=16),
                        "Refresh Data",
                        on_click=SalesDashboardState.load_data,
                        variant="outline",
                        size="3",
                        color_scheme="gray",
                        style={
                            "background": "rgba(255,255,255,0.1)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "color": "white",
                            "backdrop_filter": "blur(10px)",
                        },
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                ),
                background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                border_radius="20px",
                padding="32px",
                margin_bottom="24px",
                box_shadow="0 10px 40px rgba(102, 126, 234, 0.3)",
            ),
            
            # Filters
            sales_filters(),
            
            # Stats Cards with improved spacing
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
                spacing="6",
                width="100%",
            ),
            
            # Quick Insights - Full Width
            quick_insights(),
            
            # Charts Section
            # Daily Revenue Chart - Full Width
            daily_revenue_chart(),
            
            # Bottom Section - Pie Chart and Top Products Table side by side
            rx.grid(
                product_sales_chart(),
                top_products_table(),
                columns="2",
                spacing="6",
                width="100%",
            ),
            
            spacing="8",
            align="start",
            width="100%",
        ),
        background="linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)",
        min_height="100vh",
        padding="24px",
        width="100%",
    )
