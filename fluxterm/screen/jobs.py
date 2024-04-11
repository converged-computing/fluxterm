from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static
import fluxterm.defaults as defaults

try:
    import flux
    import flux.job

    handle = flux.Flux()
except ImportError:
    flux = None
    fortunes = [
        "If you want more help, check out <a href='https://flux-framework.readthedocs.org'>the Flux documentation</a>"
    ]


class JobsScreen(Screen):
    """
    Show running flux jobs in a table
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield FluxJobs()
        yield Footer()


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
            state = defaults.JOB_STATES.get(j["state"].lower()) or j["state"]
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
