VERSION 4.00
Begin VB.Form frmSelect_Rec 
   Caption         =   "Multiple Student Records Report"
   ClientHeight    =   4635
   ClientLeft      =   1845
   ClientTop       =   2940
   ClientWidth     =   6690
   ControlBox      =   0   'False
   BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
      Name            =   "MS Sans Serif"
      Size            =   9.75
      Charset         =   0
      Weight          =   400
      Underline       =   0   'False
      Italic          =   0   'False
      Strikethrough   =   0   'False
   EndProperty
   Height          =   5325
   Left            =   1785
   LinkTopic       =   "Form1"
   MDIChild        =   -1  'True
   ScaleHeight     =   4635
   ScaleWidth      =   6690
   Top             =   2310
   Width           =   6810
   Begin VB.TextBox txtRec10 
      Appearance      =   0  'Flat
      BackColor       =   &H00C0C0C0&
      BorderStyle     =   0  'None
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   360
      MaxLength       =   9
      TabIndex        =   9
      Top             =   4080
      Width           =   1695
   End
   Begin VB.TextBox txtRec9 
      Appearance      =   0  'Flat
      BackColor       =   &H00C0C0C0&
      BorderStyle     =   0  'None
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   360
      MaxLength       =   9
      TabIndex        =   8
      Top             =   3720
      Width           =   1695
   End
   Begin VB.TextBox txtRec8 
      Appearance      =   0  'Flat
      BackColor       =   &H00C0C0C0&
      BorderStyle     =   0  'None
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   360
      MaxLength       =   9
      TabIndex        =   7
      Top             =   3360
      Width           =   1695
   End
   Begin VB.TextBox txtRec7 
      Appearance      =   0  'Flat
      BackColor       =   &H00C0C0C0&
      BorderStyle     =   0  'None
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   360
      MaxLength       =   9
      TabIndex        =   6
      Top             =   3000
      Width           =   1695
   End
   Begin VB.TextBox txtRec6 
      Appearance      =   0  'Flat
      BackColor       =   &H00C0C0C0&
      BorderStyle     =   0  'None
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   360
      MaxLength       =   9
      TabIndex        =   5
      Top             =   2640
      Width           =   1695
   End
   Begin VB.TextBox txtRec5 
      Appearance      =   0  'Flat
      BackColor       =   &H00C0C0C0&
      BorderStyle     =   0  'None
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   360
      MaxLength       =   9
      TabIndex        =   4
      Top             =   2280
      Width           =   1695
   End
   Begin VB.TextBox txtRec4 
      Appearance      =   0  'Flat
      BackColor       =   &H00C0C0C0&
      BorderStyle     =   0  'None
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   360
      MaxLength       =   9
      TabIndex        =   3
      Top             =   1920
      Width           =   1695
   End
   Begin VB.TextBox txtRec3 
      Appearance      =   0  'Flat
      BackColor       =   &H00C0C0C0&
      BorderStyle     =   0  'None
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   360
      MaxLength       =   9
      TabIndex        =   2
      Top             =   1560
      Width           =   1695
   End
   Begin VB.TextBox txtRec2 
      Appearance      =   0  'Flat
      BackColor       =   &H00C0C0C0&
      BorderStyle     =   0  'None
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   360
      MaxLength       =   9
      TabIndex        =   1
      Top             =   1200
      Width           =   1695
   End
   Begin VB.TextBox txtRec1 
      Appearance      =   0  'Flat
      BorderStyle     =   0  'None
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   360
      MaxLength       =   9
      TabIndex        =   0
      Top             =   840
      Width           =   1695
   End
   Begin VB.CommandButton Command2 
      Caption         =   "&Cancel"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   4560
      TabIndex        =   11
      Top             =   840
      Width           =   1095
   End
   Begin VB.CommandButton cmdRunReport 
      Caption         =   "&Run Report"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   3120
      TabIndex        =   10
      Top             =   840
      Width           =   1095
   End
   Begin VB.Label lblEnterSS 
      Alignment       =   2  'Center
      BackColor       =   &H00808000&
      BackStyle       =   0  'Transparent
      Caption         =   "Enter Social Security Numbers  :  "
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00C00000&
      Height          =   255
      Left            =   360
      TabIndex        =   12
      Top             =   360
      Width           =   3375
   End
   Begin VB.Menu mnuBack 
      Caption         =   "&Back"
   End
   Begin VB.Menu mnuExit 
      Caption         =   "E&xit"
   End
End
Attribute VB_Name = "frmSelect_Rec"
Attribute VB_Creatable = False
Attribute VB_Exposed = False
Option Explicit
Private Sub cmdRunReport_Click()

'Print Multiple Records Report
Multiple_Rec_rep

End Sub


Private Sub cmdRun_Report_Click()

End Sub


Private Sub Command2_Click()

frmSelect_Rec.Hide
frmReports.Show

End Sub


Private Sub Form_Load()

' Center Form On Screen
  CenterForm Me
  
End Sub


Private Sub mnuBack_Click()

frmSelect_Rec.Hide
frmReports.Show

End Sub

Private Sub mnuExit_Click()

Exit_Program

End Sub


Private Sub txtRec1_KeyPress(KeyAscii As Integer)

If txtRec1.Text <> "" Then
txtRec2.Enabled = True
txtRec2.BackColor = &HFFFFFF

