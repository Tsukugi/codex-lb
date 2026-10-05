from __future__ import annotations

from typing import cast

from app.core.openai.requests import ResponsesRequest
from app.core.types import JsonValue
from app.modules.proxy.replay_safety import (
    project_responses_input_for_account_neutral_fresh_replay,
    responses_payload_is_account_neutral_fresh_replay,
)


def client_history_for_owner_switch(payload: ResponsesRequest) -> ResponsesRequest | None:
    """Prepare supplied history for a fresh account without proving its completeness."""
    fresh_payload = payload.model_copy(update={"previous_response_id": None})
    if isinstance(payload.input, list) and payload.input:
        projection = project_responses_input_for_account_neutral_fresh_replay(
            cast(list[JsonValue], payload.input),
            stored_count=len(payload.input),
        )
        if projection is None:
            return None
        fresh_payload = fresh_payload.model_copy(update={"input": projection.input_items})
    if not responses_payload_is_account_neutral_fresh_replay(fresh_payload.to_replay_safety_payload()):
        return None
    return fresh_payload
