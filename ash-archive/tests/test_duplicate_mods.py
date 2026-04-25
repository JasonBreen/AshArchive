from tools.check_duplicate_mods import find_duplicates


def test_find_duplicate_ids_and_names() -> None:
    mods = [
        {"id": "a", "name": "Same"},
        {"id": "a", "name": "Same"},
        {"id": "b", "name": "Same"},
    ]
    dup_ids, dup_names = find_duplicates(mods)
    assert dup_ids == ["a"]
    assert dup_names == ["Same"]
