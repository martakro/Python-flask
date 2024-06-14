# pylint: disable=missing-function-docstring, invalid-name, unused-variable, duplicate-code
from unittest.mock import create_autospec
from uuid import uuid4

import pytest
from db.models.cv_model import OrganizationModel, SkillModel
from exceptions.db_exceptions import DataExistsException
from logic.cv import CVRepository, add_cv
from models.cv import CV, Experience, Organization, Skill
from tests.assets.cv import CANDIDATE_ID

from .assets.fake_cv import fake_experience, fake_organizations, fake_skills

CANDIDATE_CV_VALID_DATA = {
    "experience": [
        {
            "employer": {
                "name": fake_organizations[index].name,
                "address": fake_organizations[index].address,
            },
            "project_description": exp.project_description,
            "years_of_employment": exp.years_of_employment,
        }
        for index, exp in enumerate(fake_experience)
    ],
    "skills": [{"level": skill.level, "skill": skill.skill} for skill in fake_skills],
}


CREATED_CV = {
    "candidate_id": str(CANDIDATE_ID),
    "id": 1,
    "experience": [
        {
            "id": index + 1,
            "employer": {
                "id": index + 1,
                "name": fake_organizations[index].name,
                "address": fake_organizations[index].address,
            },
            "project_description": exp.project_description,
            "years_of_employment": exp.years_of_employment,
        }
        for index, exp in enumerate(fake_experience)
    ],
    "skills": [
        {"id": index + 1, "level": skill.level, "skill": skill.skill}
        for index, skill in enumerate(fake_skills)
    ],
}

RAW_CV = CV(
    experience=[
        Experience(
            employer=Organization(
                name=fake_organizations[index].name,
                address=fake_organizations[index].address,
            ),
            project_description=exp.project_description,
            years_of_employment=exp.years_of_employment,
        )
        for index, exp in enumerate(fake_experience)
    ],
    skills=[Skill(level=skill.level, skill=skill.skill) for skill in fake_skills],
)


CV_VALID = CV(**CREATED_CV)
SKILL_INVALID_VALUE = {"level": ["skill level should be in range from 1 to 5"]}


def test_add_second_cv(session):
    add_cv_mock = create_autospec(add_cv, side_effect=DataExistsException)
    with pytest.raises(DataExistsException):
        add_cv_mock(session, CV(**CANDIDATE_CV_VALID_DATA))


def test_skills_are_not_unique(client):
    cv = {
        "candidate_id": CANDIDATE_ID,
        "skills": [
            {"level": 5, "skill": "Python"},
            {"level": 1, "skill": "Java"},
            {"level": 3, "skill": "Python"},
        ],
    }

    response = client.post("/my", json=cv)
    assert response.json == {"skills": ["Provided skills are not unique"]}
    assert response.status_code == 400


def test_doubled_experience_data(client):
    cv = {
        "candidate_id": CANDIDATE_ID,
        "experience": [
            {
                "employer": {
                    "name": fake_organizations[0].name,
                    "address": fake_organizations[0].address,
                },
                "project_description": fake_experience[0].project_description,
                "years_of_employment": 2,
            },
            {
                "employer": {
                    "name": fake_organizations[0].name,
                    "address": fake_organizations[0].address,
                },
                "project_description": fake_experience[0].project_description,
                "years_of_employment": 2,
            },
        ],
    }
    response = client.post("/my", json=cv)
    assert response.json == {"experience": ["Provided experience is not unique"]}
    assert response.status_code == 400


def test_add_empty_cv_to_db(session):
    raw_cv = expected_cv = CV(candidate_id=uuid4(), skills=[], experience=[])

    new_cv = CVRepository(session).create_cv(raw_cv)

    assert new_cv.candidate_id == expected_cv.candidate_id
    assert new_cv.skills == expected_cv.skills
    assert new_cv.experience == expected_cv.experience
    assert new_cv.candidate_id == expected_cv.candidate_id
    assert new_cv.id > 0


