"""Sales dashboard state management."""

from datetime import date, timedelta
from typing import List, Dict, Any

import reflex as rx

from ..backend.database import get_penjualan_data, get_produk_data, Penjualan, Produk


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
