VERSION 4.00
Begin VB.Form frmStudentInformation 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Student Information"
   ClientHeight    =   6765
   ClientLeft      =   2820
   ClientTop       =   2925
   ClientWidth     =   8280
   ControlBox      =   0   'False
   Height          =   7170
   Left            =   2760
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MDIChild        =   -1  'True
   MinButton       =   0   'False
   ScaleHeight     =   6765
   ScaleWidth      =   8280
   Top             =   2580
   Width           =   8400
   Begin VB.TextBox txtZip 
      Height          =   285
      Left            =   6720
      MaxLength       =   5
      TabIndex        =   17
      Top             =   2880
      Width           =   1215
   End
   Begin VB.Frame Frame1 
      Height          =   6015
      Left            =   120
      TabIndex        =   35
      Top             =   0
      Width           =   8055
      Begin VB.PictureBox Picture2 
         Appearance      =   0  'Flat
         BackColor       =   &H00C0C0C0&
         BorderStyle     =   0  'None
         ForeColor       =   &H80000008&
         Height          =   375
         Left            =   4800
         ScaleHeight     =   375
         ScaleWidth      =   2895
         TabIndex        =   43
         Top             =   4800
         Width           =   2895
      End
      Begin VB.TextBox txtWorkPhone 
         Height          =   285
         Left            =   1800
         MaxLength       =   13
         TabIndex        =   9
         Top             =   2160
         Width           =   2295
      End
      Begin VB.TextBox txtHomePhone 
         Height          =   285
         Left            =   1800
         MaxLength       =   13
         TabIndex        =   7
         Top             =   1800
         Width           =   2295
      End
      Begin VB.TextBox txtYear 
         Height          =   285
         Left            =   5040
         MaxLength       =   2
         TabIndex        =   24
         Top             =   3840
         Width           =   495
      End
      Begin VB.TextBox txtMonthGraduated 
         Height          =   285
         Left            =   2760
         MaxLength       =   2
         TabIndex        =   22
         Top             =   3840
         Width           =   495
      End
      Begin VB.ComboBox cboProgramName 
         BackColor       =   &H00FFFFFF&
         Height          =   300
         ItemData        =   "STUDENTS.frx":0000
         Left            =   1800
         List            =   "STUDENTS.frx":0016
         TabIndex        =   1
         Top             =   1080
         Width           =   6015
      End
      Begin VB.TextBox txtLastName 
         Height          =   285
         Left            =   1800
         TabIndex        =   3
         Top             =   1440
         Width           =   2295
      End
      Begin VB.TextBox txtFirstName 
         Height          =   285
         Left            =   5640
         TabIndex        =   5
         Top             =   1440
         Width           =   2175
      End
      Begin VB.TextBox txtAddress 
         Height          =   285
         Left            =   1800
         TabIndex        =   11
         Top             =   2520
         Width           =   6015
      End
      Begin VB.TextBox txtCity 
         Height          =   285
         Left            =   1800
         TabIndex        =   13
         Top             =   2880
         Width           =   2295
      End
      Begin VB.ComboBox cboState 
         Height          =   300
         ItemData        =   "STUDENTS.frx":010E
         Left            =   5040
         List            =   "STUDENTS.frx":0118
         Style           =   2  'Dropdown List
         TabIndex        =   15
         Top             =   2880
         Width           =   735
      End
      Begin VB.TextBox txtDescription 
         Height          =   285
         Left            =   3600
         TabIndex        =   34
         Top             =   5640
         Width           =   4215
      End
      Begin VB.OptionButton optYesNo 
         Alignment       =   1  'Right Justify
         Caption         =   "No"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   315
         Index           =   1
         Left            =   6600
         TabIndex        =   32
         Top             =   5160
         Width           =   975
      End
      Begin VB.OptionButton optYesNo 
         Alignment       =   1  'Right Justify
         Caption         =   "Yes"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   315
         Index           =   0
         Left            =   4920
         TabIndex        =   31
         Top             =   5160
         Width           =   1095
      End
      Begin VB.TextBox txtHighSchool 
         Height          =   285
         Left            =   1800
         TabIndex        =   19
         Top             =   3240
         Width           =   2295
      End
      Begin VB.ComboBox cboBirthMonth 
         Height          =   300
         ItemData        =   "STUDENTS.frx":0124
         Left            =   2760
         List            =   "STUDENTS.frx":014C
         Style           =   2  'Dropdown List
         TabIndex        =   27
         Top             =   4320
         Width           =   615
      End
      Begin VB.ComboBox cboBirthDay 
         Height          =   300
         ItemData        =   "STUDENTS.frx":0180
         Left            =   5040
         List            =   "STUDENTS.frx":01E1
         Style           =   2  'Dropdown List
         TabIndex        =   29
         Top             =   4320
         Width           =   615
      End
      Begin VB.Label lblFormatYear 
         Caption         =   " format XX"
         ForeColor       =   &H00800000&
         Height          =   255
         Left            =   4800
         TabIndex        =   42
         Top             =   3600
         Visible         =   0   'False
         Width           =   855
      End
      Begin VB.Label lblMonthRange 
         Caption         =   "format XX"
         ForeColor       =   &H00800000&
         Height          =   255
         Left            =   2520
         TabIndex        =   41
         Top             =   3600
         Visible         =   0   'False
         Width           =   855
      End
      Begin VB.Label Label18 
         AutoSize        =   -1  'True
         BackStyle       =   0  'Transparent
         Caption         =   "&Year :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   195
         Index           =   1
         Left            =   4320
         TabIndex        =   23
         Top             =   3840
         Width           =   525
      End
      Begin VB.Label Label17 
         AutoSize        =   -1  'True
         BackStyle       =   0  'Transparent
         Caption         =   "  Month "
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   195
         Left            =   1800
         TabIndex        =   21
         Top             =   3840
         Width           =   720
      End
      Begin VB.Label Label3 
         Alignment       =   1  'Right Justify
         BackStyle       =   0  'Transparent
         Caption         =   "       &Date Graduated :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   -405
         TabIndex        =   20
         Top             =   3840
         Width           =   2175
      End
      Begin VB.Label Label16 
         BackStyle       =   0  'Transparent
         Caption         =   "Please Enter Student Information :"
         BeginProperty Font 
            name            =   "Times New Roman"
            charset         =   1
            weight          =   700
            size            =   15.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00800000&
         Height          =   495
         Left            =   240
         TabIndex        =   40
         Top             =   120
         Width           =   6735
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00FFFFFF&
         Index           =   3
         X1              =   120
         X2              =   7800
         Y1              =   615
         Y2              =   615
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00808080&
         Index           =   2
         X1              =   120
         X2              =   7800
         Y1              =   600
         Y2              =   600
      End
      Begin VB.Label lblDate 
         BorderStyle     =   1  'Fixed Single
         Caption         =   "04/28/1998"
         Height          =   285
         Left            =   6720
         TabIndex        =   37
         Top             =   720
         Width           =   1095
      End
      Begin VB.Label Label2 
         Caption         =   "Date :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   6120
         TabIndex        =   36
         Top             =   750
         Width           =   615
      End
      Begin VB.Label Label13 
         Caption         =   " Are You Currently Seeking a Job ? :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   360
         TabIndex        =   30
         Top             =   5160
         Width           =   3975
      End
      Begin VB.Label lblEmployment 
         BackStyle       =   0  'Transparent
         Caption         =   "  If Yes, What Type Of Job  Are You Applying For :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   615
         Left            =   360
         TabIndex        =   33
         Top             =   5520
         Width           =   2535
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00808080&
         Index           =   4
         X1              =   120
         X2              =   7800
         Y1              =   4680
         Y2              =   4680
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00FFFFFF&
         Index           =   5
         X1              =   120
         X2              =   7800
         Y1              =   4695
         Y2              =   4695
      End
      Begin VB.Label Label14 
         Caption         =   "       &High School:"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   240
         TabIndex        =   18
         Top             =   3240
         Width           =   1575
      End
      Begin VB.Label Label11 
         Caption         =   "     &Home Phone :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   240
         TabIndex        =   6
         Top             =   1800
         Width           =   1575
      End
      Begin VB.Label Label9 
         Caption         =   "                  &City :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   240
         TabIndex        =   12
         Top             =   2880
         Width           =   1575
      End
      Begin VB.Label Label8 
         BackStyle       =   0  'Transparent
         Caption         =   "               &Address  :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   0
         TabIndex        =   10
         Top             =   2520
         Width           =   1815
      End
      Begin VB.Label Label7 
         Caption         =   "&Work Phone"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   600
         TabIndex        =   8
         Top             =   2160
         Width           =   1215
      End
      Begin VB.Label Label5 
         Caption         =   "        &Last Name :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   240
         TabIndex        =   2
         Top             =   1440
         Width           =   1575
      End
      Begin VB.Label Label4 
         Caption         =   "  Program &Name  :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   240
         TabIndex        =   0
         Top             =   1080
         Width           =   1575
      End
      Begin VB.Label Label6 
         Caption         =   "        &First Name :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   4080
         TabIndex        =   4
         Top             =   1440
         Width           =   1575
      End
      Begin VB.Label Label10 
         Caption         =   "              &State  :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   3360
         TabIndex        =   14
         Top             =   2880
         Width           =   1575
      End
      Begin VB.Label Label12 
         Caption         =   "      &Zip :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   5640
         TabIndex        =   16
         Top             =   2880
         Width           =   735
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00808080&
         Index           =   6
         X1              =   120
         X2              =   7800
         Y1              =   4200
         Y2              =   4200
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00FFFFFF&
         Index           =   7
         X1              =   120
         X2              =   7800
         Y1              =   4215
         Y2              =   4215
      End
      Begin VB.Label Label18 
         AutoSize        =   -1  'True
         BackStyle       =   0  'Transparent
         Caption         =   "  Month "
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   195
         Index           =   0
         Left            =   1800
         TabIndex        =   26
         Top             =   4350
         Width           =   720
      End
      Begin VB.Label Label19 
         BackStyle       =   0  'Transparent
         Caption         =   "  Day :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   4320
         TabIndex        =   28
         Top             =   4350
         Width           =   615
      End
      Begin VB.Label Label1 
         Caption         =   "Birthday:"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   960
         TabIndex        =   25
         Top             =   4320
         Width           =   855
      End
   End
   Begin VB.PictureBox Picture1 
      BackColor       =   &H00C0C0C0&
      Height          =   585
      Left            =   120
      ScaleHeight     =   555
      ScaleWidth      =   8025
      TabIndex        =   38
      Top             =   6120
      Width           =   8055
      Begin VB.CommandButton cmdAccept 
         Caption         =   "&Accept"
         Height          =   375
         Left            =   3360
         TabIndex        =   39
         Top             =   120
         Width           =   975
      End
   End
