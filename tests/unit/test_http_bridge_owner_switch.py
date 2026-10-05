from __future__ import annotations

import pytest

from app.core.openai.requests import ResponsesRequest
from app.core.types import JsonValue
from app.modules.proxy._service.http_bridge.owner_switch import client_history_for_owner_switch

pytestmark = pytest.mark.unit


def test_owner_switch_uses_a_delta_without_a_response_anchor() -> None:
    payload = ResponsesRequest.model_validate(
        {"model": "gpt-5.1", "instructions": "", "previous_response_id": "resp_old", "input": "continue"}
    )
    fresh = client_history_for_owner_switch(payload)
    assert fresh is not None
    assert fresh.previous_response_id is None
    assert fresh.input == payload.input
    assert payload.previous_response_id == "resp_old"


def test_owner_switch_projects_response_bookkeeping_and_keeps_tool_context() -> None:
    payload = ResponsesRequest.model_validate(
        {
            "model": "gpt-5.1",
            "instructions": "",
            "previous_response_id": "resp_old",
            "input": [
                {"type": "reasoning", "id": "rs_old", "encrypted_content": "old-account", "summary": []},
                {
                    "type": "function_call",
                    "id": "fc_old",
                    "call_id": "call_1",
                    "name": "inspect",
                    "arguments": "{}",
                },
                {"type": "function_call_output", "call_id": "call_1", "output": "done"},
                {"role": "user", "content": "continue"},
            ],
        }
    )
    fresh = client_history_for_owner_switch(payload)
    assert fresh is not None
    assert fresh.input == [
        {"type": "function_call", "call_id": "call_1", "name": "inspect", "arguments": "{}"},
        {"type": "function_call_output", "call_id": "call_1", "output": "done"},
        {"role": "user", "content": "continue"},
    ]


@pytest.mark.parametrize(
    "extra",
    [
        pytest.param({"conversation": "conv_old"}, id="stored-conversation"),
        pytest.param(
            {"input": [{"role": "user", "content": [{"type": "input_file", "file_id": "file_old"}]}]},
            id="account-file",
        ),
        pytest.param(
            {"input": [{"type": "function_call_output", "call_id": "missing", "output": "orphan"}]},
            id="orphan-tool-output",
        ),
        pytest.param({"input": [{"type": "item_reference", "id": "msg_old"}]}, id="stored-item"),
    ],
)
def test_owner_switch_rejects_account_owned_or_unresolved_input(extra: dict[str, JsonValue]) -> None:
    payload = ResponsesRequest.model_validate({"model": "gpt-5.1", "instructions": "", "input": "continue", **extra})
    assert client_history_for_owner_switch(payload) is None
