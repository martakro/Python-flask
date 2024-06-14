from random import randrange, uniform

from factory import Factory, Faker

from models.cv import Experience, Organization, Skill


class RandomOrganization(Factory):
    class Meta:
        model = Organization

    name = Faker("company")
    address = Faker("address")


class RandomExperience(Factory):
    class Meta:
        model = Experience

    employer = RandomOrganization()
    years_of_employment = uniform(0.1, 20)
    project_description = Faker("paragraph")


class RandomSkill(Factory):
    class Meta:
        model = Skill

    level = randrange(1, 6)
    skill = Faker("color_name")


fake_organizations = [RandomOrganization() for _ in range(2)]
fake_experience = [RandomExperience() for _ in range(2)]
fake_skills = [RandomSkill() for _ in range(3)]
