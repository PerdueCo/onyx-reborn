VERSION 4.00
Begin VB.Form frmCurrentEmployment 
   BackColor       =   &H00C0C0C0&
   BorderStyle     =   1  'Fixed Single
   Caption         =   "CURRENT EMPLOYMENT"
   ClientHeight    =   6195
   ClientLeft      =   1290
   ClientTop       =   4470
   ClientWidth     =   8220
   ControlBox      =   0   'False
   Height          =   6645
   Left            =   1230
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MDIChild        =   -1  'True
   MinButton       =   0   'False
   ScaleHeight     =   6597.08
   ScaleMode       =   0  'User
   ScaleWidth      =   8343.847
   Top             =   4080
   Width           =   8340
   Begin VB.TextBox txtZip 
      Height          =   285
      Left            =   6480
      MaxLength       =   10
      TabIndex        =   8
      Top             =   2280
      Width           =   1575
   End
   Begin VB.Frame Frame1 
      Height          =   5415
      Left            =   120
      TabIndex        =   24
      Top             =   0
      Width           =   8055
      Begin VB.TextBox txtWorkPhone 
         Height          =   375
         Left            =   1920
         MaxLength       =   13
         TabIndex        =   14
         Top             =   3360
         Width           =   2415
      End
      Begin VB.TextBox txtCity 
         Height          =   285
         Left            =   1920
         TabIndex        =   5
         Top             =   2280
         Width           =   2295
      End
      Begin VB.TextBox txtAmount 
         Height          =   285
         Left            =   1920
         TabIndex        =   18
         Top             =   4440
         Width           =   2655
      End
      Begin VB.ComboBox cboCompany_Type 
         Height          =   300
         ItemData        =   "CURREMPL.frx":0000
         Left            =   1920
         List            =   "CURREMPL.frx":0034
         Style           =   2  'Dropdown List
         TabIndex        =   20
         Top             =   4800
         Width           =   6015
      End
      Begin VB.TextBox txtCompanyName 
         Height          =   285
         Left            =   1920
         TabIndex        =   1
         Top             =   1560
         Width           =   6015
      End
      Begin VB.TextBox txtAddress 
         Height          =   285
         Left            =   1920
         TabIndex        =   3
         Top             =   1920
         Width           =   6015
      End
      Begin VB.ComboBox cboState 
         Height          =   315
         ItemData        =   "CURREMPL.frx":0146
         Left            =   4920
         List            =   "CURREMPL.frx":014D
         TabIndex        =   21
         Text            =   "Ga"
         Top             =   2280
         Width           =   735
      End
      Begin VB.TextBox txtJobTitle 
         Height          =   285
         Left            =   1920
         TabIndex        =   10
         Top             =   2640
         Width           =   6015
      End
      Begin VB.TextBox txtCurrentSupervisor 
         Height          =   285
         Left            =   1920
         TabIndex        =   12
         Top             =   3000
         Width           =   6015
      End
      Begin VB.TextBox txtCompanyType 
         Height          =   285
         Left            =   1920
         TabIndex        =   25
         Text            =   "Environmental Protection Air"
         Top             =   4800
         Width           =   6015
      End
      Begin VB.TextBox txtHoursPerWeek 
         Height          =   285
         Left            =   1920
         TabIndex        =   16
         Top             =   4080
         Width           =   375
      End
      Begin VB.PictureBox mskPhoneNumber 
         Height          =   375
         Left            =   1920
         ScaleHeight     =   315
         ScaleWidth      =   2370
         TabIndex        =   29
         Top             =   3360
         Width           =   2430
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
         Left            =   6240
         TabIndex        =   28
         Top             =   1230
         Width           =   615
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00808080&
         Index           =   0
         X1              =   240
         X2              =   7920
         Y1              =   3840
         Y2              =   3840
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00FFFFFF&
         Index           =   1
         X1              =   240
         X2              =   7920
         Y1              =   3855
         Y2              =   3855
      End
      Begin VB.Label lblDate 
         BorderStyle     =   1  'Fixed Single
         Caption         =   "04/28/1998"
         Height          =   285
         Left            =   6840
         TabIndex        =   27
         Top             =   1200
         Width           =   1095
      End
      Begin VB.Label Label4 
         Caption         =   "Company &Name  :"
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
         TabIndex        =   0
         Top             =   1560
         Width           =   1575
      End
      Begin VB.Label Label5 
         Caption         =   "           &Address  :"
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
         TabIndex        =   2
         Top             =   1920
         Width           =   1575
      End
      Begin VB.Label Label6 
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
         Left            =   360
         TabIndex        =   4
         Top             =   2280
         Width           =   1575
      End
      Begin VB.Label Label7 
         Caption         =   "            &JobTitle :"
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
         TabIndex        =   9
         Top             =   2640
         Width           =   1575
      End
      Begin VB.Label Label8 
         BackStyle       =   0  'Transparent
         Caption         =   "Current Super&visor  :"
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
         Left            =   120
         TabIndex        =   11
         Top             =   3000
         Width           =   1815
      End
      Begin VB.Label Label9 
         Caption         =   "  &Phone Number :"
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
         TabIndex        =   13
         Top             =   3360
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
         Left            =   3480
         TabIndex        =   6
         Top             =   2280
         Width           =   1455
      End
      Begin VB.Label Label11 
         Caption         =   "                  &Zip  :"
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
         Left            =   4680
         TabIndex        =   7
         Top             =   2280
         Width           =   1815
      End
      Begin VB.Label Label12 
         Caption         =   "&Hours Per Week :"
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
         TabIndex        =   15
         Top             =   4080
         Width           =   1575
      End
      Begin VB.Label Label14 
         BackStyle       =   0  'Transparent
         Caption         =   "            Hourly &Rate :"
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
         TabIndex        =   17
         Top             =   4440
         Width           =   2175
      End
      Begin VB.Label Label15 
         Caption         =   "  Company &Type :"
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
         TabIndex        =   19
         Top             =   4920
         Width           =   1575
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00808080&
         Index           =   2
         X1              =   240
         X2              =   7920
         Y1              =   840
         Y2              =   840
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00FFFFFF&
         Index           =   3
         X1              =   240
         X2              =   7920
         Y1              =   855
         Y2              =   855
      End
      Begin VB.Label Label16 
         BackStyle       =   0  'Transparent
         Caption         =   "Please Enter Current Employment :"
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
         Left            =   360
         TabIndex        =   26
         Top             =   360
         Width           =   6735
      End
   End
   Begin VB.PictureBox Picture1 
      BackColor       =   &H00C0C0C0&
      Height          =   585
      Left            =   120
      ScaleHeight     =   525
      ScaleWidth      =   7995
      TabIndex        =   22
      Top             =   5520
      Width           =   8055
      Begin VB.CommandButton cmdAcceptCurrentEmployment 
         Caption         =   "&Accept"
         Height          =   375
         Left            =   3360
         TabIndex        =   23
         Top             =   120
         Width           =   975
      End
   End
