import re
from pathlib import Path

from signal_ocean.supply.templates import get_supply_templates

DOCS = Path(__file__).resolve().parents[2] / "docs" / "supply.md"


def test_docs_template_table_matches_templates():
    text = DOCS.read_text(encoding="utf-8")

    codes = re.findall(r"^\| ([A-Z]{1,3}\d{1,2}[A-Z]?) \|", text, flags=re.M)

    assert tuple(codes) == tuple(t.code for t in get_supply_templates())
