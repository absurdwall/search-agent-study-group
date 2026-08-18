import pytest

import animal_facts_service
from animal_facts_service import AnimalFactsService


def test_random_fact_returns_a_defensive_copy(tmp_path, monkeypatch):
    fixture = tmp_path / "facts.jsonl"
    fixture.write_text(
        '{"animal":"Octopus","fact":"An octopus has three hearts."}\n'
        '{"animal":"Cheetah","fact":"The cheetah is the fastest land animal."}\n'
    )
    monkeypatch.setattr(animal_facts_service.random, "choice", lambda records: records[0])
    facts = AnimalFactsService(fixture)
    selected = facts.random_fact()
    selected["fact"] = "changed"
    assert facts.random_fact() == {
        "animal": "Octopus",
        "fact": "An octopus has three hearts.",
    }


@pytest.mark.parametrize(
    ("contents", "error"),
    [
        ("", "dataset is empty"),
        ("not json\n", "line 1"),
        ('{"animal":"Octopus"}\n', "line 1"),
        ('{"animal":"Octopus","fact":"fact","habitat":"ocean"}\n', "line 1"),
        ('{"animal":7,"fact":"fact"}\n', "line 1"),
        ('{"animal":"   ","fact":"fact"}\n', "line 1"),
    ],
)
def test_invalid_fixture_raises_value_error(tmp_path, contents, error):
    fixture = tmp_path / "facts.jsonl"
    fixture.write_text(contents)

    with pytest.raises(ValueError, match=error):
        AnimalFactsService(fixture)
