from uuid import uuid4

from models.cv import CV, Experience, Organization, Skill

CANDIDATE_ID = uuid4()
CV_OUTPUT = CV(
    id=1,
    candidate_id=CANDIDATE_ID,
    experience=[
        Experience(
            id=1,
            employer=Organization(id=1, name="Company A", address="Gdańsk"),
            project_description="pitu pitu pitu",
            years_of_employment=2,
        ),
        Experience(
            id=2,
            employer=Organization(
                id=2, name="Company B", address="Warszawa, al. Jerozolimskie 3"
            ),
            project_description="pitu pitu pitu",
            years_of_employment=0.5,
        ),
    ],
    skills=[
        Skill(id=1, level=5, skill="Python"),
        Skill(id=2, level=1, skill="Java"),
        Skill(id=3, level=3, skill="TS"),
    ],
)
