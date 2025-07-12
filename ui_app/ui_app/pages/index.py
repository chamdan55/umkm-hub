"""The overview page of the app."""

import datetime
from datetime import date, timedelta
from typing import List, Dict, Any

import reflex as rx

from .. import styles
from ..components.card import card
from ..components.notification import notification
from ..templates import template
from ..backend.database import get_penjualan_data, get_produk_data, Penjualan, Produk
from .profile import ProfileState


class SalesDashboardState(rx.State):
    """State for the sales dashboard."""
    
    # Data
    sales_data: List[Penjualan] = []
    products_data: List[Produk] = []
    
    # Filters
    selected_product: str = "All Products"
    selected_period: str = "All Time"
    
    # Computed metrics
    total_revenue: float = 0.0
    total_orders: int = 0
    average_order_value: float = 0.0
    items_sold: int = 0
    
    # Chart data
    daily_revenue_data: List[Dict[str, Any]] = []
    product_sales_data: List[Dict[str, Any]] = []
    top_products_data: List[Dict[str, Any]] = []
    
    # Quick insights
    revenue_growth: float = 0.0
    orders_growth: float = 0.0
    
    def load_data(self):
        """Load sales and product data."""
        try:
            self.sales_data = get_penjualan_data()
            self.products_data = get_produk_data()
            self.calculate_metrics()
            self.generate_chart_data()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.sales_data = []
            self.products_data = []
    
    def filter_sales_data(self) -> List[Penjualan]:
        """Filter sales data based on selected filters."""
        filtered_data = self.sales_data
        
        # Filter by product
        if self.selected_product != "All Products":
            filtered_data = [
                sale for sale in filtered_data 
                if sale.nama_produk == self.selected_product
            ]
        
        # Filter by period
        if self.selected_period != "All Time":
            if self.selected_period == "Last 7 Days":
                days = 7
            elif self.selected_period == "Last 30 Days":
                days = 30
            elif self.selected_period == "Last 90 Days":
                days = 90
            else:
                days = 0
            
            if days > 0:
                cutoff_date = date.today() - timedelta(days=days)
                filtered_data = [
                    sale for sale in filtered_data 
                    if date.fromisoformat(sale.tanggal_penjualan) >= cutoff_date
                ]
        
        return filtered_data
    
    def calculate_metrics(self):
        """Calculate key metrics."""
        filtered_data = self.filter_sales_data()
        
        if not filtered_data:
            self.total_revenue = 0.0
            self.total_orders = 0
            self.average_order_value = 0.0
            self.items_sold = 0
            return
        
        self.total_revenue = sum(sale.total for sale in filtered_data)
        self.total_orders = len(filtered_data)
        self.average_order_value = self.total_revenue / self.total_orders if self.total_orders > 0 else 0.0
        self.items_sold = sum(sale.kuantitas for sale in filtered_data)
        
        # Calculate growth metrics
        self.calculate_growth_metrics()
    
    def calculate_growth_metrics(self):
        """Calculate growth metrics for quick insights."""
        try:
            current_period_data = self.filter_sales_data()
            
            # Get previous period data for comparison
            if self.selected_period == "All Time":
                # Compare last 30 days vs previous 30 days
                current_cutoff = date.today() - timedelta(days=30)
                previous_cutoff = date.today() - timedelta(days=60)
                
                current_data = [
                    sale for sale in self.sales_data 
                    if date.fromisoformat(sale.tanggal_penjualan) >= current_cutoff
                ]
                previous_data = [
                    sale for sale in self.sales_data 
                    if previous_cutoff <= date.fromisoformat(sale.tanggal_penjualan) < current_cutoff
                ]
            else:
                if self.selected_period == "Last 7 Days":
                    days = 7
                elif self.selected_period == "Last 30 Days":
                    days = 30
                elif self.selected_period == "Last 90 Days":
                    days = 90
                else:
                    days = 30
                
                current_cutoff = date.today() - timedelta(days=days)
                previous_cutoff = date.today() - timedelta(days=days*2)
                
                current_data = [
                    sale for sale in self.sales_data 
                    if date.fromisoformat(sale.tanggal_penjualan) >= current_cutoff
                ]
                previous_data = [
                    sale for sale in self.sales_data 
                    if previous_cutoff <= date.fromisoformat(sale.tanggal_penjualan) < current_cutoff
                ]
            
            # Apply product filter to both periods
            if self.selected_product != "All Products":
                current_data = [
                    sale for sale in current_data 
                    if sale.nama_produk == self.selected_product
                ]
                previous_data = [
                    sale for sale in previous_data 
                    if sale.nama_produk == self.selected_product
                ]
            
            # Calculate growth
            current_revenue = sum(sale.total for sale in current_data)
            previous_revenue = sum(sale.total for sale in previous_data)
            
            current_orders = len(current_data)
            previous_orders = len(previous_data)
            
            self.revenue_growth = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0.0
            self.orders_growth = ((current_orders - previous_orders) / previous_orders * 100) if previous_orders > 0 else 0.0
            
        except Exception as e:
            print(f"Error calculating growth metrics: {e}")
            self.revenue_growth = 0.0
            self.orders_growth = 0.0
    
    def generate_chart_data(self):
        """Generate data for charts."""
        filtered_data = self.filter_sales_data()
        
        # Daily revenue data
        daily_revenue = {}
        for sale in filtered_data:
            date_str = sale.tanggal_penjualan
            if date_str not in daily_revenue:
                daily_revenue[date_str] = 0.0
            daily_revenue[date_str] += sale.total
        
        self.daily_revenue_data = [
            {"date": date_str, "revenue": revenue}
            for date_str, revenue in sorted(daily_revenue.items())
        ]
        
        # Product sales data with colors
        product_sales = {}
        for sale in filtered_data:
            product_name = sale.nama_produk
            if product_name not in product_sales:
                product_sales[product_name] = {"revenue": 0.0, "quantity": 0}
            product_sales[product_name]["revenue"] += sale.total
            product_sales[product_name]["quantity"] += sale.kuantitas
        
        colors = ["#8884d8", "#82ca9d", "#ffc658", "#ff7300", "#00ff00", "#0088fe", "#ff8042", "#ffbb28", "#8dd1e1", "#d084d0"]
        self.product_sales_data = [
            {
                "product": product, 
                "revenue": data["revenue"], 
                "quantity": data["quantity"],
                "fill": colors[i % len(colors)]
            }
            for i, (product, data) in enumerate(product_sales.items())
        ]
        
        # Top products data (keep raw values for table formatting)
        self.top_products_data = sorted(
            self.product_sales_data, 
            key=lambda x: x["revenue"], 
            reverse=True
        )[:5]
    
    def set_selected_product(self, product: str):
        """Set selected product filter."""
        self.selected_product = product
        self.calculate_metrics()
        self.generate_chart_data()
    
    def set_selected_period(self, period: str):
        """Set selected period filter."""
        self.selected_period = period
        self.calculate_metrics()
        self.generate_chart_data()

    @rx.var
    def product_options(self) -> List[str]:
        """Get list of product options for the filter."""
        return ["All Products"] + [product.nama_produk for product in self.products_data]

    @rx.var
    def pie_chart_colors(self) -> List[str]:
        """Get colors for pie chart segments."""
        colors = ["#8884d8", "#82ca9d", "#ffc658", "#ff7300", "#00ff00", "#0088fe", "#ff8042", "#ffbb28", "#8dd1e1", "#d084d0"]
        return colors[:len(self.product_sales_data)]

    @rx.var
    def formatted_top_products(self) -> List[Dict[str, str]]:
        """Get formatted top products data for the table."""
        return [
            {
                "product": item["product"],
                "revenue": f"Rp {item['revenue']:,.0f}",
                "quantity": f"{item['quantity']:,}"
            }
            for item in self.top_products_data
        ]


