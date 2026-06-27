from typing import Any

from fastapi.routing import APIRoute


class NoNullAPIRoute(APIRoute):
    """APIRoute that drops null fields from responses by default, so optional/audit
    columns (e.g. updated_at, deleted_at) that are unset don't clutter the JSON."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # APIRouter.add_api_route always passes response_model_exclude_none explicitly
        # (defaulting to False), so a plain setdefault would never take effect here.
        kwargs["response_model_exclude_none"] = True
        super().__init__(*args, **kwargs)
