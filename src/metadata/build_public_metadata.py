"""
Build public metadata from the author's private Excel inventory.

The private workbook can contain source URLs and informal collection notes.
This script intentionally excludes both from public outputs.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


MUNICIPALITIES = {"北京市", "天津市", "上海市", "重庆市"}


def clean_code(value) -> str:
    if pd.isna(value):
        return ""
    s = str(value).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s.zfill(6) if s.isdigit() else s


def parse_missing(value, start, end) -> set[int]:
    if pd.isna(value) or str(value).strip() == "":
        return set()

    s = str(value)
    s = (
        s.replace("。", ".").replace("、", ".").replace("，", ".")
         .replace(",", ".").replace("；", ".").replace(";", ".")
         .replace("—", "-").replace("–", "-").replace("至", "-")
    )

    out = set()

    for a, b in re.findall(r"((?:19|20)\d{2})\s*-\s*((?:19|20)\d{2})", s):
        out.update(range(int(a), int(b) + 1))
    s = re.sub(r"((?:19|20)\d{2})\s*-\s*((?:19|20)\d{2})", "", s)

    for token in re.findall(r"(?<!\d)((?:19|20)\d{6})(?!\d)", s):
        out.update([int(token[:4]), int(token[4:])])
        s = s.replace(token, "")

    out.update(int(y) for y in re.findall(r"(?<!\d)((?:19|20)\d{2})(?!\d)", s))
    return {y for y in out if int(start) <= y <= int(end)}


def compress_years(years: set[int]) -> str:
    years = sorted(years)
    if not years:
        return ""

    pieces = []
    a = b = years[0]

    for year in years[1:]:
        if year == b + 1:
            b = year
        else:
            pieces.append(str(a) if a == b else f"{a}-{b}")
            a = b = year

    pieces.append(str(a) if a == b else f"{a}-{b}")
    return ", ".join(pieces)


def build(input_xlsx: str, output_dir: str) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    coverage = pd.read_excel(input_xlsx, sheet_name="City Coverage")
    changes = pd.read_excel(input_xlsx, sheet_name="changes")

    city_rows = []
    year_rows = []

    for _, row in coverage.iterrows():
        start = int(row["Start year"])
        end = int(row["End year"])
        missing = parse_missing(row["Missing years"], start, end)
        unit_type = "municipality" if row["City"] in MUNICIPALITIES else "prefecture-level city"

        city_rows.append({
            "province": row["Province"],
            "province_code": clean_code(row["Pro code"]),
            "city": row["City"],
            "city_code": clean_code(row["City_code"]),
            "unit_type": unit_type,
            "start_year": start,
            "end_year": end,
            "missing_years": compress_years(missing),
            "verified": "yes" if str(row["checked"]).strip() == "√" else "no",
        })

        for year in range(start, end + 1):
            year_rows.append({
                "province": row["Province"],
                "province_code": clean_code(row["Pro code"]),
                "city": row["City"],
                "city_code": clean_code(row["City_code"]),
                "unit_type": unit_type,
                "year": year,
                "status": "missing" if year in missing else "available",
            })

    pd.DataFrame(city_rows).to_csv(
        out / "city_coverage.csv", index=False, encoding="utf-8-sig"
    )
    pd.DataFrame(year_rows).to_csv(
        out / "city_year_coverage.csv", index=False, encoding="utf-8-sig"
    )

    changes = changes.rename(columns={
        "序号":"event_id",
        "批复/公告年":"approval_year",
        "批复或公告日":"approval_or_announcement_date",
        "省级行政区":"province",
        "事件类型":"event_type",
        "变更前单位":"pre_change_unit",
        "旧代码(6位文本)":"old_code",
        "变更后单位":"post_change_unit",
        "新代码(6位文本)":"new_code",
        "现行/去向":"current_destination",
        "现行/去向代码":"current_destination_code",
        "变更内容与辖区说明":"description",
    })

    public_cols = [
        "event_id","approval_year","approval_or_announcement_date","province","event_type",
        "pre_change_unit","old_code","post_change_unit","new_code",
        "current_destination","current_destination_code","description",
    ]
    changes[public_cols].to_csv(
        out / "prefecture_changes_2000_2018.csv",
        index=False,
        encoding="utf-8-sig",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_xlsx")
    parser.add_argument("--output-dir", default="metadata")
    args = parser.parse_args()
    build(args.input_xlsx, args.output_dir)


if __name__ == "__main__":
    main()
