from tools.summarize_sourced_mods import generate_summary

FIXTURE_CANDIDATES = [
    {
        "id": "sample-candidate",
        "name": "Sample Candidate",
        "candidate_status": "candidate",
        "thematic_bucket": "foundation",
        "intended_editions": ["openmw"],
        "compatibility_status": "unverified",
        "risk_level": "low",
        "source_confidence": "likely",
    }
]


def test_generate_summary_output_structure() -> None:
    summary = generate_summary(FIXTURE_CANDIDATES)

    assert "Sourced mod candidates (intake desk)" in summary
    assert "Total: 1" in summary
    assert "[foundation]" in summary
    assert (
        "id | name | candidate_status | intended_editions | compatibility_status | risk_level | source_confidence"
        in summary
    )
    assert (
        "sample-candidate | Sample Candidate | candidate | openmw | unverified | low | likely"
        in summary
    )


def test_main_with_errors(capsys) -> None:
    import sys
    from unittest.mock import patch

    from tools.summarize_sourced_mods import main

    with patch.object(sys, "argv", ["summarize_sourced_mods.py", "--file", "dummy.meta"]):
        with patch("tools.summarize_sourced_mods.validate_sourced_mods") as mock_validate:
            mock_validate.return_value = ([], ["[ERROR] Some validation error"])
            result = main()

    assert result == 1
    captured = capsys.readouterr()
    assert "[ERROR] Some validation error" in captured.out


def test_main_with_valid_fixture(capsys) -> None:
    import sys
    from unittest.mock import patch

    from tools.summarize_sourced_mods import main

    with patch.object(sys, "argv", ["summarize_sourced_mods.py", "--file", "dummy.meta"]):
        with patch("tools.summarize_sourced_mods.validate_sourced_mods") as mock_validate:
            mock_validate.return_value = (FIXTURE_CANDIDATES, [])
            result = main()

    assert result == 0
    captured = capsys.readouterr()
    assert "Sourced mod candidates (intake desk)" in captured.out
    assert (
        "sample-candidate | Sample Candidate | candidate | openmw | unverified | low | likely"
        in captured.out
    )
