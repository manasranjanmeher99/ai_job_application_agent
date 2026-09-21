import os

import pytest

from src import tracker

TEST_DB = "test_applications.db"


@pytest.fixture(autouse=True)
def clean_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    tracker.init_db(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_add_and_get_application():
    app_id = tracker.add_application(
        company="Acme Corp", role="Data Scientist", job_url="https://x.com",
        match_score=87.5, status="Applied", notes="Great fit", db_path=TEST_DB,
    )
    apps = tracker.get_applications(TEST_DB)
    assert len(apps) == 1
    assert apps[0]["id"] == app_id
    assert apps[0]["company"] == "Acme Corp"
    assert apps[0]["match_score"] == 87.5


def test_update_status():
    app_id = tracker.add_application(company="Acme", role="ML Engineer", db_path=TEST_DB)
    tracker.update_status(app_id, "Interviewing", db_path=TEST_DB)
    apps = tracker.get_applications(TEST_DB)
    assert apps[0]["status"] == "Interviewing"


def test_delete_application():
    app_id = tracker.add_application(company="Acme", role="ML Engineer", db_path=TEST_DB)
    tracker.delete_application(app_id, db_path=TEST_DB)
    assert tracker.get_applications(TEST_DB) == []