End
Attribute VB_Name = "frmStudentInformation"
Attribute VB_Creatable = False
Attribute VB_Exposed = False









Option Explicit
Dim Mprogramname As String
Dim MprogramCode As String
Dim gfkeyEntered As Boolean
Dim Key As Integer

Const Student = "A:\StudentDB.txt"




Private Sub cboProgramName_Click()
Dim prgIndex As Integer

    prgIndex = cboProgramName.ListIndex

    Select Case prgIndex
        Case 1
            MprogramCode = "1234"
        Case 2
            MprogramCode = "2345"
        Case 3
            MprogramCode = "3456"
        Case 4
            MprogramCode = "4567"
        Case 5
            MprogramCode = "5678"
        Case 6
            MprogramCode = "6789"
        End Select
        
            
End Sub

Private Sub cboProgramName_KeyPress(KeyAscii As Integer)
    '
    AutoMatch cboProgramName, KeyAscii
    '
End Sub

Private Sub cmdAccept_Click()
  

    ' The cmdAccept_Click procedure stores the current record
    ' entry in the databse and updates the index.
    Dim isFound As Integer, I
    Dim answer As Integer, lf As String
    Dim SearchValue As String
    Dim inFileRec As Integer
    ' Set the format to invisible
    lblFormatYear.Visible = False
    lblMonthRange.Visible = False
    '
    OpenFileStudent
    '
    ' Standardize the format and search for the name.
    SearchValue = Trim(gSearchSSN)
  
    ' Otherwise, search for this number in an existing record
    ' and copy the entry to the Student record variable.
    isFound = Search(SearchValue)
  
    With Students
            
            If cboProgramName.ListIndex = -1 Then
                '.Program_Code = "-1"
            Else
                
            End If
            .Program_Code = Mid(Trim(MprogramCode), 1, 4)
            .Program_Name = Mid(Trim(cboProgramName.Text), 1, 29)
            .SS_Number = Mid(Trim(gSearchSSN), 1, 9)
            .Last_Name = Mid(Trim(txtLastName), 1, 14)
            .First_Name = Mid(Trim(txtFirstName), 1, 14)
            .Home_Phone = Mid(Trim(txtHomePhone.Text), 1, 14)
            .Work_Phone = Mid(Trim(txtWorkPhone.Text), 1, 14)
            .Address = Mid(Trim(txtAddress), 1, 29)
            .City = Mid(Trim(txtCity), 1, 29)
            .State = Mid(Trim(cboState.Text), 1, 2)
            
            .zip = Mid(Trim(txtZip.Text), 1, 10)
            .High_School = Mid(Trim(txtHighSchool), 1, 29)
            .Date_Graduated = txtMonthGraduated & "/" & txtYear
            .Month = Mid(Trim(cboBirthMonth.Text), 1, 2)
            .Day = Mid(Trim(cboBirthDay.Text), 1, 2)
            .Description = Mid(Trim(txtDescription), 1, 99)
            '.Company_Code
            gCurrentEmployeeSearchValue = .Company_Code
            
            For I = 0 To 1
                If optYesNo(I).Value Then
                    .YesNo = I
                End If
            Next I

        End With
    
    ' If the name doesn't already exist, add the record.
    If isFound = 0 Then
        numStudents = numStudents + 1
        gWhichStudentRecord = numStudents
    
        gCurrentEmployeeSearchValue = ""
        '
       ' OpenFileStudent
        '
        ' Write the record to the file and update the index.
        Put #2, numStudents, Students
        ReDim IndexStudent(numStudents)
        CreateIndex
        Close #2
      
        
    ' If the name already exists allow the user to
    ' revise the record (overwriting the previous entry).
    Else
      answer = MsgBox("This name is already on file." _
        & lf & "Do you want to save " & lf & _
        "a revised record?", 4, "Revise a Record")
        
      ' If the user confirms, store the revised record.
      If answer = 6 Then
        gWhichStudentRecord = isFound
        Put #2, IndexStudent(isFound).RecNum, Students
        Close #2
      End If
 End If
                 
    Load frmCurrentEmployment
    frmCurrentEmployment.Show
