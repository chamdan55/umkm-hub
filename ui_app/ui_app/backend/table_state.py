import csv
from pathlib import Path
from typing import List

import reflex as rx
from .database import (
    Penjualan, 
    Belanja, 
    Produk,
    KategoriPengeluaran,
    get_penjualan_data, 
    get_belanja_data, 
    get_produk_data,
    get_kategori_pengeluaran_data,
    insert_penjualan, 
    insert_belanja,
    insert_produk,
    create_tables,
    seed_sample_categories
)


class Item(rx.Base):
    """The item class."""

    name: str
    payment: float
    date: str
    status: str


class TableState(rx.State):
    """The state class."""

    items: List[Item] = []
    
    # Tab management
    selected_tab: str = "penjualan"  # Default to "penjualan" tab
    
    # Modal state for adding data
    show_add_modal: bool = False
    form_error_message: str = ""
    form_success_message: str = ""
    success_timer_active: bool = False
    
    # Database data
    penjualan_data: List[Penjualan] = []
    belanja_data: List[Belanja] = []
    produk_data: List[Produk] = []
    kategori_pengeluaran_data: List[KategoriPengeluaran] = []
    
    # Form fields for Penjualan
    form_id_produk: str = ""
    form_kuantitas: str = ""
    form_harga_saat_penjualan: str = ""
    form_total_penjualan: str = ""
    form_catatan_penjualan: str = ""
    form_tanggal_penjualan: str = ""
    
    # Form fields for new product
    form_new_product_name: str = ""
    form_new_product_price: str = ""
    show_add_product_form: bool = False
    
    # Form fields for Belanja
    form_deskripsi: str = ""
    form_id_kategori_pengeluaran: str = ""
    form_total_belanja: str = ""
    form_metode_pembayaran: str = ""
    form_bukti_transaksi: str = ""
    form_catatan_belanja: str = ""
    form_tanggal_pengeluaran: str = ""

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page
    
    def on_load(self):
        """Load data when the state is initialized."""
        self.load_data_from_db()

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[Item]:
        items = self.items

        # Filter items based on selected item
        if self.sort_value:
            if self.sort_value in ["payment"]:
                items = sorted(
                    items,
                    key=lambda item: float(getattr(item, self.sort_value)),
                    reverse=self.sort_reverse,
                )
            else:
                items = sorted(
                    items,
                    key=lambda item: str(getattr(item, self.sort_value)).lower(),
                    reverse=self.sort_reverse,
                )

        # Filter items based on search value
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in [
                        "name",
                        "payment",
                        "date",
                        "status",
                    ]
                )
            ]

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        if self.selected_tab == "penjualan":
            total = len(self.penjualan_data)
        elif self.selected_tab == "belanja":
            total = len(self.belanja_data)
        else:
            # Use total_items for backward compatibility
            total = self.total_items
        return max(1, (total + self.limit - 1) // self.limit)

    @rx.var(cache=True)
    def product_options(self) -> List[str]:
        """Get product options for dropdown - show only product names."""
        return [p.nama_produk for p in self.produk_data]
    
    @rx.var(cache=True)
    def kategori_options(self) -> List[str]:
        """Get category options for dropdown - show only category names."""
        return [k.nama_kategori for k in self.kategori_pengeluaran_data]

    @rx.var(cache=True)
    def get_penjualan_page(self) -> List[Penjualan]:
        """Get current page of penjualan data."""
        start_index = self.offset
        end_index = start_index + self.limit
        return self.penjualan_data[start_index:end_index]
    
    @rx.var(cache=True)
    def get_belanja_page(self) -> List[Belanja]:
        """Get current page of belanja data."""
        start_index = self.offset
        end_index = start_index + self.limit
        return self.belanja_data[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()
    
    def set_selected_tab(self, tab):
        """Set the selected tab and reset pagination."""
        self.selected_tab = tab
        self.offset = 0  # Reset to first page when switching tabs
        self.load_data_from_db()
    
    def load_data_from_db(self):
        """Load data from database based on selected tab."""
        try:
            create_tables()  # Ensure tables exist
            seed_sample_categories()  # Add sample categories if none exist
            if self.selected_tab == "penjualan":
                self.penjualan_data = get_penjualan_data()
                self.produk_data = get_produk_data()  # Load products for dropdown
            elif self.selected_tab == "belanja":
                self.belanja_data = get_belanja_data()
                self.kategori_pengeluaran_data = get_kategori_pengeluaran_data()  # Load categories for dropdown
        except Exception as e:
            print(f"Error loading data from database: {e}")
    
    def open_add_modal(self):
        """Open the add data modal."""
        self.show_add_modal = True
        self.form_error_message = ""
        self.form_success_message = ""  # Clear success message when opening modal
        self.clear_form()
    
    def close_add_modal(self):
        """Close the add data modal."""
        self.show_add_modal = False
        self.form_error_message = ""
        self.form_success_message = ""
        self.clear_form()
    
    def set_success_message(self, message: str):
        """Set success message."""
        self.form_success_message = message
    
    def clear_success_message(self):
        """Clear the success message."""
        self.form_success_message = ""
    
    def clear_form(self):
        """Clear all form fields."""
        # Penjualan fields
        self.form_id_produk = ""
        self.form_kuantitas = ""
        self.form_harga_saat_penjualan = ""
        self.form_total_penjualan = ""
        self.form_catatan_penjualan = ""
        self.form_tanggal_penjualan = ""
        
        # New product fields
        self.form_new_product_name = ""
        self.form_new_product_price = ""
        self.show_add_product_form = False
        
        # Belanja fields
        self.form_deskripsi = ""
        self.form_id_kategori_pengeluaran = ""
        self.form_total_belanja = ""
        self.form_metode_pembayaran = ""
        self.form_bukti_transaksi = ""
        self.form_catatan_belanja = ""
        self.form_tanggal_pengeluaran = ""
    
    def submit_form(self):
        """Submit the form data to database."""
        success = False
        self.form_error_message = ""  # Clear any previous error
        
        if self.selected_tab == "penjualan":
            # Validate required fields
            if not self.form_id_produk.strip():
                self.form_error_message = "Product is required"
                return
            if not self.form_kuantitas.strip() or int(self.form_kuantitas) <= 0:
                self.form_error_message = "Quantity must be greater than 0"
                return
                
            # Get product ID from product name
            product_id = None
            if self.form_id_produk.strip():
                for produk in self.produk_data:
                    if produk.nama_produk == self.form_id_produk.strip():
                        product_id = str(produk.id_produk)
                        break
            
            if not product_id:
                self.form_error_message = "Product is required"
                return
                
            # Prepare data with proper validation (excluding total as it's computed)
            data = {
                "tanggal_penjualan": self.form_tanggal_penjualan.strip() if self.form_tanggal_penjualan else "",
                "id_produk": product_id,
                "kuantitas": self.form_kuantitas.strip() if self.form_kuantitas else "0",
                "harga_saat_penjualan": self.form_harga_saat_penjualan.strip() if self.form_harga_saat_penjualan else "0",
                "catatan": self.form_catatan_penjualan.strip() if self.form_catatan_penjualan else "",
            }
            
            print(f"Submitting penjualan data: {data}")
            success = insert_penjualan(data)
            
        elif self.selected_tab == "belanja":
            # Validate required fields
            if not self.form_deskripsi.strip():
                self.form_error_message = "Description is required"
                return
            if not self.form_id_kategori_pengeluaran.strip():
                self.form_error_message = "Category is required"
                return
            if not self.form_metode_pembayaran.strip():
                self.form_error_message = "Payment Method is required"
                return
                
            # Get category ID from category name
            kategori_id = None
            if self.form_id_kategori_pengeluaran.strip():
                for kategori in self.kategori_pengeluaran_data:
                    if kategori.nama_kategori == self.form_id_kategori_pengeluaran.strip():
                        kategori_id = str(kategori.id_kategori)
                        break
            
            if not kategori_id:
                self.form_error_message = "Category is required"
                return
                
            # Prepare data with proper validation
            data = {
                "tanggal_pengeluaran": self.form_tanggal_pengeluaran.strip() if self.form_tanggal_pengeluaran else "",
                "deskripsi": self.form_deskripsi.strip(),
                "id_kategori_pengeluaran": kategori_id,
                "total": self.form_total_belanja.strip() if self.form_total_belanja else "0",
                "metode_pembayaran": self.form_metode_pembayaran.strip(),
                "bukti_transaksi": self.form_bukti_transaksi.strip() if self.form_bukti_transaksi else "",
                "catatan": self.form_catatan_belanja.strip() if self.form_catatan_belanja else "",
            }
            
            print(f"Submitting belanja data: {data}")
            success = insert_belanja(data)
        
        if success:
            # Set success message based on tab
            if self.selected_tab == "penjualan":
                self.form_success_message = "Penjualan data added successfully!"
            elif self.selected_tab == "belanja":
                self.form_success_message = "Belanja data added successfully!"
            
            print("Data added successfully!")
            
            # Refresh data after successful insertion
            self.load_data_from_db()
            # Clear form fields but keep the modal open to show success message
            self.clear_form()
            self.form_error_message = ""
        else:
            self.form_error_message = "Failed to insert data. Please check your input and try again."
    
    # Form field setters for Penjualan
    def set_form_id_produk(self, value: str):
        # Store the product name for display
        self.form_id_produk = value
        
        # Find the product ID based on the selected name and auto-fill price
        if value:
            for produk in self.produk_data:
                if produk.nama_produk == value:
                    self.form_harga_saat_penjualan = str(produk.harga_produk)
                    break
    
    def set_form_kuantitas(self, value: str):
        self.form_kuantitas = value
        if self.form_success_message:  # Clear success message on user interaction
            self.form_success_message = ""
        self._calculate_total_penjualan()
    
    def set_form_harga_saat_penjualan(self, value: str):
        self.form_harga_saat_penjualan = value
        if self.form_success_message:  # Clear success message on user interaction
            self.form_success_message = ""
        self._calculate_total_penjualan()
    
    def set_form_total_penjualan(self, value: str):
        self.form_total_penjualan = value
    
    def set_form_catatan_penjualan(self, value: str):
        self.form_catatan_penjualan = value
    
    def set_form_tanggal_penjualan(self, value: str):
        print(f"DEBUG tanggal_penjualan - Received value: {repr(value)}")
        print(f"DEBUG tanggal_penjualan - Type: {type(value)}")
        print(f"DEBUG tanggal_penjualan - Length: {len(value) if value else 'None'}")
        if value:
            print(f"DEBUG tanggal_penjualan - Is string: {isinstance(value, str)}")
            print(f"DEBUG tanggal_penjualan - Contains date format: {'-' in value}")
        
        self.form_tanggal_penjualan = value
    
    # New product form setters
    def set_form_new_product_name(self, value: str):
        self.form_new_product_name = value
    
    def set_form_new_product_price(self, value: str):
        self.form_new_product_price = value
    
    def toggle_add_product_form(self):
        self.show_add_product_form = not self.show_add_product_form
    
    def add_new_product(self):
        """Add a new product to the database."""
        if not self.form_new_product_name.strip():
            self.form_error_message = "Product name is required"
            return
        
        data = {
            "nama_produk": self.form_new_product_name.strip(),
            "harga_produk": self.form_new_product_price.strip() if self.form_new_product_price else "0",
        }
        
        product_id = insert_produk(data)
        if product_id:
            # Refresh product data
            self.produk_data = get_produk_data()
            # Auto-select the new product (just the name)
            product_name = self.form_new_product_name.strip()
            self.form_id_produk = product_name
            self.form_harga_saat_penjualan = self.form_new_product_price
            # Clear and hide the form
            self.form_new_product_name = ""
            self.form_new_product_price = ""
            self.show_add_product_form = False
            self.form_error_message = ""
            # Show success message
            self.form_success_message = f"Product '{product_name}' added successfully!"
        else:
            self.form_error_message = "Failed to add product"
    
    def _calculate_total_penjualan(self):
        """Calculate total for penjualan."""
        try:
            kuantitas = float(self.form_kuantitas) if self.form_kuantitas else 0
            harga = float(self.form_harga_saat_penjualan) if self.form_harga_saat_penjualan else 0
            self.form_total_penjualan = str(kuantitas * harga)
        except (ValueError, TypeError):
            self.form_total_penjualan = "0"
    
    # Form field setters for Belanja
    def set_form_deskripsi(self, value: str):
        self.form_deskripsi = value
    
    def set_form_id_kategori_pengeluaran(self, value: str):
        self.form_id_kategori_pengeluaran = value
        if self.form_success_message:  # Clear success message on user interaction
            self.form_success_message = ""
    
    def set_form_total_belanja(self, value: str):
        self.form_total_belanja = value
        if self.form_success_message:  # Clear success message on user interaction
            self.form_success_message = ""
    
    def set_form_metode_pembayaran(self, value: str):
        self.form_metode_pembayaran = value
    
    def set_form_bukti_transaksi(self, value: str):
        self.form_bukti_transaksi = value
    
    def set_form_catatan_belanja(self, value: str):
        self.form_catatan_belanja = value
    
    def set_form_tanggal_pengeluaran(self, value: str):
        self.form_tanggal_pengeluaran = value
    
    # Load data on initialization
    def load_entries(self):
        """Load data based on current tab."""
        if self.selected_tab in ["penjualan", "belanja"]:
            self.load_data_from_db()
        else:
            # Load CSV data for backward compatibility
            with Path("items.csv").open(mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.items = [
                    Item(
                        name=row.get("name", ""),
                        payment=float(row.get("payment", 0)),
                        date=row.get("date", ""),
                        status=row.get("status", "")
                    ) for row in reader
                ]
                self.total_items = len(self.items)
    
    @rx.var(cache=True)
    def get_penjualan_data(self) -> List[Penjualan]:
        """Get data for Penjualan table from database."""
        return self.penjualan_data
    
    @rx.var(cache=True)
    def get_belanja_data(self) -> List[Belanja]:
        """Get data for Belanja table from database."""
        return self.belanja_data
    
    @rx.var(cache=True)
    def current_tab_data(self) -> List:
        """Get data for the currently selected tab."""
        if self.selected_tab == "penjualan":
            return self.get_penjualan_data
        elif self.selected_tab == "belanja":
            return self.get_belanja_data
        else:
            # Fallback to original items for backwards compatibility
            return self.filtered_sorted_items
    
    def set_sort_value(self, value: str):
        """Set the sort value."""
        self.sort_value = value
        self.load_entries()
    
    def set_search_value(self, value: str):
        """Set the search value."""
        self.search_value = value

    @rx.var(cache=True)
    def get_current_page(self) -> List[Item]:
        """Get current page of filtered and sorted items."""
        items = self.filtered_sorted_items
        start_index = self.offset
        end_index = start_index + self.limit
        return items[start_index:end_index]
