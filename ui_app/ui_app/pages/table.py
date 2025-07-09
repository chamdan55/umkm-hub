"""The table page."""

import reflex as rx

from ..backend.table_state import TableState
from ..templates import template
from ..views.table import main_table_with_tabs


@template(route="/Pembukuan", title="Pembukuan")
def table() -> rx.Component:
    """The Pembukuan page.

    Returns:
        The UI for the Pembukuan page.

    """
    return rx.vstack(
        rx.heading("Pembukuan", size="5"),
        main_table_with_tabs(),
        spacing="8",
        width="100%",
    )
