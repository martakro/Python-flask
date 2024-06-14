from flask import abort


def get_all_cvs():
    """
    Returns list of all available candidates - for HR purposes
    """
    abort(501)


def get_cv_details(
    candidate_id: int,
):  # unit testy, assert type candidate_id, kiedy wykonuja sie asercje  w pythonie, typ w route(?)
    """
    Returns candidate cv for precised candidate_id
    :param candidate_id - candiddate_id
    """

    print(candidate_id)

    abort(501)


def get_candidates_skills_summary():
    """
    Returns skills summary, number of candidates with concrete skill and its level
    """
    abort(501)


def get_separate_skill_summary(skill: str):
    """
    Returns information about number of candidates which have passed skill with its level
    :param name - name
    """

    print(skill)
    abort(501)
