import reflex as rx
from .backend.backend import State

def create_section_heading(font_size, line_height, text):
    """Create a section heading with specified font size, line height, and text."""
    return rx.heading(
        text,
        font_weight="600",
        margin_bottom="1rem",
        font_size=font_size,
        line_height=line_height,
        as_="h2",
    )



def create_list_item(content):
    """Create a list item element."""
    return rx.el.li(content)


def create_colored_icon(color, icon_name):
    """Create a colored icon with specified tag and dimensions."""
    return rx.icon(
        tag=icon_name,
        height="1.25rem",
        margin_right="0.5rem",
        color=color,
        width="1.25rem",
    )


def create_span(content):
    """Create a span element with the given content."""
    return rx.text.span(content)


def create_list_item_with_check_icon(text):
    """Create a list item with a green check icon and the specified text."""
    return rx.el.li(
        # create_colored_icon(
        #     color="#10B981", icon_name="check-circle"
        # ),
        create_span(content=text),
        display="flex",
        align_items="center",
    )


def create_bold_span(content):
    """Create a span element with bold text."""
    return rx.text.span(content, font_weight="500")


def create_list_item_with_custom_icon(
    icon_color, icon_name, text
):
    """Create a list item with a custom colored icon and specified text."""
    return rx.el.li(
        create_colored_icon(
            color=icon_color, icon_name=icon_name
        ),
        create_bold_span(content=text),
        display="flex",
        align_items="center",
    )


def create_purple_subheading(text):
    """Create a purple subheading (h3) with the specified text."""
    return rx.heading(
        text,
        font_weight="600",
        margin_bottom="0.5rem",
        color="#6D28D9",
        as_="h3",
        size="4",
    )


def create_gray_small_text(content):
    """Create a small, gray text element."""
    return rx.text(
        content,
        color="#4B5563",
        font_size="0.875rem",
        line_height="1.25rem",
    )


def create_info_box(title, description):
    """Create an info box with a title and description."""
    return rx.box(
        create_purple_subheading(text=title),
        create_gray_small_text(content=description),
        class_name="flex-shrink-0",
        background_color="#F5F3FF",
        padding="1rem",
        border_radius="0.5rem",
        box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        width="16rem",
    )


def create_conversation_transcript():
    """Create a scrollable box containing the dynamic conversation transcript."""
    return rx.box(
        rx.text(State.fullTranscript, white_space="pre-wrap"),  # Maintain line breaks
        display="flex",
        flex_direction="column",
        gap="1rem",
        padding="2rem",
        border_radius="0.5rem",
        box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        max_height="300px",  # Limit the height of the box
        overflow_y="auto",  # Enable vertical scrolling
        background_color="#ffffff"
    )

def create_bookmarks():
    return rx.box(
        rx.text(State.bookmarks, white_space='pre_wrap'),
        background_color="#EFF6FF",
        padding="1.5rem",
        border_radius="0.5rem",
        box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    )

def create_key_points_list():
    """Create a list of key discussion points from the meeting."""
    return rx.box(
        rx.text(State.keyPoints, white_space="pre-wrap"),  # Maintain line breaks
        display="flex",
        flex_direction="column",
        gap="1rem",  # Add more spacing between the points
        padding="2rem",  # Add more padding for better readability
        background_color="#F3F4F6",
        border_radius="0.5rem"
    )

def create_action_items_section():
    """Create a section displaying action items from the meeting."""
    return rx.box(
        create_section_heading(
            font_size="1.25rem",
            line_height="1.75rem",
            text="Action Items",
        ),
        rx.box(
            rx.text(State.actionItems, white_space="pre-wrap"),  # Maintain line breaks
            display="flex",
            flex_direction="column",
            gap="1rem",  # Add more spacing between the items
            padding="2rem",  # Add more padding for better readability
            background_color="#F5F3FF",
            border_radius="0.5rem"
        ),
        margin_bottom="1.5rem",
        padding="2rem",
        border_radius="0.5rem",
        box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    )

def create_main_content_section():
    """Create the main content section including transcript, key points, and action items."""
    return rx.box(
        rx.box(
            create_section_heading(
                font_size="1.25rem",
                line_height="1.75rem",
                text="Key Discussion Points",
            ),
            create_key_points_list(),  # Load key discussion points generated by Gemini
            background_color="#ffffff",
            margin_bottom="1.5rem",
            padding="1.5rem",
            border_radius="0.5rem",
            box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        ),
        create_action_items_section(),  # Load action items generated by Gemini
        grid_column="span 2 / span 2",
    )

def create_dashboard_grid():
    """Create the main dashboard grid layout."""
    return rx.box(
        create_main_content_section(),
        rx.box(
            create_section_heading(
                font_size="1.25rem",
                line_height="1.75rem",
                text="Conversation Transcript",
            ),
            create_conversation_transcript(),
            create_section_heading(
                font_size="1.25rem",
                line_height="1.75rem",
                text="Bookmarks",
            ),
            create_bookmarks(),
            grid_column="span 1 / span 1",
            display="flex",
            flex_direction="column",
            gap="1.5rem",
        ),
        gap="1.5rem",
        display="grid",
        grid_template_columns="repeat(3, minmax(0, 1fr))",
    )


def create_dashboard_content():
    """Create the main content of the dashboard including all sections."""
    return rx.box(
        rx.heading(
            "William's Conversation Summary",
            font_weight="700",
            margin_bottom="2rem",
            font_size="1.875rem",
            line_height="2.25rem",
            as_="h1",
        ),
        create_dashboard_grid(),
        background_color="#ffffff",
        max_width="80rem",
        margin_left="auto",
        margin_right="auto",
        padding="1.5rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    )


def create_dashboard_page():
    """Create the complete dashboard page with styling and content."""
    return rx.fragment(
        rx.script(src="https://cdn.tailwindcss.com"),
        rx.el.style(
            """
    @font-face {
        font-family: 'LucideIcons';
        src: url(https://unpkg.com/lucide-static@latest/font/Lucide.ttf) format('truetype');
    }
    """
        ),
        rx.box(
            create_dashboard_content(),
            background_color="#F3F4F6",
            min_height="100vh",
            padding="2rem",
        ),
    )