End
Attribute VB_Name = "frmCurrentEmployment"
Attribute VB_Creatable = False
Attribute VB_Exposed = False


Option Explicit
Dim gfkeyEntered As Boolean
Dim Key As Integer

Const AmtFormat = "$#,####0.00"   ' Employment Salary data display format.
Const Student = "A:\CurrEmpDB.txt"

Private Sub cmdAcceptCurrentEmployment_Click()

  ' The cmdAcceptCurrentEmployment_Click procedure stores the current record
  ' entry in the databse and updates the index.
  Dim isFound As Integer, I
  Dim answer As Integer, lf As String
  Dim SearchValue As String
  Dim CurrentEmployment As String
  Dim StudentInformation As String
 
  ' Standardize the format and search for the name.
  SearchValue = Trim(gCurrentEmployeeSearchValue)
  isFound = Search(SearchValue)
  
  OpenFileStudent
  
  OpenFileCurrentEmployment
 
 ' Read the target record from the database.
'Get #2, gWhichStudentRecord, Students

  CurrentEmployment = frmCurrentEmployment.txtCompanyName
  StudentInformation = frmCurrentEmployment.txtWorkPhone.Text
    With Students
            .Company_Code = Mid(CreateCompanyCode(CurrentEmployment, StudentInformation), 1, 8) 'Right(Trim(frm.mskHomePhone.Text), 4) & "" & Right(Trim(txtCompanyName), 4)
            'MsgBox .Company_Code
    End With
        
 ' Read the target record from the database.
 '  Get #3, gWhichCurrEmpRecord, JOB
    
    With JOB
        .Company_Code = Mid(CreateCompanyCode(CurrentEmployment, StudentInformation), 1, 8)
        'MsgBox .Company_Code
        .Company_Name = Mid(txtCompanyName, 1, 30)
        .Address = Mid(txtAddress, 1, 26)
        .City = Mid(txtCity, 1, 30)
        '.State
        .zip = txtZip.Text
        .Job_Title = Mid(txtJobTitle, 1, 30)
        .Current_Supervisor = Mid(txtCurrentSupervisor, 1, 30)
        .Phone_Number = txtWorkPhone.Text
        .Hours_per_Week = Mid(txtHoursPerWeek, 1, 2)
        .Amount = Mid(txtAmount, 1, 16)
        If cboCompany_Type.ListIndex = -1 Then
            .Company_Type = ""
        Else
            .Company_Type = Mid(Trim(cboCompany_Type.Text), 1, 30)
        End If
        '.Company_Type = Mid(Trim(cboCompany_Type.Text), 1, 30)
        
    End With
    
     
  ' Otherwise, search for this number in an existing record
  ' and copy the entry to the Student record variable.
    'isFound = Search(Mid(CreateCompanyCode(CurrentEmployment, StudentInformation), 1, 8))
    
    ' If the name doesn't already exist, add the record.
    If isFound = 0 Then
      numCurrEmp = numCurrEmp + 1
      gWhichCurrEmpRecord = numCurrEmp
        
      ' Write the record to the file and update the index.
      Put #3, numCurrEmp, JOB
      Close #3
      ReDim IndexCurrEmp(numCurrEmp)
      CreateCurrEmpIndex
      
    
      'Put #2, IndexStudent(gWhichStudentRecord).RecNum, Students
      Put #2, gWhichStudentRecord, Students
      Close #2
      
    ' If the name already exists allow the user to
    ' revise the record (overwriting the previous entry).
    Else
      answer = MsgBox("This name is already on file." _
        & lf & "Do you want to save " & lf & _
        "a revised record?", 4, "Revise a Record")
        
      ' If the user confirms, store the revised record.
      If answer = 6 Then
        Put #3, IndexCurrEmp(isFound).RecNum, JOB
        Close #3
        'Put #intfile, IndexCurrEmp(gWhichCurrEmpRecord).RecNum, Job
        Put #2, IndexStudent(gWhichStudentRecord).RecNum, Students
        Close #2
      End If
    End If
    'frmCurrentEmployment.Hide
    'frmStudentInformation.Hide
    Unload Me
    Unload frmStudentInformation
   
    frmSSSNumber.Show
    SortEmploymentText
    SortStudentText
    CloseAll
