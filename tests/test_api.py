"""API tests: routing, validation, and mocked extraction (no API key needed)."""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import api.main as main  # noqa: E402
from src.demo_extract import PolicyFlagResult, SyllabusExtraction, ValidationResult  # noqa: E402


@pytest.fixture()
def client():
    return TestClient(main.app)


def _fake_extraction():
    return SyllabusExtraction(
        course_code="CS 4641",
        instructor_email="prof@university.edu",
    )


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"


def test_api_info_lists_endpoints(client):
    r = client.get("/api")
    assert r.status_code == 200
    assert any("/extract" in e for e in r.json()["endpoints"])


def test_root_serves_ui(client):
    r = client.get("/", follow_redirects=True)
    assert r.status_code == 200


def test_extract_requires_input(client):
    r = client.post("/extract")
    assert r.status_code == 422


def test_extract_with_mocked_llm(client, monkeypatch):
    async def fake_run_analysis(result, *, client=None, debug=False):
        return (
            ValidationResult(grading_sums_to_100=True, grading_total=100.0),
            PolicyFlagResult(overall_severity="low"),
        )

    monkeypatch.setattr(main, "_get_client", lambda: object())
    monkeypatch.setattr(main, "extract_syllabus", lambda blocks, client, debug: _fake_extraction())
    monkeypatch.setattr(main, "run_analysis", fake_run_analysis)

    r = client.post("/extract", data={"text": "CS 4641 syllabus ..."})
    assert r.status_code == 200
    body = r.json()
    assert body["extraction"]["course_code"] == "CS 4641"
    assert body["validation"]["grading_sums_to_100"] is True


def test_extract_reports_missing_key_as_503(client, monkeypatch):
    def boom():
        raise RuntimeError("ANTHROPIC_API_KEY is not set")

    monkeypatch.setattr(main, "_get_client", boom)
    r = client.post("/extract", data={"text": "anything"})
    assert r.status_code == 503
