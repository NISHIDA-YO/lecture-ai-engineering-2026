"""第5回 宿題（実装）: 検索結果に前後ページを付ける処理を確認する。APIは呼ばない。"""

import json

import pytest

from app import retrieval, tools


@pytest.fixture
def source(tmp_path, monkeypatch):
    """第1回に4ページ、第2回に2ページある小さな教材を用意する。"""
    def pages(n, count):
        return [{"id": f"lec{n:02d}-main-p{p:03d}", "title": f"第{n}回p{p}", "page": p,
                 "content": f"本文{n}-{p}"} for p in range(1, count + 1)]

    path = tmp_path / "lectures.json"
    path.write_text(json.dumps([
        {"id": "lec01-main", "title": "講義1", "content": [{"section": "章", "content": pages(1, 4)}]},
        {"id": "lec02-main", "title": "講義2", "content": [{"section": "章", "content": pages(2, 2)}]},
    ], ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(retrieval, "RAG_SOURCE", path)
    return path


def fake_search(page_ids):
    """search() の代わりに、指定したページを検索順位の順に返す。"""
    def search(query):
        pages = {p["page_id"]: p for p in retrieval.load_pages(retrieval.RAG_SOURCE)}
        return [{**pages[pid], "distance": 0.1 * i} for i, pid in enumerate(page_ids)]
    return search


def test_neighbors_are_added_without_duplicates(source, monkeypatch):
    # p2 と p3 が両方ヒット → p3 は p2 の「次」だが、ヒットとして1回だけ返す
    monkeypatch.setattr(retrieval, "search",
                        fake_search(["lec01-main-p002", "lec01-main-p003", "lec02-main-p001"]))
    result = retrieval.search_with_neighbors("質問")
    order = [(r["page_id"], r["role"]) for r in result["results"]]
    assert order == [
        ("lec01-main-p001", "neighbor"), ("lec01-main-p002", "hit"),
        ("lec01-main-p003", "hit"), ("lec01-main-p004", "neighbor"),
        ("lec02-main-p001", "hit"), ("lec02-main-p002", "neighbor"),
    ]
    assert result["hit_count"] == 3 and result["neighbor_count"] == 3
    neighbor = result["results"][0]
    assert neighbor["neighbor_of"] == "lec01-main-p002" and neighbor["offset"] == -1
    assert neighbor["content"] == "本文1-1"


def test_neighbors_stay_in_same_document(source, monkeypatch):
    # 第1回の最終ページ p4 の「次」に、第2回の p1 を付けない
    monkeypatch.setattr(retrieval, "search", fake_search(["lec01-main-p004"]))
    ids = [r["page_id"] for r in retrieval.search_with_neighbors("質問")["results"]]
    assert ids == ["lec01-main-p003", "lec01-main-p004"]


def test_window_zero_returns_hits_only(source, monkeypatch):
    monkeypatch.setattr(retrieval, "NEIGHBOR_WINDOW", 0)
    monkeypatch.setattr(retrieval, "search", fake_search(["lec01-main-p002"]))
    result = retrieval.search_with_neighbors("質問")
    assert [r["role"] for r in result["results"]] == ["hit"]


def test_tool_returns_error_as_json(monkeypatch):
    def broken(query):
        raise ValueError("検索語が空です。")
    monkeypatch.setattr(retrieval, "search", broken)
    data = json.loads(tools.search_materials_with_neighbors(""))
    assert data == {"error": "検索語が空です。", "results": []}
