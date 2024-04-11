import os

import fluxterm.defaults as defaults
import fluxterm.screen as screens
from textual.app import App
from textual.reactive import var

try:
    import flux
except ImportError:
    flux = None


class Fluxterm(App):
    """
    Flux in a terminal is flux term.

    Nobody here ever claimed to be good at naming things.
    - Computer Scientists
    """

    CSS_PATH = os.path.join(defaults.assets_dir, "fluxterm.tcss")

    # This is bindings keys (e.g., "d" to functions)
    BINDINGS = defaults.GLOBAL_BINDINGS
    MODES = {
        "browser": screens.BrowserScreen,
        "docs": screens.DocsScreen,
        "help": screens.HelpScreen,
    }

    if flux is not None:
        BINDINGS.append(("j", "switch_mode('jobs')", "Flux Jobs"))
        MODES["jobs"] = screens.JobsScreen

    def on_mount(self) -> None:
        self.switch_mode("browser")

    show_tree = var(True)

    def action_toggle_files(self) -> None:
        """
        Called in response to key binding.
        """
        self.show_tree = not self.show_tree

    def watch_show_tree(self, show_tree: bool) -> None:
        """
        Called when show_tree is modified.
        """
        self.set_class(show_tree, "-show-tree")

    # Actions are tied to bindings. E.g., "toggle_dark" with d -> action_toggle_dark
    def action_toggle_dark(self) -> None:
        """
        Toggle dark mode.
        """
        self.dark = not self.dark