End Sub  ' cmdAccept_Click
Function Search(findText As String) As Integer

  ' The Search function performs a binary search to look
  ' for a name in the Index array.
  Dim pos1 As Integer, pos2 As Integer
  Dim posX As Integer, midPos As Integer, midStr As String
  
  ' Initialize position markers and search for the
  ' target string.
  pos1 = 1
  pos2 = numStudents
  posX = 0
  Do While pos1 <= pos2 And posX = 0
    midPos = (pos1 + pos2) \ 2
    midStr = Trim(IndexStudent(midPos).SS_Number)
    If Trim(findText) = midStr Then
      posX = midPos
    ElseIf Trim(findText) > midStr Then
      pos1 = midPos + 1
    Else
      pos2 = midPos - 1
    End If
  Loop
  
  ' Return the Index subscript where the name is located,
  ' or zero if the name was not found.
  Search = posX

End Function  ' Search


Private Sub cmdCancel_Click()
    ClearStudent
End Sub
Private Sub ClearStudent()
    
    cboProgramName.ListIndex = -1
    txtLastName = ""
    txtFirstName = ""
    txtWorkPhone.Text = ""
    txtAddress = ""
    txtCity = ""
    cboState.ListIndex = -1
    txtZip.Text = ""
    txtHighSchool = ""
    txtMonthGraduated = ""
    txtYear = ""
    cboBirthMonth.ListIndex = -1
    cboBirthDay.ListIndex = -1
    'frm.txtYesNo = ""
    txtDescription = ""
    txtDescription = ""

