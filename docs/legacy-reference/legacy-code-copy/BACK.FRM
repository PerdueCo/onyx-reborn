VERSION 4.00
Begin VB.MDIForm mdiBackGround 
   BackColor       =   &H00FFFFFF&
   Caption         =   "Business Science Student Information"
   ClientHeight    =   6315
   ClientLeft      =   1365
   ClientTop       =   6210
   ClientWidth     =   6720
   Height          =   6720
   Left            =   1305
   LinkTopic       =   "MDIForm1"
   NegotiateToolbars=   0   'False
   Top             =   5865
   Width           =   6840
   WindowState     =   2  'Maximized
End
Attribute VB_Name = "mdiBackGround"
Attribute VB_Creatable = False
Attribute VB_Exposed = False


Private Sub MDIForm_Load()
    ' Launch the main menu
    Load frmMainMenu
    
    frmMainMenu.Show
    frmMainMenu.ZOrder 0
    'frmMainMenu.Refresh
    
    
    'Load frmSwitchBoard
    'frmSwitchBoard.Show
    'frmSwitchBoard.Refresh
    '
End Sub

Private Sub MDIForm_QueryUnload(Cancel As Integer, UnloadMode As Integer)
    Set frmConstruction = Nothing
    Set frmAbout = Nothing
    Set frmSwitchBoard = Nothing
    Set frmSplash = Nothing
    Set frmSSSNumber = Nothing
    Set frmStudentInformation = Nothing
    Set frmCurrentEmployment = Nothing
    Set mdiBackGround = Nothing
    Set frmSearch = Nothing
    Set frmEmployment = Nothing
    Set frmPrintSS = Nothing
    Set frmRandom = Nothing
    Set frmSearch = Nothing
    Set frmSelect_Rec = Nothing
    End
End Sub

Private Sub mnuEnd_Click()
    End
End Sub

Private Sub mnuFederalTaxIDHistory_Click()
   
    
End Sub

Private Sub mnuImportDataFile_Click()
   

End Sub
