VERSION 4.00
Begin VB.Form frmEmployment 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Company Information"
   ClientHeight    =   4575
   ClientLeft      =   3135
   ClientTop       =   2595
   ClientWidth     =   8280
   ClipControls    =   0   'False
   ControlBox      =   0   'False
   Height          =   5265
   Left            =   3075
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MDIChild        =   -1  'True
   MinButton       =   0   'False
   ScaleHeight     =   4575
   ScaleWidth      =   8280
   ShowInTaskbar   =   0   'False
   Top             =   1965
   Width           =   8400
   Begin VB.PictureBox Picture1 
      BackColor       =   &H00808000&
      Height          =   2805
      Left            =   360
      ScaleHeight     =   2745
      ScaleWidth      =   7545
      TabIndex        =   3
      Top             =   840
      Width           =   7605
      Begin VB.TextBox txtCompany_Code 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         Height          =   285
         Left            =   1680
         TabIndex        =   30
         Top             =   120
         Width           =   1335
      End
      Begin VB.TextBox txtState 
         Appearance      =   0  'Flat
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
         Height          =   285
         Left            =   3120
         TabIndex        =   16
         Top             =   1200
         Width           =   495
      End
      Begin VB.TextBox txtCompany_Name 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         Height          =   285
         Left            =   1680
         TabIndex        =   15
         Top             =   480
         Width           =   5655
      End
      Begin VB.TextBox txtAddress 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         Height          =   285
         Left            =   1680
         TabIndex        =   14
         Top             =   840
         Width           =   5655
      End
      Begin VB.TextBox txtCity 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         Height          =   285
         Left            =   600
         TabIndex        =   13
         Top             =   1200
         Width           =   1815
      End
      Begin VB.TextBox txtZip 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         Height          =   285
         Left            =   4200
         TabIndex        =   12
         Top             =   1200
         Width           =   975
      End
      Begin VB.TextBox txtJob_Title 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         Height          =   285
         Left            =   960
         TabIndex        =   11
         Top             =   1560
         Width           =   2895
      End
      Begin VB.TextBox txtCurrent_Supervisor 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         Height          =   285
         Left            =   5040
         TabIndex        =   10
         Top             =   1560
         Width           =   2295
      End
      Begin VB.TextBox txtPhone_Number 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         Height          =   285
         Left            =   6000
         TabIndex        =   9
         Top             =   1200
         Width           =   1335
      End
      Begin VB.TextBox txtCompanyType 
         Height          =   285
         Left            =   1800
         TabIndex        =   8
         Text            =   "Environmental Protection Air"
         Top             =   5040
         Width           =   4215
      End
      Begin VB.TextBox txtHours_per_Week 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         Height          =   285
         Left            =   1440
         TabIndex        =   7
         Top             =   1920
         Width           =   375
      End
      Begin VB.TextBox txtAmount 
         Height          =   285
         Left            =   1800
         TabIndex        =   6
         Text            =   "15.00"
         Top             =   4560
         Width           =   1455
      End
      Begin VB.TextBox txtAmoun 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         Height          =   285
         Left            =   3360
         TabIndex        =   5
         Top             =   1920
         Width           =   975
      End
      Begin VB.TextBox txtCompany_Type 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         Height          =   285
         Left            =   1680
         TabIndex        =   4
         Top             =   2280
         Width           =   3735
      End
      Begin VB.Label Label4 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Company Code "
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   0
         TabIndex        =   31
         Top             =   120
         Width           =   1455
      End
      Begin VB.Label Label2 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Hourly Rate"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   2160
         TabIndex        =   29
         Top             =   1920
         Width           =   1095
      End
      Begin VB.Label Label32 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Company Name "
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   0
         TabIndex        =   28
         Top             =   480
         Width           =   1455
      End
      Begin VB.Label Label31 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Address "
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   0
         TabIndex        =   27
         Top             =   840
         Width           =   1575
      End
      Begin VB.Label Label30 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "City"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   -120
         TabIndex        =   26
         Top             =   1200
         Width           =   615
      End
      Begin VB.Label Label29 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "JobTitle"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   -120
         TabIndex        =   25
         Top             =   1560
         Width           =   975
      End
      Begin VB.Label Label28 
         Alignment       =   1  'Right Justify
         BackStyle       =   0  'Transparent
         Caption         =   "Supervisor "
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   3840
         TabIndex        =   24
         Top             =   1560
         Width           =   1095
      End
      Begin VB.Label Label27 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Phone"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   5160
         TabIndex        =   23
         Top             =   1200
         Width           =   735
      End
      Begin VB.Label Label26 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "State"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   2280
         TabIndex        =   22
         Top             =   1200
         Width           =   735
      End
      Begin VB.Label Label25 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Zip"
         DataField       =   " "
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   3600
         TabIndex        =   21
         Top             =   1200
         Width           =   495
      End
      Begin VB.Label Label24 
         BackColor       =   &H00808000&
         Caption         =   "Hours/ Week"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   120
         TabIndex        =   20
         Top             =   1920
         Width           =   1575
      End
      Begin VB.Label Label22 
         Caption         =   "            A&mount :"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   240
         TabIndex        =   19
         Top             =   4560
         Width           =   1575
      End
      Begin VB.Label Label1 
         Caption         =   "  Company &Type :"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   240
         TabIndex        =   18
         Top             =   5040
         Width           =   1575
      End
      Begin VB.Label Label34 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Company Type"
         BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   0
         TabIndex        =   17
         Top             =   2280
         Width           =   1455
      End
   End
   Begin VB.CommandButton cmdNext 
      Caption         =   ">>"
      Height          =   330
      Left            =   4440
      TabIndex        =   2
      Top             =   3840
      Width           =   1380
   End
   Begin VB.CommandButton cmdPrevious 
      Caption         =   "<<"
      Height          =   330
      Left            =   2640
      TabIndex        =   1
      Top             =   3840
      Width           =   1380
   End
   Begin VB.Label Label3 
      Caption         =   "EMPLOYMENT INFORMATION"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "Times New Roman"
         Size            =   15.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00800000&
      Height          =   375
      Left            =   1680
      TabIndex        =   0
      Top             =   240
      Width           =   4815
   End
   Begin VB.Menu mnuBack 
      Caption         =   "&Back"
   End
   Begin VB.Menu mnuPrint 
      Caption         =   "&Print"
   End
   Begin VB.Menu mnuExit 
      Caption         =   "E&xit"
   End
End
Attribute VB_Name = "frmEmployment"
Attribute VB_Creatable = False
Attribute VB_Exposed = False
Private Sub cmdNext_Click()

Display_Next_4

End Sub

Private Sub cmdPrevious_Click()

    Display_Previous_4

End Sub

Private Sub Form_Load()

' Center Form On Screen
  CenterForm Me


End Sub

Private Sub mnuBack_Click()

frmEmployment.Hide
frmReports.Show

End Sub

Private Sub mnuExit_Click()

Exit_Program

End Sub


