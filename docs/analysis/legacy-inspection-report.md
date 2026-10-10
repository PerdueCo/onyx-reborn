# BSSI Student Information System — Legacy Source Code Analysis

**Application created by Clarence Perdue Jr.**
**Institution: Gwinnett Technical Institute**
**Approximate date: 1998 (VB4, ca. April–May 1998 based on hardcoded dates in forms)**

> This report is derived entirely from static reading of the source files in
> `docs/legacy-reference/legacy-code-copy/`. No legacy files were modified or executed.
> No external sources were used. All citations reference file names and line numbers
> as found in the workspace.

---

## 1. Inventory

### Source Files Present

| File | VB Name | Role |
|---|---|---|
| `BSSI06~1.VBP` | Project1 | VB4 project file |
| `MAIN.BAS` | Utilities | Global types, constants, file-open helpers, startup `Sub Main` |
| `RANDOM1.BAS` | Module1 | Navigation, binary search routines, print routines |
| `MAINMENU.FRM` | frmMainMenu | Top-level menu (Student / Instructor / Exit) |
| `SPLASH~1.FRM` | frmSplash | Splash screen |
| `SSN.FRM` | frmSSSNumber | SSN entry and verification dialog |
| `STUDENTS.FRM` | frmStudentInformation | Student data entry form |
| `CURREMPL.FRM` | frmCurrentEmployment | Employment data entry form |
| `FRMSEA~1.FRM` | frmSearch | Find/display student + employment record |
| `FRMREP~1.FRM` | frmReports | Reports menu |
| `FRMRAND1.FRM` | frmRandom | Scroll through SSN index (Random.txt) |
| `FRMDIS~1.FRM` | frmDisplay | View all student records |
| `FRMEMP~1.FRM` | frmEmployment | View all employment records |
| `FRMPRI~1.FRM` | frmPrintSS | Print output surface |
| `FRMSEL~1.FRM` | frmSelect_Rec | Multi-record selection (up to 10 SSNs) |
| `SWITCH.FRM` | frmSwitchBoard | Alternate switchboard (Instructor path) |
| `FRMABOUT.FRM` | frmAbout | About dialog |
| `FRMCONST.FRM` | frmConstruction | "Under construction" placeholder |
| `BACK.FRM` | mdiBackGround | MDI parent (referenced but commented out of startup) |
| `Copy of FRMSEL~1.FRM` | — | Duplicate backup copy |
| `RANDOM1` | — | No extension; likely a build artifact |
| `*.FRX` files | — | Binary resources (images, combo-box data) for matching `.FRM` |
| `CURREMPL.LOG` | — | VB4 load/compile log |
| `MSSCCPRJ.SCC` | — | Source-control metadata only |

### Data Files Present

| File | Contents |
|---|---|
| `Data/Student.txt` | 5 fictional test student records |
| `Data/Employment.txt` | 5 fictional test employment records |
| `Data/Random.txt` | 5 SSNs, 10 bytes each |
| `Data/RandomA.txt` | 5 SSNs in 14-byte slots |
| `Data/README.txt` | Notes about the test data pack |

### Original Documentation

**Not found.** `docs/legacy-reference/legacy-code-copy/documentation/` exists as an empty
directory. `docs/analysis/`, `docs/decisions/`, and `docs/design-reference/` were also empty
at the time of inspection. No external design documents, requirements, or original user manual
were found anywhere in the workspace.

### Missing Items

| Item | Status |
|---|---|
| `StudentVB.DB` — the primary writable student database | Not found |
| `EmploymentA.DB` — the primary writable employment database | Not found |
| `frmInstructor` form | Referenced at `MAINMENU.FRM:210` (commented out); source file not present |
| `frmMaintenance` form | Referenced at `SWITCH.FRM:327` and `MAINMENU.FRM:246`; source file not present |
| Any `.mdb` Access database | Not found; application does not use one |

---

## 2. Original Workflow

### Startup

**`Sub Main()`** — `MAIN.BAS:198–216`

