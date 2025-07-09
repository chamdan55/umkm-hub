import reflex as rx

from ..backend.table_state import Item, TableState
from ..backend.database import Penjualan, Belanja
from ..components.status_badge import status_badge


def add_data_modal() -> rx.Component:
    """Modal for adding new data to the selected table."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=20),
                "Add Data",
                size="3",
                variant="solid",
                color_scheme="blue",
                on_click=TableState.open_add_modal,
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    TableState.selected_tab == "penjualan",
                    "Add Penjualan Data",
                    "Add Belanja Data"
                )
            ),
            rx.dialog.description(
                rx.cond(
                    TableState.selected_tab == "penjualan",
                    "Enter the details for a new penjualan record.",
                    "Enter the details for a new belanja record."
                )
            ),
            # Show error message if exists
            rx.cond(
                TableState.form_error_message != "",
                rx.callout(
                    TableState.form_error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                    variant="soft",
                    size="1",
                ),
            ),
            # Show success message if exists with auto-dismiss
            rx.cond(
                TableState.form_success_message != "",
                rx.callout(
                    TableState.form_success_message,
                    icon="check",
                    color_scheme="green",
                    variant="soft",
                    size="1",
                    style={
                        "animation": "fadeIn 0.5s ease-in",
                    },
                ),
            ),
            # Add CSS for fade animation
            rx.html(
                """
                <style>
                @keyframes fadeIn {
                    0% { opacity: 0; transform: translateY(-10px); }
                    100% { opacity: 1; transform: translateY(0); }
                }
                </style>
                """
            ),
            # Conditional form based on selected tab
            rx.cond(
                TableState.selected_tab == "penjualan",
                # Penjualan form
                rx.vstack(
                    # Product selection with option to add new
                    rx.vstack(
                        rx.select(
                            TableState.product_options,
                            placeholder="Select Product",
                            value=TableState.form_id_produk,
                            on_change=TableState.set_form_id_produk,
                            size="2",
                            width="100%",
                        ),
                        rx.button(
                            rx.icon("plus", size=16),
                            "Add New Product",
                            size="2",
                            variant="ghost",
                            color_scheme="blue",
                            on_click=TableState.toggle_add_product_form,
                            width="100%",
                            justify="start",
                        ),
                        # Add new product form (conditional)
                        rx.cond(
                            TableState.show_add_product_form,
                            rx.vstack(
                                rx.text(
                                    "Add New Product",
                                    size="3",
                                    weight="medium",
                                    color=rx.color("gray", 11),
                                ),
                                rx.hstack(
                                    rx.input(
                                        placeholder="Product Name",
                                        value=TableState.form_new_product_name,
                                        on_change=TableState.set_form_new_product_name,
                                        size="2",
                                    ),
                                    rx.input(
                                        placeholder="Price",
                                        type="number",
                                        step="0.01",
                                        value=TableState.form_new_product_price,
                                        on_change=TableState.set_form_new_product_price,
                                        size="2",
                                    ),
                                    width="100%",
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.button(
                                        "Cancel",
                                        size="2",
                                        variant="soft",
                                        color_scheme="gray",
                                        on_click=TableState.toggle_add_product_form,
                                    ),
                                    rx.button(
                                        rx.icon("check", size=16),
                                        "Add Product",
                                        size="2",
                                        variant="solid",
                                        color_scheme="green",
                                        on_click=TableState.add_new_product,
                                    ),
                                    justify="end",
                                    width="100%",
                                    spacing="2",
                                ),
                                spacing="3",
                                padding="4",
                                border="1px solid",
                                border_color=rx.color("blue", 6),
                                border_radius="8px",
                                background_color=rx.color("blue", 1),
                                width="100%",
                            ),
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="Quantity",
                            type="number",
                            value=TableState.form_kuantitas,
                            on_change=TableState.set_form_kuantitas,
                            size="2",
                            width="50%",
                        ),
                        rx.input(
                            placeholder="Unit Price",
                            type="number",
                            step="0.01",
                            value=TableState.form_harga_saat_penjualan,
                            on_change=TableState.set_form_harga_saat_penjualan,
                            size="2",
                            width="50%",
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="Total (Auto-calculated)",
                            type="number",
                            step="0.01",
                            value=TableState.form_total_penjualan,
                            disabled=True,
                            size="2",
                            width="50%",
                            style={
                                "background_color": rx.color("gray", 2),
                                "color": rx.color("gray", 11),
                            },
                        ),
                        rx.input(
                            placeholder="Date (YYYY-MM-DD)",
                            type="date",
                            value=TableState.form_tanggal_penjualan,
                            on_change=TableState.set_form_tanggal_penjualan,
                            size="2",
                            width="50%",
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    rx.text_area(
                        placeholder="Notes (optional)",
                        value=TableState.form_catatan_penjualan,
                        on_change=TableState.set_form_catatan_penjualan,
                        size="2",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                # Belanja form
                rx.vstack(
                    rx.text_area(
                        placeholder="Description",
                        value=TableState.form_deskripsi,
                        on_change=TableState.set_form_deskripsi,
                        size="2",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.select(
                            TableState.kategori_options,
                            placeholder="Select Category",
                            value=TableState.form_id_kategori_pengeluaran,
                            on_change=TableState.set_form_id_kategori_pengeluaran,
                            size="2",
                            width="50%",
                        ),
                        rx.input(
                            placeholder="Total Amount",
                            type="number",
                            step="0.01",
                            value=TableState.form_total_belanja,
                            on_change=TableState.set_form_total_belanja,
                            size="2",
                            width="50%",
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    rx.hstack(
                        rx.select(
                            ["Cash", "Credit", "Debit", "Transfer", "Other"],
                            placeholder="Payment Method",
                            value=TableState.form_metode_pembayaran,
                            on_change=TableState.set_form_metode_pembayaran,
                            width="50%",
                            size="2",
                        ),
                        rx.input(
                            placeholder="Date (YYYY-MM-DD)",
                            type="date",
                            value=TableState.form_tanggal_pengeluaran,
                            on_change=TableState.set_form_tanggal_pengeluaran,
                            size="2",
                            width="50%",
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="Receipt/Proof",
                            value=TableState.form_bukti_transaksi,
                            on_change=TableState.set_form_bukti_transaksi,
                            size="2",
                            width="100%",
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    rx.text_area(
                        placeholder="Notes (optional)",
                        value=TableState.form_catatan_belanja,
                        on_change=TableState.set_form_catatan_belanja,
                        size="2",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                        on_click=TableState.close_add_modal,
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Add Data",
                        variant="solid",
                        color_scheme="blue",
                        on_click=TableState.submit_form,
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": "450px"},
        ),
        open=TableState.show_add_modal,
    )


def _header_cell_penjualan(text: str, icon: str) -> rx.Component:
    """Header cell for Penjualan table."""
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def _header_cell_belanja(text: str, icon: str) -> rx.Component:
    """Header cell for Belanja table."""
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def _show_item(item: Item, index: int) -> rx.Component:
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(item.name),
        rx.table.cell(f"${item.payment}"),
        rx.table.cell(item.date),
        rx.table.cell(status_badge(item.status)),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return rx.hstack(
            rx.text(
                "Page ",
                rx.code(TableState.page_number),
                f" of {TableState.total_pages}",
                justify="end",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevrons-left", size=18),
                    on_click=TableState.first_page,
                    opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-left", size=18),
                    on_click=TableState.prev_page,
                    opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-right", size=18),
                    on_click=TableState.next_page,
                    opacity=rx.cond(
                        TableState.page_number == TableState.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        TableState.page_number == TableState.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevrons-right", size=18),
                    on_click=TableState.last_page,
                    opacity=rx.cond(
                        TableState.page_number == TableState.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        TableState.page_number == TableState.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                align="center",
                spacing="2",
                justify="end",
            ),
            spacing="5",
            margin_top="1em",
            align="center",
            width="100%",
            justify="end",
        )


def _show_penjualan_item(item: Penjualan, index: int) -> rx.Component:
    """Display a penjualan item row."""
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(item.nama_produk),
        rx.table.cell(item.kuantitas),  # Display quantity directly
        rx.table.cell(f"Rp {item.harga_saat_penjualan:,.0f}"),  # Indonesian currency format
        rx.table.cell(f"Rp {item.total:,.0f}"),  # Indonesian currency format
        rx.table.cell(item.tanggal_penjualan),
        rx.table.cell(item.catatan),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _show_belanja_item(item: Belanja, index: int) -> rx.Component:
    """Display a belanja item row."""
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(item.deskripsi),
        rx.table.cell(item.nama_kategori),  # Show category name instead of ID
        rx.table.cell(f"Rp {item.total:,.0f}"),  # Indonesian currency format
        rx.table.cell(item.metode_pembayaran),
        rx.table.cell(item.tanggal_pengeluaran),
        rx.table.cell(item.bukti_transaksi),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def penjualan_table() -> rx.Component:
    """Penjualan table with database data."""
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell_penjualan("Produk", "package"),
                    _header_cell_penjualan("Kuantitas", "hash"),
                    _header_cell_penjualan("Harga", "dollar-sign"),
                    _header_cell_penjualan("Total", "calculator"),
                    _header_cell_penjualan("Tanggal", "calendar"),
                    _header_cell_penjualan("Catatan", "notebook-pen"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    TableState.get_penjualan_page,
                    lambda item, index: _show_penjualan_item(item, index),
                )
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        _pagination_view(),
        width="100%",
    )


def belanja_table() -> rx.Component:
    """Belanja table with database data."""
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell_belanja("Deskripsi", "shopping-cart"),
                    _header_cell_belanja("Kategori", "tag"),
                    _header_cell_belanja("Total", "dollar-sign"),
                    _header_cell_belanja("Pembayaran", "credit-card"),
                    _header_cell_belanja("Tanggal", "calendar"),
                    _header_cell_belanja("Bukti", "receipt"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    TableState.get_belanja_page,
                    lambda item, index: _show_belanja_item(item, index),
                )
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        _pagination_view(),
        width="100%",
    )


def main_table_with_tabs() -> rx.Component:
    """Main table component with tabs for Penjualan and Belanja."""
    return rx.vstack(
        # Header with tabs and add button
        rx.flex(
            rx.segmented_control.root(
                rx.segmented_control.item("Penjualan", value="penjualan"),
                rx.segmented_control.item("Belanja", value="belanja"),
                default_value="penjualan",
                on_change=TableState.set_selected_tab,
                size="3",
            ),
            add_data_modal(),
            justify="between",
            align="center",
            width="100%",
        ),
        # Tab content
        rx.match(
            TableState.selected_tab,
            ("penjualan", penjualan_table()),
            ("belanja", belanja_table()),
        ),
        spacing="6",
        width="100%",
    )


def main_table() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.flex(
                rx.cond(
                    TableState.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=TableState.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=TableState.toggle_sort,
                    ),
                ),
                rx.select(
                    [
                        "name",
                        "payment",
                        "date",
                        "status",
                    ],
                    placeholder="Sort By: Name",
                    size="3",
                    on_change=TableState.set_sort_value,
                ),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=TableState.setvar("search_value", ""),
                        display=rx.cond(TableState.search_value, "flex", "none"),
                    ),
                    value=TableState.search_value,
                    placeholder="Search here...",
                    size="3",
                    max_width=["150px", "150px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=TableState.set_search_value,
                ),
                align="center",
                justify="end",
                spacing="3",
            ),
            rx.button(
                rx.icon("arrow-down-to-line", size=20),
                "Export",
                size="3",
                variant="surface",
                display=["none", "none", "none", "flex"],
                on_click=rx.download(url="/items.csv"),
            ),
            spacing="3",
            justify="between",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Name", "user"),
                    _header_cell("Payment", "dollar-sign"),
                    _header_cell("Date", "calendar"),
                    _header_cell("Status", "notebook-pen"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    TableState.get_current_page,
                    lambda item, index: _show_item(item, index),
                )
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        _pagination_view(),
        width="100%",
    )
