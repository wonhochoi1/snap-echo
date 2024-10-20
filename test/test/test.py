"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from test.audio import create_audio_recorder_page  # Adjusted import path
from test.dash import create_dashboard_page
from .backend.backend import State


def index() -> rx.Component:
    # Welcome Page (Index)
    return create_audio_recorder_page()
    # return create_dashboard_page() 


app = rx.App()
app.add_page(index)
app.add_page(create_dashboard_page, route="analytics", on_load=State.fetch_transcript)
# app.add_page(create_dashboard_page, route="analytics", on_load=State.analyze_transcript)