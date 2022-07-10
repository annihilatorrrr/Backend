import requests
from app.apis import mongo
from fastapi import APIRouter
from time import perf_counter
from app.models import DResponse
from xmlrpc.client import boolean
from typing import Union, Optional
from fastapi.responses import RedirectResponse


router = APIRouter(
    prefix="/subtitle",
    tags=["internals"],
)


@router.get("/{id}", status_code=200)
def subtitle(
    id: int, permanent: Optional[boolean] = True
) -> Union[dict, RedirectResponse]:
    init_time = perf_counter()

    if not (os_api_key := mongo.config["subtitles"].get("api_key")):
        return DResponse(
            401, "No Open Subtitles API key was provided.", False, None, init_time
        ).__json__()
    result = requests.post(
        "https://api.opensubtitles.com/api/v1/download",
        headers={"Api-Key": os_api_key},
        data={"file_id": id},
    ).json()["link"]
    return (
        RedirectResponse(result, status_code=307)
        if permanent is not True
        else RedirectResponse(result, status_code=308)
    )
