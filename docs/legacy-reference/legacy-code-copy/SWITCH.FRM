VERSION 4.00
Begin VB.Form frmSwitchBoard 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Gwinnett Technical Institution"
   ClientHeight    =   3390
   ClientLeft      =   3825
   ClientTop       =   2310
   ClientWidth     =   4935
   ControlBox      =   0   'False
   Height          =   4080
   Left            =   3765
   LinkTopic       =   "Form4"
   MaxButton       =   0   'False
   MDIChild        =   -1  'True
   MinButton       =   0   'False
   ScaleHeight     =   3390
   ScaleWidth      =   4935
   Top             =   1680
   Width           =   5055
   Begin VB.CommandButton Command1 
      Caption         =   "&Reports                       "
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Index           =   1
      Left            =   1080
      TabIndex        =   4
      Top             =   2040
      Width           =   2775
   End
   Begin VB.CommandButton Command1 
      Caption         =   " &Student Entry               "
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Index           =   0
      Left            =   1080
      TabIndex        =   2
      Top             =   1560
      Width           =   2775
   End
   Begin VB.Label Label4 
      BackColor       =   &H00FFFFFF&
      BackStyle       =   0  'Transparent
      Caption         =   "Options     "
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Index           =   3
      Left            =   1920
      TabIndex        =   3
      Top             =   960
      Width           =   1095
   End
   Begin VB.Label Label4 
      Alignment       =   2  'Center
      BackColor       =   &H00FFFFFF&
      Caption         =   "Main Menu  "
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Index           =   2
      Left            =   1320
      TabIndex        =   1
      Top             =   360
      Width           =   2295
   End
   Begin VB.Label lblDate 
      AutoSize        =   -1  'True
      Height          =   375
      Left            =   5160
      TabIndex        =   0
      Top             =   120
      Width           =   1605
   End
   Begin VB.Menu mnuFile 
      Caption         =   "&File"
      Begin VB.Menu mnuStudentEntry 
         Caption         =   "&Student Entry"
      End
      Begin VB.Menu mnuExit 
         Caption         =   "E&xit"
      End
   End
   Begin VB.Menu mnuEdit 
      Caption         =   "E&dit"
      Begin VB.Menu mnuSupervisorEnterEdit 
         Caption         =   "Supervisor Enter/Edit"
      End
   End
   Begin VB.Menu mnuReports 
      Caption         =   "&Reports"
      Enabled         =   0   'False
   End
   Begin VB.Menu mnuHelp 
      Caption         =   "&Help"
      Begin VB.Menu mnuAbout 
         Caption         =   "&About BSSI ..."
      End
   End
End
Attribute VB_Name = "frmSwitchBoard"
Attribute VB_Creatable = False
Attribute VB_Exposed = False


Option Explicit
Dim bOverform As Boolean
Dim MyStr As String

Private Sub Command1_Click(Index As Integer)
    Select Case Index
        Case 0
            frmSwitchBoard.Hide
            frmSSSNumber.Show
        Case 1
            ' Main Reports Switch
            frmSwitchBoard.Hide
            frmReports.Show
        Case 2
            frmSwitchBoard.Hide
            'frmMaintenance.Show
    End Select
   
End Sub

Private Sub Form_KeyPress(KeyAscii As Integer)

    
    If KeyAscii = 49 Then
        frmSwitchBoard.Hide
        frmSSSNumber.Show
        frmSSSNumber.Refresh
    End If
    If KeyAscii = 50 Then
        'frmReport.Show
        frmSwitchBoard.Hide
    End If
    If KeyAscii = 51 Then
        'frmEnterEdit.Show
        frmSwitchBoard.Hide
    End If
    
End Sub

Private Sub Form_Load()
   
    ' To Center Form On Screen
    CenterForm Me
    '
    ' Set Date and time
    'MyStr = Format(Now, "mm/dd/yyyy")
    MyStr = Now
    
    lblDate = MyStr
    '
End Sub


Public Sub ButtonPress(CurrentControl As Control, Container As Object)
    'This shrinks the image a little and draws the highlight and shadow
    'lines, this makes the image appear "pushed-in"

    Container.Cls
    Container.Line (CurrentControl.Left - 25, _
     CurrentControl.Top - 25)-(CurrentControl.Left + _
     CurrentControl.Width + 25, CurrentControl.Top - 25), vb3DShadow
    Container.Line (CurrentControl.Left - 25, _
     CurrentControl.Top - 25)-(CurrentControl.Left - 25, CurrentControl.Height + _
     CurrentControl.Top + 25), vb3DShadow
    Container.Line (CurrentControl.Left - 25, _
     CurrentControl.Top + CurrentControl.Height + 25)- _
     (CurrentControl.Left + CurrentControl.Width + 25, _
     CurrentControl.Top + CurrentControl.Height + 25), vb3DHighlight
    Container.Line (CurrentControl.Left + _
     CurrentControl.Width + 25, CurrentControl.Top + _
     CurrentControl.Height + 25)-(CurrentControl.Left + _
     CurrentControl.Width + 25, CurrentControl.Top - 25), vb3DHighlight
    CurrentControl.Width = CurrentControl.Width - 30
    CurrentControl.Height = CurrentControl.Height - 30
    CurrentControl.Move CurrentControl.Left + 30, CurrentControl.Top + 30
End Sub


