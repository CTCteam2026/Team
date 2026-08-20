#!/usr/bin/env python3
"""
Back-test: feed each historical event's real inputs into the builder and compare
the model's output to the P&L that actually went out the door.

Run AFTER build_pl_template.py.  Requires LibreOffice for recalculation.
"""

import json
import shutil
import subprocess
import sys

import openpyxl

SRC = "CTC_Conference_PL_Builder.xlsx"
RECALC = "/root/.claude/skills/synced/xlsx/scripts/recalc.py"

# Scope-library row order (SCOPE!B4:B28)
SCOPE_ORDER = [
    "Planning, Timeline & Communications",
    "Meetings & Agendas",
    "Document Management (Admin Hours)",
    "Project Management (PM Hours)",
    "Venue Management: Logistics, Meeting Space",
    "Event Branding: Attendee Experience, Signage, Decor",
    "Registration: Onsite Check-In Only",
    "Registration: Online Build-Out + Onsite",
    "Food & Beverage",
    "Housing Logistics: Room Blocks, Reports, Overflow",
    "Programming: Audio Visual, Talent, Entertainment",
    "Exhibit Management",
    "Sponsorships: Opportunities & Sponsor Management",
    "Speaker Management: Prep & Onsite",
    "Third Party Vendors",
    "Financial Management",
    "Event Marketing: Strategy, Social, Email, Messaging",
    "Staff Management: Temporary Staff & Volunteers",
    "Reception / Tournament / Special Event Planning",
    "Post-Event: Reporting, Reconciliation, Debrief",
    "ENHANCEMENT: Graphic Design (web, signage, branding)",
    "ENHANCEMENT: Mobile App",
    "Stage Production & Scripting",
    "Venue Sourcing — Future Year (RFP, analysis, contracts)",
    "Site Visits",
]

CASES = [
    dict(
        key="LCT",
        name="LCT / Marine Recreation Assn 2026",
        inputs={"B8": 200, "B9": 35, "B10": 0, "B11": 25, "B12": 6,
                "B15": 3, "B16": 0, "B17": 0, "B19": 4,
                "B23": 2, "B24": 2, "B25": 1, "B26": 1},
        scope=["Planning, Timeline & Communications", "Meetings & Agendas",
               "Document Management (Admin Hours)", "Project Management (PM Hours)",
               "Venue Management: Logistics, Meeting Space",
               "Event Branding: Attendee Experience, Signage, Decor",
               "Food & Beverage", "Registration: Onsite Check-In Only",
               "Reception / Tournament / Special Event Planning",
               "Speaker Management: Prep & Onsite",
               "Staff Management: Temporary Staff & Volunteers",
               "Third Party Vendors",
               "Programming: Audio Visual, Talent, Entertainment",
               "Exhibit Management",
               "Post-Event: Reporting, Reconciliation, Debrief"],
        actual={"pre_hrs": 263, "pre_client": 22315,
                "onsite_hrs": 132, "onsite_client": 11100, "total_client": 33415},
    ),
    dict(
        key="AFCI",
        name="AFCI Studio Summit 2027",
        inputs={"B8": 500, "B9": 65, "B10": 19, "B11": 0, "B12": 5,
                "B15": 3, "B16": 1, "B17": 0, "B19": 9,
                "B23": 4, "B24": 2, "B25": 1, "B26": 1},
        scope=["Planning, Timeline & Communications", "Meetings & Agendas",
               "Document Management (Admin Hours)", "Project Management (PM Hours)",
               "Venue Management: Logistics, Meeting Space",
               "ENHANCEMENT: Graphic Design (web, signage, branding)",
               "Event Branding: Attendee Experience, Signage, Decor",
               "Registration: Online Build-Out + Onsite", "Third Party Vendors",
               "Financial Management",
               "Sponsorships: Opportunities & Sponsor Management",
               "Programming: Audio Visual, Talent, Entertainment",
               "Exhibit Management",
               "Post-Event: Reporting, Reconciliation, Debrief"],
        actual={"pre_hrs": 617, "pre_client": 51845,
                "onsite_hrs": 272, "onsite_client": 27800, "total_client": 79645},
    ),
    dict(
        key="WTUI",
        name="WTUI 2027",
        inputs={"B8": 1500, "B9": 200, "B10": 50, "B11": 0, "B12": 10,
                "B15": 4, "B16": 1, "B17": 0, "B19": 9,
                "B23": 4, "B24": 3, "B25": 1, "B26": 1},
        scope=["Planning, Timeline & Communications", "Meetings & Agendas",
               "Document Management (Admin Hours)", "Project Management (PM Hours)",
               "Programming: Audio Visual, Talent, Entertainment",
               "Exhibit Management", "Food & Beverage",
               "Event Branding: Attendee Experience, Signage, Decor",
               "ENHANCEMENT: Graphic Design (web, signage, branding)",
               "ENHANCEMENT: Mobile App",
               "Housing Logistics: Room Blocks, Reports, Overflow",
               "Registration: Online Build-Out + Onsite",
               "Sponsorships: Opportunities & Sponsor Management",
               "Staff Management: Temporary Staff & Volunteers",
               "Venue Management: Logistics, Meeting Space", "Third Party Vendors",
               "Event Marketing: Strategy, Social, Email, Messaging",
               "Stage Production & Scripting",
               "Reception / Tournament / Special Event Planning",
               "Post-Event: Reporting, Reconciliation, Debrief",
               "Venue Sourcing — Future Year (RFP, analysis, contracts)",
               "Site Visits"],
        actual={"pre_hrs": 1182, "pre_client": 107870,
                "onsite_hrs": 350, "onsite_client": 30725, "total_client": 138595},
    ),
]


