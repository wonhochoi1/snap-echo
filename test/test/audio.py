import reflex as rx
from .backend.backend import State

def create_icon(icon_name):
    """Creates an icon element with specified tag and styling."""
    return rx.icon(
        tag=icon_name,
        height="1.25rem",
        margin_right="0.5rem",
        width="1.25rem",
    )


def create_start_recording_button():
    """Creates a styled 'Start Recording' button with a microphone icon."""
    return rx.el.button(
        create_icon(icon_name="mic"),
        " Start Recording ",
        id="recordButton",
        background_color="#EF4444",
        display="flex",
        align_items="center",
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_radius="9999px",
        color="#ffffff",
        on_click=State.start_recording,
        disabled=State.isRecording,
    )


def create_recording_status_display():
    """Creates a box containing recording status and time display."""
    return rx.box(
        rx.text(
            "Not recording",
            id="recordingStatus",
            color="#4B5563",
        ),
        rx.text(
            "00:00",
            id="recordingTime",
            font_weight="600",
            font_size="1.25rem",
            line_height="1.75rem",
        ),
        margin_bottom="1.5rem",
        text_align="center",
    )


def create_stop_recording_button():
    """Creates a styled 'Stop Recording' button with a square icon."""
    return rx.el.button(
        create_icon(icon_name="square"),
        " Stop Recording ",
        id="stopButton",
        disabled=State.isRecording==False,
        background_color="#D1D5DB",
        display="flex",
        align_items="center",
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_radius="9999px",
        color="#374151",
        on_click=State.stop_recording,
    )


def create_analytics_link():
    """Creates a styled link to the analytics page with a bar chart icon."""
    return rx.box(
        rx.el.a(
            create_icon(icon_name="bar-chart"),
            " View Analytics ",
            href="/analytics",
            display="flex",
            _hover={"text-decoration": "underline"},
            align_items="center",
            justify_content="center",
            color="#3B82F6",
            disabled=State.hasRecorded==False,
            on_click=State.analyze_transcript, #TODO: Change to submit transcript to upload full transcript to State
        ),
        text_align="center",
    )


def create_audio_recorder_container():
    """Creates the main container for the audio recorder interface."""
    return rx.box(
        rx.heading(
            "Good Morning William!",
            font_weight="700",
            margin_bottom="1.5rem",
            font_size="1.5rem",
            line_height="2rem",
            text_align="center",
            as_="h1",
        ),
        rx.flex(
            create_start_recording_button(),
            display="flex",
            justify_content="center",
            margin_bottom="1.5rem",
        ),
        create_recording_status_display(),
        rx.flex(
            create_stop_recording_button(),
            display="flex",
            justify_content="center",
            margin_bottom="1.5rem",
        ),
        create_analytics_link(),
        background_color="#ffffff",
        padding="2rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        width="24rem",
    )


def create_audio_recorder_page():
    """Creates the complete audio recorder page with styling and layout."""
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
            create_audio_recorder_container(),
            background_color="#F3F4F6",
            display="flex",
            align_items="center",
            justify_content="center",
            min_height="100vh",
        ),
    )