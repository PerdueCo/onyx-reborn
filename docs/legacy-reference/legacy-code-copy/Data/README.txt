BSSI VB4 TEST DATA PACK
=======================

Purpose
-------
These files were reconstructed from the fixed-length Visual Basic 4 Type
definitions in MAIN.BAS and from the file-open/report routines. They contain
five entirely fictional test students and employers. The 900-series SSNs and
555 telephone numbers are intentionally non-production test values.

Installation
------------
The original program expects every file at A:\.

Option 1: Copy the six application data files to a real A: drive.

Option 2: On a test Windows VM, copy this folder to C:\BSSI\Data and run:

    SUBST A: C:\BSSI\Data

Do not copy README.txt, test_records.csv, or the ZIP itself to A: if the old
program enumerates every file. The six application files are:

    StudentVB.DB       5 records x 357 bytes
    EmploymentA.DB    5 records x 238 bytes
    RandomA.txt        VB4 query records in 14-byte slots
    Student.txt        reporting/search copy of StudentVB.DB
    Employment.txt     reporting/search copy of EmploymentA.DB
    Random.txt         5 records x 10 bytes

Important format finding
------------------------
RandomA.txt is binary despite its .txt extension. The source incorrectly uses
Len(Query), where Query is the path string "A:\RandomA.txt", as the Random
record length. That evaluates to 14. Each Query_File payload is 12 bytes, so
this generator reproduces the resulting two-byte inter-record gap.

Expected sizes
--------------
StudentVB.DB:    1785 bytes
Student.txt:     1785 bytes
EmploymentA.DB: 1190 bytes
Employment.txt: 1190 bytes
RandomA.txt:     68 bytes
Random.txt:      50 bytes

Safety
------
Keep the original recovered files unchanged. Use this pack only in a test VM
or in a repaired copy of the application. No real student information is used.
