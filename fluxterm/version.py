__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2024, Vanessa Sochat, HPCIC Developer Tools"
__license__ = "MIT"

__version__ = "0.0.1"
AUTHOR = "Vanessa Sochat"
AUTHOR_EMAIL = "vsoch@users.noreply.github.com"
NAME = "fluxterm"
PACKAGE_URL = "https://github.com/converged-computing/flux-term"
KEYWORDS = "Flux framework, HPC, workload manager, jobs queue, textual"
DESCRIPTION = "Terminal application to interact with Flux jobs, cheat sheets, code, and good fortune"
LICENSE = "LICENSE"

################################################################################
# Global requirements

INSTALL_REQUIRES = (
    ("textual-dev", {"min_version": None}),
    ("pyaml", {"min_version": None}),
    ("rich-pixels", {"min_version": None}),
)

TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)
INSTALL_REQUIRES_ALL = INSTALL_REQUIRES + TESTS_REQUIRES
