#!/usr/bin/env python3
"""
Builds the CTC Conference P&L Builder.

Scope of work mirrors the 2026 Master Proposal Template: the SCOPE tab carries
every sub-item ("VENUE SOURCING: Request for Proposal"), the P&L rolls them up
to the top-level headings ("VENUE SOURCING").

Hours come from an Event Scale Index rather than flat percentages -- see
HOW TO USE. Run:  python3 build_pl_template.py
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import Rule
from openpyxl.styles.differential import DifferentialStyle

OUT = "CTC_Conference_PL_Builder.xlsx"

# ------------------------------------------------------- house style ---------
HEAD_FONT = "Poppins"
BODY_FONT = "Barlow"
MAGENTA = "9C1E83"        # title bar
YELLOW_T = "FFFF00"       # title bar text
BLUE = "6D9EEB"           # section bands
PINK = "EAD1DC"           # highlighted / totals rows
INPUT_FILL = "FFF2CC"     # cells the user types in
INPUT_TXT = "0000FF"
GREY = "F2F2F2"

MONEY = '"$"#,##0;("$"#,##0);"-"'
RATE = '"$"#,##0.00;("$"#,##0.00);"-"'
PCT = '0.0%;(0.0%);"-"'
HRS = '#,##0;(#,##0);"-"'

thin = Side(style="thin", color="BFBFBF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
DBL = Border(top=Side(style="thin", color="404040"),
             bottom=Side(style="double", color="404040"))


def titlebar(ws, row, c1, c2, text):
    ws.cell(row=row, column=c1).value = text
    for c in range(c1, c2 + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = PatternFill("solid", fgColor=MAGENTA)
        cell.font = Font(name=HEAD_FONT, size=14, bold=True, color=YELLOW_T)
    ws.row_dimensions[row].height = 24


def band(ws, row, c1, c2, text):
    ws.cell(row=row, column=c1).value = text
    for c in range(c1, c2 + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = PatternFill("solid", fgColor=BLUE)
        cell.font = Font(name=HEAD_FONT, size=12, bold=True, color="FFFFFF")
    ws.row_dimensions[row].height = 20


def headers(ws, row, c1, labels, size=10):
    for i, lab in enumerate(labels):
        cell = ws.cell(row=row, column=c1 + i)
        cell.value = lab
        cell.font = Font(name=HEAD_FONT, size=size, bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="bottom",
                                   wrap_text=True)
        cell.border = Border(bottom=Side(style="medium", color="404040"))


def inp(ws, cell, value, fmt=None):
    ws[cell] = value
    ws[cell].fill = PatternFill("solid", fgColor=INPUT_FILL)
    ws[cell].font = Font(name=BODY_FONT, size=10, bold=True, color=INPUT_TXT)
    ws[cell].border = BOX
    if fmt:
        ws[cell].number_format = fmt


def lab(ws, cell, text, bold=False):
    ws[cell] = text
    ws[cell].font = Font(name=BODY_FONT, size=10, bold=bold)


def note(ws, cell, text):
    ws[cell] = text
    ws[cell].font = Font(name=BODY_FONT, size=9, italic=True, color="7F7F7F")


def calc(ws, cell, formula, fmt=None, bold=True):
    ws[cell] = formula
    ws[cell].font = Font(name=BODY_FONT, size=10, bold=bold)
    ws[cell].border = BOX
    if fmt:
        ws[cell].number_format = fmt


wb = openpyxl.Workbook()

# ============================================================= INPUTS ========
iw = wb.active
iw.title = "INPUTS"
iw.sheet_view.showGridLines = False
iw.column_dimensions["A"].width = 6.6
iw.column_dimensions["B"].width = 44
iw.column_dimensions["C"].width = 15
iw.column_dimensions["D"].width = 66

titlebar(iw, 1, 2, 4, "CTC CONFERENCE P&L BUILDER  —  INPUTS")
note(iw, "B2", "Type in the yellow cells only. Choose the scope of work on the SCOPE tab. "
               "The P&L tab is all formulas — nothing to fill in there.")

band(iw, 4, 2, 4, "1.  EVENT PROFILE")
lab(iw, "B5", "Event / Client Name");        inp(iw, "C5", "New Conference 2027")
lab(iw, "B6", "Event Dates (display text)"); inp(iw, "C6", "April 6-8, 2027")
lab(iw, "B7", "Location");                   inp(iw, "C7", "Los Angeles, CA")

band(iw, 9, 2, 4, "2.  EVENT SIZE")
lab(iw, "B10", "Attendees");                     inp(iw, "C10", 500, HRS)
lab(iw, "B11", "Exhibitors");                    inp(iw, "C11", 60, HRS)
lab(iw, "B12", "Sponsors");                      inp(iw, "C12", 20, HRS)
lab(iw, "B13", "Speakers");                      inp(iw, "C13", 15, HRS)
lab(iw, "B14", "Third-Party Vendors to Source"); inp(iw, "C14", 5, HRS)
lab(iw, "B15", "Site Visits");                   inp(iw, "C15", 1, HRS)
note(iw, "D10", "Main driver of the Event Scale Index below")
note(iw, "D11", "Exhibit Management bills at 1 hour per exhibitor")
note(iw, "D12", "Sponsor Management bills at 1 hour per sponsor")
note(iw, "D13", "Speaker Management bills at 1 hour per speaker, split prep / onsite")
note(iw, "D14", "Third Party Vendors bills at 5 hours per vendor sourced")
note(iw, "D15", "Site Visits bills at 10 hours each (travel, walk-through, write-up)")

band(iw, 17, 2, 4, "3.  SCHEDULE")
lab(iw, "B18", "Event Days");             inp(iw, "C18", 3, HRS)
lab(iw, "B19", "Set-Up / Load-In Days");  inp(iw, "C19", 1, HRS)
lab(iw, "B20", "Travel Days");            inp(iw, "C20", 0, HRS)
lab(iw, "B21", "TOTAL ONSITE DAYS", bold=True)
calc(iw, "C21", "=C18+C19+C20", HRS)
lab(iw, "B22", "Months of Pre-Planning"); inp(iw, "C22", 9, HRS)
lab(iw, "B23", "Planning Weeks", bold=True)
calc(iw, "C23", "=ROUND(C22*4.33,0)", HRS)
lab(iw, "B24", "EVENT SCALE INDEX", bold=True)
calc(iw, "C24",
     "=ROUND((MAX(1,C10)/250)^(1/3)*(MAX(1,C22)/6)^(1/2)*(MAX(1,C18)/3)^(1/4),2)",
     "0.00")
for c in ("C21", "C23", "C24"):
    iw[c].fill = PatternFill("solid", fgColor=GREY)
note(iw, "D22", "Months from contract signature to day 1 of the event")
note(iw, "D23", "Weekly meetings, the project management system and approvals key off this")
note(iw, "D24", "Calculated, not typed. 1.00 = a 250-person, 3-day event with 6 months "
                "of planning. Doubling attendance moves it about 26%, not 100%.")

band(iw, 26, 2, 4, "4.  STAFFING  (headcount)")
lab(iw, "B27", "ONSITE — Managers");           inp(iw, "C27", 3, HRS)
lab(iw, "B28", "ONSITE — Coordinators");       inp(iw, "C28", 2, HRS)
lab(iw, "B29", "PRE-PLANNING — Managers");     inp(iw, "C29", 1, HRS)
lab(iw, "B30", "PRE-PLANNING — Coordinators"); inp(iw, "C30", 1, HRS)
note(iw, "D27", "Onsite staff are costed PER PERSON — one line each on the P&L")
note(iw, "D29", "Pre-planning is costed BY CATEGORY. Headcount sets the weekly meeting "
                "rate and the workload check on the P&L.")

band(iw, 32, 2, 4, "5.  RATES")
lab(iw, "B33", "Manager — OUR COST / hr", bold=True);     inp(iw, "C33", 60, RATE)
lab(iw, "B34", "Coordinator — OUR COST / hr", bold=True); inp(iw, "C34", 42, RATE)
lab(iw, "B35", "Manager — CLIENT RATE / hr (pre-planning)");     inp(iw, "C35", 90, RATE)
lab(iw, "B36", "Coordinator — CLIENT RATE / hr (pre-planning)"); inp(iw, "C36", 65, RATE)
lab(iw, "B37", "Manager — CLIENT RATE / hr (onsite)");     inp(iw, "C37", 100, RATE)
lab(iw, "B38", "Coordinator — CLIENT RATE / hr (onsite)"); inp(iw, "C38", 65, RATE)
lab(iw, "B39", "Overtime Multiplier");                     inp(iw, "C39", 1.5, '0.00"x"')
note(iw, "D33", "Applies to every manager hour, pre-planning and onsite")
note(iw, "D34", "Applies to every coordinator hour, pre-planning and onsite")
note(iw, "D39", "Coordinator overtime is billed and costed at 1.5x")

band(iw, 41, 2, 4, "6.  ONSITE HOURS PER DAY")
lab(iw, "B42", "Manager hours per onsite day");             inp(iw, "C42", 12, HRS)
lab(iw, "B43", "Coordinator REGULAR hours per onsite day"); inp(iw, "C43", 8, HRS)
lab(iw, "B44", "Coordinator OVERTIME hours per onsite day");inp(iw, "C44", 2, HRS)
lab(iw, "B45", "Hours per travel day");                     inp(iw, "C45", 8, HRS)
note(iw, "D42", "Applied to event days + set-up days")
note(iw, "D43", "Coordinators run 8 regular + 2 overtime on a normal show day")

band(iw, 47, 2, 4, "7.  OVERHEAD, FEES & DISCOUNTS")
lab(iw, "B48", "Staff Overhead per hour", bold=True); inp(iw, "C48", 0.61, RATE)
lab(iw, "B49", "Admin Fee %", bold=True);             inp(iw, "C49", 0.02, "0.0%")
lab(iw, "B50", "Multi-Year Discount %");              inp(iw, "C50", 0.05, "0.0%")
lab(iw, "B51", "Apply Multi-Year Discount?");         inp(iw, "C51", "No")
lab(iw, "B52", "Target Net Margin %", bold=True);          inp(iw, "C52", 0.40, "0.0%")
note(iw, "D52", "Used by the margin check on the P&L — what client price hits this margin.")
lab(iw, "B53", "Utilization %", bold=True);                inp(iw, "C53", 1.00, "0.0%")
lab(iw, "B54", "Overhead % of direct labor", bold=True);   inp(iw, "C54", 0.00, "0.0%")
note(iw, "D53", "Share of a paid hour that is billable to a client. 100% leaves the P&L "
                "exactly as quoted; agencies plan around 75-85%. Measure it before trusting it.")
note(iw, "D54", "Rent, software, insurance, non-billable salaries as a share of staff cost. "
                "Typical agency range 15-30%. Feeds the TRUE COST view only.")
note(iw, "D48", "Charged against every CTC staff hour. A cost to us — not billed.")
note(iw, "D49", "2% of the client subtotal, added to the client price. No cost against it.")
note(iw, "D50", "The '5% off additional years' line, off unless switched on below.")

band(iw, 56, 2, 4, "8.  ONSITE ROLE TITLES")
note(iw, "D57", "Only the first N lines are used, where N is the headcount in section 4. "
                "Titles are labels only — rates come from section 5.")
lab(iw, "B57", "ONSITE MANAGERS", bold=True)
MGR_ROW1 = 58
for i, t in enumerate(["Project Manager", "Event Manager", "Executive Producer",
                       "Registration Manager", "Housing / Expo Manager",
                       "Production Manager", "Manager 7", "Manager 8",
                       "Manager 9", "Manager 10"]):
    lab(iw, f"B{MGR_ROW1+i}", f"    Manager {i+1}")
    inp(iw, f"C{MGR_ROW1+i}", t)

CRD_ROW1 = 69
lab(iw, f"B{CRD_ROW1-1}", "ONSITE COORDINATORS", bold=True)
for i, t in enumerate(["Event Coordinator", "Registration Coordinator",
                       "Office Manager", "Production Assistant",
                       "Exhibit Coordinator", "Housing Coordinator",
                       "Coordinator 7", "Coordinator 8",
                       "Coordinator 9", "Coordinator 10"]):
    lab(iw, f"B{CRD_ROW1+i}", f"    Coordinator {i+1}")
    inp(iw, f"C{CRD_ROW1+i}", t)

dv = DataValidation(type="list", formula1='"Yes,No"', allow_blank=False)
iw.add_data_validation(dv)
dv.add(iw["C51"])
iw.freeze_panes = "A5"

# INPUTS cell shortcuts used everywhere below
N = "INPUTS!$C$"
ATT, EXH, SPO, SPK, VEN, SIT = N+"10", N+"11", N+"12", N+"13", N+"14", N+"15"
EVD, SETD, TRVD, ONSD = N+"18", N+"19", N+"20", N+"21"
MONTHS, WEEKS, ESI = N+"22", N+"23", N+"24"
ON_M, ON_C, PRE_M, PRE_C = N+"27", N+"28", N+"29", N+"30"
R_MGR, R_CRD = N+"33", N+"34"
R_MGR_CL, R_CRD_CL = N+"35", N+"36"
R_MGR_ON, R_CRD_ON, OT_X = N+"37", N+"38", N+"39"
H_MGR, H_CRD, H_OT, H_TRV = N+"42", N+"43", N+"44", N+"45"
OVH, FEE, DISC, DISC_ON, TGT = N+"48", N+"49", N+"50", N+"51", N+"52"
UTIL, OHP = N+"53", N+"54"

# ============================================================== SCOPE ========
# (top level, sub-item, staff, driver kind, weight, driver text)
S_ = "SCALE"; W_ = "WEEKS"; C_ = "COUNT"
SCOPE = [
 ("PLANNING, TIMELINE & COMMUNICATIONS",
  "Project management system, meetings & minutes, roles, approvals",
  "Team", "PLAN", 0,
  "3 hrs per planning week + 5 x scale index"),

 ("VENUE SOURCING", "Request for Proposal", "Manager", S_, 6, "6 x scale index"),
 ("VENUE SOURCING", "Venue/Hotel Analysis", "Manager", S_, 6, "6 x scale index"),
 ("VENUE SOURCING", "Site Visits", "Manager", C_+":"+SIT, 10, "10 hrs per site visit"),
 ("VENUE SOURCING", "Contract Negotiations", "Manager", S_, 5, "5 x scale index"),

 ("VENUE MANAGEMENT", "Venue Logistics", "Manager", S_, 16, "16 x scale index"),
 ("VENUE MANAGEMENT", "Meeting Space", "Manager", S_, 10, "10 x scale index"),

 ("EVENT BRANDING", "Attendee Experience", "Manager", S_, 7, "7 x scale index"),
 ("EVENT BRANDING", "Signage", "Manager", S_, 14, "14 x scale index"),
 ("EVENT BRANDING", "Décor", "Manager", S_, 8, "8 x scale index"),
 ("EVENT BRANDING", "Graphic Design (add-on)", "Manager", S_, 26, "26 x scale index"),

 ("FOOD & BEVERAGE", "Food & Beverage Management", "Manager", S_, 22, "22 x scale index"),

 ("REGISTRATION", "Online Registration / Build-Out", "Coordinator", S_, 35, "35 x scale index"),
 ("REGISTRATION", "Onsite Registration", "Coordinator", S_, 18, "18 x scale index"),
 ("REGISTRATION", "Mobile App", "Coordinator", S_, 25, "25 x scale index"),

 ("SWAG BAG", "Swag Bag Sourcing, Assembly & Distribution", "Coordinator", S_, 20,
  "20 x scale index"),

 ("HOUSING LOGISTICS", "Room Blocks", "Coordinator", S_, 8, "8 x scale index"),
 ("HOUSING LOGISTICS", "Housing Reports", "Coordinator", S_, 4, "4 x scale index"),
 ("HOUSING LOGISTICS", "Concession Management", "Coordinator", S_, 3, "3 x scale index"),
 ("HOUSING LOGISTICS", "Attendee Liaison", "Coordinator", S_, 5, "5 x scale index"),
 ("HOUSING LOGISTICS", "Overflow Hotel Sourcing", "Coordinator", S_, 3, "3 x scale index"),

 ("THIRD PARTY VENDORS", "Vendors", "Coordinator", C_+":"+VEN, 5, "5 hrs per vendor sourced"),
 ("THIRD PARTY VENDORS", "Photographer / Videographer", "Coordinator", S_, 10,
  "10 x scale index"),

 ("STAFF MANAGEMENT", "Temporary Staff", "Manager", S_, 5, "5 x scale index"),
 ("STAFF MANAGEMENT", "Volunteers", "Manager", S_, 4, "4 x scale index"),

 ("VIP & PRESS LOGISTICS", "VIPs", "Coordinator", S_, 12, "12 x scale index"),
 ("VIP & PRESS LOGISTICS", "Press Logistics", "Coordinator", S_, 8, "8 x scale index"),

 ("SPONSORSHIPS", "Sponsorship Opportunities", "Coordinator", S_, 8, "8 x scale index"),
 ("SPONSORSHIPS", "Sponsor Management", "Coordinator", C_+":"+SPO, 1.0, "1 hr per sponsor"),

 ("SPEAKER MANAGEMENT", "Speaker Prep", "Coordinator", C_+":"+SPK, 0.7,
  "0.7 hrs per speaker"),
 ("SPEAKER MANAGEMENT", "Speaker Management Onsite", "Coordinator", C_+":"+SPK, 0.3,
  "0.3 hrs per speaker"),

 ("PROGRAMMING", "Audio Visual", "Manager", S_, 18, "18 x scale index"),
 ("PROGRAMMING", "Stage Production", "Manager", S_, 15, "15 x scale index"),
 ("PROGRAMMING", "Entertainment & Talent", "Manager", S_, 8, "8 x scale index"),
 ("PROGRAMMING", "Recording & Broadcast — Pre-Event Coordination", "Manager", S_, 8,
  "8 x scale index"),
 ("PROGRAMMING", "Recording & Broadcast — Onsite Support", "Manager", S_, 10,
  "10 x scale index"),

 ("RECEPTION PLANNING", "Concept & Strategy", "Coordinator", S_, 3, "3 x scale index"),
 ("RECEPTION PLANNING", "Venue & Layout", "Coordinator", S_, 4, "4 x scale index"),
 ("RECEPTION PLANNING", "Food & Beverage", "Coordinator", S_, 4, "4 x scale index"),
 ("RECEPTION PLANNING", "Entertainment & Atmosphere", "Coordinator", S_, 3, "3 x scale index"),
 ("RECEPTION PLANNING", "Guest Experience", "Coordinator", S_, 3, "3 x scale index"),
 ("RECEPTION PLANNING", "Staffing & Logistics", "Coordinator", S_, 3, "3 x scale index"),
 ("RECEPTION PLANNING", "Capture & Follow-Up", "Coordinator", S_, 2, "2 x scale index"),

 ("FINANCIAL MANAGEMENT", "Budgets, Reporting & Billing", "Manager", S_, 12,
  "12 x scale index"),

 ("EVENT MARKETING", "Strategy & Timeline", "Manager", S_, 8, "8 x scale index"),
 ("EVENT MARKETING", "Social Media & Email Campaigns", "Manager", S_, 9, "9 x scale index"),
 ("EVENT MARKETING", "Messaging", "Manager", S_, 5, "5 x scale index"),
 ("EVENT MARKETING", "Marketing Assistance", "Manager", S_, 5, "5 x scale index"),

 ("EXHIBIT MANAGEMENT", "Exhibitor Planning & Onsite Execution", "Manager",
  C_+":"+EXH, 1.0, "1 hr per exhibitor"),

 ("POST-EVENT", "Debrief, Reporting & Recommendations", "Manager", S_, 10,
  "10 x scale index"),

 ("TOURNAMENTS", "Venue Booking & Coordination", "Coordinator", S_, 7, "7 x scale index"),
 ("TOURNAMENTS", "Registration & Communications", "Coordinator", S_, 8, "8 x scale index"),
 ("TOURNAMENTS", "Check-In & Onsite Management", "Coordinator", S_, 7, "7 x scale index"),
]

DEFAULT_YES = {
    "PLANNING, TIMELINE & COMMUNICATIONS", "VENUE MANAGEMENT", "EVENT BRANDING",
    "FOOD & BEVERAGE", "REGISTRATION", "THIRD PARTY VENDORS", "STAFF MANAGEMENT",
    "SPONSORSHIPS", "PROGRAMMING", "FINANCIAL MANAGEMENT", "EXHIBIT MANAGEMENT",
    "POST-EVENT",
}
DEFAULT_NO_ITEMS = {"Graphic Design (add-on)", "Mobile App",
                    "Recording & Broadcast — Pre-Event Coordination",
                    "Recording & Broadcast — Onsite Support"}

TOPS = []
for t, *_ in SCOPE:
    if t not in TOPS:
        TOPS.append(t)

# Interleave a banded heading row above each category's sub-items.
LAYOUT = []                      # (kind, payload) where kind is "head" or "item"
for top in TOPS:
    LAYOUT.append(("head", top))
    for row in SCOPE:
        if row[0] == top:
            LAYOUT.append(("item", row))

sc = wb.create_sheet("SCOPE")
sc.sheet_view.showGridLines = False
F1 = 4
FN = F1 + len(LAYOUT) - 1
HEAD_ROWS = {F1 + i: p for i, (k, p) in enumerate(LAYOUT) if k == "head"}

titlebar(sc, 1, 1, 13, "SCOPE OF WORK")
note(sc, "B2", "Headings are grey; the lines underneath are what you switch on. Hours "
               "calculate from the INPUTS tab — type a number into OVERRIDE HOURS to force "
               "any line. The P&L reports at heading level.")
headers(sc, 3, 1, ["#", "SCOPE OF WORK", "STAFF", "INCLUDE?",
                   "HOW THE HOURS ARE CALCULATED", "CALC.\nHOURS",
                   "OVERRIDE\nHOURS", "HOURS\nUSED", "CLIENT\nRATE",
                   "OUR\nRATE", "CLIENT\nCOST", "OUR\nCOST", "HEADING"])
sc.row_dimensions[3].height = 30

dvs = DataValidation(type="list", formula1='"Yes,No"', allow_blank=False)
sc.add_data_validation(dvs)

# the always-on planning line prices three different rate bands in one row
PLAN_HRS = f"3*{WEEKS}+ROUND(5*{ESI},0)"
PLAN_CL = (f"({WEEKS}*({PRE_M}*{R_MGR_CL}+{PRE_C}*{R_CRD_CL})+{WEEKS}*{R_CRD_CL}"
           f"+({WEEKS}+ROUND(5*{ESI},0))*{R_MGR_CL})")
PLAN_OU = (f"({WEEKS}*({PRE_M}*{R_MGR}+{PRE_C}*{R_CRD})+{WEEKS}*{R_CRD}"
           f"+({WEEKS}+ROUND(5*{ESI},0))*{R_MGR})")

n_item = 0
for i, (kind, payload) in enumerate(LAYOUT):
    r = F1 + i
    if kind == "head":
        sc.cell(row=r, column=2, value=payload)
        for col in range(1, 14):
            cell = sc.cell(row=r, column=col)
            cell.fill = PatternFill("solid", fgColor="D9D9D9")
            cell.font = Font(name=HEAD_FONT, size=10, bold=True, color="1F1F1F")
            cell.border = Border(top=Side(style="medium", color="808080"),
                                 bottom=Side(style="thin", color="808080"))
        sc.row_dimensions[r].height = 17
        continue

    top, item, staff, kind_d, wgt, dtext = payload
    n_item += 1
    if kind_d == "PLAN":
        f = f"={PLAN_HRS}"
    elif kind_d == S_:
        f = f"=ROUND({wgt}*{ESI},0)"
    elif kind_d == W_:
        f = f"=ROUND({wgt}*{WEEKS},0)"
    else:
        f = f"=ROUND({wgt}*{kind_d.split(':')[1]},0)"
    always = kind_d == "PLAN"
    on = always or ((top in DEFAULT_YES) and (item not in DEFAULT_NO_ITEMS))

    sc.cell(row=r, column=1, value=n_item).number_format = "0"
    sc.cell(row=r, column=2, value="      " + item)
    sc.cell(row=r, column=3, value=staff)
    c = sc.cell(row=r, column=4, value="Yes" if on else "No")
    if always:
        c.fill = PatternFill("solid", fgColor=GREY)
        c.font = Font(name=BODY_FONT, size=10, bold=True, color="595959")
    else:
        c.fill = PatternFill("solid", fgColor=INPUT_FILL)
        c.font = Font(name=BODY_FONT, size=10, bold=True, color=INPUT_TXT)
        dvs.add(c)
    c.alignment = Alignment(horizontal="center")
    sc.cell(row=r, column=5, value=dtext + (" — always included" if always else ""))
    sc.cell(row=r, column=6, value=f).number_format = HRS
    o = sc.cell(row=r, column=7)
    o.fill = PatternFill("solid", fgColor=INPUT_FILL)
    o.font = Font(name=BODY_FONT, size=10, bold=True, color=INPUT_TXT)
    o.number_format = HRS
    sc.cell(row=r, column=8,
            value=f"=IF(ISNUMBER(G{r}),G{r},F{r})").number_format = HRS
    if always:
        sc.cell(row=r, column=9,
                value=f'=IF(H{r}=0,"",{PLAN_CL}/H{r})').number_format = RATE
        sc.cell(row=r, column=10,
                value=f'=IF(H{r}=0,"",{PLAN_OU}/H{r})').number_format = RATE
    else:
        sc.cell(row=r, column=9, value=(
            f'=IF(C{r}="Manager",{R_MGR_CL},IF(C{r}="Coordinator",{R_CRD_CL},'
            f'{PRE_M}*{R_MGR_CL}+{PRE_C}*{R_CRD_CL}))')).number_format = RATE
        sc.cell(row=r, column=10, value=(
            f'=IF(C{r}="Manager",{R_MGR},IF(C{r}="Coordinator",{R_CRD},'
            f'{PRE_M}*{R_MGR}+{PRE_C}*{R_CRD}))')).number_format = RATE
    sc.cell(row=r, column=11,
            value=f'=IF(D{r}="Yes",H{r}*I{r},0)').number_format = MONEY
    sc.cell(row=r, column=12,
            value=f'=IF(D{r}="Yes",H{r}*J{r},0)').number_format = MONEY
    sc.cell(row=r, column=13, value=top)
    for col in range(1, 14):
        cell = sc.cell(row=r, column=col)
        cell.border = BOX
        if cell.font.name != BODY_FONT:
            cell.font = Font(name=BODY_FONT, size=10)
        if col in (2, 5):
            cell.alignment = Alignment(wrap_text=True, vertical="center")

TR = FN + 1
sc.cell(row=TR, column=2, value="TOTAL — INCLUDED SCOPE")
sc.cell(row=TR, column=8, value=f'=SUMIF($D${F1}:$D${FN},"Yes",$H${F1}:$H${FN})')
sc.cell(row=TR, column=11, value=f'=SUMIF($D${F1}:$D${FN},"Yes",$K${F1}:$K${FN})')
sc.cell(row=TR, column=12, value=f'=SUMIF($D${F1}:$D${FN},"Yes",$L${F1}:$L${FN})')
sc.cell(row=TR, column=8).number_format = HRS
for col in (11, 12):
    sc.cell(row=TR, column=col).number_format = MONEY
for col in range(1, 14):
    cell = sc.cell(row=TR, column=col)
    cell.border = DBL
    cell.font = Font(name=BODY_FONT, size=10, bold=True)
    cell.fill = PatternFill("solid", fgColor=PINK)

# --- roll-up helper block (columns O:T), one row per heading
band(sc, 3, 15, 20, "HEADING ROLL-UP  —  feeds the P&L, nothing to edit")
R1 = 4
RN = R1 + len(TOPS) - 1
for n, top in enumerate(TOPS):
    r = R1 + n
    sc.cell(row=r, column=15, value=top)
    sc.cell(row=r, column=16, value=(
        f'=SUMIFS($H${F1}:$H${FN},$M${F1}:$M${FN},$O{r},$D${F1}:$D${FN},"Yes")')
    ).number_format = HRS
    sc.cell(row=r, column=17,
            value=f"=SUMIF($M${F1}:$M${FN},$O{r},$K${F1}:$K${FN})").number_format = MONEY
    sc.cell(row=r, column=18,
            value=f"=SUMIF($M${F1}:$M${FN},$O{r},$L${F1}:$L${FN})").number_format = MONEY
    sc.cell(row=r, column=19,
            value=f'=IF(P{r}>0,COUNTIF($P${R1}:P{r},">0"),"")')
    sc.cell(row=r, column=20, value=(
        f'=IF(P{r}=0,"",IF(SUMIFS($H${F1}:$H${FN},$M${F1}:$M${FN},$O{r},'
        f'$D${F1}:$D${FN},"Yes",$C${F1}:$C${FN},"Manager")=P{r},"PM",'
        f'IF(SUMIFS($H${F1}:$H${FN},$M${F1}:$M${FN},$O{r},$D${F1}:$D${FN},"Yes",'
        f'$C${F1}:$C${FN},"Coordinator")=P{r},"EC","PM/EC")))'))
    for col in range(15, 21):
        cell = sc.cell(row=r, column=col)
        cell.border = BOX
        cell.font = Font(name=BODY_FONT, size=10)
headers(sc, 3, 15, ["HEADING", "HOURS", "CLIENT COST", "OUR COST", "SEQ", "STAFF"])

for col, w in {1: 5, 2: 58, 3: 12, 4: 10, 5: 44, 6: 9, 7: 10, 8: 9,
               10: 9, 9: 10, 11: 12, 12: 12, 13: 3, 14: 3,
               15: 34, 16: 9, 17: 13, 18: 13, 19: 6, 20: 8}.items():
    sc.column_dimensions[get_column_letter(col)].width = w
sc.column_dimensions["M"].hidden = True          # heading key, machinery only
sc.freeze_panes = "B4"

# ================================================================ P&L ========
N_ONSITE = 8
pl = wb.create_sheet("P&L", 0)
pl.sheet_view.showGridLines = False
SS = "SCOPE!"
SEQ = f"{SS}$S${R1}:$S${RN}"

R_PRE, R_ON, R_OH, R_SUB, R_FEE, R_DISC, R_GT = 6, 7, 8, 9, 10, 11, 12
CHK_B, CHK_H = 14, 15
CAT_M, CAT_C, CAT_T, CAT_TOT = 16, 17, 18, 19
EM_BAND, EM_H = 21, 22
EM_1 = 23
EM_N = EM_1 + len(TOPS) - 1
EM_TOT = EM_N + 1
ON_BAND = EM_TOT + 2
ON_H = ON_BAND + 1
M1 = ON_H + 1
C1 = M1 + N_ONSITE
OT = C1 + N_ONSITE
ON_TOT = OT + 1
OH_BAND = ON_TOT + 3
OH_H = OH_BAND + 1
OH_PRE, OH_ON, OH_TOT = OH_H + 1, OH_H + 2, OH_H + 3

titlebar(pl, 1, 2, 10, "")
pl["B1"] = "=INPUTS!C5"
pl["B1"].font = Font(name=HEAD_FONT, size=14, bold=True, color=YELLOW_T)
pl["B2"] = ('=INPUTS!C6&"   |   "&INPUTS!C7&"   |   "&TEXT(INPUTS!C18,"0")&'
            '" event days + "&TEXT(INPUTS!C19,"0")&" set-up   |   "&'
            'TEXT(INPUTS!C22,"0")&" months planning"')
pl["B2"].font = Font(name=BODY_FONT, size=10, italic=True, color="595959")

# --- proposal summary
band(pl, 4, 2, 6, "PROPOSAL SUMMARY")
headers(pl, 5, 2, ["ITEM", "CLIENT COST", "OUR COST", "NET PROFIT", "% Profit"], size=12)

pl[f"B{R_PRE}"] = f'="Project Hours  ("&TEXT(D{EM_TOT},"#,##0")&")"'
pl[f"C{R_PRE}"] = f"=E{EM_TOT}"
pl[f"D{R_PRE}"] = f"=H{EM_TOT}"
pl[f"B{R_ON}"] = f'="Onsite Management  ("&TEXT(D{ON_TOT},"#,##0")&")"'
pl[f"C{R_ON}"] = f"=E{ON_TOT}"
pl[f"D{R_ON}"] = f"=H{ON_TOT}"
pl[f"B{R_OH}"] = f'="Staff Overhead  ("&TEXT({OVH},"$0.00")&" / staff hour)"'
pl[f"C{R_OH}"] = 0
pl[f"D{R_OH}"] = f"=E{OH_TOT}"
for r in (R_PRE, R_ON, R_OH):
    pl[f"E{r}"] = f"=C{r}-D{r}"
    pl[f"F{r}"] = f'=IF(C{r}=0,"",E{r}/C{r})'

pl[f"B{R_SUB}"] = "TOTALS"
for col in "CDE":
    pl[f"{col}{R_SUB}"] = f"=SUM({col}{R_PRE}:{col}{R_OH})"
pl[f"F{R_SUB}"] = f'=IF(C{R_SUB}=0,"",E{R_SUB}/C{R_SUB})'
pl[f"B{R_FEE}"] = f'="Admin Fee  ("&TEXT({FEE},"0.0%")&")"'
pl[f"C{R_FEE}"] = f"=C{R_SUB}*{FEE}"
pl[f"D{R_FEE}"] = 0
pl[f"E{R_FEE}"] = f"=C{R_FEE}-D{R_FEE}"
pl[f"B{R_DISC}"] = f'="Less Multi-Year Discount  ("&TEXT({DISC},"0.0%")&")"'
pl[f"C{R_DISC}"] = f'=-IF({DISC_ON}="Yes",(C{R_SUB}+C{R_FEE})*{DISC},0)'
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
        cell.font = Font(name=BODY_FONT, size=12 if r in (R_SUB, R_GT) else 10,
                         bold=r in (R_SUB, R_GT))
        cell.number_format = MONEY if col in "CDE" else (PCT if col == "F" else "General")
        if r in (R_SUB, R_GT):
            cell.fill = PatternFill("solid", fgColor=PINK)
for col in "BCDEF":
    pl[f"{col}{R_GT}"].border = DBL

# --- workload check (B:G) and margin check (H:J), side by side
band(pl, CHK_B, 2, 7, "PRE-PLANNING WORKLOAD")
band(pl, CHK_B, 8, 10, "TRUE COST VIEW")
headers(pl, CHK_H, 2, ["CATEGORY", "HOURS", "OUR RATE / HR", "OUR COST",
                       "STAFF", "HRS / PERSON / WEEK"])
headers(pl, CHK_H, 8, ["", "", ""])
pl.row_dimensions[CHK_H].height = 28
for r, name, key, cnt in ((CAT_M, "Managers", "Manager", PRE_M),
                          (CAT_C, "Coordinators", "Coordinator", PRE_C),
                          (CAT_T, "Team (project management & meetings)", "Team",
                           f"{PRE_M}+{PRE_C}")):
    pl[f"B{r}"] = name
    pl[f"C{r}"] = (f'=SUMIFS({SS}$H${F1}:$H${FN},{SS}$C${F1}:$C${FN},"{key}",'
                   f'{SS}$D${F1}:$D${FN},"Yes")')
    pl[f"E{r}"] = (f'=SUMIFS({SS}$L${F1}:$L${FN},{SS}$C${F1}:$C${FN},"{key}",'
                   f'{SS}$D${F1}:$D${FN},"Yes")')
    pl[f"D{r}"] = f'=IF(C{r}=0,"",E{r}/C{r})'
    pl[f"F{r}"] = f"={cnt}"
    pl[f"G{r}"] = f'=IF(OR(F{r}=0,{WEEKS}=0),"",C{r}/F{r}/{WEEKS})'
pl[f"B{CAT_TOT}"] = "TOTAL PRE-PLANNING"
pl[f"C{CAT_TOT}"] = f"=SUM(C{CAT_M}:C{CAT_T})"
pl[f"E{CAT_TOT}"] = f"=SUM(E{CAT_M}:E{CAT_T})"
pl[f"D{CAT_TOT}"] = f'=IF(C{CAT_TOT}=0,"",E{CAT_TOT}/C{CAT_TOT})'
pl[f"F{CAT_TOT}"] = f"={PRE_M}+{PRE_C}"
for r in range(CAT_M, CAT_TOT + 1):
    for col in "BCDEFG":
        cell = pl[f"{col}{r}"]
        cell.border = DBL if r == CAT_TOT else BOX
        cell.font = Font(name=BODY_FONT, size=10, bold=(r == CAT_TOT))
        if r == CAT_TOT:
            cell.fill = PatternFill("solid", fgColor=PINK)
    pl[f"C{r}"].number_format = HRS
    pl[f"D{r}"].number_format = RATE
    pl[f"E{r}"].number_format = MONEY
    pl[f"F{r}"].number_format = HRS
    pl[f"G{r}"].number_format = '#,##0.0;;"-"'

TRUECOST = (f"(D{R_PRE}+D{R_ON})/{UTIL}*(1+{OHP})+D{R_OH}")
MARGIN = [("True cost of delivery", f"={TRUECOST}", MONEY),
          ("True net profit", f"=C{R_GT}-({TRUECOST})", MONEY),
          ("True net margin",
           f'=IF(C{R_GT}=0,"",(C{R_GT}-({TRUECOST}))/C{R_GT})', PCT),
          ("Client price for target margin",
           f'=IF({TGT}>=1,"",({TRUECOST})/(1-{TGT}))', MONEY)]
for n, (name, formula, fmt) in enumerate(MARGIN):
    r = CAT_M + n
    pl[f"H{r}"] = name
    pl[f"J{r}"] = formula
    pl[f"J{r}"].number_format = fmt
    for col in "HIJ":
        pl[f"{col}{r}"].border = BOX
        pl[f"{col}{r}"].font = Font(name=BODY_FONT, size=10, bold=(n == 2))
    if n == 2:
        for col in "HIJ":
            pl[f"{col}{r}"].fill = PatternFill("solid", fgColor=PINK)
pl[f"B{CAT_TOT+1}"] = (
    '="HRS / PERSON / WEEK above ~10 means the headcount is too thin for the scope.    '
    'TRUE COST assumes "&TEXT(' + UTIL + ',"0%")&" utilization and "&TEXT(' + OHP + ',"0%")&'
    '" overhead — at 100% and 0% it equals the quoted cost above."')
pl[f"B{CAT_TOT+1}"].font = Font(name=BODY_FONT, size=9, italic=True, color="7F7F7F")

# --- event management (heading roll-up)
TBL = ["SCOPE OF WORK", "CLIENT RATE", "HOURS", "CLIENT COST", "OUR RATE",
       "HOURS", "OUR COST", "NET PROFIT", "% Profit"]
band(pl, EM_BAND, 2, 10, "EVENT MANAGEMENT")
headers(pl, EM_H, 2, TBL)
pl.row_dimensions[EM_H].height = 26
for n in range(len(TOPS)):
    r = EM_1 + n
    m = f"MATCH({n+1},{SEQ},0)"
    pl[f"A{r}"] = f'=IFERROR(INDEX({SS}$T${R1}:$T${RN},{m}),"")'
    pl[f"B{r}"] = f'=IFERROR(INDEX({SS}$O${R1}:$O${RN},{m}),"")'
    pl[f"D{r}"] = f'=IFERROR(INDEX({SS}$P${R1}:$P${RN},{m}),"")'
    pl[f"E{r}"] = f'=IFERROR(INDEX({SS}$Q${R1}:$Q${RN},{m}),"")'
    pl[f"G{r}"] = f'=IF(B{r}="","",D{r})'
    pl[f"H{r}"] = f'=IFERROR(INDEX({SS}$R${R1}:$R${RN},{m}),"")'
    pl[f"C{r}"] = f'=IF(OR(B{r}="",D{r}=0),"",E{r}/D{r})'
    pl[f"F{r}"] = f'=IF(OR(B{r}="",G{r}=0),"",H{r}/G{r})'
    pl[f"I{r}"] = f'=IF(B{r}="","",E{r}-H{r})'
    pl[f"J{r}"] = f'=IF(OR(B{r}="",E{r}=0),"",I{r}/E{r})'
pl[f"B{EM_TOT}"] = "TOTALS"
for col in ("D", "E", "G", "H", "I"):
    pl[f"{col}{EM_TOT}"] = f"=SUM({col}{EM_1}:{col}{EM_N})"
pl[f"J{EM_TOT}"] = f'=IF(E{EM_TOT}=0,"",I{EM_TOT}/E{EM_TOT})'

# --- onsite management
band(pl, ON_BAND, 2, 10, "ONSITE MANAGEMENT")
headers(pl, ON_H, 2, TBL)
pl.row_dimensions[ON_H].height = 26
MGR_HRS = f"({EVD}+{SETD})*{H_MGR}+{TRVD}*{H_TRV}"
CRD_HRS = f"({EVD}+{SETD})*{H_CRD}+{TRVD}*{H_TRV}"
for i in range(N_ONSITE):
    r = M1 + i
    on = f"{i+1}<={ON_M}"
    pl[f"A{r}"] = f'=IF({on},"PM","")'
    pl[f"B{r}"] = f'=IF({on},INPUTS!$C${MGR_ROW1+i},"")'
    pl[f"C{r}"] = f'=IF({on},{R_MGR_ON},"")'
    pl[f"D{r}"] = f'=IF({on},{MGR_HRS},"")'
    pl[f"F{r}"] = f'=IF({on},{R_MGR},"")'
for j in range(N_ONSITE):
    r = C1 + j
    on = f"{j+1}<={ON_C}"
    pl[f"A{r}"] = f'=IF({on},"EC","")'
    pl[f"B{r}"] = f'=IF({on},INPUTS!$C${CRD_ROW1+j},"")'
    pl[f"C{r}"] = f'=IF({on},{R_CRD_ON},"")'
    pl[f"D{r}"] = f'=IF({on},{CRD_HRS},"")'
    pl[f"F{r}"] = f'=IF({on},{R_CRD},"")'
pl[f"A{OT}"] = f'=IF({ON_C}=0,"","EC")'
pl[f"B{OT}"] = (f'=IF({ON_C}=0,"","Coordinator Overtime  ("&TEXT({ON_C},"0")&'
                f'" x "&TEXT({H_OT},"0")&" hrs x "&TEXT({EVD}+{SETD},"0")&" days)")')
pl[f"C{OT}"] = f'=IF({ON_C}=0,"",{R_CRD_ON}*{OT_X})'
pl[f"D{OT}"] = f'=IF({ON_C}=0,"",{ON_C}*({EVD}+{SETD})*{H_OT})'
pl[f"F{OT}"] = f'=IF({ON_C}=0,"",{R_CRD}*{OT_X})'
for r in range(M1, OT + 1):
    pl[f"E{r}"] = f'=IF(B{r}="","",C{r}*D{r})'
    pl[f"G{r}"] = f'=IF(B{r}="","",D{r})'
    pl[f"H{r}"] = f'=IF(B{r}="","",F{r}*G{r})'
    pl[f"I{r}"] = f'=IF(B{r}="","",E{r}-H{r})'
    pl[f"J{r}"] = f'=IF(OR(B{r}="",E{r}=0),"",I{r}/E{r})'
pl[f"B{ON_TOT}"] = "TOTALS"
for col in ("D", "E", "G", "H", "I"):
    pl[f"{col}{ON_TOT}"] = f"=SUM({col}{M1}:{col}{OT})"
pl[f"J{ON_TOT}"] = f'=IF(E{ON_TOT}=0,"",I{ON_TOT}/E{ON_TOT})'

pl[f"B{ON_TOT+1}"] = (f'=IF(OR({ON_M}>{N_ONSITE},{ON_C}>{N_ONSITE}),'
                      f'"WARNING: more than {N_ONSITE} managers or coordinators — '
                      f'the extra people are NOT costed above.","")')
pl[f"B{ON_TOT+1}"].font = Font(name=BODY_FONT, size=10, bold=True, color="C00000")

for rng in (range(EM_1, EM_TOT + 1), range(M1, ON_TOT + 1)):
    for r in rng:
        tot = r in (EM_TOT, ON_TOT)
        for col in "ABCDEFGHIJ":
            cell = pl[f"{col}{r}"]
            cell.border = DBL if tot else BOX
            cell.font = Font(name=BODY_FONT, size=10, bold=tot)
            if tot:
                cell.fill = PatternFill("solid", fgColor=PINK)
            cell.alignment = Alignment(wrap_text=(col == "B"), vertical="center",
                                       horizontal="center" if col == "A" else None)
            if col in ("C", "F"):
                cell.number_format = RATE
            elif col in ("D", "G"):
                cell.number_format = HRS
            elif col in ("E", "H", "I"):
                cell.number_format = MONEY
            elif col == "J":
                cell.number_format = PCT

# blank out unused rows in both tables so they read as empty space
blank = DifferentialStyle(font=Font(color="FFFFFF"), border=Border(),
                          fill=PatternFill(bgColor="FFFFFF", fill_type="solid"))
for first, last in ((EM_1, EM_N), (M1, OT - 1)):
    rule = Rule(type="expression", dxf=blank, stopIfTrue=True)
    rule.formula = [f'$B{first}=""']
    pl.conditional_formatting.add(f"A{first}:J{last}", rule)

# --- staff overhead
band(pl, OH_BAND, 2, 5, "STAFF OVERHEAD")
headers(pl, OH_H, 2, ["ITEM", "STAFF HOURS", "RATE / HR", "OVERHEAD COST"])
pl[f"B{OH_PRE}"] = "Pre-planning staff hours"
pl[f"C{OH_PRE}"] = f"=D{EM_TOT}"
pl[f"B{OH_ON}"] = "Onsite staff hours (incl. overtime)"
pl[f"C{OH_ON}"] = f"=D{ON_TOT}"
for r in (OH_PRE, OH_ON):
    pl[f"D{r}"] = f"={OVH}"
    pl[f"E{r}"] = f"=C{r}*D{r}"
pl[f"B{OH_TOT}"] = "TOTAL STAFF OVERHEAD"
pl[f"C{OH_TOT}"] = f"=SUM(C{OH_PRE}:C{OH_ON})"
pl[f"E{OH_TOT}"] = f"=SUM(E{OH_PRE}:E{OH_ON})"
for r in range(OH_PRE, OH_TOT + 1):
    for col in "BCDE":
        cell = pl[f"{col}{r}"]
        cell.border = DBL if r == OH_TOT else BOX
        cell.font = Font(name=BODY_FONT, size=10, bold=(r == OH_TOT))
        if r == OH_TOT:
            cell.fill = PatternFill("solid", fgColor=PINK)
    pl[f"C{r}"].number_format = HRS
    pl[f"D{r}"].number_format = RATE
    pl[f"E{r}"].number_format = MONEY
note(pl, f"B{OH_TOT+2}", "Overhead is a CTC cost — not billed, so it comes out of margin. "
                         "The admin fee is charged on top of the client subtotal.")

pl.column_dimensions["A"].width = 6.6
pl.column_dimensions["B"].width = 49.1
for col, w in {"C": 14.4, "D": 12.0, "E": 15.4, "F": 13.0, "G": 12.0,
               "H": 15.4, "I": 13.2, "J": 9.9}.items():
    pl.column_dimensions[col].width = w
pl.freeze_panes = "A5"
pl.sheet_properties.pageSetUpPr.fitToPage = True
pl.page_setup.orientation = "landscape"
pl.page_setup.fitToWidth = 1
pl.page_setup.fitToHeight = 0

# =========================================================== HOW TO USE ======
rd = wb.create_sheet("HOW TO USE")
rd.sheet_view.showGridLines = False
rd.column_dimensions["A"].width = 4
rd.column_dimensions["B"].width = 112
titlebar(rd, 1, 2, 2, "HOW TO BUILD A NEW CONFERENCE P&L")

STEPS = [
 ("STEP 1 — INPUTS", None),
 (None, "Event size: attendees, exhibitors, sponsors, speakers, vendors to source, site visits."),
 (None, "Schedule: event days, set-up days, travel days, months of pre-planning."),
 (None, "Staffing: how many managers and coordinators onsite, and how many in pre-planning."),
 (None, "Rates are pre-set — manager $60/hr cost, coordinator $42/hr cost. Change only if the "
        "rate card changes."),
 (None, None),
 ("STEP 2 — SCOPE", None),
 (None, "Every line matches the Master Proposal Template, sub-item by sub-item. Set INCLUDE? "
        "to Yes or No on each."),
 (None, "Hours calculate automatically. Disagree with a line? Type your number into OVERRIDE "
        "HOURS — nothing else changes."),
 (None, None),
 ("STEP 3 — P&L", None),
 (None, "Nothing to type. Scope rolls up to the top-level proposal headings, so the P&L reads "
        "the same way the proposal does."),
 (None, "Watch HRS / PERSON / WEEK — above roughly 10 the headcount is too thin for the scope."),
 (None, None),
 ("THE EVENT SCALE INDEX", None),
 (None, "Most scope lines are priced as a base weight multiplied by the Event Scale Index, "
        "shown on INPUTS. The index is:"),
 (None, "        (attendees / 250) ^ 1/3   x   (planning months / 6) ^ 1/2   x   "
        "(event days / 3) ^ 1/4"),
 (None, "An index of 1.00 is a 250-person, 3-day event with 6 months of planning. The cube "
        "and square roots matter: doubling attendance raises the index about 26%, not 100%, "
        "which is how our hours have actually behaved. Straight percentage-of-attendees rules "
        "break down badly at 1,000+ people."),
 (None, "Lines with a real count behind them skip the index and bill directly: exhibitors x 1 hr, "
        "sponsors x 1 hr, speakers x 1 hr, vendors x 5 hrs, site visits x 10 hrs. Weekly items "
        "— meetings, the project management system, approvals — bill 1 hour per planning week."),
 (None, None),
 ("HOW THE MONEY WORKS", None),
 (None, "CLIENT COST = hours x client rate. Pre-planning: manager $90 / coordinator $65. "
        "Onsite: manager $100 / coordinator $65. Coordinator overtime bills at 1.5x."),
 (None, "OUR COST = hours x our rate. Manager $60, coordinator $42, overtime 1.5x."),
 (None, "STAFF OVERHEAD = $0.61 x every CTC staff hour, pre-planning and onsite. A cost to us, "
        "not billed, so it reduces margin."),
 (None, "ADMIN FEE = 2% of the client subtotal, added to what the client pays. Nothing costs "
        "against it, so all of it is profit."),
 (None, "MULTI-YEAR DISCOUNT = the 5% off additional years. Off by default — switch it on at "
        "the bottom of INPUTS section 7."),
 (None, None),
 ("THE TRUE COST VIEW  —  read this before trusting a margin", None),
 (None, "The % Profit column is a GROSS margin on direct labour. It counts salary and burden. "
        "It does not count the part of the year staff are paid but not billable, and it does "
        "not count real overhead. Those are the two inputs at the bottom of INPUTS section 7."),
 (None, "UTILIZATION % = billable hours divided by paid hours. At 100% the true cost view "
        "matches the quoted cost exactly, so the workbook behaves as before until you change "
        "it. Agencies plan around 75-85%. Measure it from timesheets against payroll before "
        "you trust any number here."),
 (None, "OVERHEAD % OF DIRECT LABOR = rent, software, insurance, non-billable salaries and "
        "business development as a share of staff cost. Typical agency range is 15-30%. This "
        "supersedes the $0.61/hr line, which is around 1% of a manager hour."),
 (None, "TRUE NET MARGIN on the P&L is what is left after both. At 80% utilization and 15% "
        "overhead a P&L quoting 36% returns about 8%. CLIENT PRICE FOR TARGET MARGIN tells you "
        "what to charge instead."),
]
r = 3
for head, body in STEPS:
    if head:
        c = rd.cell(row=r, column=2, value=head)
        c.font = Font(name=HEAD_FONT, size=12, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=BLUE)
        rd.row_dimensions[r].height = 20
    elif body:
        c = rd.cell(row=r, column=2, value="•  " + body)
        c.font = Font(name=BODY_FONT, size=10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        rd.row_dimensions[r].height = 15 * (1 + len(body) // 105)
    r += 1

wb.save(OUT)
print(f"wrote {OUT}: {len(SCOPE)} scope sub-items, {len(TOPS)} top-level headings")
