from client_google_visual import find_keywords
from fixtures import visual_api_non_target, visual_api_target


def test_find_target_keywords():
    not_target = find_keywords(visual_api_non_target)
    target = find_keywords(visual_api_target)

    assert not_target is False
    assert target is True
