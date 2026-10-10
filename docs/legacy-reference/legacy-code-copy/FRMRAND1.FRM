VERSION 4.00
Begin VB.Form frmRandom 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "View Student Social Security"
   ClientHeight    =   3510
   ClientLeft      =   3525
   ClientTop       =   4455
   ClientWidth     =   6900
   ControlBox      =   0   'False
   Height          =   4200
   Left            =   3465
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MDIChild        =   -1  'True
   MinButton       =   0   'False
   ScaleHeight     =   3510
   ScaleWidth      =   6900
   ShowInTaskbar   =   0   'False
   Top             =   3825
   Width           =   7020
   Begin VB.CommandButton cmdPrintAll 
      Caption         =   "Print &All"
      Height          =   375
      Left            =   2880
      TabIndex        =   4
      Top             =   2640
      Width           =   1215
   End
   Begin VB.CommandButton cmdNext 
      Caption         =   ">>"
      Height          =   330
      Left            =   3600
      TabIndex        =   3
      Top             =   2220
      Width           =   1380
   End
   Begin VB.CommandButton cmdPrevious 
      Caption         =   "<<"
      Height          =   330
      Left            =   1440
      TabIndex        =   2
      Top             =   2160
      Width           =   1380
   End
   Begin VB.TextBox txtSS 
      Alignment       =   2  'Center
      BorderStyle     =   0  'None
      Enabled         =   0   'False
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   360
      Left            =   3720
      TabIndex        =   1
      Text            =   "Text1"
      Top             =   960
      Width           =   1575
   End
   Begin VB.Label Label1 
      Caption         =   "Social Security No."
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00800000&
      Height          =   345
      Left            =   1200
      TabIndex        =   0
      Top             =   960
      Width           =   2175
   End
   Begin VB.Menu mnuPrint 
      Caption         =   "&Print "
      Begin VB.Menu mnuAll 
         Caption         =   "&All"
      End
      Begin VB.Menu mnuThisRecord 
         Caption         =   "&This Record"
      End
   End
   Begin VB.Menu mnuReturn 
      Caption         =   "&Back"
   End
   Begin VB.Menu mnuExit 
      Caption         =   "E&xit"
   End
End
Attribute VB_Name = "frmRandom"
Attribute VB_Creatable = False
Attribute VB_Exposed = False
Option Explicit



Private Sub cmdNext_Click()
    
   Display_Next
        
End Sub

Private Sub cmdPrevious_Click()
   
   Display_Previous
        
End Sub


Private Sub cmdPrintAll_Click()
    
    Print_All_SS

End Sub

Private Sub Form_Unload(Cancel As Integer)
   
 'Center Form On Screen
  CenterForm Me

End Sub

      


Private Sub mnuAll_Click()

    Print_All_SS

End Sub

Private Sub mnuExit_Click()
    
 
    Exit_Program


End Sub
    



Private Sub mnuReturn_Click()

    frmRandom.Hide
    
    Close #1
    
    frmReports.Show

End Sub


Private Sub mnuThisRecord_Click()

    Print_Current

End Sub


