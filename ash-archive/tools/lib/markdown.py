from __future__ import annotations

from collections import defaultdict


def _sanitize_inline(value: str) -> str:
    return " ".join(value.replace("`", "'").splitlines()).strip()


def render_mod_sections(mods: list[dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for mod in mods:
        grouped[mod["category"]].append(mod)
    lines: list[str] = []
    for category in sorted(grouped):
        lines.append(f"## {_sanitize_inline(category)}")
        for mod in sorted(grouped[category], key=lambda m: m.get("priority", 9999)):
            engines = ", ".join(mod.get("engine", []))
            lines.append(
                f"- **{_sanitize_inline(mod['name'])}** "
                f"(`{_sanitize_inline(mod['id'])}`) — status: `{_sanitize_inline(mod['status'])}`, "
                f"engine: `{_sanitize_inline(engines)}`, "
                f"cross-edition: `{_sanitize_inline(mod['cross_edition_status'])}`. "
                f"Reason: {_sanitize_inline(mod['decision_reason'])}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