End Sub

Private Sub cmdNext_Click()
    frmCurrentEmployment.Show
    frmStudentInformation.Hide
End Sub

Private Sub Form_Load()
 
    On Error GoTo FormLoad_EH
    
    lblDate = Format(Date, "mm/d/yyyy")
    
    Dim SearchValue As String
    Dim rec As Integer
    Dim inFileRec As Integer
    Dim Records As Integer
    Dim MStudentSSN As String
    
  ' The Form_Load procedure opens the database file and
  ' creates the index. (The Index array allows the
  ' program to search effectively for any record by
  ' a person's name.)

  ' Open the database file.
  'Open Student For Random As #2 Len = Len(Students)
  OpenFileStudent
  
  ' Compute the number of records.
  numStudents = LOF(2) / Len(Students)
  
  ' If the file exists and contains one or
  ' more records, create the Index array.
  If numStudents > 0 Then
    ReDim IndexStudent(numStudents)
    CreateIndex
  End If
  
    
    
    ' Hide the Social Security Entry Screen
    frmSSSNumber.Hide
    '
    ' To Center Form On Screen
    CenterForm Me
    '
    ' Show the program
    Me.Show
    '
    ' Load Programs into cboProgramName
    'LoadProgramName Me
    '
    ' Search string
    gSearchSSN = Trim(frmSSSNumber.txtVerifySSN.Text)
    'MsgBox gSearchSSN
    'cmdSearch_Click
     ' Standardize the format and search for the name.
            SearchValue = gSearchSSN
            rec = Search(SearchValue)
           
            
            ' If the Social Number is found, display the record.
            If rec > 0 Then
                inFileRec = IndexStudent(rec).RecNum
                '
                 gWhichStudentRecord = inFileRec
                '
                ShowRecord IndexStudent(rec).RecNum
                '
                ' Otherwise, tell the user that the search failed.
            Else
                'MsgBox "Can't find " & SearchValue & ".", , "Search"
                ClearStudent
            End If
            
            ' Clear value from the Social Security Entry Screen
    frmSSSNumber.txtSNN.Text = ""
    frmSSSNumber.txtVerifySSN.Text = ""
    '
    
    '  Text BOX Program Name to have focus on the initial displaying of form.
    'cboProgramName.SetFocus
    
    Exit Sub
    
