#!/usr/bin/env python3
"""
check_xml_loc_duplicates.py

Detect duplicate <loc> entries in one or more XML files (e.g., sitemap.xml).

Usage:
  python check_xml_loc_duplicates.py              # auto-detect common sitemap path
  python check_xml_loc_duplicates.py _site/sitemap.xml
  python check_xml_loc_duplicates.py sitemap.xml search.xml
  python check_xml_loc_duplicates.py --fail-on-duplicates _site/sitemap.xml

Exit codes:
  0: success, no duplicates (unless --fail-on-duplicates and duplicates found)
  1: duplicates found with --fail-on-duplicates
  2: invalid input or file not found
"""

import argparse
import os
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from typing import Dict, List, Tuple


def extract_loc_values(xml_path: str) -> List[str]:
    """Parse XML and return all <loc> text values.

    Handles namespaced tags by comparing the localname (after any '}' in tag).
    """
    try:
        tree = ET.parse(xml_path)
    except FileNotFoundError:
        raise
    except ET.ParseError as e:
        raise RuntimeError(f"XML parse error in {xml_path}: {e}")

    root = tree.getroot()
    locs: List[str] = []
    for elem in root.iter():
        tag = getattr(elem, "tag", None)
        if isinstance(tag, str) and tag.split("}")[-1] == "loc":
            text = (elem.text or "").strip()
            if text:
                locs.append(text)
    return locs


def find_duplicates(values: List[str]) -> Tuple[Dict[str, int], Counter]:
    counts = Counter(values)
    dups = {v: c for v, c in counts.items() if c > 1}
    return dups, counts


def auto_default_path() -> str | None:
    """Pick a sensible default XML path if none provided."""
    candidates = [
        os.path.join("_site", "sitemap.xml"),
        "sitemap.xml",
        os.path.join("_site", "atom.xml"),
        "search.xml",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def find_duplicates_in_xml(xml_path: str) -> Dict:
    locs = extract_loc_values(xml_path)
    dups, counts = find_duplicates(locs)
    return {
        "file": xml_path,
        "total": len(locs),
        "unique": len(counts),
        "duplicates": dups,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check XML files for duplicate <loc> entries (handles namespaces)",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="XML file(s) to check; defaults to a common sitemap path if omitted",
    )
    parser.add_argument(
        "--fail-on-duplicates",
        action="store_true",
        help="Exit with code 1 if any duplicates are found",
    )
    args = parser.parse_args()

    paths = args.paths
    if not paths:
        default = auto_default_path()
        if default:
            paths = [default]
        else:
            print(
                "No input paths and no default XML found (expected _site/sitemap.xml or sitemap.xml).",
                file=sys.stderr,
            )
            sys.exit(2)

    overall_dup_found = False

    for p in paths:
        if not os.path.exists(p):
            print(f"Missing file: {p}", file=sys.stderr)
            overall_dup_found = True  # treat missing as failure in batch
            continue

        try:
            result = find_duplicates_in_xml(p)
        except (FileNotFoundError, RuntimeError) as e:
            print(str(e), file=sys.stderr)
            overall_dup_found = True
            continue

        dups = result["duplicates"]
        print(f"Checking {p}")
        print(f"Total loc: {result['total']}, Unique: {result['unique']}")
        if dups:
            overall_dup_found = True
            print("Duplicate loc values:")
            for v, c in sorted(dups.items(), key=lambda x: (-x[1], x[0])):
                print(f"{c} × {v}")
        else:
            print("No duplicates found.")
        print()

    if args.fail_on_duplicates and overall_dup_found:
        sys.exit(1)


if __name__ == "__main__":
    main()
