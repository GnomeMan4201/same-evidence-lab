#!/usr/bin/env python3
"""Compare Labeler 1 and Labeler 2 labels for the rival-naming study.

Committed before Labeler 2's labels were posted. It only checks and compares;
it does not decide outcomes. Every split is marked NEEDS ADJUDICATION and is
resolved by hand under ADJUDICATION_RULES.md, with the reason published.

Usage:
    python3 compare_labels.py LABELER1_FILE LABELER2_FILE

LABELER1_FILE  the file whose sha256 is in LABELER1_COMMITMENT.md (checked byte-for-byte)
LABELER2_FILE  Labeler 2's issue text, copied as-is (other lines and notes are ignored)

Standard library only. Exit code 0 = checks passed, 1 = a check failed.
"""
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LINE = re.compile(r"(case-[0-9a-f]{6})\s*[:=-]\s*([A-Ca-c](?:\s*[,/&]?\s*(?:and\s+)?[A-Ca-c])*)\b")


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def committed_hash():
    text = (HERE / "LABELER1_COMMITMENT.md").read_text(encoding="utf-8")
    m = re.search(r"sha256:\s*([0-9a-f]{64})", text)
    if not m:
        fail("no sha256 found in LABELER1_COMMITMENT.md")
    return m.group(1)


def worksheet_order():
    text = (HERE / "BLIND_LABELING.md").read_text(encoding="utf-8")
    return re.findall(r"^## (case-[0-9a-f]{6})\s*$", text, flags=re.M)


def parse(text, who, strict):
    labels = {}
    for raw in text.splitlines():
        m = LINE.search(raw)
        if not m:
            continue
        case = m.group(1)
        letters = frozenset(re.findall(r"[A-C]", m.group(2).upper()))
        if case in labels and labels[case] != letters:
            fail(f"{who}: {case} labeled twice with different answers")
        labels[case] = letters
    if strict:
        # Labeler 1's file must follow the committed format exactly.
        for raw in text.splitlines():
            if raw and not re.fullmatch(r"case-[0-9a-f]{6}: [A-C](, [A-C])*", raw):
                fail(f"{who}: line not in committed format: {raw!r}")
    return labels


def fmt(s):
    return ", ".join(sorted(s)) if s else "(none)"


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    f1, f2 = Path(sys.argv[1]), Path(sys.argv[2])
    order = worksheet_order()
    if len(order) != 24:
        fail(f"worksheet has {len(order)} cases, expected 24")

    raw1 = f1.read_bytes()
    got = hashlib.sha256(raw1).hexdigest()
    want = committed_hash()
    print(f"Labeler 1 file sha256: {got}")
    print(f"Committed sha256:      {want}")
    if got != want:
        fail("Labeler 1 file does not match the commitment. Do not compare.")
    print("OK: Labeler 1 file matches the commitment.\n")

    l1 = parse(raw1.decode("utf-8"), "Labeler 1", strict=True)
    l2 = parse(f2.read_text(encoding="utf-8"), "Labeler 2", strict=False)
    if list(l1) != order:
        fail("Labeler 1 cases are not exactly the worksheet cases in worksheet order")
    missing = [c for c in order if c not in l2]
    extra = [c for c in l2 if c not in order]
    if extra:
        fail(f"Labeler 2 has unknown cases: {extra}")
    if missing:
        print(f"NOTE: Labeler 2 has no label for {len(missing)} case(s): {missing}")
        print("      Ask before comparing; do not fill these in.\n")

    agree, split = [], []
    print(f"{'case':<13} {'L1':<9} {'L2':<9} result")
    for c in order:
        a, b = l1[c], l2.get(c)
        if b is None:
            res = "MISSING"
        elif a == b:
            res = "agree"
            agree.append(c)
        else:
            only1, only2 = fmt(a - b), fmt(b - a)
            res = f"NEEDS ADJUDICATION (only L1: {only1}; only L2: {only2})"
            split.append(c)
        print(f"{c:<13} {fmt(a):<9} {fmt(b) if b else '-':<9} {res}")

    n = len(order) - len(missing)
    print(f"\nExact agreement: {len(agree)}/{n} labeled cases")
    print(f"Splits to adjudicate by hand: {len(split)}")
    print("Reminder: a case either labeler flags as badly written is dropped even if labels agree.")


if __name__ == "__main__":
    main()