FormLoad_EH:
    Resume Next
    Exit Sub
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



Private Sub Form_Unload(Cancel As Integer)

    Close #2
    frmSSSNumber.Show
    Unload frmStudentInformation
    'Set frmStudentInformation = Nothing
    
End Sub

Private Sub MaskEdBox2_ValidationError(InvalidText As String, StartPosition As Integer)

End Sub

Private Sub mskHomePhone_GotFocus()
    frmStudentInformation.mskHomePhone.SelStart = 0
    frmStudentInformation.mskHomePhone.SelLength = Len(frmStudentInformation.mskHomePhone.Text)
    Exit Sub
End Sub

Private Sub mskHomePhone_KeyPress(KeyAscii As Integer)
If Not gfkeyEntered Then
         frmStudentInformation.mskHomePhone.Mask = ""
         frmStudentInformation.mskHomePhone.Text = ""
         frmStudentInformation.mskHomePhone.Mask = "(###)###-####"
         gfkeyEntered = True
End If

End Sub

Private Sub mskHomePhone_LostFocus()
 Dim strPos As String
 Dim strMask As String
  gfkeyEntered = False
    If mskHomePhone.Text = "(___)___-____" Then
       mskHomePhone.Mask = ""
       mskHomePhone.Text = ""
    End If
    If mskHomePhone.Text <> "" Then
       strPos = InStr(1, mskHomePhone.Text, "_", 1)
       If strPos <> "0" Then
          MsgBox " Please Enter Home Phone as (404)648-2815"
          mskHomePhone.SetFocus
          Exit Sub
       End If
    End If
    Exit Sub

End Sub

Private Sub mskWorkPhone_GotFocus()
    frmStudentInformation.MSKWORKPHONE.SelStart = 0
    frmStudentInformation.MSKWORKPHONE.SelLength = Len(frmStudentInformation.MSKWORKPHONE.Text)
    Exit Sub
End Sub





Private Sub mskWorkPhone_KeyPress(KeyAscii As Integer)
If Not gfkeyEntered Then
         frmStudentInformation.MSKWORKPHONE.Mask = ""
         frmStudentInformation.MSKWORKPHONE.Text = ""
         frmStudentInformation.MSKWORKPHONE.Mask = "(###)###-####"
         gfkeyEntered = True
End If

End Sub

Private Sub mskWorkPhone_LostFocus()
Dim strPos As String
Dim strMask As String
   gfkeyEntered = False
    If MSKWORKPHONE.Text = "(___)___-____" Then
       MSKWORKPHONE.Mask = ""
       MSKWORKPHONE.Text = ""
    End If
    If MSKWORKPHONE.Text <> "" Then
       strPos = InStr(1, MSKWORKPHONE.Text, "_", 1)
       If strPos <> "0" Then
          MsgBox " Please Enter phone number as (404)648-2815"
          MSKWORKPHONE.SetFocus
          Exit Sub
       End If
    End If
    Exit Sub
End Sub



Private Sub cmdSearch_Click()

  ' The cmdSearch_Click procedure searches for a name in
  ' the phone directory, and retrieves the record.
  
  Dim searchSoc As String
  Dim rec As Integer, inFileRec As Integer
  
  
    ' Standardize the format and search for the name.
    searchSoc = gSearchSSN
    
    rec = Search(searchSoc)
  
    ' If the name is found, display the record.
    If rec > 0 Then
      inFileRec = IndexStudent(rec).RecNum
      gWhichStudentRecord = inFileRec
      ShowRecord inFileRec
    
    ' Otherwise, tell the user that the search failed.
    Else
      'MsgBox "Can't find " & searchSoc & ".", , "Search"
      ClearStudent
        'numStudents = numStudents + 1
        'gWhichStudentRecord = numStudents
        
        ' If the file exists and contains one or
        ' more records, create the Index array.
        'If numStudents > 0 Then
        'ReDim IndexStudent(numStudents)
        'CreateIndex
        'End If
        
        'ShowRecord numStudents
    End If