def test_add_cv_to_db(session):
    raw_cv = expected_cv = RAW_CV
    raw_cv.candidate_id = uuid4()

    new_cv = CVRepository(session).create_cv(raw_cv)

    assert new_cv.candidate_id == expected_cv.candidate_id
    assert new_cv.candidate_id == expected_cv.candidate_id
    assert new_cv.id > 0

    # how check skill and exp equality  ???


# def test_add_cv(client):
#     response = client.post("/my", json=CANDIDATE_CV_VALID_DATA)
#     assert response.json == CREATED_CV
#     assert response.status_code == 201

# czy test nie jest zbyt wysoko poziomowy ??


def test_add_empty_cv(client):
    response = client.post("/my", json={"experience": [], "skills": []})
    assert response.json == {
        "skills and experience": [
            "Provided cv has no data. Add at least one skill or experience"
        ]
    }
    assert response.status_code == 400


@pytest.mark.parametrize(
    "candidate_cv_data,expected_response,expected_status_code",
    [
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [{"skill": "Python", "level": -10}],
                "experience": [],
            },
            SKILL_INVALID_VALUE,
            400,
        ),
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [{"skill": "Python", "level": 0}],
                "experience": [],
            },
            SKILL_INVALID_VALUE,
            400,
        ),
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [{"skill": "Python", "level": 6}],
                "experience": [],
            },
            SKILL_INVALID_VALUE,
            400,
        ),
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [{"skill": "", "level": 3}],
                "experience": [],
            },
            {"skill": ["ensure this value has at least 1 characters"]},
            400,
        ),
    ],
)
def test_invalid_skill_level(
    candidate_cv_data, expected_response, expected_status_code, client
):
    response = client.post("/my", json=candidate_cv_data)
    assert response.json == expected_response
    assert response.status_code == expected_status_code


def test_invalid_skill_level_data_type(client):
    candidate_cv_data = {
        "skills": [{"skill": "Python", "level": "some_level"}],
        "experience": [],
    }

    response = client.post("/my", json=candidate_cv_data)
    assert response.json == {
        "detail": "'some_level' is not of type 'integer' - 'skills.0.level'",
        "status": 400,
        "title": "Bad Request",
        "type": "about:blank",
    }
    assert response.status_code == 400


def test_skill_without_level_value(client):
    candidate_cv_data = {
        "candidate_id": CANDIDATE_ID,
        "skills": [{"skill": "Python"}],
        "experience": [],
    }
    response = client.post("/my", json=candidate_cv_data)
    assert response.json == {"level": ["field required"]}
    assert response.status_code == 400


@pytest.mark.parametrize(
    "candidate_cv_data,expected_response,expected_status_code",
    [
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [],
                "experience": [
                    {
                        "employer": {"name": "", "address": "Zamość"},
                        "years_of_employment": 2,
                        "project_description": "some description",
                    }
                ],
            },
            {"name": ["ensure this value has at least 1 characters"]},
            400,
        ),
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [],
                "experience": [
                    {
                        "employer": {"name": "Company A", "address": ""},
                        "years_of_employment": 2,
                        "project_description": "some description",
                    }
                ],
            },
            {"address": ["ensure this value has at least 1 characters"]},
            400,
        ),
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [],
                "experience": [
                    {
                        "employer": {"name": "", "address": ""},
                        "years_of_employment": 2,
                        "project_description": "some description",
                    }
                ],
            },
            {
                "name": ["ensure this value has at least 1 characters"],
                "address": ["ensure this value has at least 1 characters"],
            },
            400,
        ),
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [],
                "experience": [
                    {
                        "employer": {"name": "Company A", "address": "Gdańsk"},
                        "years_of_employment": -4,
                        "project_description": "some description",
                    }
                ],
            },
            {
                "years_of_employment": [
                    "Years of employment value should be greater than 0"
                ]
            },
            400,
        ),
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [],
                "experience": [
                    {
                        "employer": {"name": "Company A", "address": "Gdańsk"},
                        "years_of_employment": 0,
                        "project_description": "some description",
                    }
                ],
            },
            {
                "years_of_employment": [
                    "Years of employment value should be greater than 0"
                ]
            },
            400,
        ),
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [],
                "experience": [
                    {
                        "employer": {"name": "Company A", "address": "Gdańsk"},
                        "years_of_employment": "AB",
                        "project_description": "some description",
                    }
                ],
            },
            {
                "years_of_employment": ["value is not a valid decimal"],
            },
            400,
        ),
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [],
                "experience": [
                    {
                        "employer": {"name": "Company A", "address": "Gdańsk"},
                        "years_of_employment": 3,
                        "project_description": "s" * 501,
                    }
                ],
            },
            {"project_description": ["ensure this value has at most 500 characters"]},
            400,
        ),
        (
            {
                "candidate_id": CANDIDATE_ID,
                "skills": [],
                "experience": [
                    {
                        "employer": {"name": "Company A", "address": "Gdańsk"},
                        "years_of_employment": 2,
                        "project_description": "",
                    }
                ],
            },
            {"project_description": ["ensure this value has at least 10 characters"]},
            400,
        ),
    ],
)
def test_experience_invalid_data(
    candidate_cv_data, expected_response, expected_status_code, client
):
    response = client.post("/my", json=candidate_cv_data)
    assert response.json == expected_response
    assert response.status_code == expected_status_code


