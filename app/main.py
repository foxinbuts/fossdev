"""Executable application entry point.

Delegates execution to the reusable `sales` domain library.
"""

import sys
from sales.cli import main

if __name__ == "__main__":
    sys.exit(main())
