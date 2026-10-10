VERSION 4.00
Begin VB.Form frmReports 
   BackColor       =   &H00808080&
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Reports"
   ClientHeight    =   6120
   ClientLeft      =   855
   ClientTop       =   5730
   ClientWidth     =   9510
   ControlBox      =   0   'False
   ForeColor       =   &H00FF0000&
   Height          =   6810
   Left            =   795
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MDIChild        =   -1  'True
   MinButton       =   0   'False
   ScaleHeight     =   6120
   ScaleWidth      =   9510
   ShowInTaskbar   =   0   'False
   Top             =   5100
   Width           =   9630
   Begin VB.CommandButton cmd1 
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "&1 - Print Selected Student Records "
      BeginProperty Font 
         name            =   "MS Sans Serif"
         charset         =   1
         weight          =   700
         size            =   9.75
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   2400
      TabIndex        =   0
      Top             =   840
      Width           =   4575
   End
   Begin VB.CommandButton cmd4 
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "&4 - View/Print All Student Information"
      BeginProperty Font 
         name            =   "MS Sans Serif"
         charset         =   1
         weight          =   700
         size            =   9.75
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   2400
      TabIndex        =   3
      Top             =   2640
      Width           =   4575
   End
   Begin VB.CommandButton cmd5 
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "&5 - View/Print Employment Inf.          "
      BeginProperty Font 
         name            =   "MS Sans Serif"
         charset         =   1
         weight          =   700
         size            =   9.75
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   2400
      TabIndex        =   4
      Top             =   3240
      Width           =   4575
   End
   Begin VB.CommandButton cmd2 
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      Caption         =   "&2 - Find/Print One Student Record   "
      BeginProperty Font 
         name            =   "MS Sans Serif"
         charset         =   1
         weight          =   700
         size            =   9.75
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   2400
      TabIndex        =   1
      Top             =   1440
      Width           =   4575
   End
   Begin VB.CommandButton cmd3 
      Appearance      =   0  'Flat
      BackColor       =   &H00808000&
      Caption         =   "&3 - View/Print All Social Securities   "
      BeginProperty Font 
         name            =   "MS Sans Serif"
         charset         =   1
         weight          =   700
         size            =   9.75
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   2400
      TabIndex        =   2
      Top             =   2040
      Width           =   4575
   End
   Begin VB.Label Label3 
      Alignment       =   2  'Center
      BackStyle       =   0  'Transparent
      Caption         =   "REPORTS"
      BeginProperty Font 
         name            =   "Times New Roman"
         charset         =   1
         weight          =   700
         size            =   18
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00800000&
      Height          =   375
      Left            =   2520
      TabIndex        =   6
      Top             =   240
      Width           =   4095
   End
   Begin VB.Label Label1 
      Alignment       =   2  'Center
      Appearance      =   0  'Flat
      BackColor       =   &H80000005&
      BackStyle       =   0  'Transparent
      Caption         =   $"FRMREP~1.frx":0000
      BeginProperty Font 
         name            =   "Arial"
         charset         =   1
         weight          =   700
         size            =   11.25
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00FF0000&
      Height          =   855
      Left            =   3120
      TabIndex        =   5
      Top             =   4560
      Width           =   2895
   End
   Begin VB.Menu mnuReport 
      Caption         =   "&Reports"
      Begin VB.Menu mnuAllSS 
         Caption         =   "&1 - View/Print All SS"
      End
      Begin VB.Menu mnuAllStudents 
         Caption         =   "&2 - View/Print All Students"
      End
      Begin VB.Menu mnuFind 
         Caption         =   "&3 - Find Student Record"
      End
   End
   Begin VB.Menu mnuReturn 
      Caption         =   "&Back"
   End
   Begin VB.Menu mnuExit 
      Caption         =   "&Exit"
   End
End
Attribute VB_Name = "frmReports"
Attribute VB_Creatable = False
Attribute VB_Exposed = False
Option Explicit









Private Sub Command4_Click()
 
frmReports.Hide
frmDisplay.Show
Scroll_Student_Info

End Sub

Private Sub Command5_Click()

frmReports.Hide
frmSelect_Rec.Show

End Sub

Private Sub cmd1_Click()
   
    frmReports.Hide
    frmSelect_Rec.Show


frmSelect_Rec.txtRec2.Enabled = False
frmSelect_Rec.txtRec3.Enabled = False
frmSelect_Rec.txtRec4.Enabled = False
frmSelect_Rec.txtRec5.Enabled = False
frmSelect_Rec.txtRec6.Enabled = False
frmSelect_Rec.txtRec7.Enabled = False
frmSelect_Rec.txtRec8.Enabled = False
frmSelect_Rec.txtRec9.Enabled = False
frmSelect_Rec.txtRec10.Enabled = False