def stats_card(title: str, value: str, icon: str, color: str = "blue") -> rx.Component:
    """Create a stats card component."""
    return card(
        rx.hstack(
            rx.vstack(
                rx.text(title, size="2", color="gray"),
                rx.text(value, size="6", weight="bold"),
                spacing="1",
                align="start",
            ),
            rx.icon(icon, size=24, color=color),
            justify="between",
            align="center",
            width="100%",
        ),
        min_height="100px",
    )


def quick_insights() -> rx.Component:
    """Create quick insights panel."""
    return card(
        rx.vstack(
            rx.hstack(
                rx.icon("trending-up", size=20),
                rx.text("Quick Insights", size="4", weight="medium"),
                align="center",
                spacing="2",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text("Revenue Growth:", size="2", weight="medium"),
                    rx.text(
                        f"{SalesDashboardState.revenue_growth:.1f}%",
                        size="2",
                        color="green",
                        weight="bold",
                    ),
                    justify="between",
                    width="100%",
                ),
                rx.hstack(
                    rx.text("Orders Growth:", size="2", weight="medium"),
                    rx.text(
                        f"{SalesDashboardState.orders_growth:.1f}%",
                        size="2",
                        color="blue",
                        weight="bold",
                    ),
                    justify="between",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
    )


def sales_filters() -> rx.Component:
    """Create sales filters."""
    return rx.hstack(
        rx.vstack(
            rx.text("Product", size="2", weight="medium"),
            rx.select(
                SalesDashboardState.product_options,
                placeholder="Select Product",
                value=SalesDashboardState.selected_product,
                on_change=SalesDashboardState.set_selected_product,
                width="200px",
            ),
            spacing="1",
            align="start",
        ),
        rx.vstack(
            rx.text("Period", size="2", weight="medium"),
            rx.select(
                ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
                placeholder="Select Period",
                value=SalesDashboardState.selected_period,
                on_change=SalesDashboardState.set_selected_period,
                width="200px",
            ),
            spacing="1",
            align="start",
        ),
        spacing="4",
        align="end",
    )


def product_sales_chart() -> rx.Component:
    """Create product sales pie chart."""
    return rx.vstack(
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=SalesDashboardState.product_sales_data,
                data_key="quantity",
                name_key="product",
                cx="50%",
                cy="50%",
                inner_radius=60,
                outer_radius=120,
                fill="#8884d8",
                label=False,
            ),
            rx.recharts.tooltip(),
            width="100%",
            height=300,
        ),
        rx.vstack(
            rx.text("Product Sales", size="3", weight="medium"),
            rx.foreach(
                SalesDashboardState.product_sales_data,
                render_product_item,
            ),
            spacing="2",
            align="start",
            width="100%",
        ),
        spacing="3",
        width="100%",
    )


