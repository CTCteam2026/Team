#!/usr/bin/env python3
"""
Builds the CTC Conference P&L Builder — an input-driven P&L template.

Every number in the P&L is a live formula. The only cells anyone types into are
the yellow ones on INPUTS and the two input columns on SCOPE.

Hour drivers are calibrated against four final, accurate P&Ls:
  - LCT / Marine Recreation Association Annual 2026 (FINAL June.10.2026 v3)
  - AFCI Studio Summit 2027            (FINAL July.27.2026 v2)
  - WTUI 2027                          (FINAL June.24.2026 v2)
  - NICA 2026                          (Actual NICA 2026)

Run:  python3 build_pl_template.py
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = "CTC_Conference_PL_Builder.xlsx"

# ---------------------------------------------------------------- styling ----
FONT = "Arial"
NAVY = "1F3864"
TEAL = "2E7D8F"
GREY = "F2F2F2"
YELLOW = "FFF2CC"          # cells the user fills in
BLUE_TXT = "0000FF"        # hardcoded inputs
GREEN_TXT = "008000"       # cross-sheet links

MONEY = '$#,##0;($#,##0);"-"'
MONEY2 = '$#,##0.00;($#,##0.00);"-"'
PCT = '0.0%;(0.0%);"-"'
HRS = '#,##0;(#,##0);"-"'

thin = Side(style="thin", color="BFBFBF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
TOPLINE = Border(top=Side(style="thin", color="404040"))
DBL = Border(top=Side(style="thin", color="404040"),
             bottom=Side(style="double", color="404040"))


def title(ws, cell, text, size=14):
    ws[cell] = text
    ws[cell].font = Font(name=FONT, size=size, bold=True, color=NAVY)


def band(ws, row, first_col, last_col, text):
    """Section header bar."""
    ws.cell(row=row, column=first_col).value = text
    for c in range(first_col, last_col + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.font = Font(name=FONT, size=11, bold=True, color="FFFFFF")


def headers(ws, row, first_col, labels):
    for i, lab in enumerate(labels):
        cell = ws.cell(row=row, column=first_col + i)
        cell.value = lab
        cell.fill = PatternFill("solid", fgColor=TEAL)
        cell.font = Font(name=FONT, size=10, bold=True, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center", vertical="center",
                                   wrap_text=True)
        cell.border = BOX


def inp(ws, cell, value, fmt=None, note=None):
    """An input cell: yellow fill, blue text."""
    ws[cell] = value
    ws[cell].fill = PatternFill("solid", fgColor=YELLOW)
    ws[cell].font = Font(name=FONT, size=10, bold=True, color=BLUE_TXT)
    ws[cell].border = BOX
    if fmt:
        ws[cell].number_format = fmt
    if note:
        ws.cell(row=ws[cell].row, column=ws[cell].column + 1).value = note


def lab(ws, cell, text, bold=False, indent=0):
    ws[cell] = text
    ws[cell].font = Font(name=FONT, size=10, bold=bold)
    if indent:
        ws[cell].alignment = Alignment(indent=indent)


def note(ws, cell, text):
    ws[cell] = text
    ws[cell].font = Font(name=FONT, size=9, italic=True, color="7F7F7F")


wb = openpyxl.Workbook()

# =============================================================== INPUTS ======
ws = wb.active
ws.title = "INPUTS"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 42
ws.column_dimensions["B"].width = 16
ws.column_dimensions["C"].width = 62

title(ws, "A1", "CTC CONFERENCE P&L BUILDER  —  INPUTS", 16)
note(ws, "A2", "Fill in the yellow cells only. Everything on the P&L tab "
               "recalculates automatically. Scope of work is selected on the SCOPE tab.")

# --- 1. Event profile
band(ws, 4, 1, 3, "1.  EVENT PROFILE")
lab(ws, "A5", "Event / Client Name");            inp(ws, "B5", "New Conference 2027")
lab(ws, "A6", "Event Dates (display text)");     inp(ws, "B6", "April 6-8, 2027")
lab(ws, "A7", "Location");                       inp(ws, "B7", "Los Angeles, CA")
lab(ws, "A8", "Attendees");                      inp(ws, "B8", 500, HRS)
lab(ws, "A9", "Exhibitors");                     inp(ws, "B9", 60, HRS)
lab(ws, "A10", "Sponsors");                      inp(ws, "B10", 20, HRS)
lab(ws, "A11", "Speakers");                      inp(ws, "B11", 15, HRS)
lab(ws, "A12", "Third-Party Items to Source");   inp(ws, "B12", 6, HRS)
note(ws, "C8", "Drives Venue, Branding, Registration, F&B, Housing, Programming hours")
note(ws, "C9", "Exhibit Management = exhibitors x 1 hour  (matches WTUI 200 & LCT 35 exactly)")
note(ws, "C10", "Sponsorships = sponsors x 1.5 hours, minimum 15")
note(ws, "C11", "Speaker Management = speakers x 1 hour, minimum 10")
note(ws, "C12", "3rd Party Vendors = items x 5 hours (25-50 hr band)")

# --- 2. Schedule
band(ws, 14, 1, 3, "2.  SCHEDULE")
lab(ws, "A15", "Event Days");                    inp(ws, "B15", 3, HRS)
lab(ws, "A16", "Set-Up / Load-In Days");         inp(ws, "B16", 1, HRS)
lab(ws, "A17", "Travel Days");                   inp(ws, "B17", 0, HRS)
lab(ws, "A18", "TOTAL ONSITE DAYS", bold=True)
ws["B18"] = "=B15+B16+B17"
lab(ws, "A19", "Months of Pre-Planning");        inp(ws, "B19", 9, HRS)
lab(ws, "A20", "Planning Weeks", bold=True)
ws["B20"] = "=ROUND(B19*4.33,0)"
note(ws, "C17", "Travel days are paid but not billed at full onsite hours - see section 5")
note(ws, "C19", "Months from contract/proposal to event day 1")
note(ws, "C20", "Weekly meetings, document management and PM hours all key off this")

# --- 3. Staffing
band(ws, 22, 1, 3, "3.  STAFFING  (headcount)")
lab(ws, "A23", "ONSITE — Managers");             inp(ws, "B23", 3, HRS)
lab(ws, "A24", "ONSITE — Coordinators");         inp(ws, "B24", 2, HRS)
lab(ws, "A25", "PRE-PLANNING — Managers");       inp(ws, "B25", 1, HRS)
lab(ws, "A26", "PRE-PLANNING — Coordinators");   inp(ws, "B26", 1, HRS)
note(ws, "C23", "Onsite staff are costed PER PERSON - one line each on the P&L")
note(ws, "C25", "Pre-planning is costed BY CATEGORY - headcount drives the weekly "
                "meeting line and the workload check")

# --- 4. Rates
band(ws, 28, 1, 3, "4.  RATES")
lab(ws, "A29", "Manager — OUR COST / hr", bold=True);      inp(ws, "B29", 60, MONEY2)
lab(ws, "A30", "Coordinator — OUR COST / hr", bold=True);  inp(ws, "B30", 42, MONEY2)
lab(ws, "A31", "Manager — CLIENT RATE / hr (pre-planning)");   inp(ws, "B31", 90, MONEY2)
lab(ws, "A32", "Coordinator — CLIENT RATE / hr (pre-planning)"); inp(ws, "B32", 65, MONEY2)
lab(ws, "A33", "Manager — CLIENT RATE / hr (onsite)");     inp(ws, "B33", 100, MONEY2)
lab(ws, "A34", "Coordinator — CLIENT RATE / hr (onsite)"); inp(ws, "B34", 65, MONEY2)
lab(ws, "A35", "Overtime Multiplier");                     inp(ws, "B35", 1.5, "0.00\"x\"")
note(ws, "C29", "Set by CTC. Applies to every manager hour, onsite and pre-planning.")
note(ws, "C30", "Set by CTC. Applies to every coordinator hour, onsite and pre-planning.")
note(ws, "C31", "Historical standard: PM $90 / EC $65 pre-planning; PM $100 onsite")
note(ws, "C35", "Coordinator OT billed at 1.5x ($97.50) and costed at 1.5x - matches all 3 prior P&Ls")

# --- 5. Onsite hours per day
band(ws, 37, 1, 3, "5.  ONSITE HOURS PER DAY")
lab(ws, "A38", "Manager hours per onsite day");            inp(ws, "B38", 12, HRS)
lab(ws, "A39", "Coordinator REGULAR hours per onsite day"); inp(ws, "B39", 8, HRS)
lab(ws, "A40", "Coordinator OVERTIME hours per onsite day"); inp(ws, "B40", 2, HRS)
lab(ws, "A41", "Hours per travel day");                    inp(ws, "B41", 8, HRS)
note(ws, "C38", "AFCI billed 12 hrs/day x 4 days = 48. WTUI 10 hrs/day x 5 = 50.")
note(ws, "C39", "AFCI & WTUI both: 8 regular + 2 OT per coordinator per day.")

# --- 6. Overhead, fees, discounts
band(ws, 43, 1, 3, "6.  OVERHEAD, FEES & DISCOUNTS")
lab(ws, "A44", "Staff Overhead per hour", bold=True);      inp(ws, "B44", 0.61, MONEY2)
lab(ws, "A45", "Admin Fee %", bold=True);                  inp(ws, "B45", 0.02, "0.0%")
lab(ws, "A46", "Multi-Year Discount %");                   inp(ws, "B46", 0.05, "0.0%")
lab(ws, "A47", "Apply Multi-Year Discount?");              inp(ws, "B47", "No")
note(ws, "C44", "$0.61 x every CTC staff hour (pre-planning + onsite + OT). A cost, not billed.")
note(ws, "C45", "2% of the client subtotal (pre-planning + onsite). Added to the client price.")
note(ws, "C46", "The '5% off additional years' line used on NICA and WTUI.")

# --- 7. Onsite role titles
band(ws, 49, 1, 3, "7.  ONSITE ROLE TITLES")
note(ws, "C50", "Only the first N rows are used, where N = the headcount in section 3. "
                "Titles are cosmetic; rates come from section 4.")
lab(ws, "A50", "ONSITE MANAGERS", bold=True)
mgr_defaults = ["Project Manager", "Event Manager", "Executive Producer",
                "Registration Manager", "Housing / Expo Manager",
                "Production Manager", "Manager 7", "Manager 8",
                "Manager 9", "Manager 10"]
for i, t in enumerate(mgr_defaults):
    lab(ws, f"A{51+i}", f"   Manager {i+1}")
    inp(ws, f"B{51+i}", t)

lab(ws, "A62", "ONSITE COORDINATORS", bold=True)
coord_defaults = ["Event Coordinator", "Registration Coordinator",
                  "Office Manager", "Production Assistant",
                  "Exhibit Coordinator", "Housing Coordinator",
                  "Coordinator 7", "Coordinator 8",
                  "Coordinator 9", "Coordinator 10"]
for i, t in enumerate(coord_defaults):
    lab(ws, f"A{63+i}", f"   Coordinator {i+1}")
    inp(ws, f"B{63+i}", t)

# formula cells styled
for c in ("B18", "B20"):
    ws[c].font = Font(name=FONT, size=10, bold=True)
    ws[c].number_format = HRS
    ws[c].border = BOX

dv_yn = DataValidation(type="list", formula1='"Yes,No"', allow_blank=False)
ws.add_data_validation(dv_yn)
dv_yn.add(ws["B47"])

ws.freeze_panes = "A5"

# ================================================================ SCOPE ======
sc = wb.create_sheet("SCOPE")
sc.sheet_view.showGridLines = False

# item, category, driver description, driver formula, LCT, AFCI, WTUI
I = "INPUTS!"
SCOPE_ITEMS = [
    ("Planning, Timeline & Communications", "Manager",
     "8 hrs per 3 onsite days", f"=8*ROUNDUP({I}$B$18/3,0)", 8, 16, 15),
    ("Meetings & Agendas", "Team",
     "1 per week x planning weeks", f"={I}$B$20", 18, 36, 39),
    ("Document Management (Admin Hours)", "Coordinator",
     "1 per week x planning weeks", f"={I}$B$20", 15, 36, 39),
    ("Project Management (PM Hours)", "Manager",
     "1 per week x planning weeks", f"={I}$B$20", 15, 36, 39),
    ("Venue Management: Logistics, Meeting Space", "Manager",
     "5% of attendees (20-75 hrs)", f"=ROUND(MEDIAN(20,0.05*{I}$B$8,75),0)", 20, 35, 70),
    ("Event Branding: Attendee Experience, Signage, Decor", "Manager",
     "5% of attendees (18-55 hrs)", f"=ROUND(MEDIAN(18,0.05*{I}$B$8,55),0)", 18, 25, 50),
    ("Registration: Onsite Check-In Only", "Coordinator",
     "3% of attendees (16-40 hrs)", f"=ROUND(MEDIAN(16,0.03*{I}$B$8,40),0)", 16, None, None),
    ("Registration: Online Build-Out + Onsite", "Coordinator",
     "6% of attendees (30-150 hrs)", f"=ROUND(MEDIAN(30,0.06*{I}$B$8,150),0)", None, 30, 90),
    ("Food & Beverage", "Manager",
     "3% of attendees (18-45 hrs)", f"=ROUND(MEDIAN(18,0.03*{I}$B$8,45),0)", 18, None, 45),
    ("Housing Logistics: Room Blocks, Reports, Overflow", "Coordinator",
     "3.5% of attendees (20-50 hrs)", f"=ROUND(MEDIAN(20,0.035*{I}$B$8,50),0)", None, None, 50),
    ("Programming: Audio Visual, Talent, Entertainment", "Manager",
     "5% of attendees (12-65 hrs)", f"=ROUND(MEDIAN(12,0.05*{I}$B$8,65),0)", 12, 65, 65),
    ("Exhibit Management", "Manager",
     "exhibitors x 1 hr", f"={I}$B$9*1", 35, 65, 200),
    ("Sponsorships: Opportunities & Sponsor Management", "Coordinator",
     "sponsors x 1.5 hrs, min 15", f"=ROUND(MAX(15,{I}$B$10*1.5),0)", None, 30, 75),
    ("Speaker Management: Prep & Onsite", "Coordinator",
     "speakers x 1 hr, min 10", f"=ROUND(MAX(10,{I}$B$11*1),0)", 25, None, None),
    ("Third Party Vendors", "Coordinator",
     "sourcing items x 5 hrs (25-50)", f"=ROUND(MEDIAN(25,{I}$B$12*5,50),0)", 30, 25, 50),
    ("Financial Management", "Manager",
     "planning months x 2 hrs", f"={I}$B$19*2", None, 18, None),
    ("Event Marketing: Strategy, Social, Email, Messaging", "Manager",
     "planning months x 6 hrs (30-60)", f"=ROUND(MEDIAN(30,{I}$B$19*6,60),0)", None, None, 60),
    ("Staff Management: Temporary Staff & Volunteers", "Manager",
     "10 hrs + 1 per event day, max 15", f"=MIN(15,10+{I}$B$15)", 10, None, 15),
    ("Reception / Tournament / Special Event Planning", "Coordinator",
     "planning months x 3 hrs (15-50)", f"=ROUND(MEDIAN(15,{I}$B$19*3,50),0)", 15, None, 50),
    ("Post-Event: Reporting, Reconciliation, Debrief", "Manager",
     "8 hrs per 3 onsite days", f"=8*ROUNDUP({I}$B$18/3,0)", 8, 15, 20),
    ("ENHANCEMENT: Graphic Design (web, signage, branding)", "Manager",
     "flat 55 hrs", "=55", None, 65, 55),
    ("ENHANCEMENT: Mobile App", "Manager",
     "flat 60 hrs", "=60", None, None, 60),
    ("Stage Production & Scripting", "Manager",
     "flat 30 hrs", "=30", None, None, 30),
    ("Venue Sourcing — Future Year (RFP, analysis, contracts)", "Manager",
     "flat 45 hrs", "=45", None, None, 45),
    ("Site Visits", "Manager",
     "flat 20 hrs", "=20", None, None, 20),
]

DEFAULT_ON = {
    "Planning, Timeline & Communications", "Meetings & Agendas",
    "Document Management (Admin Hours)", "Project Management (PM Hours)",
    "Venue Management: Logistics, Meeting Space",
    "Event Branding: Attendee Experience, Signage, Decor",
    "Registration: Online Build-Out + Onsite", "Food & Beverage",
    "Programming: Audio Visual, Talent, Entertainment", "Exhibit Management",
    "Sponsorships: Opportunities & Sponsor Management",
    "Third Party Vendors", "Financial Management",
    "Staff Management: Temporary Staff & Volunteers",
    "Post-Event: Reporting, Reconciliation, Debrief",
}

FIRST = 4
LAST = FIRST + len(SCOPE_ITEMS) - 1

title(sc, "A1", "SCOPE OF WORK LIBRARY  —  turn line items on and off here", 14)
note(sc, "A2", "Set INCLUDE? to Yes/No for each line. Hours calculate from the INPUTS tab; "
               "type a number in OVERRIDE HOURS to force a different number for any line.")

headers(sc, 3, 1, ["#", "SCOPE OF WORK ITEM", "STAFF\nCATEGORY", "INCLUDE?",
                   "HOW THE HOURS ARE CALCULATED", "CALC.\nHOURS",
                   "OVERRIDE\nHOURS", "HOURS\nUSED", "CLIENT\nRATE",
                   "OUR\nRATE", "CLIENT\nCOST", "OUR\nCOST",
                   "LCT\n2026", "AFCI\n2027", "WTUI\n2027", "SEQ"])

dv_scope = DataValidation(type="list", formula1='"Yes,No"', allow_blank=False)
sc.add_data_validation(dv_scope)

for n, (item, cat, drv_txt, drv_f, lct, afci, wtui) in enumerate(SCOPE_ITEMS):
    r = FIRST + n
    sc.cell(row=r, column=1, value=n + 1).number_format = "0"
    sc.cell(row=r, column=2, value=item)
    sc.cell(row=r, column=3, value=cat)
    c = sc.cell(row=r, column=4, value="Yes" if item in DEFAULT_ON else "No")
    c.fill = PatternFill("solid", fgColor=YELLOW)
    c.font = Font(name=FONT, size=10, bold=True, color=BLUE_TXT)
    dv_scope.add(c)
    sc.cell(row=r, column=5, value=drv_txt)
    sc.cell(row=r, column=6, value=drv_f).number_format = HRS
    o = sc.cell(row=r, column=7)
    o.fill = PatternFill("solid", fgColor=YELLOW)
    o.font = Font(name=FONT, size=10, bold=True, color=BLUE_TXT)
    o.number_format = HRS
    sc.cell(row=r, column=8,
            value=f"=IF(ISNUMBER(G{r}),G{r},F{r})").number_format = HRS
    sc.cell(row=r, column=9, value=(
        f'=IF(C{r}="Manager",{I}$B$31,'
        f'IF(C{r}="Coordinator",{I}$B$32,'
        f'{I}$B$25*{I}$B$31+{I}$B$26*{I}$B$32))')).number_format = MONEY2
    sc.cell(row=r, column=10, value=(
        f'=IF(C{r}="Manager",{I}$B$29,'
        f'IF(C{r}="Coordinator",{I}$B$30,'
        f'{I}$B$25*{I}$B$29+{I}$B$26*{I}$B$30))')).number_format = MONEY2
    sc.cell(row=r, column=11,
            value=f'=IF(D{r}="Yes",H{r}*I{r},0)').number_format = MONEY
    sc.cell(row=r, column=12,
            value=f'=IF(D{r}="Yes",H{r}*J{r},0)').number_format = MONEY
    for col, val in ((13, lct), (14, afci), (15, wtui)):
        cc = sc.cell(row=col and r, column=col, value=val)
        cc.number_format = HRS
        cc.font = Font(name=FONT, size=9, italic=True, color="7F7F7F")
    sc.cell(row=r, column=16,
            value=f'=IF(D{r}="Yes",COUNTIF($D$4:D{r},"Yes"),"")')
    for col in range(1, 17):
        sc.cell(row=r, column=col).border = BOX
        if col in (2, 3, 5):
            sc.cell(row=r, column=col).font = Font(name=FONT, size=10)
        sc.cell(row=r, column=col).alignment = Alignment(
            wrap_text=(col in (2, 5)), vertical="center")

# scope totals
TR = LAST + 1
sc.cell(row=TR, column=2, value="TOTALS — INCLUDED SCOPE").font = Font(
    name=FONT, size=10, bold=True)
sc.cell(row=TR, column=8,
        value=f'=SUMIF($D${FIRST}:$D${LAST},"Yes",$H${FIRST}:$H${LAST})')
sc.cell(row=TR, column=11, value=f"=SUM(K{FIRST}:K{LAST})")
sc.cell(row=TR, column=12, value=f"=SUM(L{FIRST}:L{LAST})")
sc.cell(row=TR, column=8).number_format = HRS
for col in (11, 12):
    sc.cell(row=TR, column=col).number_format = MONEY
for col in range(1, 17):
    sc.cell(row=TR, column=col).border = DBL
    sc.cell(row=TR, column=col).font = Font(name=FONT, size=10, bold=True)

note(sc, f"A{TR+2}",
     "Grey italic columns M:O are the ACTUAL hours charged on the three most recent final "
     "P&Ls — use them as a sanity check on the calculated hours.")
note(sc, f"A{TR+3}",
     "STAFF CATEGORY drives the rate: Manager = manager rates; Coordinator = coordinator "
     "rates; Team = (pre-planning managers x manager rate) + (pre-planning coordinators x "
     "coordinator rate), which is how the weekly meeting line has always been priced.")

widths = {1: 5, 2: 46, 3: 13, 4: 11, 5: 32, 6: 10, 7: 11, 8: 10, 9: 11,
          10: 10, 11: 12, 12: 12, 13: 9, 14: 9, 15: 9, 16: 7}
for col, w in widths.items():
    sc.column_dimensions[get_column_letter(col)].width = w
sc.row_dimensions[3].height = 34
sc.freeze_panes = "B4"

# ================================================================== P&L ======
pl = wb.create_sheet("P&L", 0)
pl.sheet_view.showGridLines = False

S = "SCOPE!"
SEQ = f"{S}$P${FIRST}:$P${LAST}"

# --- layout constants
R_SUM_HDR = 5
R_PRE, R_ON, R_OH, R_SUB, R_FEE, R_DISC, R_GT = 6, 7, 8, 9, 10, 11, 12
R_CAT_HDR = 15
R_CAT_M, R_CAT_C, R_CAT_T, R_CAT_TOT = 16, 17, 18, 19
R_PRE_HDR = 22
R_PRE_1 = 23
R_PRE_N = R_PRE_1 + len(SCOPE_ITEMS) - 1        # 46
R_PRE_TOT = R_PRE_N + 1                          # 47
R_ON_HDR = R_PRE_TOT + 3                         # 50
R_MGR_1 = R_ON_HDR + 1                           # 51
R_CRD_1 = R_MGR_1 + 10                           # 61
R_OT = R_CRD_1 + 10                              # 71
R_ON_TOT = R_OT + 1                              # 72
R_OH_HDR = R_ON_TOT + 3                          # 75
R_OH_PRE, R_OH_ON, R_OH_TOT = R_OH_HDR + 1, R_OH_HDR + 2, R_OH_HDR + 3

title(pl, "A1", "CONFERENCE P&L", 16)
pl["C1"] = "=INPUTS!B5"
pl["C1"].font = Font(name=FONT, size=16, bold=True, color=TEAL)
pl["B2"] = '=INPUTS!B6&"   |   "&INPUTS!B7&"   |   "&TEXT(INPUTS!B18,"0")&' \
           ' " onsite days   |   "&TEXT(INPUTS!B19,"0")&" months planning"'
pl["B2"].font = Font(name=FONT, size=10, italic=True, color="595959")

# ---- summary
band(pl, 4, 2, 6, "PROPOSAL SUMMARY")
headers(pl, R_SUM_HDR, 2, ["ITEM", "CLIENT COST", "OUR COST",
                           "NET PROFIT", "% PROFIT"])

pl[f"B{R_PRE}"] = f'="Pre-Planning / Project Hours  ("&TEXT(E{R_PRE_TOT},"#,##0")&" hrs)"'
pl[f"C{R_PRE}"] = f"=F{R_PRE_TOT}"
pl[f"D{R_PRE}"] = f"=I{R_PRE_TOT}"

pl[f"B{R_ON}"] = f'="Onsite Management  ("&TEXT(E{R_ON_TOT},"#,##0")&" hrs)"'
pl[f"C{R_ON}"] = f"=F{R_ON_TOT}"
pl[f"D{R_ON}"] = f"=I{R_ON_TOT}"

pl[f"B{R_OH}"] = f'="Staff Overhead  ("&TEXT(INPUTS!$B$44,"$0.00")&" / staff hour)"'
pl[f"C{R_OH}"] = 0
pl[f"D{R_OH}"] = f"=E{R_OH_TOT}"

for r in (R_PRE, R_ON, R_OH):
    pl[f"E{r}"] = f"=C{r}-D{r}"
    pl[f"F{r}"] = f'=IF(C{r}=0,"",E{r}/C{r})'

pl[f"B{R_SUB}"] = "SUBTOTAL"
for col in "CDE":
    pl[f"{col}{R_SUB}"] = f"=SUM({col}{R_PRE}:{col}{R_OH})"
pl[f"F{R_SUB}"] = f'=IF(C{R_SUB}=0,"",E{R_SUB}/C{R_SUB})'

pl[f"B{R_FEE}"] = '="Admin Fee  ("&TEXT(INPUTS!$B$45,"0.0%")&" of client subtotal)"'
pl[f"C{R_FEE}"] = f"=C{R_SUB}*INPUTS!$B$45"
pl[f"D{R_FEE}"] = 0
pl[f"E{R_FEE}"] = f"=C{R_FEE}-D{R_FEE}"
pl[f"F{R_FEE}"] = ""

pl[f"B{R_DISC}"] = '="Less Multi-Year Discount  ("&TEXT(INPUTS!$B$46,"0.0%")&")"'
pl[f"C{R_DISC}"] = (f'=-IF(INPUTS!$B$47="Yes",(C{R_SUB}+C{R_FEE})*INPUTS!$B$46,0)')
pl[f"D{R_DISC}"] = 0
pl[f"E{R_DISC}"] = f"=C{R_DISC}-D{R_DISC}"

pl[f"B{R_GT}"] = "GRAND TOTAL"
for col in "CDE":
    pl[f"{col}{R_GT}"] = f"=SUM({col}{R_SUB}:{col}{R_DISC})"
pl[f"F{R_GT}"] = f'=IF(C{R_GT}=0,"",E{R_GT}/C{R_GT})'

for r in range(R_PRE, R_GT + 1):
    for col in "BCDEF":
        cell = pl[f"{col}{r}"]
        cell.border = BOX
        cell.font = Font(name=FONT, size=10,
                         bold=(r in (R_SUB, R_GT)))
        if col in "CDE":
            cell.number_format = MONEY
        if col == "F":
            cell.number_format = PCT
    if r in (R_SUB, R_GT):
        for col in "BCDEF":
            pl[f"{col}{r}"].fill = PatternFill("solid", fgColor=GREY)
for col in "BCDEF":
    pl[f"{col}{R_GT}"].border = DBL
    pl[f"{col}{R_GT}"].font = Font(name=FONT, size=11, bold=True, color=NAVY)

# ---- pre-planning hours by category
band(pl, 14, 2, 7, "PRE-PLANNING HOURS BY STAFF CATEGORY")
headers(pl, R_CAT_HDR, 2, ["CATEGORY", "HOURS", "OUR RATE / HR", "OUR COST",
                           "STAFF COUNT", "HRS / PERSON / WEEK"])

cat_rows = [
    (R_CAT_M, "Managers", "Manager", "INPUTS!$B$29", "INPUTS!$B$25"),
    (R_CAT_C, "Coordinators", "Coordinator", "INPUTS!$B$30", "INPUTS!$B$26"),
]
for r, label_, key, rate, cnt in cat_rows:
    pl[f"B{r}"] = label_
    pl[f"C{r}"] = (f'=SUMIFS({S}$H${FIRST}:$H${LAST},{S}$C${FIRST}:$C${LAST},'
                   f'"{key}",{S}$D${FIRST}:$D${LAST},"Yes")')
    pl[f"D{r}"] = f"={rate}"
    pl[f"E{r}"] = f"=C{r}*D{r}"
    pl[f"F{r}"] = f"={cnt}"
    pl[f"G{r}"] = f'=IF(OR(F{r}=0,INPUTS!$B$20=0),"",C{r}/F{r}/INPUTS!$B$20)'

r = R_CAT_T
pl[f"B{r}"] = "Team (weekly meetings — all staff)"
pl[f"C{r}"] = (f'=SUMIFS({S}$H${FIRST}:$H${LAST},{S}$C${FIRST}:$C${LAST},'
               f'"Team",{S}$D${FIRST}:$D${LAST},"Yes")')
pl[f"D{r}"] = "=INPUTS!$B$25*INPUTS!$B$29+INPUTS!$B$26*INPUTS!$B$30"
pl[f"E{r}"] = f"=C{r}*D{r}"
pl[f"F{r}"] = "=INPUTS!$B$25+INPUTS!$B$26"
pl[f"G{r}"] = f'=IF(INPUTS!$B$20=0,"",C{r}/INPUTS!$B$20)'

r = R_CAT_TOT
pl[f"B{r}"] = "TOTAL PRE-PLANNING"
pl[f"C{r}"] = f"=SUM(C{R_CAT_M}:C{R_CAT_T})"
pl[f"E{r}"] = f"=SUM(E{R_CAT_M}:E{R_CAT_T})"
pl[f"F{r}"] = f"=INPUTS!$B$25+INPUTS!$B$26"

for r in range(R_CAT_M, R_CAT_TOT + 1):
    for col in "BCDEFG":
        cell = pl[f"{col}{r}"]
        cell.border = BOX
        cell.font = Font(name=FONT, size=10, bold=(r == R_CAT_TOT))
    pl[f"C{r}"].number_format = HRS
    pl[f"D{r}"].number_format = MONEY2
    pl[f"E{r}"].number_format = MONEY
    pl[f"F{r}"].number_format = HRS
    pl[f"G{r}"].number_format = '#,##0.0;;"-"'
for col in "BCDEFG":
    pl[f"{col}{R_CAT_TOT}"].border = DBL
    pl[f"{col}{R_CAT_TOT}"].fill = PatternFill("solid", fgColor=GREY)

note(pl, f"B{R_CAT_TOT+1}",
     "HRS / PERSON / WEEK is a workload check — if it climbs above roughly 10, "
     "either add staff or trim scope.")

# ---- pre-planning detail table
TBL_HDRS = ["SCOPE OF WORK", "STAFF", "CLIENT RATE", "HOURS", "CLIENT COST",
            "OUR RATE", "HOURS", "OUR COST", "NET PROFIT", "% PROFIT"]
band(pl, R_PRE_HDR - 1, 2, 11, "PRE-PLANNING  —  EVENT MANAGEMENT")
headers(pl, R_PRE_HDR, 2, TBL_HDRS)

for n in range(len(SCOPE_ITEMS)):
    r = R_PRE_1 + n
    m = f'MATCH({n+1},{SEQ},0)'
    pl[f"B{r}"] = f'=IFERROR(INDEX({S}$B${FIRST}:$B${LAST},{m}),"")'
    pl[f"C{r}"] = f'=IFERROR(INDEX({S}$C${FIRST}:$C${LAST},{m}),"")'
    pl[f"D{r}"] = f'=IFERROR(INDEX({S}$I${FIRST}:$I${LAST},{m}),"")'
    pl[f"E{r}"] = f'=IFERROR(INDEX({S}$H${FIRST}:$H${LAST},{m}),"")'
    pl[f"F{r}"] = f'=IF(B{r}="","",D{r}*E{r})'
    pl[f"G{r}"] = f'=IFERROR(INDEX({S}$J${FIRST}:$J${LAST},{m}),"")'
    pl[f"H{r}"] = f'=IF(B{r}="","",E{r})'
    pl[f"I{r}"] = f'=IF(B{r}="","",G{r}*H{r})'
    pl[f"J{r}"] = f'=IF(B{r}="","",F{r}-I{r})'
    pl[f"K{r}"] = f'=IF(OR(B{r}="",F{r}=0),"",J{r}/F{r})'

r = R_PRE_TOT
pl[f"B{r}"] = "TOTALS"
for col in ("E", "F", "H", "I", "J"):
    pl[f"{col}{r}"] = f"=SUM({col}{R_PRE_1}:{col}{R_PRE_N})"
pl[f"K{r}"] = f'=IF(F{r}=0,"",J{r}/F{r})'

# ---- onsite table
band(pl, R_ON_HDR - 1, 2, 11, "ONSITE MANAGEMENT  —  one line per person")
headers(pl, R_ON_HDR, 2, TBL_HDRS)

ONSITE_MGR_HRS = "(INPUTS!$B$15+INPUTS!$B$16)*INPUTS!$B$38+INPUTS!$B$17*INPUTS!$B$41"
ONSITE_CRD_HRS = "(INPUTS!$B$15+INPUTS!$B$16)*INPUTS!$B$39+INPUTS!$B$17*INPUTS!$B$41"

for i in range(10):
    r = R_MGR_1 + i
    on = f"{i+1}<=INPUTS!$B$23"
    pl[f"B{r}"] = f'=IF({on},INPUTS!$B${51+i},"")'
    pl[f"C{r}"] = f'=IF({on},"Manager","")'
    pl[f"D{r}"] = f'=IF({on},INPUTS!$B$33,"")'
    pl[f"E{r}"] = f'=IF({on},{ONSITE_MGR_HRS},"")'
    pl[f"G{r}"] = f'=IF({on},INPUTS!$B$29,"")'

for j in range(10):
    r = R_CRD_1 + j
    on = f"{j+1}<=INPUTS!$B$24"
    pl[f"B{r}"] = f'=IF({on},INPUTS!$B${63+j},"")'
    pl[f"C{r}"] = f'=IF({on},"Coordinator","")'
    pl[f"D{r}"] = f'=IF({on},INPUTS!$B$34,"")'
    pl[f"E{r}"] = f'=IF({on},{ONSITE_CRD_HRS},"")'
    pl[f"G{r}"] = f'=IF({on},INPUTS!$B$30,"")'

r = R_OT
pl[f"B{r}"] = ('="Coordinator Overtime  ("&TEXT(INPUTS!$B$24,"0")&" coordinators x "'
               '&TEXT(INPUTS!$B$40,"0")&" hrs x "&TEXT(INPUTS!$B$15+INPUTS!$B$16,"0")&" days)"')
pl[f"C{r}"] = '=IF(INPUTS!$B$24=0,"","Coordinator")'
pl[f"D{r}"] = '=IF(INPUTS!$B$24=0,"",INPUTS!$B$34*INPUTS!$B$35)'
pl[f"E{r}"] = ('=IF(INPUTS!$B$24=0,"",INPUTS!$B$24*(INPUTS!$B$15+INPUTS!$B$16)'
               '*INPUTS!$B$40)')
pl[f"G{r}"] = '=IF(INPUTS!$B$24=0,"",INPUTS!$B$30*INPUTS!$B$35)'

for r in list(range(R_MGR_1, R_OT + 1)):
    pl[f"F{r}"] = f'=IF(B{r}="","",D{r}*E{r})'
    pl[f"H{r}"] = f'=IF(B{r}="","",E{r})'
    pl[f"I{r}"] = f'=IF(B{r}="","",G{r}*H{r})'
    pl[f"J{r}"] = f'=IF(B{r}="","",F{r}-I{r})'
    pl[f"K{r}"] = f'=IF(OR(B{r}="",F{r}=0),"",J{r}/F{r})'

r = R_ON_TOT
pl[f"B{r}"] = "TOTALS"
for col in ("E", "F", "H", "I", "J"):
    pl[f"{col}{r}"] = f"=SUM({col}{R_MGR_1}:{col}{R_OT})"
pl[f"K{r}"] = f'=IF(F{r}=0,"",J{r}/F{r})'

# ---- format both detail tables
for rng in (range(R_PRE_1, R_PRE_TOT + 1), range(R_MGR_1, R_ON_TOT + 1)):
    for r in rng:
        is_tot = r in (R_PRE_TOT, R_ON_TOT)
        for col in "BCDEFGHIJK":
            cell = pl[f"{col}{r}"]
            cell.border = DBL if is_tot else BOX
            cell.font = Font(name=FONT, size=10, bold=is_tot)
            if is_tot:
                cell.fill = PatternFill("solid", fgColor=GREY)
            cell.alignment = Alignment(wrap_text=(col == "B"),
                                       vertical="center")
            if col in ("D", "G"):
                cell.number_format = MONEY2
            elif col in ("E", "H"):
                cell.number_format = HRS
            elif col in ("F", "I", "J"):
                cell.number_format = MONEY
            elif col == "K":
                cell.number_format = PCT

# ---- overhead block
band(pl, R_OH_HDR - 1, 2, 5, "STAFF OVERHEAD")
headers(pl, R_OH_HDR, 2, ["ITEM", "STAFF HOURS", "RATE / HR", "OVERHEAD COST"])

pl[f"B{R_OH_PRE}"] = "Pre-Planning staff hours"
pl[f"C{R_OH_PRE}"] = f"=E{R_PRE_TOT}"
pl[f"B{R_OH_ON}"] = "Onsite staff hours (incl. overtime)"
pl[f"C{R_OH_ON}"] = f"=E{R_ON_TOT}"
for r in (R_OH_PRE, R_OH_ON):
    pl[f"D{r}"] = "=INPUTS!$B$44"
    pl[f"E{r}"] = f"=C{r}*D{r}"
pl[f"B{R_OH_TOT}"] = "TOTAL STAFF OVERHEAD"
pl[f"C{R_OH_TOT}"] = f"=SUM(C{R_OH_PRE}:C{R_OH_ON})"
pl[f"E{R_OH_TOT}"] = f"=SUM(E{R_OH_PRE}:E{R_OH_ON})"

for r in range(R_OH_PRE, R_OH_TOT + 1):
    for col in "BCDE":
        cell = pl[f"{col}{r}"]
        cell.border = DBL if r == R_OH_TOT else BOX
        cell.font = Font(name=FONT, size=10, bold=(r == R_OH_TOT))
        if r == R_OH_TOT:
            cell.fill = PatternFill("solid", fgColor=GREY)
    pl[f"C{r}"].number_format = HRS
    pl[f"D{r}"].number_format = MONEY2
    pl[f"E{r}"].number_format = MONEY

note(pl, f"B{R_OH_TOT+2}",
     "Overhead is a CTC cost only — it is not billed to the client, so it reduces net profit.")
note(pl, f"B{R_OH_TOT+3}",
     "Admin fee is charged ON TOP of the client subtotal (pre-planning + onsite) "
     "and is pure margin.")

pl.column_dimensions["A"].width = 3
pl.column_dimensions["B"].width = 48
for col, w in {"C": 15, "D": 13, "E": 10, "F": 13, "G": 11, "H": 10,
               "I": 13, "J": 13, "K": 11}.items():
    pl.column_dimensions[col].width = w
pl.row_dimensions[R_SUM_HDR].height = 28
pl.row_dimensions[R_CAT_HDR].height = 34
pl.row_dimensions[R_PRE_HDR].height = 28
pl.row_dimensions[R_ON_HDR].height = 28
pl.row_dimensions[R_OH_HDR].height = 28
pl.freeze_panes = "B5"

# =========================================================== BENCHMARKS ======
bm = wb.create_sheet("BENCHMARKS")
bm.sheet_view.showGridLines = False
title(bm, "A1", "BENCHMARKS  —  the four final P&Ls this model is built from", 14)
note(bm, "A2", "Hardcoded from the source workbooks. Use to sanity-check a new P&L "
               "before it goes out.")

headers(bm, 4, 1, ["EVENT", "SOURCE TAB", "ATTENDEES", "EVENT DAYS",
                   "PRE-PLANNING HRS", "PRE-PLANNING CLIENT $",
                   "ONSITE HRS", "ONSITE CLIENT $", "TOTAL CLIENT $",
                   "TOTAL OUR COST $", "NET PROFIT $", "% PROFIT"])

BENCH = [
    ("LCT / Marine Recreation Assn 2026", "FINAL June.10.2026 Version 3",
     "~200", 3, 263, 22315, 132, 11100, 33415, 19630, 13785, 0.4125),
    ("AFCI Studio Summit 2027", "FINAL July.27.2026 Version 2",
     "350-500", 3, 617, 51845, 272, 27800, 79645, 42274, 37371, 0.4692),
    ("WTUI 2027", "FINAL June.24.2026 Version 2",
     "1100-1500", 4, 1182, 107870, 350, 30725, 138595, 73966, 64629, 0.4663),
    ("NICA 2026", "Actual NICA 2026",
     "n/a", 3, 1887, 134545, 334, 31900, 166445, 105151, 61294, 0.3683),
]
for n, row in enumerate(BENCH):
    r = 5 + n
    for i, v in enumerate(row):
        cell = bm.cell(row=r, column=i + 1, value=v)
        cell.border = BOX
        cell.font = Font(name=FONT, size=10)
        if i in (4, 6):
            cell.number_format = HRS
        elif i in (5, 7, 8, 9, 10):
            cell.number_format = MONEY
        elif i == 11:
            cell.number_format = PCT

note(bm, "A11", "NICA 2026 predates the current template (it used per-person named rows "
                "rather than a scope-of-work list) and is shown for totals comparison only.")

band(bm, 13, 1, 6, "BACK-TEST  —  the model re-run on each event's real inputs")
headers(bm, 14, 1, ["EVENT", "PRE-PLANNING HRS\nmodel vs actual",
                    "PRE-PLANNING $\nmodel vs actual", "ONSITE HRS\nmodel vs actual",
                    "ONSITE $\nmodel vs actual", "CLIENT SUBTOTAL\nmodel vs actual"])
BACKTEST = [
    ("LCT / Marine Recreation Assn 2026", "269 vs 263  (+2%)", "$22,740 vs $22,315  (+2%)",
     "132 vs 132  (0%)", "$11,490 vs $11,100  (+4%)", "$34,230 vs $33,415  (+2%)"),
    ("AFCI Studio Summit 2027", "446 vs 617  (-28%)", "$39,600 vs $51,845  (-24%)",
     "272 vs 272  (0%)", "$24,920 vs $27,800  (-10%)", "$64,520 vs $79,645  (-19%)"),
    ("WTUI 2027", "1,159 vs 1,182  (-2%)", "$98,570 vs $107,870  (-9%)",
     "390 vs 350  (+11%)", "$34,725 vs $30,725  (+13%)", "$133,295 vs $138,595  (-4%)"),
]
for n, row in enumerate(BACKTEST):
    r = 15 + n
    for i, v in enumerate(row):
        cell = bm.cell(row=r, column=i + 1, value=v)
        cell.border = BOX
        cell.font = Font(name=FONT, size=10, bold=(i == 0))
        cell.alignment = Alignment(wrap_text=True, vertical="center")
note(bm, "A19", "LCT and WTUI land within a few percent. AFCI reads low because its final "
                "proposal priced Registration at 150 hrs (full Cvent build-out plus mobile "
                "app) and Programming at 65 hrs (recording & broadcast) — both well above "
                "base scope. Use OVERRIDE HOURS on the SCOPE tab when a line is genuinely "
                "bigger than standard.")
note(bm, "A20", "WTUI onsite reads high only because this model defaults managers to 12 "
                "hrs/onsite day; WTUI billed 10. Set 'Manager hours per onsite day' to 10 "
                "on INPUTS and the 390 becomes 350 — an exact match.")

band(bm, 22, 1, 6, "WHAT CHANGED IN THIS MODEL")
CHANGES = [
    ("Manager cost rate", "was $54/hr (PM) and $57/hr", "now $60/hr — flat, all manager hours"),
    ("Coordinator cost rate", "was $38/hr (EC) and $35/hr", "now $42/hr — flat, all coordinator hours"),
    ("Staff overhead", "not on prior P&Ls", "NEW: $0.61 x every CTC staff hour, booked as a cost"),
    ("Admin fee", "not on prior P&Ls", "NEW: 2% of the client subtotal, added to the client price"),
    ("Onsite staffing", "hand-typed, one row per named person",
     "driven by manager / coordinator headcount, one row per person"),
    ("Pre-planning staffing", "hand-typed per line", "rolled up by category (manager / coordinator / team)"),
    ("Scope hours", "typed in each time", "calculated from event size, schedule and planning months"),
]
headers(bm, 23, 1, ["ITEM", "PRIOR P&Ls", "THIS MODEL"])
for n, (a, b, c) in enumerate(CHANGES):
    r = 24 + n
    for i, v in enumerate((a, b, c)):
        cell = bm.cell(row=r, column=i + 1, value=v)
        cell.border = BOX
        cell.font = Font(name=FONT, size=10, bold=(i == 0))
        cell.alignment = Alignment(wrap_text=True, vertical="center")

for col, w in {"A": 34, "B": 34, "C": 44, "D": 12, "E": 16, "F": 20,
               "G": 12, "H": 16, "I": 16, "J": 16, "K": 14, "L": 11}.items():
    bm.column_dimensions[col].width = w
bm.row_dimensions[4].height = 34
bm.row_dimensions[14].height = 34
bm.row_dimensions[23].height = 20

# ============================================================== README =======
rd = wb.create_sheet("HOW TO USE")
rd.sheet_view.showGridLines = False
rd.column_dimensions["A"].width = 4
rd.column_dimensions["B"].width = 110
title(rd, "B1", "HOW TO BUILD A NEW CONFERENCE P&L", 16)

STEPS = [
    ("", ""),
    ("STEP 1 — INPUTS tab", ""),
    ("", "Fill in the yellow cells: event name, dates, attendees, exhibitors, sponsors, "
         "speakers, third-party items."),
    ("", "Enter EVENT DAYS, SET-UP DAYS, TRAVEL DAYS and MONTHS OF PRE-PLANNING."),
    ("", "Enter how many MANAGERS and COORDINATORS work the event onsite, and how many "
         "work it in pre-planning."),
    ("", "Rates are pre-set: manager $60/hr cost, coordinator $42/hr cost. Change them "
         "only if the rate card changes."),
    ("", ""),
    ("STEP 2 — SCOPE tab", ""),
    ("", "Set INCLUDE? to Yes or No on each of the 24 scope-of-work lines. That is your "
         "scope of work."),
    ("", "Hours calculate automatically from the INPUTS. If you disagree with a number, "
         "type your own into OVERRIDE HOURS — nothing else needs to change."),
    ("", "Columns M:O show what the last three events actually charged for that same line, "
         "as a reality check."),
    ("", ""),
    ("STEP 3 — P&L tab", ""),
    ("", "Read it. Nothing to type. The proposal summary, the pre-planning table, the "
         "onsite table, overhead and the admin fee are all live formulas."),
    ("", "Watch HRS / PERSON / WEEK in the category block — over ~10 means the headcount "
         "is too thin for the scope."),
    ("", ""),
    ("HOW THE MONEY WORKS", ""),
    ("", "CLIENT COST = hours x client rate.  Pre-planning: manager $90 / coordinator $65. "
         "Onsite: manager $100 / coordinator $65. Coordinator overtime bills at 1.5x."),
    ("", "OUR COST = hours x our rate. Manager $60, coordinator $42, overtime 1.5x."),
    ("", "STAFF OVERHEAD = $0.61 x every CTC staff hour (pre-planning + onsite + overtime). "
         "A cost to us — it is not billed, so it comes out of profit."),
    ("", "ADMIN FEE = 2% of the client subtotal, added to what the client pays. It has no "
         "cost against it, so all of it is profit."),
    ("", "MULTI-YEAR DISCOUNT = the 5% off used on NICA and WTUI. Off by default — switch "
         "'Apply Multi-Year Discount?' to Yes on INPUTS."),
    ("", ""),
    ("WHERE THE HOUR DRIVERS CAME FROM", ""),
    ("", "Every driver is calibrated against the final LCT 2026, AFCI 2027 and WTUI 2027 "
         "P&Ls. Where the old note in the sheet disagreed with what was actually charged, "
         "the actuals won — e.g. Exhibit Management was noted as 'exhibitors x 5' but was "
         "charged at exactly exhibitors x 1 on both WTUI (200) and LCT (35)."),
    ("", "Percentage-of-attendee drivers carry a floor and a cap so a 1,500-person event "
         "does not produce an absurd number. The bands are the observed range across the "
         "three finals."),
    ("", "See the BENCHMARKS tab for the totals each of those P&Ls landed on."),
]
r = 3
for head, body in STEPS:
    if head:
        rd.cell(row=r, column=2, value=head).font = Font(
            name=FONT, size=11, bold=True, color=NAVY)
    elif body:
        cell = rd.cell(row=r, column=2, value="•  " + body)
        cell.font = Font(name=FONT, size=10)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        rd.row_dimensions[r].height = 30
    r += 1

# default font everywhere
for sheet in wb.worksheets:
    for row in sheet.iter_rows():
        for cell in row:
            if cell.font and cell.font.name != FONT:
                f = cell.font
                cell.font = Font(name=FONT, size=f.size or 10, bold=f.bold,
                                 italic=f.italic, color=f.color)

wb.save(OUT)
print("wrote", OUT)
