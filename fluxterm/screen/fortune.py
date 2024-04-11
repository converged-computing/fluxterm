import os
import random

from rich_pixels import Pixels

import fluxterm.defaults as defaults
from textual.app import ComposeResult
from textual.containers import Center, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static

try:
    import flux
    import flux.job
    from flux.cli.fortune import fortunes

    handle = flux.Flux()
except ImportError:
    flux = None
    fortunes = [
        "If you want more help, check out <a href='https://flux-framework.readthedocs.org'>the Flux documentation</a>"
    ]


class FluxBird(Static):
    """
    Render the flux bird!
    """

    def compose(self) -> ComposeResult:
        pixels = Pixels.from_image_path(
            os.path.join(defaults.assets_dir, "fluxbird-small.png")
        )
        yield Static(pixels)


class Fortune(Static):
    def compose(self) -> ComposeResult:
        with Center():
            yield Static(random.choice(fortunes), classes="wisdom")


class HelpScreen(Screen):
    CSS = """
    Screen {
        align: center middle;
        align: center bottom;
    }
    .again-button {
        text-align: center;
        content-align: center middle;
        border: round;
    }
    .wisdom {
        border: wide white round;
        width: 40;
        height: 9;
        text-align: center;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(Fortune(), FluxBird(), id="fortunes")
        with Center():
            yield Button("Again!", id="fortune", classes="again-button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Triggers when the button presses and updates the fortune.
        """
        button_id = event.button.id
        if button_id == "fortune":
            fortune_display = self.query_one("#fortunes")
            wisdom = self.query("Fortune")
            bird = self.query("FluxBird")
            if wisdom:
                wisdom.last().remove()
            if bird:
                bird.last().remove()
            new_fortune = Fortune()
            new_bird = FluxBird()
            fortune_display.mount(new_fortune)
            fortune_display.mount(new_bird)
