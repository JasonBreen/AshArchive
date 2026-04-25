from collections import defaultdict


def render_mod_sections(mods: list[dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for mod in mods:
        grouped[mod["category"]].append(mod)
    lines: list[str] = []
    for category in sorted(grouped):
        lines.append(f"## {category}")
        for mod in sorted(grouped[category], key=lambda m: m.get("priority", 9999)):
            engines = ", ".join(mod.get("engine", []))
            lines.append(
                f"- **{mod['name']}** (`{mod['id']}`) — status: `{mod['status']}`, "
                f"engine: `{engines}`, cross-edition: `{mod['cross_edition_status']}`. "
                f"Reason: {mod['decision_reason']}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
