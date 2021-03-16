from fastapi.responses import JSONResponse
from typing import Any
from orjson import dumps

class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return dumps(content)
        