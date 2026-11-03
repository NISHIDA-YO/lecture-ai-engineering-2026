"""第3回 宿題（実装）: save_learning_log と承認フローのテスト（APIキー不要）。"""

from pydantic_ai import DeferredToolRequests, DeferredToolResults, ToolDenied
from pydantic_ai.models.test import TestModel

from app import tools
from app.agent import agent


def test_save_learning_log_writes_file(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path)
    msg = tools.save_learning_log("第3回 ツール/呼び出し", "requests は2回だった")
    files = list(tmp_path.glob("*.md"))
    assert len(files) == 1 and "保存しました" in msg
    assert "/" not in files[0].name.removesuffix(".md").split("_", 2)[-1]
    assert "requests は2回だった" in files[0].read_text(encoding="utf-8")


def test_save_learning_log_rejects_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path)
    assert "保存はしていません" in tools.save_learning_log(" ", "")
    assert not list(tmp_path.glob("*.md"))


def _run_until_approval(model):
    with agent.override(model=model):
        result = agent.run_sync("今日学んだことを記録して")
    assert isinstance(result.output, DeferredToolRequests)
    assert [c.tool_name for c in result.output.approvals] == ["save_learning_log"]
    return result


def test_save_waits_for_approval_then_saves(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path)
    model = TestModel(call_tools=["save_learning_log"])
    result = _run_until_approval(model)
    assert not list(tmp_path.glob("*.md"))  # 承認前は保存されない

    call_id = result.output.approvals[0].tool_call_id
    with agent.override(model=model):
        agent.run_sync(
            message_history=result.all_messages(),
            deferred_tool_results=DeferredToolResults(approvals={call_id: True}),
        )
    assert len(list(tmp_path.glob("*.md"))) == 1


def test_denied_save_does_not_write(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path)
    model = TestModel(call_tools=["save_learning_log"])
    result = _run_until_approval(model)

    call_id = result.output.approvals[0].tool_call_id
    with agent.override(model=model):
        final = agent.run_sync(
            message_history=result.all_messages(),
            deferred_tool_results=DeferredToolResults(approvals={call_id: ToolDenied("不許可")}),
        )
    assert isinstance(final.output, str)
    assert not list(tmp_path.glob("*.md"))