def render_product_item(item) -> rx.Component:
    """Render a single product item for the chart legend."""
    return rx.hstack(
        rx.box(
            width="12px",
            height="12px",
            bg=item.fill,
            border_radius="2px",
        ),
        rx.text(f"{item.product}: {item.quantity} items", size="2"),
        spacing="2",
        align="center",
    )


def top_products_table() -> rx.Component:
    """Create top products table."""
    return rx.vstack(
        rx.text("Top Products", size="3", weight="medium"),
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
                    render_product_row,
                ),
            ),
            width="100%",
            variant="surface",
        ),
        spacing="3",
        width="100%",
    )


def render_product_row(item) -> rx.Component:
    """Render a single product row for the top products table."""
    return rx.table.row(
        rx.table.cell(item.product),
        rx.table.cell(item.revenue),
        rx.table.cell(item.quantity),
    )


def daily_revenue_chart() -> rx.Component:
    """Create daily revenue line chart."""
    return rx.recharts.line_chart(
        rx.recharts.line(
            data_key="revenue",
            stroke="#8884d8",
            stroke_width=2,
        ),
        rx.recharts.x_axis(data_key="date"),
        rx.recharts.y_axis(),
        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
        rx.recharts.tooltip(),
        data=SalesDashboardState.daily_revenue_data,
        width="100%",
        height=300,
    )


@template(route="/", title="Sales Dashboard")
def index() -> rx.Component:
    """The sales dashboard page.

    Returns:
        The UI for the sales dashboard.

    """
    return rx.vstack(
        rx.heading(f"Welcome, {ProfileState.profile.name}", size="5"),
        rx.flex(
            rx.input(
                rx.input.slot(rx.icon("search"), padding_left="0"),
                placeholder="Search here...",
                size="3",
                width="100%",
                max_width="450px",
                radius="large",
                style=styles.ghost_input_style,
            ),
            rx.flex(
                notification("bell", "cyan", 12),
                notification("message-square-text", "plum", 6),
                spacing="4",
                width="100%",
                wrap="nowrap",
                justify="end",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        
        # Sales Dashboard Header
        rx.hstack(
            rx.heading("Sales Dashboard", size="6"),
            rx.hstack(
                rx.button(
                    "Refresh Data",
                    on_click=SalesDashboardState.load_data,
                    size="2",
                    variant="outline",
                ),
                sales_filters(),
                spacing="4",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        
        # Key Metrics
        rx.grid(
            stats_card(
                "Total Revenue",
                rx.text(f"Rp {SalesDashboardState.total_revenue:,.0f}"),
                "dollar-sign",
                "green"
            ),
            stats_card(
                "Total Orders",
                rx.text(SalesDashboardState.total_orders),
                "shopping-cart",
                "blue"
            ),
            stats_card(
                "Average Order Value",
                rx.text(f"Rp {SalesDashboardState.average_order_value:,.0f}"),
                "trending-up",
                "purple"
            ),
            stats_card(
                "Items Sold",
                rx.text(SalesDashboardState.items_sold),
                "package",
                "orange"
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
                "repeat(4, 1fr)",
            ],
            width="100%",
        ),
        
        # Daily Revenue Chart
        card(
            rx.hstack(
                rx.icon("trending-up", size=20),
                rx.text("Daily Revenue Trends", size="4", weight="medium"),
                align="center",
                spacing="2",
            ),
            daily_revenue_chart(),
        ),
        
        # Charts and Insights
        rx.grid(
            card(
                rx.hstack(
                    rx.icon("pie-chart", size=20),
                    rx.text("Sales by Product", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                ),
                product_sales_chart(),
            ),
            card(
                rx.hstack(
                    rx.icon("bar-chart", size=20),
                    rx.text("Top Products", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                ),
                top_products_table(),
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
            ],
            width="100%",
        ),
        
        # Quick Insights
        quick_insights(),
        
        spacing="6",
        width="100%",
    )