The VB project's startup is a code sub, not a form (confirmed by `StartMode=0` with no
`StartupObject` form in `BSSI06~1.VBP:26`).

```
Sub Main → show frmSplash (modal) → unload frmSplash → load and show frmMainMenu
```

`frmMainMenu` displays the application title **"ONYX Student Information System"**
(`MAINMENU.FRM:129`) and the institution name **"Gwinnett Technical Institute"**
(`MAINMENU.FRM:148`). Three buttons appear: **STUDENT**, **INSTRUCTOR**, and **EXIT**.

The MDI parent `mdiBackGround` is present in the project (`BSSI06~1.VBP:5`) and referenced in
cleanup code (`MAINMENU.FRM:253`), but the lines that load and show it in `Sub Main` are
commented out (`MAIN.BAS:203`, `MAIN.BAS:215`). Several forms declare `MDIChild = -1 'True`,
so they were designed to dock inside an MDI container — but the container is not activated at
startup.

### Student Entry Workflow

1. **STUDENT button** → `MAINMENU.FRM:189–191`: loads and shows `frmSSSNumber`, hides
   `frmMainMenu`.
2. **SSN dialog (`frmSSSNumber`)** — `SSN.FRM`: user types SSN in `txtSNN` and re-types it in
   `txtVerifySSN` (both masked with `*`). MaxLength = 9 on both fields (`SSN.FRM:41`,
   `SSN.FRM:51`).
