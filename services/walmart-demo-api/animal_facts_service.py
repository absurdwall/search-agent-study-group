import json
import random
from pathlib import Path
from typing import TypedDict


class AnimalFact(TypedDict):
    animal: str
    fact: str


class AnimalFactsService:
    def __init__(self, fixture: Path | None = None):
        fixture = fixture or Path(__file__).with_name("animal_facts.jsonl")
        facts: list[AnimalFact] = []

        for line_number, line in enumerate(fixture.read_text().splitlines(), start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid JSON on line {line_number}") from error

            if not isinstance(record, dict) or set(record) != {"animal", "fact"}:
                raise ValueError(
                    f"line {line_number} must contain exactly 'animal' and 'fact'"
                )
            if any(not isinstance(value, str) or not value.strip() for value in record.values()):
                raise ValueError(f"line {line_number} fields must be non-blank strings")

            facts.append(AnimalFact(animal=record["animal"], fact=record["fact"]))

        if not facts:
            raise ValueError("animal facts dataset is empty")

        self._facts = facts

    def random_fact(self) -> AnimalFact:
        selected = random.choice(self._facts)
        return AnimalFact(animal=selected["animal"], fact=selected["fact"])