frmSelect_Rec.txtRec1 = ""
frmSelect_Rec.txtRec2 = ""
frmSelect_Rec.txtRec3 = ""
frmSelect_Rec.txtRec4 = ""
frmSelect_Rec.txtRec5 = ""
frmSelect_Rec.txtRec6 = ""
frmSelect_Rec.txtRec7 = ""
frmSelect_Rec.txtRec8 = ""
frmSelect_Rec.txtRec9 = ""
frmSelect_Rec.txtRec10 = ""

frmSelect_Rec.txtRec2.BackColor = &HC0C0C0
frmSelect_Rec.txtRec3.BackColor = &HC0C0C0
frmSelect_Rec.txtRec4.BackColor = &HC0C0C0
frmSelect_Rec.txtRec5.BackColor = &HC0C0C0
frmSelect_Rec.txtRec6.BackColor = &HC0C0C0
frmSelect_Rec.txtRec7.BackColor = &HC0C0C0
frmSelect_Rec.txtRec8.BackColor = &HC0C0C0
frmSelect_Rec.txtRec9.BackColor = &HC0C0C0
frmSelect_Rec.txtRec10.BackColor = &HC0C0C0



frmSelect_Rec.txtRec1.SetFocus


End Sub

Private Sub cmd2_Click()
    
    frmReports.Hide
    frmSearch.Show
    
  'Deactivate Previous, Next and Print Buttons

  frmSearch.cmdPrevious.Enabled = False
  frmSearch.cmdNext.Enabled = False
  frmSearch.cmdPrint.Enabled = False

  Clear_Search_Screen
  frmSearch.txtSearch = ""


End Sub

Private Sub cmd3_Click()

frmReports.Hide
frmRandom.Show
Close #1
Scroll_SS

End Sub

Private Sub cmd4_Click()

frmReports.Hide
frmDisplay.Show
Scroll_Student_Info

End Sub

Private Sub cmd5_Click()
    
    frmReports.Hide
    frmEmployment.Show
    Scroll_Employment_Info

End Sub



Private Sub Form_Load()

' Center Form On Screen
  CenterForm Me
'
CloseAll
'
' Sort the report query file for output to
' the text file random.txt.
SortQueryText
'
' Sort the report Student file for output to
' the text file student.txt.
SortStudentText
'
'
' Sort the report Student file for output to
' the text file student.txt.
SortEmploymentText
'
CloseAll
'
End Sub ' Form_Load

Private Sub SortStudentText()
    ' Open the database file.
    OpenFileStudent
  
    ' Compute the number of records.
    numStudents = LOF(2) / Len(Students)
  
    ' If the file exists and contains one or
    ' more records, create the Index array.
    If numStudents > 0 Then
        ReDim IndexStudent(numStudents)
        CreateIndex
    End If
  
    Open "A:\Student.txt" For Output As #5
    For I = 1 To numStudents
        Get #2, IndexStudent(I).RecNum, Students
            With Students
                Print #5, .Program_Code;
                Print #5, .Date;
                Print #5, .Program_Name;
                Print #5, .SS_Number;
                Print #5, .Last_Name;
                Print #5, .First_Name;
                Print #5, .Home_Phone;
                Print #5, .Work_Phone;
                Print #5, .Address;
                Print #5, .City;
                Print #5, .State;
                Print #5, .zip;
                Print #5, .High_School;
                Print #5, .Date_Graduated;
                Print #5, .Month;
                Print #5, .Day;
                Print #5, .YesNo;
                Print #5, .Description;
                Print #5, .Company_Code;
            End With
    Next I
    Close #2
    Close #5
    '
End Sub
Sub CreateIndex()

  ' The CreateIndex procedure develops the Index array
  ' when the program begins and after each record is added.
  Dim indexEntry As StudentIndexType, I, j, temp As String
  
  OpenFileStudent
  
  ' Read each record, from the beginning to the end.
  For I = 1 To numStudents
    Get #2, I, Students
    
    ' Standardize the name entry in each record, and store
    ' the full name and record number as the fields.
    temp = Students.SS_Number
    IndexStudent(I).SS_Number = temp
    IndexStudent(I).RecNum = I
  Next I

  ' Sort the index array by the FullName field.
  For I = 1 To numStudents - 1
    For j = I + 1 To numStudents
      If IndexStudent(I).SS_Number > IndexStudent(j).SS_Number Then
        indexEntry = IndexStudent(I)
        IndexStudent(I) = IndexStudent(j)
        IndexStudent(j) = indexEntry
      End If
    Next j
  Next I
    
 'Close #2
