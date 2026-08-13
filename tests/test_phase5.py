import json

from v_astra.integrations.claude_code import ClaudeCodeAdapter
from v_astra.cli.claude import run


def test_prompt_optimized_and_metadata_preserved():
    payload = {
        "prompt": "hello\n\n\nworld",
        "session_id": "session-123",
        "hook_event_name": "UserPromptSubmit",
    }

    result = ClaudeCodeAdapter().optimize_payload(payload)

    assert result["session_id"] == "session-123"
    assert result["hook_event_name"] == "UserPromptSubmit"
    assert result["prompt"] == "hello\nworld"


def test_non_prompt_fields_are_preserved():
    payload = {
        "prompt": "hello",
        "cwd": "/tmp/project",
        "extra": {"keep": True},
    }

    result = ClaudeCodeAdapter().optimize_payload(payload)

    assert result["cwd"] == "/tmp/project"
    assert result["extra"] == {"keep": True}


def test_messages_payload_supported():
    payload = {
        "messages": [
            {"role": "user", "content": "hello\n\n\nhello\n\n\nhello"}
        ],
        "custom": "keep",
    }

    result = ClaudeCodeAdapter().optimize_payload(payload)

    assert result["custom"] == "keep"
    assert result["messages"][0]["content"] == "hello [x3]"


def test_cli_hook_round_trip(monkeypatch, capsys):
    payload = {
        "prompt": "hello\n\n\nworld",
        "session_id": "abc",
    }

    monkeypatch.setattr("sys.stdin", type("S", (), {"read": lambda self: json.dumps(payload)})())
    assert run() == 0

    output = json.loads(capsys.readouterr().out)
    assert output["prompt"] == "hello\nworld"
    assert output["session_id"] == "abc"


def test_cli_rejects_non_object(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", type("S", (), {"read": lambda self: "[]"} )())
    assert run() == 2
    assert "JSON object" in capsys.readouterr().err
