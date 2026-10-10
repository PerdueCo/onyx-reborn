VERSION 4.00
Begin VB.Form frmSSSNumber 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Student's Social Security Number"
   ClientHeight    =   2145
   ClientLeft      =   2505
   ClientTop       =   1800
   ClientWidth     =   6735
   ControlBox      =   0   'False
   Height          =   2550
   Left            =   2445
   LinkTopic       =   "Form2"
   MaxButton       =   0   'False
   MDIChild        =   -1  'True
   MinButton       =   0   'False
   ScaleHeight     =   2145
   ScaleWidth      =   6735
   ShowInTaskbar   =   0   'False
   Top             =   1455
   Width           =   6855
   Begin VB.CommandButton cmdSearch 
      Caption         =   "&OK"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   5400
      TabIndex        =   5
      Top             =   840
      Width           =   1095
   End
   Begin VB.TextBox txtVerifySSN 
      Height          =   375
      Left            =   3360
      MaxLength       =   9
      PasswordChar    =   "*"
      TabIndex        =   1
      Top             =   1440
      Width           =   1695
   End
   Begin VB.TextBox txtSNN 
      Height          =   375
      Left            =   3360
      MaxLength       =   9
      PasswordChar    =   "*"
      TabIndex        =   0
      Top             =   840
      Width           =   1695
   End
   Begin VB.Image Image1 
      Height          =   615
      Left            =   0
      Picture         =   "SSN.frx":0000
      Top             =   0
      Width           =   600
   End
   Begin VB.Label Label3 
      AutoSize        =   -1  'True
      Caption         =   "Re-Enter Social Securrity Number :"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   195
      Left            =   240
      TabIndex        =   4
      Top             =   1560
      Width           =   2985
   End
   Begin VB.Label Label2 
      AutoSize        =   -1  'True
      Caption         =   "Enter Social Security Number :"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   195
      Left            =   577
      TabIndex        =   3
      Top             =   960
      Width           =   2865
   End
   Begin VB.Label Label1 
      Alignment       =   2  'Center
      AutoSize        =   -1  'True
      Caption         =   "Enter  your Social Security Number "
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Times New Roman"
         Size            =   18
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   -1  'True
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00000080&
      Height          =   420
      Left            =   0
      TabIndex        =   2
      Top             =   120
      Width           =   6735
   End
End
Attribute VB_Name = "frmSSSNumber"
Attribute VB_Creatable = False
Attribute VB_Exposed = False
Option Explicit

'Const Query = "A:\Random.txt"

Private Sub cmdOK_Click(Index As Integer)
     ' Hide the Student Social Security Number
     frmSSSNumber.Hide
     '
     Select Case Index
        Case 0
            ' Launch the Student Input Form
            Load frmStudentInformation
            frmStudentInformation.Show
            '
        Case 1
            ' Unhide the Switch Board
            frmSwitchBoard.Show
            '
    End Select
    
     
End Sub

Private Sub cmdSearch_Click()

  ' The cmdSearch_Click procedure searches for a name in
  ' the phone directory, and retrieves the record.
  
  Dim SearchValue As String
  Dim rec As Integer, inFileRec As Integer
  Dim State As ComboBox
  
  SearchValue = ""
  
   OpenFileQuery
     If UCase(Me.txtSNN.Text) = "EXIT" Then
        frmSSSNumber.Hide
        frmSSSNumber.txtSNN.Text = ""
        'frmSwitchBoard.Show
        frmMainMenu.Show
        Refresh
        Exit Sub
  End If
  
  If Not SSNumberOK Then
    MsgBox "Enter the Social Security Number and Verify Social Security Number.", , "Search"
  Else
  
    If Trim(txtSNN.Text) = Trim(txtVerifySSN.Text) Then
        If Len(txtSNN.Text) = 9 And Len(txtVerifySSN.Text) Then
            ' Standardize the format and search for the name.
            SearchValue = Trim(txtSNN.Text)
            
            rec = Search(SearchValue)
                        
            ' If the Social Number is found, display the record.
            If rec > 0 Then
                inFileRec = Index(rec).RecNum
                
                ' Sort the report query file for output to
                ' the text file random.txt.
                SortQueryText
                '
                ShowStudentInfo frmStudentInformation
               
    
                ' Otherwise, tell the user that the search failed.
            Else
                'MsgBox "Can't find " & SearchValue & ".", , "Search"
                cmdSave_Click
                ShowStudentInfo frmStudentInformation
            End If
        Else
            MsgBox "Enter the Social Security Number and Verify Social Security Number."
            'Exit Sub
        End If
    
    Else
       MsgBox "Enter the Social Security Number and Verify Social Security Number."
      
    End If
  End If
  
  
  txtSNN = ""
  txtVerifySSN = ""
  
  ' Sort the report query file for output to
  ' the text file random.txt.
  SortQueryText
  
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
        CreateIndex
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