End Sub  ' cmdSearch_Click
Private Sub ShowRecord(ReadRecord As Integer)
Dim inFileRec As Integer
Dim SearchValue As String
Dim strProgram_Name As String
Dim Program As ComboBox
Dim State As ComboBox
Dim BirthMonth As ComboBox
Dim BirthDay As ComboBox
Dim MonthGraduated As ComboBox
Dim YearGraduated As ComboBox

 
  ' The variable readRecord represents an actual
  ' record number, not an element of the Index
  ' array.
    
   OpenFileStudent
   
  ' Read the target record from the database.
  Get #2, ReadRecord, Students
  

    
  ' Copy the fields of the record to
  ' the controls on the frmStudent Information form.
  ' Copy the fields of the record to
        ' the controls on the frmStudentInformation form.
        With Students
            
            .SS_Number = gSearchSSN
            'frm.txtProgramCode = .Program_Code
            'cboProgramName.Index = .Program_Name
            txtLastName = .Last_Name
            txtFirstName = .First_Name
            
            txtHomePhone.Text = .Home_Phone
            txtWorkPhone.Text = .Work_Phone
            txtAddress = .Address
            txtCity = .City
            txtZip.Text = .zip
            txtHighSchool = .High_School
            txtMonthGraduated = Left(.Date_Graduated, 2)
            txtYear = Right(Trim(.Date_Graduated), 2)
            'frm.cboMonth = .Month
            'frm.cboDay = .Day
            optYesNo(Val(.YesNo)) = True
            txtDescription = .Description
            gCurrentEmployeeSearchValue = .Company_Code
            
            ' Passing object variable
            Set Program = cboProgramName
            Set State = cboState
            Set BirthMonth = cboBirthMonth
            Set BirthDay = cboBirthDay
            'Set MonthGraduated = frm.cboMonthGraduated
            'Set YearGraduated = frm.cboYearGraduated
            
            ' Find String Code In Combo Boxes
            Call CBFindString(frmStudentInformation, State, .State)
            
            Call CBFindPartialString(frmStudentInformation, Program, .Program_Name)
            Call CBFindString(frmStudentInformation, BirthMonth, .Month)
            Call CBFindString(frmStudentInformation, BirthDay, .Day)
            'Call CBFindString(frmStudentInformation, State, .State)
            'Call CBFindString(frmStudentInformation, State, .State)
        End With
        
        'Put #2, ReadRecord, Students
  
        Close #2
        
End Sub  ' ShowRecord
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

Private Sub Text1_Change()

End Sub

Private Sub Text1_GotFocus()

End Sub

Private Sub optEmployment_Click(Index As Integer)
    Select Case Index
        Case 0
            ' Set Current Employment Input/view
            gCurrentEmploymentMode = True
            '
        Case 1
            ' Set Current Employment Input/view
            gCurrentEmploymentMode = False
            '
    End Select

End Sub

Private Sub optYesNo_Click(Index As Integer)
    Select Case Index
        Case 0
            ' Make visible
            'lblEmployment.Visible = True
            'txtDescription.Visible = True
            '
        Case 1
            ' Make visible
            'lblEmployment.Visible = False
            'txtDescription.Visible = False
            '
    End Select
End Sub

Private Sub txtFirstName_KeyUp(KeyCode As Integer, Shift As Integer)
Dim intCurPos As Integer
    intCurPos = txtFirstName.SelStart
    txtFirstName.Text = StrConv(txtFirstName, vbProperCase)
    txtFirstName.SelStart = intCurPos
End Sub

Private Sub txtFirstName_LostFocus()
If Not gfkeyEntered Then
    If Trim$(txtFirstName) = "" Then
        gfkeyEntered = True
        MsgBox "Please Enter Name"
        txtFirstName.SetFocus
    Else
        gfkeyEntered = False
    End If
Else
    gfkeyEntered = False
End If
    
End Sub

Private Sub txtHomePhone_Change()
Dim Phone As Single
Dim MyStr As String

Phone = Len(txtHomePhone.Text)
MyStr = txtHomePhone.Text

Select Case Phone
    Case 1
        If Key <> 8 Then
            txtHomePhone.Text = ""
            txtHomePhone.Text = "(" & MyStr
            txtHomePhone.SelStart = 2
        End If
    
    Case 4
        If Key <> 8 Then
            txtHomePhone.Text = txtHomePhone.Text & ")"
            txtHomePhone.SelStart = 8
        Else
            txtHomePhone.Text = txtHomePhone.Text & ""
            txtHomePhone.SelStart = 8
        End If
    Case 8
        If Key <> 8 Then
            txtHomePhone.Text = txtHomePhone.Text & "-"
            txtHomePhone.SelStart = 9
        End If
End Select
End Sub

Private Sub txtHomePhone_GotFocus()
    txtHomePhone.SelStart = 0
    txtHomePhone.SelLength = Len(txtWorkPhone)
    Exit Sub
End Sub

Private Sub txtHomePhone_KeyPress(KeyAscii As Integer)
Dim KeyVal As Integer
    KeyAscii = ValiText(KeyAscii, "0123456789-", True)
    
    Key = KeyAscii
    KeyVal = KeyAscii
    
    If Not gfkeyEntered Then
        If KeyVal = vbKeyReturn Then
            SendKeys "{TAB}"
        End If
    End If
    Exit Sub
End Sub

Private Sub txtHomePhone_LostFocus()
' The txtAmount_LostFocus procedure validates each data
' entry, reformats it for display.