def run_case(case):
    path = f"backtest_{case['key']}.xlsx"
    shutil.copy(SRC, path)
    wb = openpyxl.load_workbook(path)
    inp, sc = wb["INPUTS"], wb["SCOPE"]
    inp["B5"] = case["name"]
    for cell, val in case["inputs"].items():
        inp[cell] = val
    for n, item in enumerate(SCOPE_ORDER):
        sc.cell(row=4 + n, column=4,
                value="Yes" if item in case["scope"] else "No")
    wb.save(path)

    out = subprocess.run([sys.executable, RECALC, path, "200"],
                         capture_output=True, text=True)
    res = json.loads(out.stdout)
    if res.get("status") != "success":
        raise SystemExit(f"{case['key']}: recalc failed -> {res}")

    v = openpyxl.load_workbook(path, data_only=True)["P&L"]
    return {
        "pre_hrs": v["E48"].value, "pre_client": v["F48"].value,
        "onsite_hrs": v["E73"].value, "onsite_client": v["F73"].value,
        "total_client": v["C9"].value,       # subtotal, before admin fee
        "grand_client": v["C12"].value, "grand_cost": v["D12"].value,
        "grand_profit": v["E12"].value, "margin": v["F12"].value,
        "errors": res["total_errors"],
    }


def pct(model, actual):
    return "n/a" if not actual else f"{(model - actual) / actual:+.0%}"


print(f"{'EVENT':<34}{'METRIC':<18}{'MODEL':>12}{'ACTUAL':>12}{'DELTA':>9}")
print("-" * 85)
for case in CASES:
    m = run_case(case)
    a = case["actual"]
    for k, label in (("pre_hrs", "pre-planning hrs"),
                     ("pre_client", "pre-planning $"),
                     ("onsite_hrs", "onsite hrs"),
                     ("onsite_client", "onsite $"),
                     ("total_client", "client subtotal $")):
        print(f"{case['name'][:33]:<34}{label:<18}"
              f"{m[k]:>12,.0f}{a[k]:>12,.0f}{pct(m[k], a[k]):>9}")
    print(f"{'':<34}{'-> new grand total':<18}{m['grand_client']:>12,.0f}"
          f"{'':>12}{'':>9}   "
          f"(cost {m['grand_cost']:,.0f}, profit {m['grand_profit']:,.0f}, "
          f"margin {m['margin']:.1%}, formula errors {m['errors']})")
    print("-" * 85)
