from time import perf_counter
from app.models import DResponse
from fastapi import Response, APIRouter


router = APIRouter(
    prefix="/series",
    tags=["internals"],
)


@router.get("/{id}", response_model=dict, status_code=200)
def series_id_route(response: Response, id: int) -> dict:
    init_time = perf_counter()
    from app.apis import mongo

    if results := list(mongo.series_col.find({"tmdb_id": id}, {"_id": 0})):
        result = results[0]
        return DResponse(
            200,
            f"Successfully retrieved a match for the TMDB ID {id}.",
            True,
            result,
            init_time,
        ).__json__()
    else:
        response.status_code = 404
        return DResponse(
            404,
            f"No series matching the TMDB ID {id} were found.",
            False,
            None,
            init_time,
        ).__json__()
