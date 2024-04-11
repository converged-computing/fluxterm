import os

here = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(here, "assets")

GLOBAL_BINDINGS = [
    ("m", "toggle_dark", "Dark mode"),
    ("b", "switch_mode('browser')", "Code Browser"),
    ("c", "switch_mode('docs')", "Commands"),
    ("h", "switch_mode('help')", "Help"),
    ("q", "quit", "Quit"),
]

# It's confusing to distinguish job states from status, so I'll just
# provide lookups for all terms I find.
JOB_STATES = {
    "depend": "👀️",
    "sched": "📅️",
    "run": "🏃️",
    "cleanup": "🧹️",
    "inactive": "😴️",
    # These are "virtual" states that I'm not sure show up here
    "pending": "🦩️",
    "running": "🏃️",
    "active": "🟢️",
    # status
    "completed": "✅️",
    "failed": "🔴️",
    "cancelled": "✖️",
    "timeout": "⌛️",
}