End Sub

Private Sub Form_Activate()
 ' Display the current record
    If gWhichStudentRecord > 0 Then
        'ShowRecord gWhichCurrEmpRecord
    End If

End Sub

Private Sub Form_Load()

    Dim SearchValue As String
    Dim rec As Integer
    Dim inFileRec As Integer
    Dim Records As Integer
    Dim MCompanyCode As String

      On Error GoTo FormLoad_EH
    
    lblDate = Format(Date, "mm/d/yyyy")
    
     OpenFileCurrentEmployment
    
    ' Compute the number of records.
    numCurrEmp = LOF(3) / Len(JOB)
  
    'MsgBox numCurrEmp
    ' If the file exists and contains one or
    ' more records, create the Index array.
    If numCurrEmp > 0 Then
        ReDim IndexCurrEmp(numCurrEmp)
        CreateCurrEmpIndex
    End If
    '
    ' To Center Form On Screen
    CenterForm Me
    '
    ' Show the program
    Me.Show
    '
    ' Load Programs into cboProgramName
    'LoadState Me
    '
    ' Search string
    SearchValue = Trim(gCurrentEmployeeSearchValue)
    '
    rec = Search(SearchValue)
           'MsgBox rec
            
            ' If the Social Number is found, display the record.
            If rec > 0 Then
                inFileRec = IndexCurrEmp(rec).RecNum
                '
                 gWhichCurrEmpRecord = inFileRec
                '
                ShowRecord IndexCurrEmp(rec).RecNum
                '
                '
                ShowEmploymentInfo Me
                '
                ' Otherwise, tell the user that the search failed.
            Else
                'If Len(SearchValue) = 0 Then
            
                    'MsgBox "Can't find " & SearchValue & ".", , "Search"
                    '
                    ShowEmploymentInfo Me
                    '
                    ClearCurrentEmployment Me
                    '
                'Else
                
                'End If
            End If
    'cmdSearch_Click
    
    '  Text BOX Program Name to have focus on the initial displaying of form.
    txtCompanyName.SetFocus
    
    Exit Sub
    