Dim intPhone As Double
Dim strPhone As Double
Dim entryWidth As String

     
    
If Not gfkeyEntered Then
    If Trim$(txtHomePhone.Text) = "" Or Len(txtHomePhone) < 13 Then
        gfkeyEntered = True
        MsgBox "Please Enter Phone Number"
        txtHomePhone.SetFocus
        Exit Sub
    Else
        gfkeyEntered = False
    End If
Else
    gfkeyEntered = False
End If
    Exit Sub
End Sub


Private Sub txtLastName_GotFocus()
    txtLastName.SelStart = 0
    txtLastName.SelLength = Len(txtLastName.Text)
    Exit Sub
End Sub

Private Sub txtLastName_KeyPress(KeyAscii As Integer)
Dim KeyVal As Integer
    KeyVal = KeyAscii
    KeyAscii = ValiText(KeyAscii, "abcdefghijklmnopqrstuvwxyz", True)
    If Not gfkeyEntered Then
        If KeyVal = vbKeyReturn Then
            SendKeys "{TAB}"
        ElseIf KeyVal = vbKeySpace Then
            MsgBox txtLastName
            txtLastName = txtLastName & " "
        Else
            
        End If
    End If
    Exit Sub
End Sub

Private Sub txtLastName_KeyUp(KeyCode As Integer, Shift As Integer)
Dim intCurPos As Integer
    intCurPos = txtLastName.SelStart
    txtLastName.Text = StrConv(txtLastName, vbProperCase)
    txtLastName.SelStart = intCurPos
End Sub



Private Sub txtLastName_LostFocus()
If Not gfkeyEntered Then
    If Trim$(txtLastName) = "" Then
        gfkeyEntered = True
        MsgBox "Please Enter Name"
        txtLastName.SetFocus
    Else
        gfkeyEntered = False
    End If
Else
    gfkeyEntered = False
End If
    
End Sub

Private Sub txtMonthGraduated_GotFocus()
    lblMonthRange.Visible = True
    txtMonthGraduated.SelStart = 0
    txtMonthGraduated.SelLength = Len(txtMonthGraduated)
    Exit Sub
End Sub

Private Sub txtMonthGraduated_KeyPress(KeyAscii As Integer)
Dim KeyVal As Integer
    KeyVal = KeyAscii
    KeyAscii = ValiText(KeyAscii, "0123456789", True)
    If Not gfkeyEntered Then
        If KeyVal = vbKeyReturn Then
            SendKeys "{TAB}"
        End If
    End If
    Exit Sub
End Sub

Private Sub txtMonthGraduated_LostFocus()
' The txtAmount_LostFocus procedure validates each data
' entry, reformats it for display.

Dim intMonth As Double
Dim strMonth As Double
Dim forMonth As String
    
 
    ' If the entry is not zero, display the value
    ' with a two digits format.
    If Len(txtMonthGraduated.Text) <> 0 Then
        forMonth = Format(txtMonthGraduated, "#00")
        txtMonthGraduated = forMonth
    End If

    
     If Not gfkeyEntered Then
            '
            ' Do not allow negative values, or entries longer
            ' than six digits.
            If Val(txtMonthGraduated.Text) > 13 Then
                gfkeyEntered = True
                MsgBox "Month Range between 0 and 13"
                txtMonthGraduated.SetFocus
            
            ElseIf Trim$(txtMonthGraduated.Text) = "" Then
                gfkeyEntered = True
                MsgBox " Please Enter a Month"
                txtMonthGraduated.SetFocus
           
            Else
                    
                gfkeyEntered = False
            End If
        Else
            
            gfkeyEntered = False
        End If
    
    Exit Sub
End Sub

Private Sub txtWorkPhone_Change()
Dim Phone As Single
Dim MyStr As String

Phone = Len(txtWorkPhone.Text)
MyStr = txtWorkPhone.Text

Select Case Phone
    Case 1
        If Key <> 8 Then
            txtWorkPhone.Text = ""
            txtWorkPhone.Text = "(" & MyStr
            txtWorkPhone.SelStart = 2
        End If
    
    Case 4
        If Key <> 8 Then
            txtWorkPhone.Text = txtWorkPhone.Text & ")"
            txtWorkPhone.SelStart = 8
        Else
            txtWorkPhone.Text = txtWorkPhone.Text & ""
            txtWorkPhone.SelStart = 8
        End If
    Case 8
        If Key <> 8 Then
            txtWorkPhone.Text = txtWorkPhone.Text & "-"
            txtWorkPhone.SelStart = 9
        End If
End Select
End Sub

Private Sub txtWorkPhone_GotFocus()
    txtWorkPhone.SelStart = 0
    txtWorkPhone.SelLength = Len(txtWorkPhone)
    Exit Sub
