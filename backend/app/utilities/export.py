import io
from fastapi.responses import StreamingResponse
from pandas import DataFrame
from app.models.databases.queries.base import LazyLoadResult
from app.utilities.logger import logger


def prepare_streaming_response(lazyload_result: LazyLoadResult) -> StreamingResponse:
    logger.debug(
        "Prepare Streaming Response",
        extra={
            "lazyload_result": lazyload_result,
        },
    )
    dataframe = DataFrame(
        columns=lazyload_result.columns,
        data=[x.dict(exclude_unset=True).values() for x in lazyload_result.data],
    )
    string_io = io.StringIO()
    dataframe.to_csv(string_io, index=False)
    response = StreamingResponse(
        iter([string_io.getvalue()]),
        media_type="text/csv",
    )
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response