FormLoad_EH:
    Resume Next
    Exit Sub
End Sub

Private Sub ShowRecord(ReadRecord As Integer)
Dim inFileRec As Integer
'Dim ReadRecord As Integer
Dim SearchValue As String
Dim CompanyType As ComboBox
Dim State As ComboBox

    ' The ShowRecord procedure retrieves a record
    ' from the database and displays its fields in
    ' the frm form. (Note that this procedure
    ' is called from cmdSearch_Click and from
    ' Form_Activate.)

    ' The variable readRecord represents an actual
    ' record number, not an element of the Index
    ' array.
    
    
    OpenFileCurrentEmployment
    
        ' Read the target record from the database.
        Get #3, ReadRecord, JOB
    
        ' Copy the fields of the record to
        ' the controls on the frmStudentInformation form.
        With JOB
            
            txtCompanyName = .Company_Name
            txtAddress = .Address
            txtCity = .City
            txtZip.Text = .zip
            txtJobTitle = .Job_Title
            txtCurrentSupervisor = .Current_Supervisor
            txtWorkPhone.Text = .Phone_Number
            txtHoursPerWeek = .Hours_per_Week
            txtAmount = .Amount
            '.frm.txtCompanyType = .Company_Type
            
            ' Passing object variable
            Set CompanyType = cboCompany_Type
            
            ' Find String Code In Combo Boxes
            Call CBFindPartialString(frmCurrentEmployment, CompanyType, .Company_Type)
            
        End With
        
        ' Put #3, ReadRecord, JOB
  
        Close #3
        
End Sub  ' ShowRecord
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

Function Search(findText As String) As Integer

  ' The Search function performs a binary search to look
  ' for a name in the Index array.
  Dim pos1 As Integer, pos2 As Integer
  Dim posX As Integer, midPos As Integer, midStr As String
  
  ' Initialize position markers and search for the
  ' target string.
  pos1 = 1
  pos2 = numCurrEmp
  posX = 0
  Do While pos1 <= pos2 And posX = 0
    midPos = (pos1 + pos2) \ 2
    midStr = RTrim(IndexCurrEmp(midPos).Company_Code)
    If findText = midStr Then
      posX = midPos
    ElseIf findText > midStr Then
      pos1 = midPos + 1
    Else
      pos2 = midPos - 1
    End If
  Loop
  
  ' Return the Index subscript where the name is located,
  ' or zero if the name was not found.
  Search = posX

End Function  ' Search

Function CreateCompanyCode(f As String, l As String) _
    As String

  ' The CreateCompanyCode function standardizes the
  ' company code of each current employment and student record, so that
  ' different name entries can be compared
  ' successfully.
  
  ' Concatenate the last four digits of home phone
  ' and last four digit of the company name.
  ' into a standard uppercase , trimmed and right trimmed format.
  CreateCompanyCode = UCase(Left(Trim(f), 4) + "" + Right(Trim(l), 4))

End Function  ' CreateCompanyCode

Private Sub cmdSearch_Click()

  ' The cmdSearch_Click procedure searches for a name in
  ' the phone directory, and retrieves the record.
  
  Dim searchSoc As String
  Dim rec As Integer, inFileRec As Integer
  
  
    ' Standardize the format and search for the name.
    searchSoc = Trim(gCurrentEmployeeSearchValue)
    
    rec = Search(searchSoc)
    'gWhichCurrEmpRecord = rec
  
    ' If the name is found, display the record.
    If rec > 0 Then
      inFileRec = IndexCurrEmp(rec).RecNum
      gWhichCurrEmpRecord = inFileRec
      ShowRecord inFileRec
    
    ' Otherwise, tell the user that the search failed.
    Else
      'MsgBox "Can't find " & searchSoc & ".", , "Search"
      ClearCurrentEmployment Me
      
    End If