End Sub


Private Sub txtWorkPhone_KeyPress(KeyAscii As Integer)
Dim KeyVal As Integer
    KeyAscii = ValiText(KeyAscii, "0123456789-", True)
    
    Key = KeyAscii
    KeyVal = KeyAscii
    
    If Not gfkeyEntered Then
        If KeyVal = vbKeyReturn Then
            SendKeys "{TAB}"
        End If
    End If
    Exit Sub
End Sub


Private Sub txtWorkPhone_LostFocus()
' The txtAmount_LostFocus procedure validates each data
' entry, reformats it for display.

Dim intPhone As Double
Dim strPhone As Double
Dim entryWidth As String

     
    
If Not gfkeyEntered Then
    If Trim$(txtWorkPhone.Text) = "" Or Len(txtWorkPhone) < 13 Then
        gfkeyEntered = True
        MsgBox "Please Enter Phone Number"
        txtWorkPhone.SetFocus
        Exit Sub
    Else
        gfkeyEntered = False
    End If
Else
    gfkeyEntered = False
End If
    Exit Sub
End Sub


Private Sub txtYear_GotFocus()
    lblFormatYear.Visible = True
    txtYear.SelStart = 0
    txtYear.SelLength = Len(txtYear)
    Exit Sub
End Sub

Private Sub txtYear_KeyPress(KeyAscii As Integer)
Dim KeyVal As Integer
    KeyVal = KeyAscii
    KeyAscii = ValiText(KeyAscii, "0123456789", True)
    If Not gfkeyEntered Then
        If KeyVal = vbKeyReturn Then
            SendKeys "{TAB}"
        End If
    End If
    Exit Sub
End Sub

Private Sub txtYear_LostFocus()
' The txtAmount_LostFocus procedure validates each data
' entry, reformats it for display.

Dim intYear As Double
Dim strYear As Double
Dim entryWidth As String

    
     If Not gfkeyEntered Then
        
        ' Determine whether the value has changed.
        If txtYear.Text <> "" Then
            ' Use Val function to eliminate nonnumeric characters.
            intYear = Val(Trim$(txtYear.Text))
            '
        End If
            '
            ' Do not allow negative values, or entries longer
            ' than six digits.
            If intYear < 0 Or intYear > 99 Then
                intYear = 0
                MsgBox "Year Range between 00 and 99"
                txtYear.SetFocus
                Exit Sub
            End If
                '
                ' If the entry is not zero, display the value
                ' in a right-justified dollar-and-cent format.
                If intYear <> 0 Then
                
                    
                ElseIf intYear = 0 And Trim$(txtYear.Text) = "" Then
                    gfkeyEntered = True
                    MsgBox " Please Enter an Year"
                    txtYear.SetFocus
                    Exit Sub
                Else
                    
                    gfkeyEntered = False
                End If
        Else
            
            gfkeyEntered = False
        End If
    
    Exit Sub
End Sub

Private Sub txtZip_GotFocus()
    txtZip.SelStart = 0
    txtZip.SelLength = Len(txtZip)
    Exit Sub
End Sub

Private Sub txtZip_KeyPress(KeyAscii As Integer)
Dim KeyVal As Integer
    KeyVal = KeyAscii
    KeyAscii = ValiText(KeyAscii, "0123456789", True)
    If Not gfkeyEntered Then
        If KeyVal = vbKeyReturn Then
            SendKeys "{TAB}"
        End If
    End If
    Exit Sub
End Sub

Private Sub txtZip_LostFocus()
' The txtAmount_LostFocus procedure validates each data
' entry, reformats it for display.

Dim intZip As Double
Dim strZip As Double
Dim entryWidth As String

    
     If Not gfkeyEntered Then
        
        ' Determine whether the value has changed.
        If txtZip.Text <> "" Then
            ' Use Val function to eliminate nonnumeric characters.
            intZip = Val(Trim$(txtZip.Text))
            '
        End If
        '
        ' Do not allow negative values, or entries longer
        ' than six digits.
        If Len(txtZip) < 5 Then
            intZip = 0
            MsgBox "Invalid Zip Code. Length must be at least five characters."
            txtZip.SetFocus
            Exit Sub
        End If
        '
        ' If the entry is not zero, display the value
        ' in a right-justified dollar-and-cent format.
        If Len(txtZip) <> 0 Then
                
                    
        ElseIf intZip = 0 And Trim$(txtZip.Text) = "" Then
            gfkeyEntered = True
            MsgBox " Please Enter a Zip Code"
            txtZip.SetFocus
            Exit Sub
        Else
            gfkeyEntered = False
        End If
    Else
        gfkeyEntered = False
    End If
    
    Exit Sub
End Sub
