from __future__ import annotations

from typing import Any


VALID_DISPOSITIONS = {
    "ELIGIBLE",
    "FOUNDATION_ONLY",
    "OUT_OF_SCOPE",
    "REQUIRES_REVIEW",
}


def qp_key(row: dict[str, Any]) -> tuple[str, str]:
    concept_id = row.get("concept_id")
    qp_id = row.get("qp_id")
    if not isinstance(concept_id, str) or not concept_id.strip():
        raise ValueError("QP concept_id must be a non-empty string.")
    if not isinstance(qp_id, str) or not qp_id.strip():
        raise ValueError("QP qp_id must be a non-empty string.")
    return concept_id, qp_id


def validate_catalog_response(
    *,
    response: Any,
    input_qps: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Validate one disposition-aware QP/archetype batch or persisted catalogue."""
    if not isinstance(response, dict):
        raise ValueError("Catalogue response must be a JSON object.")
    if set(response) != {"qp_dispositions", "archetypes"}:
        raise ValueError(
            "Catalogue response must contain exactly "
            "'qp_dispositions' and 'archetypes'."
        )

    dispositions = response["qp_dispositions"]
    archetypes = response["archetypes"]
    if not isinstance(dispositions, list):
        raise ValueError("'qp_dispositions' must be a list.")
    if not isinstance(archetypes, list):
        raise ValueError("'archetypes' must be a list.")

    input_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for qp in input_qps:
        if not isinstance(qp, dict):
            raise ValueError("Every input QP must be an object.")
        key = qp_key(qp)
        if key in input_by_key:
            raise ValueError(f"Duplicate input QP key: {key}.")
        input_by_key[key] = qp

    disposition_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for index, item in enumerate(dispositions, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"QP disposition #{index} must be an object.")
        expected_fields = {"concept_id", "qp_id", "disposition", "rationale"}
        if set(item) != expected_fields:
            raise ValueError(
                f"QP disposition #{index} must contain exactly "
                f"{sorted(expected_fields)}."
            )
        key = qp_key(item)
        if key not in input_by_key:
            raise ValueError(f"Disposition references unknown QP: {key}.")
        if key in disposition_by_key:
            raise ValueError(f"Duplicate QP disposition: {key}.")
        status = item.get("disposition")
        if status not in VALID_DISPOSITIONS:
            raise ValueError(
                f"QP disposition for {key} must be one of "
                f"{sorted(VALID_DISPOSITIONS)}."
            )
        rationale = item.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ValueError(f"QP disposition for {key} needs a rationale.")
        disposition_by_key[key] = item

    missing = set(input_by_key) - set(disposition_by_key)
    if missing:
        raise ValueError(f"Missing QP dispositions: {sorted(missing)}.")

    archetypes_by_key: dict[tuple[str, str], list[dict[str, Any]]] = {
        key: [] for key in input_by_key
    }
    copied_fields = (
        "subject", "unit", "chapter", "subtopic", "concept_id",
        "concept", "qp_id", "question_possibility",
    )
    for index, archetype in enumerate(archetypes, start=1):
        if not isinstance(archetype, dict):
            raise ValueError(f"Archetype #{index} must be an object.")
        key = qp_key(archetype)
        if key not in input_by_key:
            raise ValueError(f"Archetype references unknown QP: {key}.")
        if disposition_by_key[key]["disposition"] != "ELIGIBLE":
            raise ValueError(f"Archetype references non-eligible QP {key}.")
        source = input_by_key[key]
        for field in copied_fields:
            if archetype.get(field) != source.get(field):
                raise ValueError(
                    f"Archetype #{index} field '{field}' does not exactly "
                    f"match source QP {key}."
                )
        archetypes_by_key[key].append(archetype)

    for key, item in disposition_by_key.items():
        if item["disposition"] == "ELIGIBLE":
            if not archetypes_by_key[key]:
                raise ValueError(
                    f"ELIGIBLE QP {key} must have at least one archetype."
                )
        elif archetypes_by_key[key]:
            raise ValueError(f"Non-eligible QP {key} cannot have archetypes.")

    return {
        "qp_dispositions": dispositions,
        "archetypes": archetypes,
    }


__all__ = ["VALID_DISPOSITIONS", "qp_key", "validate_catalog_response"]