Private Sub Form_Load()

  ' The Form_Load procedure opens the database file and
  ' creates the index. (The Index array allows the
  ' program to search effectively for any record by
  ' a person's name.)
  'Initialize
  
  ' Open the database file.
  
  Open Query For Random As #1 Len = Len(Query)
  'OpenFileQuery
    
  ' Compute the number of records.
  numQuery = LOF(1) / Len(Query)
  

  ' If the file exists and contains one or
  ' more records, create the Index array.
  If numQuery > 0 Then
    ReDim Index(numQuery)
    CreateIndex
  End If
  
    '
    ' To Center Form On Screen
    CenterForm Me
    '
End Sub  ' Form_Load
Sub CreateIndex()

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
    

Private Function SSNumberOK() As Boolean

  ' The FullNameOK function checks to see if either
  ' of the name fields is blank. Returns True if
  ' the user has entered both names, or False if a
  ' name is missing.
  
  Dim blankSSN As Boolean, blankVerifySSN As Boolean
  
  blankSSN = (Trim(txtSNN.Text) = "")
  blankVerifySSN = (Trim(txtVerifySSN.Text) = "")
  
  SSNumberOK = Not (blankSSN Or blankVerifySSN)
  
End Function ' FullNameOK

Function Search(findText As String) As Integer

  ' The Search function performs a binary search to look
  ' for a name in the Index array.
  Dim pos1 As Integer, pos2 As Integer
  Dim posX As Integer, midPos As Integer, midStr As String
  
  ' Initialize position markers and search for the
  ' target string.
  pos1 = 1
  pos2 = numQuery
  posX = 0
  Do While pos1 <= pos2 And posX = 0
    midPos = (pos1 + pos2) \ 2
    midStr = Trim(Index(midPos).SS_Number)
  
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

Private Sub txtSNN_KeyPress(KeyAscii As Integer)
    KeyAscii = ValiText(KeyAscii, "0123456789exit", True)
    Exit Sub
End Sub

Private Sub txtVerifySSN_KeyPress(KeyAscii As Integer)
    KeyAscii = ValiText(KeyAscii, "0123456789", True)
    Exit Sub
End Sub
Private Sub cmdSave_Click()
     
  ' The cmdSave_Click procedure stores the current record
  ' entry in the databse and updates the index.
  Dim isFound As Integer, I
  Dim answer As Integer, lf As String
    
    OpenFileStudent
    OpenFileQuery
    isFound = Search(Trim(txtSNN))
    
    With QuerySoc
    
      .SS_Number = Trim(txtSNN.Text)
      
    End With
    
    ' If the name doesn't already exist, add the record.
    If isFound = 0 Then
      numQuery = numQuery + 1

       OpenFileQuery
      ' Write the record to the file and update the index.
      Put #1, numQuery, QuerySoc
    
      ReDim Index(numQuery)
      CreateIndex
      
    ' If the name already exists allow the user to
    ' revise the record (overwriting the previous entry).
    Else
      answer = MsgBox("This name is already on file." _
        & lf & "Do you want to save " & lf & _
        "a revised record?", 4, "Revise a Record")
        
      ' If the user confirms, store the revised record.
      If answer = 6 Then
        'OpenFileQuery
        'Put #1, Index(isFound).RecNum, QuerySoc
        'Open Query For Output As #1
       
      End If
    End If

  
End Sub  ' cmdSave_Click
Sub ShowStudentInfo(frm As Form)
    frmSSSNumber.Hide
    frm.Show
    
End Sub

