from fluxterm.command import make_commands
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, MarkdownViewer

markdown, data = make_commands()


class DocsScreen(Screen):
    """
    The docs screen renders the flux cheat sheet as markdown.
    """

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
