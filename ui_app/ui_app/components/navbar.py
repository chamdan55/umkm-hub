"""Navbar component for the app."""

import reflex as rx

from .. import styles


def nav_item_icon(icon: str) -> rx.Component:
    return rx.icon(icon, size=18)


def nav_item(text: str, url: str) -> rx.Component:
    """Navigation item for top navbar.

    Args:
        text: The text of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The navigation item component.

    """
    # Simple direct approach - check if current path matches
    # For Overview page, we want to highlight when on "/"
    active = rx.cond(
        text == "Overview",
        rx.State.router.page.path == "/",
        rx.State.router.page.path == url,
    )

    return rx.link(
        rx.hstack(
            rx.match(
                text,
                ("Overview", nav_item_icon("home")),
                ("Pembukuan", nav_item_icon("book-open")),
                ("About", nav_item_icon("book")),
                ("Profile", nav_item_icon("user")),
                ("Settings", nav_item_icon("settings")),
                nav_item_icon("layout-dashboard"),
            ),
            rx.text(text, size="2", weight="medium"),
            color=rx.cond(
                active,
                "#4F46E5",  # Blue color when active
                "#6B7280",  # Gray color when inactive
            ),
            style={
                "_hover": {
                    "background_color": rx.cond(
                        active,
                        "#EEF2FF",  # Light blue background when active
                        "#F3F4F6",  # Light gray background for hover
                    ),
                    "color": rx.cond(
                        active,
                        "#4F46E5",  # Blue color when active
                        "#374151",  # Darker gray for hover
                    ),
                    "opacity": "1",
                },
                "background_color": rx.cond(
                    active,
                    "#EEF2FF",  # Light blue background when active
                    "transparent",
                ),
                "opacity": rx.cond(
                    active,
                    "1",
                    "0.8",
                ),
            },
            align="center",
            border_radius=styles.border_radius,
            spacing="1",
            padding="0.4em 0.8em",
        ),
        underline="none",
        href=url,
    )


def navbar_footer() -> rx.Component:
    """Navbar footer.

    Returns:
        The navbar footer component.

    """
    return rx.hstack(
        rx.link(
            rx.text("Docs", size="3"),
            href="https://reflex.dev/docs/getting-started/introduction/",
            color_scheme="gray",
            underline="none",
        ),
        rx.link(
            rx.text("Blog", size="3"),
            href="https://reflex.dev/blog/",
            color_scheme="gray",
            underline="none",
        ),
        rx.spacer(),
        rx.color_mode.button(style={"opacity": "0.8", "scale": "0.95"}),
        justify="start",
        align="center",
        width="100%",
        padding="0.35em",
    )


def menu_button() -> rx.Component:
    from reflex.page import DECORATED_PAGES

    ordered_page_routes = [
        "/",
        "/Pembukuan",  # Your table page
        "/about",
        "/profile",
        "/settings",
    ]

    pages = [
        page_dict
        for page_list in DECORATED_PAGES.values()
        for _, page_dict in page_list
    ]

    ordered_pages = sorted(
        pages,
        key=lambda page: (
            ordered_page_routes.index(page["route"])
            if page["route"] in ordered_page_routes
            else len(ordered_page_routes)
        ),
    )

    return rx.drawer.root(
        rx.drawer.trigger(
            rx.icon("align-justify"),
        ),
        rx.drawer.overlay(z_index="5"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    rx.hstack(
                        rx.drawer.close(rx.icon(tag="x")),
                        rx.spacer(),
                        justify="start",
                        width="100%",
                    ),
                    rx.divider(),
                    *[
                        nav_item(
                            text=page.get(
                                "title", page["route"].strip("/").capitalize()
                            ),
                            url=page["route"],
                        )
                        for page in ordered_pages
                    ],
                    rx.spacer(),
                    navbar_footer(),
                    spacing="4",
                    width="100%",
                ),
                top="auto",
                right="auto",
                height="100%",
                width="20em",
                padding="1em",
                bg=rx.color("gray", 1),
            ),
            width="100%",
        ),
        direction="left",
        display=["block", "block", "block", "block", "block", "none"],
    )


def navbar() -> rx.Component:
    """The navbar with top navigation.

    Returns:
        The navbar component.

    """
    from reflex.page import DECORATED_PAGES

    ordered_page_routes = [
        "/",
        "/Pembukuan",  # Your table page
        "/about", 
        "/profile",
        "/settings",
    ]

    pages = [
        page_dict
        for page_list in DECORATED_PAGES.values()
        for _, page_dict in page_list
    ]

    ordered_pages = sorted(
        pages,
        key=lambda page: (
            ordered_page_routes.index(page["route"])
            if page["route"] in ordered_page_routes
            else len(ordered_page_routes)
        ),
    )

    return rx.el.nav(
        rx.hstack(
            # Brand/Logo
            rx.hstack(
                # rx.color_mode_cond(
                #     rx.image(src="/reflex_black.svg", height="1.2em"),
                #     rx.image(src="/reflex_white.svg", height="1.2em"),
                # ),
                menu_button(),
                # rx.text("UMKM", size="4", weight="bold", color="blue"),
                # rx.text("Hub.", size="4", weight="bold"),
                rx.color_mode_cond(
                    rx.image(src="/logo.png", height="1.2em"),
                    rx.image(src="/logo.png", height="1.2em"),
                ),
                spacing="2",
                align="center",
            ),
            rx.spacer(),
            # Navigation items - visible on desktop
            # rx.hstack(
            #     # rx.link(
            #     #     rx.text("Docs", size="2"),
            #     #     href="https://reflex.dev/docs/getting-started/introduction/",
            #     #     color_scheme="gray",
            #     #     underline="none",
            #     # ),
            #     # rx.link(
            #     #     rx.text("Blog", size="2"),
            #     #     href="https://reflex.dev/blog/",
            #     #     color_scheme="gray", 
            #     #     underline="none",
            #     # ),
            #     rx.color_mode.button(style={"opacity": "0.8", "scale": "0.95"}),
            #     # Mobile menu button
            #     spacing="3",
            #     align="center",
            # ),
            # Right side items
            rx.hstack(
                *[
                    nav_item(
                        text=page.get("title", page["route"].strip("/").capitalize()),
                        url=page["route"],
                    )
                    for page in ordered_pages
                ],
                spacing="1",
                display=["none", "none", "none", "none", "none", "flex"],
                margin_left="3em",
                align="center",
            ),
            align="center",
            width="100%",
            padding_y="0.75em",
            padding_x=["1em", "1em", "2em"],
        ),
        position="sticky",
        background_color=rx.color("gray", 1),
        top="0px",
        z_index="5",
        border_bottom=styles.border,
        width="100%",
    )
