VERSION 4.00
Begin VB.Form frmConstruction 
   BackColor       =   &H00FFFFFF&
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Construction"
   ClientHeight    =   960
   ClientLeft      =   1575
   ClientTop       =   1515
   ClientWidth     =   4680
   ControlBox      =   0   'False
   ForeColor       =   &H00FFFFFF&
   Height          =   1365
   Left            =   1515
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Picture         =   "frmconst.frx":0000
   ScaleHeight     =   960
   ScaleWidth      =   4680
   ShowInTaskbar   =   0   'False
   Top             =   1170
   Width           =   4800
   Begin VB.PictureBox imgConstruction 
      Appearance      =   0  'Flat
      AutoRedraw      =   -1  'True
      AutoSize        =   -1  'True
      BackColor       =   &H00FFFF80&
      BorderStyle     =   0  'None
      ForeColor       =   &H80000008&
      Height          =   1005
      Left            =   -120
      ScaleHeight     =   1005
      ScaleWidth      =   1005
      TabIndex        =   1
      Top             =   0
      Width           =   1005
   End
   Begin VB.Timer Timer1 
      Interval        =   200
      Left            =   1320
      Top             =   -120
   End
   Begin VB.Timer tmrConstruction 
      Interval        =   10000
      Left            =   3360
      Top             =   480
   End
   Begin VB.Image const2 
      Height          =   1020
      Left            =   -120
      Picture         =   "frmconst.frx":0BA6
      Top             =   0
      Width           =   960
   End
   Begin VB.Image const1 
      Height          =   975
      Left            =   -122
      Picture         =   "frmconst.frx":3EEA
      Top             =   0
      Width           =   915
   End
   Begin VB.Label Label1 
      AutoSize        =   -1  'True
      BackColor       =   &H00FFFFFF&
      Caption         =   "Still under construction !!"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Times New Roman"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   270
      Left            =   960
      TabIndex        =   0
      Top             =   240
      Width           =   3015
   End
End
Attribute VB_Name = "frmConstruction"
Attribute VB_Creatable = False
Attribute VB_Exposed = False
Option Explicit
Dim digging As Integer

Private Sub Construction()
    ' Alternate between the two bitmaps.
    If digging = 0 Then
        imgConstruction.Picture = const2.Picture
        digging = 1
    Else
        imgConstruction.Picture = const1.Picture
        digging = 0
    End If
End Sub

Private Sub Form_Load()
    Me.ZOrder 0
End Sub

Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)
    Unload frmConstruction
    Set frmConstruction = Nothing
End Sub

Private Sub Timer1_Timer()
 Call Construction
End Sub


Private Sub tmrConstruction_Timer()
   
Timer1.Enabled = False
tmrConstruction.Enabled = False
Unload frmConstruction
Set frmConstruction = Nothing

End Sub


