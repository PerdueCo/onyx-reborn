VERSION 4.00
Begin VB.Form frmPrintSS 
   Caption         =   "Student Report"
   ClientHeight    =   5385
   ClientLeft      =   1740
   ClientTop       =   3375
   ClientWidth     =   9660
   ControlBox      =   0   'False
   BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
      Name            =   "Courier New"
      Size            =   8.25
      Charset         =   0
      Weight          =   400
      Underline       =   0   'False
      Italic          =   0   'False
      Strikethrough   =   0   'False
   EndProperty
   Height          =   6075
   Left            =   1680
   LinkTopic       =   "Form1"
   MDIChild        =   -1  'True
   ScaleHeight     =   5385
   ScaleWidth      =   9660
   Top             =   2745
   Width           =   9780
   Begin VB.Menu mnuReturn 
      Caption         =   "&Back"
   End
   Begin VB.Menu mnuExit 
      Caption         =   "E&xit"
   End
End
Attribute VB_Name = "frmPrintSS"
Attribute VB_Creatable = False
Attribute VB_Exposed = False
Option Explicit

Private Sub cmdExit_Click()

    End

End Sub


Private Sub Command1_Click()




End Sub

Private Sub cmdReturn_Click()
 
    frmPrintSS.Cls
    frmPrintSS.Hide
    frmRandom.Show
   

End Sub

Private Sub Form_Load()

' Center Form On Screen
  CenterForm Me

End Sub

Private Sub mnuExit_Click()

    Exit_Program

End Sub


Private Sub mnuReturn_Click()

    frmPrintSS.Cls
    frmPrintSS.Hide
    frmReports.Show

End Sub


