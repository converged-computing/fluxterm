#!/usr/bin/env python3

# usage:
# python fluxterm.py

import sys
import random

from rich.syntax import Syntax
from rich.traceback import Traceback
from rich_pixels import Pixels

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, Center, ScrollableContainer
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import (
    Button,
    DirectoryTree,
    MarkdownViewer,
    Footer,
    Header,
    Static,
    DataTable,
)

import yaml
import os

here = os.path.dirname(os.path.abspath(__file__))

GLOBAL_BINDINGS = [
    ("m", "toggle_dark", "Dark mode"),
    ("b", "switch_mode('browser')", "Code Browser"),
    ("c", "switch_mode('docs')", "Commands"),
    ("h", "switch_mode('help')", "Help"),
    ("q", "quit", "Quit"),
]


def read_yaml(filename):
    with open(filename, "r") as fd:
        data = yaml.safe_load(fd)
    return data


try:
    import flux
    import flux.job
    from flux.cli.fortune import fortunes, art

    handle = flux.Flux()
except:
    flux = None
    fortunes = [
        "If you want more help, check out <a href='https://flux-framework.readthedocs.org'>the Flux documentation"
    ]

markdown = None
data = None


def make_commands():
    """
    Read in commands from yaml
    """
    global markdown
    global data
    data = read_yaml(os.path.join(here, "flux-commands.yaml"))["commands"]
    lines = ["# Flux Commands"]
    for command in data:
        lines.append(f"\n## {command['name']}")
        for group in command["groups"]:
            lines.append(f"\n### {group['name']}\n")
            for example in group["items"]:
                lines.append(example["title"] + "\n")
                lines.append(f"\n```bash\n{example['command']}\n````")
    markdown = "\n".join(lines)


make_commands()


class FluxJobs(Static):
    """
    Generate a table of flux jobs
    """

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        listing = flux.job.job_list(handle)

        # The first row are columns
        ROWS = [
            (
                "id",
                "user",
                "urgency",
                "priority",
                "state",
                "name",
                "cwd",
                "ntasks",
                "ncores",
                "duration",
                "nnodes",
                "ranks",
                "expiration",
            )
        ]
        for job in listing.get_jobinfos():
            j = job.to_dict()
            try:
                state = job.status_emoji
            except:
                state = j["state"]
            ROWS.append(
                (
                    j["id"],
                    j["userid"],
                    j["urgency"],
                    j["priority"],
                    state,
                    j["cwd"],
                    j["ntasks"],
                    j["ncores"],
                    j["duration"],
                    j["nnodes"],
                    j["ranks"],
                    j["expiration"],
                )
            )
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])


class CodeBrowser(Static):
    """
    A code browser widget
    """

    BINDINGS = [
        ("f", "toggle_files", "Files"),
    ] + GLOBAL_BINDINGS

    def compose(self) -> ComposeResult:
        path = "./" if len(sys.argv) < 2 else sys.argv[1]
        with Container():
            yield DirectoryTree(path, id="tree-view")
            with VerticalScroll(id="code-view"):
                yield Static(id="code", expand=True)

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected):
        """
        Called when the user click a file in the directory tree.
        """
        event.stop()
        code_view = self.query_one("#code", Static)
        try:
            syntax = Syntax.from_path(
                str(event.path),
                line_numbers=True,
                word_wrap=False,
                indent_guides=True,
                theme="github-dark",
            )
        except Exception:
            code_view.update(Traceback(theme="github-dark", width=None))
            self.sub_title = "ERROR"
        else:
            code_view.update(syntax)
            self.query_one("#code-view").scroll_home(animate=False)
            self.sub_title = str(event.path)

    def on_mount(self) -> None:
        self.query_one(DirectoryTree).focus()


class BrowserScreen(Screen):
    """
    A code browser widget
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield CodeBrowser()
        yield Footer()


class JobsScreen(Screen):
    """
    Show running flux jobs in a table
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield FluxJobs()
        yield Footer()


class DocsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield MarkdownViewer(markdown=markdown)
        yield Footer()

    @property
    def markdown_viewer(self) -> MarkdownViewer:
        return self.query_one(MarkdownViewer)

    async def on_mount(self) -> None:
        self.markdown_viewer.focus()

    def action_toggle_table_of_contents(self) -> None:
        self.markdown_viewer.show_table_of_contents = (
            not self.markdown_viewer.show_table_of_contents
        )

    async def action_back(self) -> None:
        await self.markdown_viewer.back()

    async def action_forward(self) -> None:
        await self.markdown_viewer.forward()

class FluxBird(Static):
    def compose(self) -> ComposeResult:
        pixels = Pixels.from_image_path("fluxbird-small.png")
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


class Fluxterm(App):
    """
    Flux in a terminal is flux term.

    Nobody here ever claimed to be good at naming things.
    - Computer Scientists
    """

    CSS_PATH = "fluxterm.tcss"

    # This is bindings keys (e.g., "d" to functions)
    BINDINGS = GLOBAL_BINDINGS
    MODES = {
        "browser": BrowserScreen,
        "docs": DocsScreen,
        "help": HelpScreen,
    }

    if flux is not None:
        BINDINGS.append(("j", "switch_mode('jobs')", "Flux Jobs"))
        MODES["jobs"] = JobsScreen

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


if __name__ == "__main__":
    app = Fluxterm()
    app.run()
