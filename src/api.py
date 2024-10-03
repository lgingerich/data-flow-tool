from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from schemas import URLInput, APIResponse
from utils import fetch_data, collect_metadata, infer_schema

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/fetch", response_model=APIResponse)
async def fetch_url(url_input: URLInput):
    response, data = fetch_data(url_input.url)
    if response and data:
        metadata = collect_metadata(response)
        schema = infer_schema(data)
        return APIResponse(metadata=metadata, schema=schema, data=data)
    else:
        return APIResponse(error="Failed to fetch data")
