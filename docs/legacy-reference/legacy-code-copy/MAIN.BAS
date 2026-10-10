Attribute VB_Name = "Utilities"
Option Explicit
'=====================================================

' File:     Main.bas
'
' DESCRIPTION: Define types, constants, global variables, and procedures
'              needed to support the Student Information System project.
'

'---------------------------------------------------------------------------
'               USER-DEFINED TYPES

'
' DESCRIPTION: User-Defined Types for the following files: Student Information,
' Student Current Employment, and Query Report file
'

'---------------------------------------------------------------------------
'               USER-DEFINED TYPES
'
Type Student_File
    
    'SS_Number As String * 10
    'Program_Code As String * 6
    'Program_Name As String * 30
   ' Last_Name As String * 15
   ' First_Name As String * 15
    'Home_Phone As String * 15
   ' Work_Phone As String * 15
    'Address As String * 30
    'City As String * 30
   ' State As String * 3
   ' Zip As String * 11
    'High_School As String * 30
   'Date_Graduated As String * 10
   ' Month As String * 3
    'Day As String * 3
    'YesNo As String * 2
    'Description As String * 100
    'Company_Code As String * 9
    
    Program_Code As String * 7
    Date As String * 9
    Program_Name As String * 31
    SS_Number As String * 10
    Last_Name As String * 16
    First_Name As String * 16
    Home_Phone As String * 16
    Work_Phone As String * 16
    Address As String * 31
    City As String * 31
    State As String * 3
    zip As String * 11
    High_School As String * 31
    Date_Graduated As String * 11
    Month As String * 3
    Day As String * 3
    YesNo As String * 2
    Description As String * 101
    Company_Code As String * 9


End Type
Public Students As Student_File

Type Query_File

    SS_Number As String * 10
    RecNum As Integer

End Type
Public QuerySoc As Query_File

Type Query_Type
    
    SS_Number As String * 10
    RecNum As Integer
    
End Type
Public Index() As Query_Type

Type StudentIndexType

    SS_Number As String * 10
    RecNum As Integer

End Type
Public IndexStudent() As StudentIndexType

Type CurrentEmployeeIndexType

   Company_Code As String * 9
    RecNum As Integer

End Type
Public IndexCurrEmp() As CurrentEmployeeIndexType




'Type Current_Employment
Type Employment_Type

    Company_Code As String * 9
    Company_Name As String * 31
    Address As String * 26
    City As String * 31
    State As String * 3
    zip As String * 11
    Job_Title As String * 31
    Current_Supervisor As String * 31
    Phone_Number As String * 16
    Hours_per_Week As String * 3
    Amount As String * 16
    Company_Type As String * 30
    

End Type
'Public Job As Current_Employment
'Public JOB As Employment_File
Public JOB As Employment_Type


'--------------------------------------------------------------
'
'                       API CALLS

#If Win16 Then
    Const CB_ERR = -1
    Const CB_FINDSTRING = &H40C
    Declare Function SENDMESSAGE Lib "User" Alias "SendMessage" (ByVal _
        HWND As Integer, ByVal WMSG As Integer, ByVal _
        WPARAM As Integer, LPARAM As Any) As Long
#Else
    Const CB_ERR = -1
    Const CB_FINDSTRING = &H14C
    Declare Function SENDMESSAGE Lib "User32" Alias _
        "SendMessageA" (ByVal HWND As Long, ByVal WMSG _
        As Long, ByVal WPARAM As Long, LPARAM As Any) As Long
#End If


'---------------------------------------------------------------
'
'                       CONSTANTS

Public Const StudentTextFile As String = "E:\StudentVB.DB"
Public Const CurrentEmploymentTextFile As String = "E:\EmploymentA.DB"
Public Const Query As String = "E:\RandomA.txt"
Public Const Student As String = "E:\Student.txt"
'---------------------------------------------------------------
'
'                       GLOBAL VARIABLES

Public FileIsOpen As Boolean     ' Indicates whether file is open
Public StudentSearchResult As Integer
Public CurrentEmploymentResult As Integer
Public numQuery As Integer
Public numStudents As Integer
Public numCurrEmp As Integer
Public gWhichRecord As Integer
Public gWhichStudentRecord As Integer
Public gWhichCurrEmpRecord As Integer
Public gSearchSSN As String
Public gCurrentEmployeeSearchValue As String
Public qQueryFile As Integer
Public gCurrentEmploymentMode As Boolean
' End of general declarations



Public Sub AutoMatch(cbo As ComboBox, KeyAscii As Integer)
Dim sBuffer As String
Dim iRetVal As Long
sBuffer = Left(cbo.Text, cbo.SelStart) & Chr(KeyAscii)
iRetVal = SENDMESSAGE((cbo.HWND), CB_FINDSTRING, _
-1, ByVal sBuffer)
If iRetVal <> CB_ERR Then
    cbo.ListIndex = iRetVal
    cbo.Text = cbo.List(iRetVal)
    cbo.SelStart = Len(sBuffer)
    cbo.SelLength = Len(cbo.Text)
    KeyAscii = 0
End If

End Sub ' AutoMatch


