"""HTML-templates module, based on Jinja2 (somewhat was ported from Django)..."""


from fastapi.templating import Jinja2Templates

from src.fraand_core.constants import TEMPLATES_ABS_FILE_PATH

app_templates = Jinja2Templates(directory=TEMPLATES_ABS_FILE_PATH, auto_reload=True)
