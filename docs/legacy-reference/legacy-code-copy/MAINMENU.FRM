VERSION 4.00
Begin VB.Form frmMainMenu 
   ClientHeight    =   7335
   ClientLeft      =   4875
   ClientTop       =   1845
   ClientWidth     =   11145
   ControlBox      =   0   'False
   Height          =   7740
   Left            =   4815
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   7335
   ScaleWidth      =   11145
   Top             =   1500
   Width           =   11265
   WindowState     =   2  'Maximized
   Begin VB.PictureBox Picture1 
      Height          =   4335
      Left            =   360
      ScaleHeight     =   4275
      ScaleWidth      =   4155
      TabIndex        =   2
      Top             =   1920
      Width           =   4215
      Begin VB.CommandButton cmdMainMenu 
         Appearance      =   0  'Flat
         BackColor       =   &H80000005&
         Caption         =   "&STUDENT"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Index           =   0
         Left            =   480
         TabIndex        =   6
         Top             =   1080
         Width           =   3135
      End
      Begin VB.CommandButton cmdMainMenu 
         Appearance      =   0  'Flat
         BackColor       =   &H80000005&
         Caption         =   "E&XIT"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Index           =   2
         Left            =   480
         TabIndex        =   5
         Top             =   2760
         Width           =   3135
      End
      Begin VB.CommandButton cmdMainMenu 
         Appearance      =   0  'Flat
         BackColor       =   &H80000005&
         Caption         =   "&INSTRUCTOR"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Index           =   1
         Left            =   480
         TabIndex        =   4
         Top             =   1920
         Width           =   3135
      End
      Begin VB.Label lblMainMenu 
         Alignment       =   2  'Center
         BackColor       =   &H00FFFFFF&
         Caption         =   "Main Menu"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   13.5
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00808000&
         Height          =   495
         Index           =   1
         Left            =   480
         TabIndex        =   3
         Top             =   240
         Width           =   3015
      End
   End
   Begin VB.Shape Shape1 
      BackColor       =   &H00404000&
      BorderColor     =   &H00808000&
      BorderWidth     =   4
      Height          =   2295
      Left            =   7080
      Top             =   1920
      Width           =   3975
   End
   Begin VB.Image Image2 
      Height          =   2055
      Left            =   7200
      Picture         =   "MAINMENU.frx":0000
      Stretch         =   -1  'True
      Top             =   2040
      Width           =   3735
   End
   Begin VB.Label Label3 
      AutoSize        =   -1  'True
      BackColor       =   &H00808000&
      BackStyle       =   0  'Transparent
      Caption         =   "ONYX Student Information System"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Times New Roman"
         Size            =   24
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   -1  'True
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00808000&
      Height          =   540
      Left            =   1800
      TabIndex        =   1
      Top             =   480
      Width           =   6930
   End
   Begin VB.Label Label2 
      AutoSize        =   -1  'True
      Caption         =   " Gwinnett Technical Institute "
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Times New Roman"
         Size            =   24
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   -1  'True
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00808000&
      Height          =   540
      Left            =   240
      TabIndex        =   0
      Top             =   0
      Width           =   5865
   End
   Begin VB.Line Line2 
      BorderColor     =   &H00808080&
      X1              =   0
      X2              =   12000
      Y1              =   1440
      Y2              =   1440
   End
   Begin VB.Line Line1 
      BorderColor     =   &H00FFFFFF&
      X1              =   0
      X2              =   12000
      Y1              =   1320
      Y2              =   1320
   End
End
Attribute VB_Name = "frmMainMenu"
Attribute VB_Creatable = False
Attribute VB_Exposed = False
Private Sub cmdMainMenu_Click(Index As Integer)
    Select Case Index
        Case 0
           
            If Trim(cmdMainMenu(0).Caption) = "&STUDENT" Then
                ' Call Student Entry Point
                Load frmSSSNumber
                frmSSSNumber.Show
                frmMainMenu.Hide
                '
            Else
                ' Call the Report Switch Board
                Load frmReports
                frmReports.Show
                frmMainMenu.Hide
                '
            End If
                
        Case 1
            
            If Trim(cmdMainMenu(1).Caption) = "&INSTRUCTOR" Then
                ' Setup the new menu
                Call InstuctorMenu
                '
            Else
                'Load frmConstruction
                'frmConstruction.Show
                'Load frmInstructor
                'frmInstructor.Show
                '
            End If
                
        Case 2
            
            If Trim(cmdMainMenu(2).Caption) = "&CLOSE MENU" Then
                ' Setup the new menu
                Call ToggleInstuctorMenu
                '
            Else
                ' Terminate the program
                End
                '
            End If
                   
    End Select
End Sub

Private Sub InstuctorMenu()
    lblMainMenu(1) = "Instructor Menu"
    cmdMainMenu(0).Caption = "&REPORT MENU"
    cmdMainMenu(1).Caption = "&STUDENT MAINTENANCE"
    cmdMainMenu(2).Caption = "&CLOSE MENU"

End Sub
Private Sub ToggleInstuctorMenu()
    lblMainMenu(1) = "Main Menu"
    cmdMainMenu(0).Caption = "&STUDENT"
    cmdMainMenu(1).Caption = "&INSTRUCTOR"
    cmdMainMenu(2).Caption = "&EXIT"

End Sub

Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)
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
End Sub