' The frmMain is the Parent MDI Screen(frmMain)
'Public fMainForm As frmMain
'================================================================
'                       PUBLIC SUB-PROCEDURES
'
'-----------------------------------------------------------------
'FUNCTION Main -- Open the Splash Screen followed by MDI parent frmMain
'
Sub Main()
    frmSplash.Show vbModal
    frmSplash.Refresh
    DoEvents
    
    'Load mdiBackGround
   
    ' unload the splash screen and free it's memory
    Unload frmSplash
    Set frmSplash = Nothing
    ' Launch the main menu
    Load frmMainMenu
    
    frmMainMenu.Show
    frmMainMenu.ZOrder 0
    frmMainMenu.Refresh

    'mdiBackGround.Show
    
End Sub
'================================================================
'                       PUBLIC SUB-PROCEDURES
'
'-----------------------------------------------------------------
'Public Sub CenterForm -- Procedure to center a form on the screen in VB3 or VB4
'
Public Sub CenterForm(frmTarget As Form)
     frmTarget.Move (Screen.Width - frmTarget.Width) / 2, _
          (Screen.Height - frmTarget.Height) / 2
End Sub


Function IsAlreadyOpen(testFileName As String) As Boolean

  ' The IsAlreadyOpen function determines whether
  ' a file that the user has requested is already
  ' open. (If it is, the program avoids the attempt
  ' to open it a second time.)
  
  Dim I

  ' Start out assuming the file is not open.
  IsAlreadyOpen = False
  
  

End Function  ' IsAlreadyOpen



Sub CBFindString(frm As Form, cbo As ComboBox, sFindStr As String)
   ' Search For String
   Dim iLoop As Integer
   Dim sStr As String

   For iLoop = 0 To cbo.ListCount - 1
      sStr = cbo.List(iLoop)
      If Trim$(UCase$(sStr)) = Trim$(UCase$(sFindStr)) Then
         cbo.ListIndex = iLoop
         iLoop = cbo.ListCount        ' Force Exit From Loop
      Else
         cbo.ListIndex = -1
      End If
   Next iLoop
End Sub
Sub CBFindPartialString(frm As Form, ctrControlName As Control, ByVal sFindStr As String)
   ' Search For String
   Dim iLoop As Integer
   Dim iLen As Integer
   Dim sStr As String

   sFindStr = Trim$(UCase$(sFindStr))
   iLen = Len(sFindStr)
   For iLoop = 0 To ctrControlName.ListCount - 1
      sStr = Left$(UCase$(ctrControlName.List(iLoop)), iLen)
      If sStr = sFindStr Then
       
         ctrControlName.ListIndex = iLoop
         iLoop = ctrControlName.ListCount        ' Force Exit From Loop
      Else
         ctrControlName.ListIndex = -1
      End If
   Next iLoop
End Sub
Function ValiText(KeyIn As Integer, _
   ValidateString As String, _
   Editable As Boolean) As Integer
   
    Dim ValidateList As String
    Dim KeyOut As Integer
    '
    If Editable = True Then
         ValidateList = UCase$(ValidateString) & Chr(8)
    Else
         ValidateList = UCase$(ValidateString)
    End If
    '
    If InStr(1, ValidateList, UCase$(Chr(KeyIn)), 1) > 0 Then
        KeyOut = KeyIn
    Else
        KeyOut = 0
        Beep
    End If
    
    ValiText = KeyOut
    
End Function
'================================================================
'                       PUBLIC SUB-PROCEDURES
'
'-----------------------------------------------------------------
'FUNCTION LoadProgramName -- Load the program name code into the
'                            cboProgramName combo box of the
'                            frmStudentInformation form.

'
Public Sub LoadProgramName(frm As Form)
    
    ' Clear the combo box
    frm.cboProgramName.Clear
    '
    ' Load the combo box with program Names and New Index
    frm.cboProgramName.AddItem "Computer Information Systems(Associate Degree)"
    frm.cboProgramName.ItemData(frm.cboProgramName.NewIndex) = 1234
    
    frm.cboProgramName.AddItem "Computer Information Systems(Diploma)"
    frm.cboProgramName.ItemData(frm.cboProgramName.NewIndex) = 2345
    
    frm.cboProgramName.AddItem "Lan Administrator(Certificate)"
    frm.cboProgramName.ItemData(frm.cboProgramName.NewIndex) = 3456
    
    frm.cboProgramName.AddItem "Visual Basic Programmer (Certificate)"
    frm.cboProgramName.ItemData(frm.cboProgramName.NewIndex) = 4567
    
    frm.cboProgramName.AddItem "Multimedia Programmer(Certificate)"
    frm.cboProgramName.ItemData(frm.cboProgramName.NewIndex) = 5678
    
    frm.cboProgramName.AddItem "Windows Proramming Specialist(Certificate)"
    frm.cboProgramName.ItemData(frm.cboProgramName.NewIndex) = 6789
    frm.cboProgramName.Index = 6789
End Sub
Public Sub OpenFileStudent()
    
    Close #2

    ' Open the database file.
    Open StudentTextFile For Random As #2 Len = Len(Students)

End Sub
Public Sub OpenFileStudentDb()
Close #4

    ' Open the database file.
    Open Student For Random As #4 Len = Len(Students)
End Sub

Public Sub OpenFileCurrentEmployment()
    
    Close #3


    ' Open the database file.
    Open CurrentEmploymentTextFile For Random As #3 Len = Len(JOB)

End Sub
 Public Sub OpenFileQuery()

    Close #1

    ' Open the database file.
    Open Query For Random As #1 Len = Len(Query)
End Sub
Public Sub CloseAll()
    Close #1
    Close #2
    Close #3
    Close #4
    Close #5
    Close #6
End Sub