Public Sub ButtonRelease(CurrentConttrol As Control, Container As Object)
    'This enlarges the image to its original size and draws the highlight
    'and shadow lines

    Container.Cls
    CurrentConttrol.Width = CurrentConttrol.Width + 30
    CurrentConttrol.Height = CurrentConttrol.Height + 30
    CurrentConttrol.Move CurrentConttrol.Left - 30, CurrentConttrol.Top - 30
    Container.Line (CurrentConttrol.Left - 25, _
     CurrentConttrol.Top - 25)-(CurrentConttrol.Left + _
     CurrentConttrol.Width + 25, CurrentConttrol.Top - 25), vb3DHighlight
    Container.Line (CurrentConttrol.Left - 25, _
     CurrentConttrol.Top - 25)-(CurrentConttrol.Left - 25, _
     CurrentConttrol.Height + CurrentConttrol.Top + 25), vb3DHighlight
    Container.Line (CurrentConttrol.Left - 25, _
     CurrentConttrol.Top + CurrentConttrol.Height + 25)- _
     (CurrentConttrol.Left + CurrentConttrol.Width + 25, _
     CurrentConttrol.Top + CurrentConttrol.Height + 25), vb3DShadow
    Container.Line (CurrentConttrol.Left + _
     CurrentConttrol.Width + 25, CurrentConttrol.Top + _
     CurrentConttrol.Height + 25)-(CurrentConttrol.Left + _
     CurrentConttrol.Width + 25, CurrentConttrol.Top - 25), vb3DShadow
End Sub

Public Sub HighlightBorder(CurrentControl As Control, Container As Object)
    'This draws the highlight and shadow lines that make the image
    'appear 3D
    
    Container.Line (CurrentControl.Left - 25, CurrentControl.Top - 25)- _
     (CurrentControl.Left + CurrentControl.Width + 25, CurrentControl.Top - _
     25), vb3DHighlight
    Container.Line (CurrentControl.Left - 25, CurrentControl.Top - 25)- _
     (CurrentControl.Left - 25, CurrentControl.Height + CurrentControl.Top + _
     25), vb3DHighlight
    Container.Line (CurrentControl.Left - 25, CurrentControl.Top + _
     CurrentControl.Height + 25)-(CurrentControl.Left + _
     CurrentControl.Width + 25, CurrentControl.Top + _
     CurrentControl.Height + 25), vb3DShadow
    Container.Line (CurrentControl.Left + CurrentControl.Width + 25, _
     CurrentControl.Top + CurrentControl.Height + 25)-(CurrentControl.Left + _
     CurrentControl.Width + 25, CurrentControl.Top - 25), vb3DShadow
End Sub
Private Sub Form_MouseMove(Button As Integer, Shift As Integer, X As Single, Y As Single)
    'This tells VB that the mouse is not over the image

    If Not bOverform Then
        Cls
        bOverform = True
    End If
End Sub


Private Sub Image1_Click()

    frmSwitchBoard.Hide
    frmSSSNumber.Show
End Sub

Private Sub Image1_MouseDown(Button As Integer, Shift As Integer, X As Single, Y As Single)
    'This calls the ButtonPress procedure for Image1

    ButtonPress Image1, Me
End Sub


Private Sub Image1_MouseMove(Button As Integer, Shift As Integer, X As Single, Y As Single)
    'This tells VB that the mouse is over the image, then it calls the HighlightBorder
    'procedure for Image1

    If bOverform Then
        HighlightBorder Image1, Me
        bOverform = False
    End If
End Sub


Private Sub Image1_MouseUp(Button As Integer, Shift As Integer, X As Single, Y As Single)
    'This calls the ButtonRelease procedure for Image1

    'Form1.Show
    ButtonRelease Image1, Me
End Sub




Private Sub Image2_MouseDown(Button As Integer, Shift As Integer, X As Single, Y As Single)
    'This calls the ButtonPress procedure for Image1

    ButtonPress Image2, Me
End Sub


Private Sub Image2_MouseMove(Button As Integer, Shift As Integer, X As Single, Y As Single)
    'This tells VB that the mouse is over the image, then it calls the HighlightBorder
    'procedure for Image2

    If bOverform Then
        HighlightBorder Image2, Me
        bOverform = False
    End If
End Sub


Private Sub Image2_MouseUp(Button As Integer, Shift As Integer, X As Single, Y As Single)
    'This calls the ButtonRelease procedure for Image2

    ButtonRelease Image2, Me
End Sub


Private Sub Image3_Click()
    frmSwitchBoard.Hide
    frmMaintenance.Show
   
End Sub

Private Sub Image3_MouseDown(Button As Integer, Shift As Integer, X As Single, Y As Single)
    'This calls the ButtonPress procedure for Image1
    
    ButtonPress Image3, Me
End Sub


Private Sub Image3_MouseMove(Button As Integer, Shift As Integer, X As Single, Y As Single)
    'This tells VB that the mouse is over the image, then it calls the HighlightBorder
    'procedure for Image3

    If bOverform Then
        HighlightBorder Image3, Me
        bOverform = False
    End If
End Sub


Private Sub Image3_MouseUp(Button As Integer, Shift As Integer, X As Single, Y As Single)
    'This calls the ButtonRelease procedure for Image2
    
    ButtonRelease Image3, Me
End Sub




Private Sub mnuAbout_Click()
    frmAbout.Show vbModal
End Sub

Private Sub mnuExit_Click()
    End
End Sub

Private Sub Timer1_Timer()
    'lblTime = Format$(Time, "hh:mm:ss AMPM")
End Sub
