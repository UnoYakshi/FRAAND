"""HTML-templates module, based on Jinja2 (somewhat was ported from Django)..."""

from typing import Any, Collection

from fastapi.templating import Jinja2Templates

from src.fraand_core.constants import TEMPLATES_ABS_FILE_PATH

app_templates = Jinja2Templates(directory=TEMPLATES_ABS_FILE_PATH, auto_reload=True)


def jinja2_filter_enumerate(sequence: Collection) -> Collection[tuple[int, Any]]:
    """Simple ``enumerate()`` for Jinja2..."""

    return zip(range(0, len(sequence)), sequence, strict=True)


app_templates.env.filters['enumerate'] = jinja2_filter_enumerate
