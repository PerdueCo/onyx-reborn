VERSION 4.00
Begin VB.Form frmSplash 
   BackColor       =   &H8000000E&
   BorderStyle     =   0  'None
   Caption         =   "Splash"
   ClientHeight    =   5340
   ClientLeft      =   2220
   ClientTop       =   2835
   ClientWidth     =   7425
   Height          =   5745
   Left            =   2160
   LinkTopic       =   "Form1"
   ScaleHeight     =   5340
   ScaleWidth      =   7425
   ShowInTaskbar   =   0   'False
   Top             =   2490
   Width           =   7545
   Begin VB.Timer Timer1 
      Interval        =   7000
      Left            =   1800
      Top             =   2160
   End
   Begin VB.Shape Shape1 
      BorderWidth     =   2
      Height          =   5320
      Left            =   0
      Top             =   10
      Width           =   7425
   End
   Begin VB.Label lblStopSplash 
      BackStyle       =   0  'Transparent
      Height          =   5415
      Left            =   0
      TabIndex        =   13
      Top             =   0
      Width           =   7215
   End
   Begin VB.Label Label10 
      BackStyle       =   0  'Transparent
      Caption         =   "I"
      BeginProperty Font 
         name            =   "Arial"
         charset         =   1
         weight          =   700
         size            =   36
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00800000&
      Height          =   975
      Index           =   2
      Left            =   2160
      TabIndex        =   12
      Top             =   3360
      Width           =   615
   End
   Begin VB.Label Label10 
      BackStyle       =   0  'Transparent
      Caption         =   "S"
      BeginProperty Font 
         name            =   "Arial"
         charset         =   1
         weight          =   700
         size            =   36
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00800000&
      Height          =   975
      Index           =   1
      Left            =   1560
      TabIndex        =   11
      Top             =   3360
      Width           =   615
   End
   Begin VB.Label Label11 
      BackStyle       =   0  'Transparent
      Caption         =   "S"
      BeginProperty Font 
         name            =   "Arial"
         charset         =   1
         weight          =   700
         size            =   36
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00800000&
      Height          =   975
      Left            =   960
      TabIndex        =   10
      Top             =   3360
      Width           =   615
   End
   Begin VB.Label Label10 
      BackStyle       =   0  'Transparent
      Caption         =   "B"
      BeginProperty Font 
         name            =   "Arial"
         charset         =   1
         weight          =   700
         size            =   36
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00800000&
      Height          =   975
      Index           =   0
      Left            =   360
      TabIndex        =   9
      Top             =   3360
      Width           =   615
   End
   Begin VB.Label Label7 
      AutoSize        =   -1  'True
      BackStyle       =   0  'Transparent
      Caption         =   "What's Possible Today"
      BeginProperty Font 
         name            =   "Times New Roman"
         charset         =   1
         weight          =   700
         size            =   12
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      Height          =   285
      Left            =   4575
      TabIndex        =   6
      Top             =   2385
      Width           =   2280
   End
   Begin VB.Label Label6 
      BackStyle       =   0  'Transparent
      Caption         =   "Gwinnett Tech"
      BeginProperty Font 
         name            =   "Times New Roman"
         charset         =   1
         weight          =   400
         size            =   36
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00400000&
      Height          =   735
      Left            =   2760
      TabIndex        =   5
      Top             =   1600
      Width           =   4455
   End
   Begin VB.Label Label4 
      BackStyle       =   0  'Transparent
      Caption         =   $"SPLASH~1.frx":0000
      BeginProperty Font 
         name            =   "Times New Roman"
         charset         =   1
         weight          =   700
         size            =   11.25
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      Height          =   615
      Left            =   360
      TabIndex        =   4
      Top             =   4560
      Width           =   6495
   End
   Begin VB.Label Label5 
      BackStyle       =   0  'Transparent
      BeginProperty Font 
         name            =   "Times New Roman"
         charset         =   1
         weight          =   400
         size            =   9
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      Height          =   255
      Left            =   360
      TabIndex        =   3
      Top             =   5280
      Width           =   3735
   End
   Begin VB.Image Image1 
      Height          =   1670
      Left            =   4560
      Picture         =   "SPLASH~1.frx":0051
      Stretch         =   -1  'True
      Top             =   2760
      Width           =   2505
   End
   Begin VB.Label Label3 
      BackColor       =   &H00800000&
      Caption         =   "  Information Management System"
      BeginProperty Font 
         name            =   "Times New Roman"
         charset         =   1
         weight          =   700
         size            =   21.75
         underline       =   0   'False
         italic          =   -1  'True
         strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H8000000E&
      Height          =   615
      Left            =   0
      TabIndex        =   2
      Top             =   600
      Width           =   7455
   End
   Begin VB.Label Label2 
      BackColor       =   &H00004000&
      Caption         =   "Label2"
      Height          =   615
      Left            =   0
      TabIndex        =   1
      Top             =   600
      Width           =   7455
   End
   Begin VB.Label Label1 
      BackColor       =   &H00808000&
      BeginProperty Font 
         name            =   "Arial"
         charset         =   1
         weight          =   700
         size            =   27.75
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      Height          =   615
      Left            =   0
      TabIndex        =   0
      Top             =   0
      Width           =   7455
   End
   Begin VB.Label Label8 
      BackStyle       =   0  'Transparent
      Caption         =   "Gwinnett Tech"
      BeginProperty Font 
         name            =   "Times New Roman"
         charset         =   1
         weight          =   400
         size            =   36
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00C0C000&
      Height          =   735
      Left            =   2780
      TabIndex        =   7
      Top             =   1600
      Width           =   4815
   End
   Begin VB.Label Label9 
      AutoSize        =   -1  'True
      BackStyle       =   0  'Transparent
      Caption         =   "What's Possible Today"
      BeginProperty Font 
         name            =   "Times New Roman"
         charset         =   1
         weight          =   700
         size            =   12
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00808000&
      Height          =   285
      Left            =   4560
      TabIndex        =   8
      Top             =   2400
      Width           =   2280
   End
End
Attribute VB_Name = "frmSplash"
Attribute VB_Creatable = False
Attribute VB_Exposed = False


Option Explicit

Private Sub Form_Load()
'Center the form on the screen
    
    'Top Offset for form centering
    frmSplash.Top = (Screen.Height - frmSplash.Height) / 2
    
    'Left Offset for form centering
    frmSplash.Left = (Screen.Width - frmSplash.Width) / 2
    
End Sub

Private Sub Frame1_DragDrop(Source As Control, X As Single, Y As Single)

End Sub

Private Sub lblStopSplash_Click()
'Terminates the splash screen

    Timer1.Enabled = False
    
    ' unload the splash screen and free it's memory
    Unload frmSplash
    Set frmSplash = Nothing

    'Load mdiBackGround
    'mdiBackGround.Show
    ' Launch the main menu
    Load frmMainMenu
    
    frmMainMenu.Show
    frmMainMenu.ZOrder 0
    frmMainMenu.Refresh
End Sub
Private Sub Timer1_Timer()
'Terminates the splash screen

    Timer1.Enabled = False
    
    ' unload the splash screen and free it's memory
    Unload frmSplash
    Set frmSplash = Nothing

    Load mdiBackGround
    mdiBackGround.Show
End Sub