End Sub  ' CreateIndex
Private Sub SortEmploymentText()
    ' Open the database file.
    OpenFileCurrentEmployment
    
    ' Compute the number of records.
    numCurrEmp = LOF(3) / Len(JOB)
  
    ' If the file exists and contains one or
    ' more records, create the Index array.
    If numCurrEmp > 0 Then
        ReDim IndexCurrEmp(numCurrEmp)
        CreateCurrEmpIndex
    End If
    
    Open "A:\Employment.txt" For Output As #1
    For I = 1 To numCurrEmp
        Get #3, IndexCurrEmp(I).RecNum, JOB
            With JOB
                Print #1, .Company_Code;
                Print #1, .Company_Name;
                Print #1, .Address;
                Print #1, .City;
                Print #1, .State;
                Print #1, .zip;
                Print #1, .Job_Title;
                Print #1, .Current_Supervisor;
                Print #1, .Phone_Number;
                Print #1, .Hours_per_Week;
                Print #1, .Amount;
                Print #1, .Company_Type;
            End With
    Next I
    Close #3
    Close #1
   ' Close #6
    '
End Sub     ' SortEmploymentText
Sub CreateCurrEmpIndex()

  ' The CreateIndex procedure develops the Index array
  ' when the program begins and after each record is added.
  Dim indexEntry As CurrentEmployeeIndexType, I, j, temp As String
  
  OpenFileCurrentEmployment
  
  ' Read each record, from the beginning to the end.
  For I = 1 To numCurrEmp
    Get #3, I, JOB
    
    ' Standardize the name entry in each record, and store
    ' the full name and record number as the fields.
    temp = JOB.Company_Code
    IndexCurrEmp(I).Company_Code = temp
    IndexCurrEmp(I).RecNum = I
  Next I

  ' Sort the index array by the FullName field.
  For I = 1 To numCurrEmp - 1
    For j = I + 1 To numCurrEmp
      If IndexCurrEmp(I).Company_Code > IndexCurrEmp(j).Company_Code Then
        indexEntry = IndexCurrEmp(I)
        IndexCurrEmp(I) = IndexCurrEmp(j)
        IndexCurrEmp(j) = indexEntry
      End If
    Next j
  Next I
'Close #3
End Sub  ' CreateCurrEmpIndex


Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)

    Set frmSearch = Nothing
    Set frmEmployment = Nothing
    Set frmPrintSS = Nothing
    Set frmRandom = Nothing
    Set frmSearch = Nothing
    Set frmSelect_Rec = Nothing
    
    'frmSwitchBoard.Show

End Sub

Private Sub mnuAllSS_Click()

frmReports.Hide
frmRandom.Show
Scroll_SS

End Sub


Private Sub mnuAllStudents_Click()

frmReports.Hide
frmDisplay.Show
Scroll_Student_Info

End Sub

Private Sub mnuExit_Click()

    Exit_Program

End Sub

Private Sub mnuFind_Click()
    
    frmReports.Hide
    frmSearch.Show

End Sub


Private Sub mnuReturn_Click()
    frmReports.Hide
    frmMainMenu.Show
    'frmSwitchBoard.Show
End Sub
Private Sub SortQueryText()
Dim intFile As Integer
    ' Open the database file.
    'Open Query For Random As #1 Len = Len(Query)
    OpenFileQuery
    
    ' Compute the number of records.
    numQuery = LOF(1) / Len(Query)
  

    ' If the file exists and contains one or
    ' more records, create the Index array.
    If numQuery > 0 Then
        ReDim Index(numQuery)
        CreateQueryIndex
    End If
  
    intFile = FreeFile()
    Open "A:\RANDOM.txt" For Output As #intFile
    For I = 1 To numQuery
        Get #1, Index(I).RecNum, QuerySoc
            With QuerySoc
                Print #intFile, .SS_Number;
            End With
    Next I
    Close #1
    Close #intFile
    '
End Sub

Sub CreateQueryIndex()

  ' The CreateIndex procedure develops the Index array
  ' when the program begins and after each record is added.
  Dim indexEntry As Query_Type, I, j, temp As String
   
  ' Read each record, from the beginning to the end.
  For I = 1 To numQuery
    Get #1, I, QuerySoc
    
    ' Standardize the name entry in each record, and store
    ' the full name and record number as the fields.
    temp = QuerySoc.SS_Number
    Index(I).SS_Number = temp
    Index(I).RecNum = I
  Next I


  ' Sort the index array by the Social Security field.
  For I = 1 To numQuery - 1
    For j = I + 1 To numQuery
      If Index(I).SS_Number > Index(j).SS_Number Then
        indexEntry = Index(I)
        Index(I) = Index(j)
        Index(j) = indexEntry
      End If
    Next j
  Next I

End Sub  ' CreateIndex