k = 1

End If


If KeyAscii = 13 Then

    
    frmSelect_Rec.txtRec2.SetFocus

    End If
    
    
End Sub







Private Sub txtRec10_Change()

If txtRec2.Text <> "" Then

k = 10

End If


End Sub

Private Sub txtRec10_KeyPress(KeyAscii As Integer)

If KeyAscii = 13 Then
    

       
    cmdRunReport.SetFocus
        

End If


End Sub


Private Sub txtRec2_Change()

If txtRec2.Text <> "" Then
txtRec3.Enabled = True
txtRec3.BackColor = &HFFFFFF

k = 2

End If


End Sub


Private Sub txtRec2_KeyPress(KeyAscii As Integer)


If KeyAscii = 13 Then

If txtRec2.Text <> "" Then
txtRec3.Enabled = True
txtRec3.BackColor = &HFFFFFF
frmSelect_Rec.txtRec3.SetFocus

Else

  cmdRunReport.SetFocus
    
End If

End If


 End Sub

Private Sub txtRec3_Change()

If txtRec3.Text <> "" Then
txtRec4.Enabled = True
txtRec4.BackColor = &HFFFFFF

k = 3

End If




End Sub


Sub ValiText()

'Function ValiText(KeyIn As Integer,
 Dim ValidateString As String
 Dim Editable As Boolean
   
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


End Function

Private Sub txtRec3_KeyPress(KeyAscii As Integer)

If KeyAscii = 13 Then
 
If txtRec3.Text <> "" Then
txtRec4.Enabled = True
txtRec4.BackColor = &HFFFFFF
frmSelect_Rec.txtRec4.SetFocus

Else

  cmdRunReport.SetFocus
    
End If
   
   
End If

End Sub

Private Sub txtRec4_Change()

If txtRec4.Text <> "" Then
txtRec5.Enabled = True
txtRec5.BackColor = &HFFFFFF

k = 4

End If




End Sub


Private Sub txtRec4_KeyPress(KeyAscii As Integer)

If KeyAscii = 13 Then
    
 If txtRec4.Text <> "" Then
    txtRec5.Enabled = True
    txtRec5.BackColor = &HFFFFFF
    frmSelect_Rec.txtRec5.SetFocus

    Else

    cmdRunReport.SetFocus
    
    End If
    
End If

End Sub


Private Sub txtRec5_Change()

If txtRec5.Text <> "" Then
txtRec6.Enabled = True
txtRec6.BackColor = &HFFFFFF

k = 5

End If





End Sub


Private Sub txtRec5_KeyPress(KeyAscii As Integer)

If KeyAscii = 13 Then
    
    If txtRec5.Text <> "" Then
        txtRec6.Enabled = True
        txtRec6.BackColor = &HFFFFFF
        frmSelect_Rec.txtRec6.SetFocus

    Else

        cmdRunReport.SetFocus
    
    End If
    
End If

End Sub


Private Sub txtRec6_Change()

If txtRec6.Text <> "" Then
txtRec7.Enabled = True
txtRec7.BackColor = &HFFFFFF

k = 6

End If



End Sub


Private Sub txtRec6_KeyPress(KeyAscii As Integer)

If KeyAscii = 13 Then
    
    If txtRec6.Text <> "" Then
    
        txtRec7.Enabled = True
        txtRec7.BackColor = &HFFFFFF
        frmSelect_Rec.txtRec7.SetFocus

    Else

    cmdRunReport.SetFocus
    
    End If
    

End If

End Sub


Private Sub txtRec7_Change()

If txtRec7.Text <> "" Then
txtRec8.Enabled = True
txtRec8.BackColor = &HFFFFFF

k = 7

End If



End Sub


Private Sub txtRec7_KeyPress(KeyAscii As Integer)

If KeyAscii = 13 Then
  
  If txtRec7.Text <> "" Then
    
        txtRec8.Enabled = True
        txtRec8.BackColor = &HFFFFFF
        frmSelect_Rec.txtRec8.SetFocus

    Else

    cmdRunReport.SetFocus
    
    
End If

End If

End Sub


Private Sub txtRec8_Change()

If txtRec8.Text <> "" Then
txtRec9.Enabled = True
txtRec9.BackColor = &HFFFFFF

k = 8

End If



End Sub


Private Sub txtRec8_KeyPress(KeyAscii As Integer)

If KeyAscii = 13 Then
    
 If txtRec8.Text <> "" Then
    
        txtRec9.Enabled = True
        txtRec9.BackColor = &HFFFFFF
        frmSelect_Rec.txtRec9.SetFocus

    Else

  
    cmdRunReport.SetFocus
      
  End If
      
End If


End Sub


Private Sub txtRec9_Change()

If txtRec9.Text <> "" Then
txtRec10.Enabled = True
txtRec10.BackColor = &HFFFFFF

k = 9

End If




End Sub


Private Sub txtRec9_KeyPress(KeyAscii As Integer)

If KeyAscii = 13 Then
    
 If txtRec9.Text <> "" Then
    
        txtRec10.Enabled = True
        txtRec10.BackColor = &HFFFFFF
        frmSelect_Rec.txtRec10.SetFocus

    Else

    cmdRunReport.SetFocus
    
End If

End If

End Sub


