"""Legacy spiritual Render entry point.

The existing service URL remains valid. Upgraded Adalo clients can override this
default by passing ``spiritual=true`` or ``spiritual=false`` in the URL.
"""

import os
import runpy
from pathlib import Path


os.environ["COACH_EDGE_DEFAULT_SPIRITUAL"] = "true"
runpy.run_path(str(Path(__file__).with_name("coach_edge_app.py")), run_name="__main__")