3. **OK button (`cmdSearch_Click`)** — `SSN.FRM:146`:
   - Opens `RandomA.txt` (file #1) via `OpenFileQuery`.
   - Computes `numQuery = LOF(1) / Len(Query)` where `Len(Query)` = 14 (see §4).
   - Builds in-memory `Index()` array; binary-searches for the entered SSN.
   - **If found**: calls `SortQueryText` then `ShowStudentInfo frmStudentInformation`.
   - **If not found**: calls `cmdSave_Click` (writes a new `QuerySoc` record to `RandomA.txt`),
     then calls `ShowStudentInfo`.
   - Special case: if the user types `EXIT` (case-insensitive, `SSN.FRM:158`), it hides
     `frmSSSNumber` and shows `frmMainMenu`.
4. **Student information form (`frmStudentInformation`)** — `STUDENTS.FRM`: user fills in all
   fields. On **Accept** (`STUDENTS.FRM:703`):
   - Opens `StudentVB.DB` (file #2).
   - Searches `IndexStudent()` for the SSN.
   - Writes `Put #2, numStudents, Students` for new; prompts and writes
     `Put #2, IndexStudent(isFound).RecNum, Students` for existing.
   - Loads and shows `frmCurrentEmployment`.

### Employment Entry Workflow

5. **Employment form (`frmCurrentEmployment`)** — `CURREMPL.FRM`: user fills in employer
   details. On **Accept** (`CURREMPL.FRM:428`):
   - Generates `Company_Code` via `CreateCompanyCode()` — first 4 chars of company name +
     last 4 chars of work phone, uppercased (`CURREMPL.FRM:738`).
   - Writes `Company_Code` back into the `Students` record (`CURREMPL.FRM:452`).
   - Writes `Put #3, numCurrEmp, JOB` for new employment (`CURREMPL.FRM:492`).
   - Also writes the updated `Students` record: `Put #2, gWhichStudentRecord, Students`
     (`CURREMPL.FRM:499`).
   - Calls `SortEmploymentText` and `SortStudentText` to regenerate the `.txt` reporting copies.
   - Unloads both forms; shows `frmSSSNumber` for the next student.

### Instructor Workflow

The **INSTRUCTOR button** on `frmMainMenu` relabels the three buttons to **REPORT MENU**,
**STUDENT MAINTENANCE**, and **CLOSE MENU** (`MAINMENU.FRM:230–235`). REPORT MENU shows
`frmReports`. STUDENT MAINTENANCE is mapped but its handler body is empty (commented out,
`MAINMENU.FRM:208–212`). `frmInstructor` is referenced in a comment but its source file is not
present.

### Search Workflow

From `frmReports`, button 2 opens `frmSearch` (`FRMREP~1.FRM:252`).

User types an SSN in `txtSearch` (MaxLength 9) and clicks **Search**. This calls `Search_SS`
(`RANDOM1.BAS:1253`):

- Opens `random.txt` (file #1), binary-searches for the SSN in `RecBuf` (`Query_File`).
- If found, calls `Query_Student` which opens `student.txt`, binary-searches by SSN, fills all
  student fields on screen.
- `Query_Student` then calls `Query_Employment` which opens `employment.txt`, binary-searches by
  the `Company_Code` found in the student record, fills all employment fields on screen.
- Previous / Next buttons scroll through `student.txt` by record number.

### Reports Workflow

`frmReports.Form_Load` (`FRMREP~1.FRM:296`) regenerates all three text files before showing any
report. Five report options:

1. **Print Selected** — opens `frmSelect_Rec` for up to 10 SSNs.
2. **Find/Display Single** — opens `frmSearch`.
3. **View/Print All SSNs** — opens `frmRandom` (scrolls `random.txt`).
4. **View/Print All Students** — opens `frmDisplay` (scrolls `student.txt`).
5. **View/Print Employment** — opens `frmEmployment` (scrolls `employment.txt`).

Print output goes to `frmPrintSS`, which is a VB4 form used as a print surface (sends to local
printer).

---

## 3. Data Structures

### Active Disk Record Types

#### `Student_File` (active definition)

Defined in `MAIN.BAS:22–64`. An identical copy is in `RANDOM1.BAS:65–87` named `Student_File`
(module-local).

| Field | Declared Type | Declared Length (bytes) | Notes |
|---|---|---|---|
| `Program_Code` | String | 7 | e.g. `CIS101` |
| `Date` | String | 9 | Entry date, e.g. `01/15/98` |
| `Program_Name` | String | 31 | e.g. `Computer Information Systems` |
| `SS_Number` | String | 10 | Primary key. 9 digits padded to 10 |
| `Last_Name` | String | 16 | |
| `First_Name` | String | 16 | |
| `Home_Phone` | String | 16 | Format `(555)555-0101` |
| `Work_Phone` | String | 16 | |
| `Address` | String | 31 | |
| `City` | String | 31 | |
| `State` | String | 3 | 2-letter abbreviation |
| `zip` | String | 11 | |
| `High_School` | String | 31 | |
| `Date_Graduated` | String | 11 | e.g. `06/01/1996` |
| `Month` | String | 3 | Birth month |
| `Day` | String | 3 | Birth day |
| `YesNo` | String | 2 | Job-seeking flag |
| `Description` | String | 101 | Desired job type |
| `Company_Code` | String | 9 | Foreign key → Employment record |
| **Total** | | **357 bytes** | |

> ⚠️ **Unverified — commented-out earlier version**: Lines 24–41 of `MAIN.BAS` show a previous
> `Student_File` definition with different field widths (e.g. `Last_Name As String * 15`). Those
> lines are fully commented and inactive. The 357-byte layout above is the one the code actually
> uses.

#### `Employment_Type` (active definition)

Named `Employment_Type` in `MAIN.BAS:103–119`; named `Employment_File` in
`RANDOM1.BAS:101–116`. Field names and lengths are identical in both.

| Field | Declared Type | Declared Length (bytes) | Notes |
|---|---|---|---|
| `Company_Code` | String | 9 | Primary key; also stored in `Student_File` |
| `Company_Name` | String | 31 | |
| `Address` | String | 26 | **26, not 31** — narrower than student address |
| `City` | String | 31 | |
| `State` | String | 3 | |
| `zip` | String | 11 | |
| `Job_Title` | String | 31 | |
| `Current_Supervisor` | String | 31 | |
| `Phone_Number` | String | 16 | |
| `Hours_per_Week` | String | 3 | |
| `Amount` | String | 16 | Stored as string; formatted `$#,####0.00` on display |
| `Company_Type` | String | 30 | |
| **Total** | | **238 bytes** | |

#### `Query_File` (RandomA.txt / SSN index)

Defined in `MAIN.BAS:67–72` and `RANDOM1.BAS:92–96`.

| Field | Declared Type | Declared Length (bytes) |
|---|---|---|
| `SS_Number` | String | 10 |
| `RecNum` | Integer | 2 |
| **Payload total** | | **12 bytes** |

> ⚠️ **Unverified — `Len(Query)` bug**: The file is opened with slot size 14, not 12. See §4.

---

### In-Memory Index Types (never written to disk as their own records)

#### `Query_Type`

`MAIN.BAS:75–80`. Array variable: `Index()`. Used by `frmSSSNumber`.

| Field | Type | Length |
|---|---|---|
| `SS_Number` | String | 10 |
| `RecNum` | Integer | 2 |

#### `StudentIndexType`

`MAIN.BAS:83–88`. Array variable: `IndexStudent()`. Used by `frmStudentInformation` and
`frmReports`.

| Field | Type | Length |
|---|---|---|
| `SS_Number` | String | 10 |
| `RecNum` | Integer | 2 |

#### `CurrentEmployeeIndexType`

`MAIN.BAS:91–96`. Array variable: `IndexCurrEmp()`. Used by `frmCurrentEmployment` and
`frmReports`.

| Field | Type | Length |
|---|---|---|
| `Company_Code` | String | 9 |
| `RecNum` | Integer | 2 |

---

### Student–Employer Linkage

The link between a student and their employer is the `Company_Code` field, which appears in
both records.

- **Student side**: `Student_File.Company_Code` (9 bytes, last field). Written by
  `frmCurrentEmployment.cmdAcceptCurrentEmployment_Click` at `CURREMPL.FRM:452` — this is the
  only place where the student record is updated with the company code.
- **Employment side**: `Employment_Type.Company_Code` (9 bytes, first field = sort key for that
  file).
- **Code is generated, not entered**: `CreateCompanyCode()` at `CURREMPL.FRM:727–740` builds it
  as `UCase(Left(companyName, 4) + Right(workPhone, 4))`. Example: company name `Peachtree
  Software Services` + work phone last 4 `2101` → `PEAC2101`.

> ⚠️ **Unverified — test data discrepancy**: The test data in `Employment.txt` uses codes like
> `PEAC1101`, not `PEAC2101`. The last 4 of work phone `(555)555-2101` should produce `2101`,
> but the test data shows `1101`. This could mean the test data used the student's home phone
> `(555)555-1101` instead, or was constructed manually without following the formula. The code
> at `CURREMPL.FRM:450` passes `txtWorkPhone.Text` as the second argument, but whether that
> matched the test entry is unknown.

---

## 4. Read and Write Behavior

### File Paths (hardcoded constants)

All paths are declared in `MAIN.BAS:148–151`:

```vb
Public Const StudentTextFile           = "E:\StudentVB.DB"     ' channel #2
Public Const CurrentEmploymentTextFile = "E:\EmploymentA.DB"   ' channel #3
Public Const Query                     = "E:\RandomA.txt"      ' channel #1
Public Const Student                   = "E:\Student.txt"      ' channel #4
```

`RANDOM1.BAS` overrides these with `A:\` paths in its own `Open` statements
(`RANDOM1.BAS:685`, `RANDOM1.BAS:695`, `RANDOM1.BAS:994`, `RANDOM1.BAS:1035`,
`RANDOM1.BAS:1097`):

```vb
Open "a:\random.txt"     For Random As #1 Len = Len(MyRecord)
Open "a:\student.txt"    For Random As #1 Len = Len(MyRecord2)
Open "a:\employment.txt" For Random As #1 Len = Len(MyRecord3)
```

> ⚠️ **Unverified — path conflict**: Entry and reporting use different drives. `MAIN.BAS` opens
> `StudentVB.DB` on `E:\`; `RANDOM1.BAS` reads the reporting copy `student.txt` from `A:\`.
> The `README.txt` states the original program expected all files on `A:\`. The `E:\` constants
> may reflect a development machine mapping, not the production path.

### Channel Assignment

| Channel | File | Opened by |
|---|---|---|
| #1 | `RandomA.txt` (entry) or `random.txt` / `student.txt` / `employment.txt` (reports) | `OpenFileQuery` / `RANDOM1.BAS` `Open` statements |
| #2 | `StudentVB.DB` | `OpenFileStudent` (`MAIN.BAS:339`) |
| #3 | `EmploymentA.DB` | `OpenFileCurrentEmployment` (`MAIN.BAS:354`) |
| #4 | `Student.txt` (via `OpenFileStudentDb`) | `MAIN.BAS:347` — used in one helper only |
| #5 | `Student.txt` (reporting output) | `SortStudentText` (`FRMREP~1.FRM:334`) |
| #intFile (FreeFile) | `RANDOM.txt` (reporting output) | `SortQueryText` (`SSN.FRM:232`) |

> ⚠️ **Channel #1 is reused** for four different files depending on which module opens it last.
> `CloseAll` (`MAIN.BAS:370`) closes #1 through #6 to reset state, and `frmReports.Form_Load`
> calls it before regenerating files.

### Record Lengths — Calculated vs. Declared

| File | `Len()` expression used | Calculated value | Correct? |
|---|---|---|---|
| `StudentVB.DB` | `Len(Students)` | 357 bytes | ✅ Matches sum of `Student_File` fields |
| `EmploymentA.DB` | `Len(JOB)` | 238 bytes | ✅ Matches sum of `Employment_Type` fields |
| `random.txt` | `Len(MyRecord)` where `MyRecord As Query_File` | 12 bytes | ✅ Correct (10 + 2) |
| `RandomA.txt` (entry path) | `Len(Query)` where `Query = "E:\RandomA.txt"` | **14 bytes** | ❌ Bug — `Len()` of a String constant returns the string's character count, not the record size |
| `RandomA.txt` (reporting output via `SortQueryText`) | `Len(Query)` again | **14 bytes** | ❌ Same bug — consistent with each other but not with the `Query_File` payload of 12 bytes |

> ⚠️ **Unverified — effect of bug**: Each record in `RandomA.txt` occupies a 14-byte slot. The
> 12-byte payload fills the first 12 bytes; the last 2 bytes of each slot are uninitialised
> padding. Because the same wrong length is used for both reading and writing, the file is
> self-consistent — it just wastes 2 bytes per record. `Data/README.txt` documents this
> explicitly.

### Read and Write Statements

**Writing student records** — `STUDENTS.FRM:770`, `STUDENTS.FRM:786`:

```vb
Put #2, numStudents, Students                       ' new record
Put #2, IndexStudent(isFound).RecNum, Students      ' update existing
```

**Writing employment records** — `CURREMPL.FRM:492`, `CURREMPL.FRM:511`:

```vb
Put #3, numCurrEmp, JOB                             ' new record
Put #3, IndexCurrEmp(isFound).RecNum, JOB           ' update existing
```

**Writing `RandomA.txt`** — `SSN.FRM:385`:

```vb
Put #1, numQuery, QuerySoc                          ' new SSN entry
```

**Writing `Student.txt` (reporting copy)** — `FRMREP~1.FRM:334–361`:

```vb
Open "A:\Student.txt" For Output As #5
Print #5, .Program_Code; .Date; .Program_Name; ... .Company_Code;
```

Every `Print #5` ends with a semicolon including the last field per record
(`FRMREP~1.FRM:356`). This means there is **no CRLF between records** — the entire file is one
continuous stream of fixed-width characters. When read back as a `Random` file with the correct
357-byte record length, this works correctly. The apparent line breaks visible in a text editor
are an accident of where the fixed-width fields happen to reach line-wrap width.

---

## 5. Business Rules

### Confirmed by Source Code

**SSN entry and verification**

- Both `txtSNN` and `txtVerifySSN` must be non-empty (`SSNumberOK` function, `SSN.FRM:306`).
- Both fields must match: `Trim(txtSNN) = Trim(txtVerifySSN)` (`SSN.FRM:171`).
- Both must be exactly 9 characters: `Len(txtSNN.Text) = 9` (`SSN.FRM:172`).
- Accepted characters: digits `0–9` and the letters `e`, `x`, `i`, `t`
  (`SSN.FRM:354`: `ValiText(KeyAscii, "0123456789exit", True)`). Typing the word `EXIT` triggers
  the escape path; individual letters `e`, `x`, `i`, `t` would also be silently accepted.

**Duplicate detection — Query/SSN file**

`SSN.FRM.cmdSave_Click` (`SSN.FRM:362`) searches `RandomA.txt` first. If the SSN exists, it
prompts "This name is already on file. Do you want to save a revised record?" — but the update
branch is commented out (`SSN.FRM:399–401`). A confirmed "Yes" (answer = 6) does nothing.

**Duplicate detection — Student file**

`STUDENTS.FRM.cmdAccept_Click` (`STUDENTS.FRM:703`) searches `IndexStudent()`. If found,
prompts the same message. A confirmed "Yes" overwrites the record at
`IndexStudent(isFound).RecNum` (`STUDENTS.FRM:786`). This path is active.

**Duplicate detection — Employment file**

`CURREMPL.FRM.cmdAcceptCurrentEmployment_Click` (`CURREMPL.FRM:428`) searches `IndexCurrEmp()`
by the generated `Company_Code`. If found, prompts and overwrites
(`Put #3, IndexCurrEmp(isFound).RecNum, JOB` at `CURREMPL.FRM:511`). This path is active.

**Required fields (source-confirmed)**

- Last Name: must not be blank on `LostFocus` (`STUDENTS.FRM:1388`).
- First Name: must not be blank on `LostFocus` (`STUDENTS.FRM:1263`).
- Home Phone: must not be blank and must be ≥ 13 characters on `LostFocus` (`STUDENTS.FRM:1340`).
- No other fields have confirmed required-field validation in the source code.

**Company code generation**

- Formula: `UCase(Left(companyName, 4) + Right(workPhone, 4))` (`CURREMPL.FRM:738`).
- Result is truncated to 8 characters (`Mid(..., 1, 8)` at `CURREMPL.FRM:452`), stored in a
  9-byte field (1 byte trailing space).

**Report regeneration**

`frmReports.Form_Load` always regenerates `Random.txt`, `Student.txt`, and `Employment.txt`
from the primary DB files before any report is shown (`FRMREP~1.FRM:296–318`). The text files
are always fresh as of the moment the Reports form opens.

**Binary search precondition**

All three binary searches (`Search_SS`, `Query_Student`, `Query_Employment`) assume the target
file is **sorted by its key field**. The sort is performed by the `CreateIndex` /
`SortStudentText` / `SortEmploymentText` routines before any search. If the DB files are
modified outside the application, the search would fail silently or return wrong results.

### Assumed / Unverified

> ⚠️ **Unverified**: It is not known whether the application ran successfully on the original
> 1998 hardware. The `E:\` drive constants in `MAIN.BAS` suggest a secondary drive mapping that
> may differ from the `A:\` floppy paths used in `RANDOM1.BAS`. Whether these were reconciled
> at runtime (e.g. via `SUBST`) is unknown.

> ⚠️ **Unverified**: The `frmInstructor` / STUDENT MAINTENANCE path was never finished. It is
> unknown what it was intended to do.

> ⚠️ **Unverified**: The `frmConstruction` form has a 10-second timer (`tmrConstruction`,
> interval 10000ms, `FRMCONST.FRM:43`). Its timer event code is not visible without the binary
> `.FRX`, so its behavior is unknown.

> ⚠️ **Unverified**: `SortQueryText` (`SSN.FRM:215`) calls `CreateIndex` which reads from
> channel #1 — but `OpenFileQuery` has already opened channel #1. Whether this produces a
> double-open error depends on VB4 runtime behavior.

> ⚠️ **Unverified**: The `YesNo` field is set from the loop index (`0` or `1`) of the radio
> button array, so the stored value is `"0"` or `"1"`, not `"Y"` or `"N"`. The display code
> uses `Val(.YesNo)` to select the radio button, which is consistent — but this means the field
> is not human-readable in the text files.

---

## 6. Documentation Comparison

**Not found.** No original documentation exists in the workspace. All folders intended for
documentation (`docs/analysis/`, `docs/decisions/`, `docs/design-reference/`,
`docs/legacy-reference/legacy-code-copy/documentation/`) were empty at the time of inspection.
This analysis is derived entirely from the source code.

---

## 7. Questions for Clarence

These are the decisions that cannot be inferred from the source code alone and must be answered
before a faithful modernization can proceed.

**Q1 — File paths in production**
`MAIN.BAS` hardcodes `E:\StudentVB.DB` and `E:\RandomA.txt`, while `RANDOM1.BAS` opens
`a:\student.txt` and `a:\random.txt`. On the original machine, were all six data files on the
floppy (`A:\`) — and was `E:\` a drive letter you assigned temporarily during development?

**Q2 — The Instructor / Student Maintenance path**
The INSTRUCTOR menu button changes the labels but the Student Maintenance handler is empty and
`frmInstructor` is missing. Was that feature ever built? If so, what was it supposed to do —
edit existing records, add programs, or something else?

**Q3 — Company code collisions**
The `Company_Code` is auto-generated from 4 characters of company name + 4 characters of a
phone number. Two companies with similar names and similar phone endings would produce the same
code. Was collision ever a real problem, or was the student population small enough that it
never occurred?

**Q4 — The `YesNo` field encoding**
The field is declared `String * 2`. On input it is set to the loop index `0` or `1` from the
`optYesNo` radio buttons. On display it is used as `Val(.YesNo)` to select which radio button
to show. So the stored value is `"0"` or `"1"`, not `"Y"` or `"N"`. Is that correct — or
should it be `"Y"`/`"N"` to be human-readable in the text files?

**Q5 — The `Date` field on the student record**
`Student_File.Date` (9 bytes) appears to be the entry date, not the graduation date. It is
written in `SortStudentText` but is never populated in
`frmStudentInformation.cmdAccept_Click` — the code sets `Program_Code`, `SS_Number`, names,
phones, etc., but never sets `.Date`. How should the entry date be handled in the new system?

**Q6 — State field on employment record**
`frmCurrentEmployment.cmdAcceptCurrentEmployment_Click` copies all `JOB` fields from the form
except `.State` — there is a comment `'.State` at `CURREMPL.FRM:465`. The state is never
written to the employment record. Is this intentional (employer state was considered
unimportant) or a bug?

**Q7 — HoursPerWeek truncation**
The `Hours_per_Week` field is declared 3 bytes in the type but the form writes
`Mid(txtHoursPerWeek, 1, 2)` (`CURREMPL.FRM:470`) — only 2 characters. Should the field hold
2 or 3 digits of hours?

**Q8 — Multiple employers per student**
The schema stores exactly one `Company_Code` per student. Was it ever the intent to allow a
student to have more than one current employer — or is one employer per student by design?

**Q9 — Report output destination**
Reports print to `frmPrintSS`, a VB4 form used as a print canvas sending output to a local
printer. In the new web application, should reports be downloadable (PDF, CSV), printed from
the browser, or something else?

**Q10 — The application name**
The main menu shows **"ONYX Student Information System"** at `MAINMENU.FRM:129`, and this
project is called `onyx-reborn`. The `.VBP` project name is `Project1` and the company name is
`Gateway 2000`. Should the modernized system retain the ONYX name officially?

---

*Report generated from static source inspection. No legacy files were modified or executed.
Stack context for modernization: FastAPI + Jinja2 + SQLite/SQLAlchemy + pytest
(C# / ASP.NET Core fallback; React roadmap).*