End Sub  ' cmdSearch_Click
Public Sub ClearCurrentEmployment(frm As Form)
    
    frm.txtCompanyName = ""
    frm.txtAddress = ""
    frm.txtCity = ""
    frm.cboState.ListIndex = -1
    frm.mskZipCode.Mask = ""
    frm.mskZipCode.Text = ""
    frm.txtJobTitle = ""
    frm.txtCurrentSupervisor = ""
    frm.mskPhoneNumber.Mask = ""
    frm.mskPhoneNumber.Text = ""
    frm.txtAmount = ""
    frm.cboCompany_Type.ListIndex = -1
    
End Sub ' ClearCurrentEmployment

Private Sub Form_Unload(Cancel As Integer)
    Close #2
    Close #3
    Unload frmCurrentEmployment
    Unload frmStudentInformation
    frmSSSNumber.Show
       
End Sub

Private Sub SortEmploymentText()
    ' Open the database file.
    OpenFileCurrentEmployment
    
    ' Compute the number of records.
    numCurrEmp = LOF(3) / Len(JOB)
  
    'MsgBox numCurrEmp
    ' If the file exists and contains one or
    ' more records, create the Index array.
    If numCurrEmp > 0 Then
        ReDim IndexCurrEmp(numCurrEmp)
        CreateCurrEmpIndex
    End If
    
    Open "A:\Employment.txt" For Output As #6
    For I = 1 To numCurrEmp
        Get #3, IndexCurrEmp(I).RecNum, JOB
            With JOB
                Print #6, .Company_Code;
                Print #6, .Company_Name;
                Print #6, .Address;
                Print #6, .City;
                Print #6, .State;
                Print #6, .zip;
                Print #6, .Job_Title;
                Print #6, .Current_Supervisor;
                Print #6, .Phone_Number;
                Print #6, .Hours_per_Week;
                Print #6, .Amount;
                Print #6, .Company_Type;
               
            End With
    Next I
    Close #3
    Close #6
    '
End Sub












Private Sub MaskEdBox1_ValidationError(InvalidText As String, StartPosition As Integer)

End Sub

Private Sub mskPhoneNumber_KeyPress(KeyAscii As Integer)


If Not gfkeyEntered Then
         mskPhoneNumber.Mask = ""
         mskPhoneNumber.Text = ""
         mskPhoneNumber.Mask = "(###)###-####"
         gfkeyEntered = True
End If

End Sub

Private Sub mskPhoneNumber_LostFocus()
Dim strPos As String
Dim strMask As String
   gfkeyEntered = False
    If mskPhoneNumber.Text = "(___)___-____" Then
       mskPhoneNumber.Mask = ""
       mskPhoneNumber.Text = ""
    End If
    If mskPhoneNumber.Text <> "" Then
       strPos = InStr(1, mskPhoneNumber.Text, "_", 1)
       If strPos <> "0" Then
          MsgBox " Please Enter Phone Number as (404)648-2815"
          mskPhoneNumber.SetFocus
          Exit Sub
       End If
    End If
    Exit Sub
End Sub

Private Sub Text2_Change()

End Sub

Private Sub txtAmount_GotFocus()
    txtAmount.SelStart = 0
    txtAmount.SelLength = Len(txtAmount.Text)
    Exit Sub
End Sub

Private Sub txtAmount_KeyPress(KeyAscii As Integer)

Dim KeyVal As Integer
    KeyVal = KeyAscii
    KeyAscii = ValiText(KeyAscii, "0123456789.", True)
    If Not gfkeyEntered Then
        If KeyVal = vbKeyReturn Then
            SendKeys "{TAB}"
        End If
    End If
    Exit Sub
End Sub

Private Sub txtAmount_LostFocus()

' The txtAmount_LostFocus procedure validates each data
' entry, reformats it for display.

