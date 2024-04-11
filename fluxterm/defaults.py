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
