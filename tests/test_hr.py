# pylint: disable=missing-function-docstring
from tests.assets.cv import CANDIDATE_ID
from tests.assets.requests_validatiion_constants import METHOD_NOT_IMPLEMENTED


def test_get_single_skill_summary(client):
    response = client.get("/hr/skills/python")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED


def test_get_skills_summary(client):
    response = client.get("/hr/skills")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED


def test_get_candidate_cv_hr(client):
    response = client.get(f"/hr/candidates/{CANDIDATE_ID}")
    assert response.status_code == 501
    assert response.json == METHOD_NOT_IMPLEMENTED