def test_add_skill_duplicates_to_db(session):
    raw_cv = CV(
        skills=[Skill(level=3, skill="python"), Skill(level=4, skill="js")],
        experience=[],
    )

    raw_cv_2 = CV(
        skills=[Skill(level=3, skill="python"), Skill(level=4, skill="js")],
        experience=[],
    )

    new_cv = CVRepository(session).create_cv(raw_cv)
    skills_table_len_before_duplicates = session.query(SkillModel).all()
    new_cv_2 = CVRepository(session).create_cv(raw_cv_2)
    skills_table_len_after_duplicates = session.query(SkillModel).all()

    assert new_cv.skills == new_cv_2.skills
    assert skills_table_len_before_duplicates == skills_table_len_after_duplicates


def test_add_org_duplicates_to_db(session):
    raw_cv = CV(
        experience=[
            Experience(
                employer=Organization(
                    name=fake_organizations[index].name,
                    address=fake_organizations[index].address,
                ),
                project_description=exp.project_description,
                years_of_employment=exp.years_of_employment,
            )
            for index, exp in enumerate(fake_experience)
        ],
        skills=[],
    )

    raw_cv_2 = CV(
        experience=[
            Experience(
                employer=Organization(
                    name=fake_organizations[index].name,
                    address=fake_organizations[index].address,
                ),
                project_description=exp.project_description,
                years_of_employment=exp.years_of_employment,
            )
            for index, exp in enumerate(fake_experience)
        ],
        skills=[],
    )

    new_cv = CVRepository(session).create_cv(raw_cv)
    org_table_len_before_duplicates = session.query(OrganizationModel).all()
    new_cv_2 = CVRepository(session).create_cv(raw_cv_2)
    org_table_len_after_duplicates = session.query(OrganizationModel).all()

    assert [exp.employer for exp in new_cv.experience] == [
        exp.employer for exp in new_cv_2.experience
    ]
    assert org_table_len_before_duplicates == org_table_len_after_duplicates


def test_add_to_db_same_skills_with_diff_lvl(session):
    raw_cv = CV(
        skills=[Skill(level=3, skill="python"), Skill(level=4, skill="python")],
        experience=[],
    )
    with pytest.raises(ValueError):
        new_cv = CVRepository(session).create_cv(raw_cv)


def test_get_candidate_via_id(session):
    cv = RAW_CV
    cv.candidate_id = uuid4()
    add_cv = CVRepository(session).create_cv(cv)

    searched_cv = CVRepository(session).get_candidate_cv_via_id(add_cv.candidate_id)
    assert add_cv == searched_cv


# def test_add_cv_returns_correct_data(session):
#     new_cv = add_cv(session, RAW_CV)
#     assert new_cv == CV_OUTPUT

# do zastanowienia jak sprawdzic
