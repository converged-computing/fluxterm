from rich.syntax import Syntax
from rich.traceback import Traceback

import fluxterm.defaults as defaults
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.screen import Screen
from textual.widgets import DirectoryTree, Footer, Header, Static


class CodeBrowser(Static):
    """
    A code browser widget
    """

    BINDINGS = [
        ("f", "toggle_files", "Files"),
    ] + defaults.GLOBAL_BINDINGS

    def compose(self) -> ComposeResult:
        # Only allow browsing the PWD
        path = "./"
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