Dim intAmount As Double
Dim strAmount As Double
Dim entryWidth As String

     entryWidth = Space(15) ' Width for right-justifying data.
     If Not gfkeyEntered Then
        
        ' Determine whether the value has changed.
        If txtAmount.Text <> "" Then
            ' Use Val function to eliminate nonnumeric characters.
            intAmount = Val(Trim$(txtAmount.Text))
            '
        End If
            '
            ' Do not allow negative values, or entries longer
            ' than six digits.
            If intAmount < 0 Or intAmount > 999999999999999# Then
                intAmount = 0
                MsgBox "Amount Range between $0.00 and $1,000,000,000.00"
                txtAmount.SetFocus
                Exit Sub
            End If
                '
                ' If the entry is not zero, display the value
                ' in a right-justified dollar-and-cent format.
                If intAmount <> 0 Then
                 RSet entryWidth = _
                    Format(txtAmount, AmtFormat)
                    txtAmount.Text = entryWidth
                ElseIf intAmount = 0 And Trim$(txtAmount.Text) = "" Then
                    gfkeyEntered = True
                    MsgBox " Please Enter an Amount"
                    txtAmount.SetFocus
                    Exit Sub
                Else
                    gfkeyEntered = False
                End If
        Else
            gfkeyEntered = False
        End If
    
    Exit Sub
End Sub

Private Sub mskZipCode_GotFocus()
    mskZipCode.SelStart = 0
    mskZipCode.SelLength = Len(mskZipCode.Text)
    Exit Sub
End Sub

Private Sub mskZipCode_KeyPress(KeyAscii As Integer)
If Not gfkeyEntered Then
         mskZipCode.Mask = ""
         mskZipCode.Text = ""
         mskZipCode.Mask = "#####-####"
         gfkeyEntered = True
End If
'Dim KeyVal As Integer
    'KeyVal = KeyAscii
    'If Not gfkeyEntered Then
        'If KeyVal = vbKeyReturn Then
            'SendKeys "{TAB}"
        'End If
    'End If
    'Exit Sub
End Sub

Private Sub mskZipCode_LostFocus()
Dim strPos As String
Dim strMask As String
 
     If Not gfkeyEntered Then
        If mskZipCode.Text <> "" Then
            strPos = InStr(1, mskZipCode.Text, "_", 1)
            If strPos <> "0" Then
                gfkeyEntered = True
                MsgBox " Please Enter Zip Code as 30334-3453"
                mskZipCode.SetFocus
                Exit Sub
            End If
        Else
            gfkeyEntered = False
        End If
    Else
        gfkeyEntered = False
    End If
    
    Exit Sub
End Sub
Sub ShowEmploymentInfo(frm As Form)
    
    frm.Show
    
End Sub
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


Private Sub txtZip_Change()
Dim zip As Single
    'Dim MyStr As String
    
    zip = Len(txtZip.Text)
    'MyStr = txtZip.Text
    
    Select Case zip
        Case 1
            If Key <> 8 Then
                txtZip.SelStart = 2
            End If
        
        Case 5
            If Key <> 8 Then
                txtZip = txtZip.Text & "-"
                txtZip.SelStart = 7
            End If
    End Select
End Sub


Private Sub txtZip_GotFocus()
    txtZip.SelStart = 0
    txtZip.SelLength = Len(txtZip)
    Exit Sub
End Sub


Private Sub txtZip_KeyPress(KeyAscii As Integer)
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

Private Sub txtZip_LostFocus()
Dim intLength As Integer

If Not gfkeyEntered Then
    intLength = Len(txtZip)
    If Trim$(txtZip.Text) = "" Or Len(txtZip) < 5 Or Len(txtZip) < 10 Then
        Select Case intLength
        Case 6
            txtZip = txtZip & "0000"
        Case 7, 8, 9
            gfkeyEntered = True
            MsgBox "Invalid Zip Code. Length must be at least nine characters "
            txtZip.SetFocus
        Case 1, 2, 3, 4
            gfkeyEntered = True
            MsgBox "Invalid Zip Code. Length must be at least five characters."
            txtZip.SetFocus
        End Select
        Exit Sub
    Else
        gfkeyEntered = False
    End If
Else
    gfkeyEntered = False
End If
    Exit Sub
End Sub


