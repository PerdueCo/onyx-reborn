VERSION 4.00
Begin VB.Form frmSearch 
   BackColor       =   &H00808000&
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Find/Display Student Record"
   ClientHeight    =   7170
   ClientLeft      =   2415
   ClientTop       =   2400
   ClientWidth     =   7890
   ControlBox      =   0   'False
   Height          =   7860
   Left            =   2355
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MDIChild        =   -1  'True
   MinButton       =   0   'False
   ScaleHeight     =   7170
   ScaleWidth      =   7890
   ShowInTaskbar   =   0   'False
   Top             =   1770
   Width           =   8010
   Begin VB.PictureBox Picture1 
      BackColor       =   &H00808000&
      Height          =   2445
      Left            =   120
      ScaleHeight     =   2415
      ScaleWidth      =   7575
      TabIndex        =   48
      Top             =   4560
      Width           =   7605
      Begin VB.TextBox txtCompany_Type 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1680
         TabIndex        =   73
         Top             =   1920
         Width           =   3735
      End
      Begin VB.TextBox txtAmoun 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   3480
         TabIndex        =   72
         Top             =   1560
         Width           =   975
      End
      Begin VB.TextBox txtAmount 
         Height          =   285
         Left            =   1800
         TabIndex        =   59
         Text            =   "15.00"
         Top             =   4560
         Width           =   1455
      End
      Begin VB.TextBox txtHours_Per_Week 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1440
         TabIndex        =   58
         Top             =   1560
         Width           =   375
      End
      Begin VB.TextBox txtCompanyType 
         Height          =   285
         Left            =   1800
         TabIndex        =   57
         Text            =   "Environmental Protection Air"
         Top             =   5040
         Width           =   4215
      End
      Begin VB.TextBox txtPhone_Number 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   5760
         TabIndex        =   56
         Top             =   840
         Width           =   1575
      End
      Begin VB.TextBox txtCurrent_Supervisor 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   5040
         TabIndex        =   55
         Top             =   1200
         Width           =   2295
      End
      Begin VB.TextBox txtJob_Title 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   960
         TabIndex        =   54
         Top             =   1200
         Width           =   2895
      End
      Begin VB.TextBox txtZip_E 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   4080
         TabIndex        =   53
         Top             =   840
         Width           =   975
      End
      Begin VB.TextBox txtCity_E 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   600
         TabIndex        =   52
         Top             =   840
         Width           =   1815
      End
      Begin VB.TextBox txtAddress_E 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1680
         TabIndex        =   51
         Top             =   480
         Width           =   5655
      End
      Begin VB.TextBox txtCompany_Name 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1680
         TabIndex        =   50
         Top             =   120
         Width           =   5655
      End
      Begin VB.TextBox txtSTate_E 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   3000
         TabIndex        =   49
         Top             =   840
         Width           =   495
      End
      Begin VB.Label Label34 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Company Type"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   0
         TabIndex        =   74
         Top             =   1920
         Width           =   1455
      End
      Begin VB.Label Label3 
         Caption         =   "  Company &Type :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   240
         TabIndex        =   71
         Top             =   5040
         Width           =   1575
      End
      Begin VB.Label Label22 
         Caption         =   "            A&mount :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   240
         TabIndex        =   70
         Top             =   4560
         Width           =   1575
      End
      Begin VB.Label Label24 
         BackColor       =   &H00808000&
         Caption         =   "Hours/ Week"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   120
         TabIndex        =   69
         Top             =   1560
         Width           =   1575
      End
      Begin VB.Label Label25 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Zip"
         DataField       =   " "
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   3480
         TabIndex        =   68
         Top             =   840
         Width           =   495
      End
      Begin VB.Label Label26 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "State"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   2160
         TabIndex        =   67
         Top             =   840
         Width           =   735
      End
      Begin VB.Label Label27 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Phone"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   4920
         TabIndex        =   66
         Top             =   840
         Width           =   735
      End
      Begin VB.Label Label28 
         Alignment       =   1  'Right Justify
         BackStyle       =   0  'Transparent
         Caption         =   "Supervisor "
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   3840
         TabIndex        =   65
         Top             =   1200
         Width           =   1095
      End
      Begin VB.Label Label29 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "JobTitle"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   -120
         TabIndex        =   64
         Top             =   1200
         Width           =   975
      End
      Begin VB.Label Label30 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "City"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   -120
         TabIndex        =   63
         Top             =   840
         Width           =   615
      End
      Begin VB.Label Label31 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Address "
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   0
         TabIndex        =   62
         Top             =   480
         Width           =   1575
      End
      Begin VB.Label Label32 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Company Name "
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   0
         TabIndex        =   61
         Top             =   120
         Width           =   1455
      End
      Begin VB.Label Label2 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Hourly Rate"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   2160
         TabIndex        =   60
         Top             =   1560
         Width           =   1095
      End
   End
   Begin VB.CommandButton cmdPrint 
      Caption         =   "Print"
      Height          =   375
      Left            =   6000
      TabIndex        =   35
      Top             =   120
      Width           =   615
   End
   Begin VB.CommandButton cmdPrevious 
      Caption         =   "<<"
      Height          =   375
      Left            =   4680
      TabIndex        =   34
      Top             =   120
      Width           =   660
   End
   Begin VB.CommandButton cmdNext 
      Caption         =   ">>"
      Height          =   375
      Left            =   5340
      TabIndex        =   33
      Top             =   120
      Width           =   660
   End
   Begin VB.PictureBox SSPanel1 
      BackColor       =   &H00808000&
      Height          =   3765
      Left            =   120
      ScaleHeight     =   3735
      ScaleWidth      =   7575
      TabIndex        =   4
      Top             =   720
      Width           =   7605
      Begin VB.TextBox txtCompany_Code 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1680
         TabIndex        =   47
         Top             =   3360
         Width           =   1215
      End
      Begin VB.TextBox txtDate_Graduated 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   6120
         TabIndex        =   40
         Top             =   2280
         Width           =   1215
      End
      Begin VB.TextBox txtMonth 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   2280
         TabIndex        =   39
         Top             =   2640
         Width           =   1095
      End
      Begin VB.TextBox txtDay 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   4200
         TabIndex        =   38
         Top             =   2640
         Width           =   495
      End
      Begin VB.TextBox txtDescription 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1680
         TabIndex        =   37
         Top             =   3000
         Width           =   3735
      End
      Begin VB.TextBox txtYesNo 
         Alignment       =   2  'Center
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Height          =   285
         Left            =   6120
         TabIndex        =   36
         Top             =   3240
         Width           =   495
      End
      Begin VB.TextBox txtSState 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   4680
         TabIndex        =   32
         Top             =   1920
         Width           =   615
      End
      Begin VB.TextBox txtProgram_Code 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   5040
         TabIndex        =   29
         Top             =   120
         Width           =   2295
      End
      Begin VB.TextBox txtSS 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1440
         TabIndex        =   28
         Top             =   120
         Width           =   1575
      End
      Begin VB.TextBox txtHigh_School 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1440
         TabIndex        =   14
         Top             =   2280
         Width           =   2295
      End
      Begin VB.TextBox txtPosition 
         Height          =   285
         Left            =   3600
         TabIndex        =   13
         Text            =   "Visual Basic Programming Certification"
         Top             =   5160
         Width           =   4215
      End
      Begin VB.TextBox txtZip 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   6120
         TabIndex        =   12
         Top             =   1920
         Width           =   1215
      End
      Begin VB.TextBox txtCity 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1440
         TabIndex        =   11
         Top             =   1920
         Width           =   2295
      End
      Begin VB.TextBox txtAddress 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1440
         TabIndex        =   10
         Top             =   1560
         Width           =   5895
      End
      Begin VB.TextBox txtWork_Phone 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   5160
         TabIndex        =   9
         Top             =   1200
         Width           =   2175
      End
      Begin VB.TextBox txtHome_Phone 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1440
         TabIndex        =   8
         Top             =   1200
         Width           =   2295
      End
      Begin VB.TextBox txtFirst_Name 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   5160
         TabIndex        =   7
         Top             =   840
         Width           =   2175
      End
      Begin VB.TextBox txtLast_Name 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1440
         TabIndex        =   6
         Top             =   840
         Width           =   2295
      End
      Begin VB.TextBox txtProgram_Name 
         Appearance      =   0  'Flat
         BorderStyle     =   0  'None
         Enabled         =   0   'False
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   9.75
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   1440
         TabIndex        =   5
         Top             =   480
         Width           =   5895
      End
      Begin VB.Label Label33 
         Alignment       =   2  'Center
         BackColor       =   &H00808000&
         Caption         =   " Are You Currently Seeking a Job ? :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   615
         Left            =   5520
         TabIndex        =   46
         Top             =   2760
         Width           =   1935
      End
      Begin VB.Label Label18 
         BackColor       =   &H00FFFFFF&
         BackStyle       =   0  'Transparent
         Caption         =   "Month  :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   1440
         TabIndex        =   45
         Top             =   2640
         Width           =   855
      End
      Begin VB.Label Label13 
         BackColor       =   &H00FFFFFF&
         BackStyle       =   0  'Transparent
         Caption         =   "  Day :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   3480
         TabIndex        =   44
         Top             =   2640
         Width           =   615
      End
      Begin VB.Label Label20 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Date Graduated  :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   4320
         TabIndex        =   43
         Top             =   2280
         Width           =   1695
      End
      Begin VB.Label Label21 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Company Type  :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   0
         TabIndex        =   42
         Top             =   3000
         Width           =   1575
      End
      Begin VB.Label Label1 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Company  Code  :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   0
         TabIndex        =   41
         Top             =   3360
         Width           =   1575
      End
      Begin VB.Label Label23 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Program  Code :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   375
         Left            =   3360
         TabIndex        =   31
         Top             =   120
         Width           =   1575
      End
      Begin VB.Label Label16 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Social   Security  :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   375
         Left            =   120
         TabIndex        =   30
         Top             =   0
         Width           =   1215
      End
      Begin VB.Label Label19 
         BackColor       =   &H00FFFFFF&
         BackStyle       =   0  'Transparent
         Caption         =   "  Day :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   3120
         TabIndex        =   27
         Top             =   2280
         Width           =   615
      End
      Begin VB.Label Label12 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Zip :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   5520
         TabIndex        =   26
         Top             =   1920
         Width           =   495
      End
      Begin VB.Label Label10 
         BackColor       =   &H00808000&
         Caption         =   "State  :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   375
         Left            =   3960
         TabIndex        =   25
         Top             =   1920
         Width           =   735
      End
      Begin VB.Label Label6 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "First Name :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   3960
         TabIndex        =   24
         Top             =   840
         Width           =   1095
      End
      Begin VB.Label Label4 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Program  :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   360
         TabIndex        =   23
         Top             =   480
         Width           =   975
      End
      Begin VB.Label Label5 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Last Name :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   120
         TabIndex        =   22
         Top             =   840
         Width           =   1215
      End
      Begin VB.Label Label7 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Work Phone :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   3840
         TabIndex        =   21
         Top             =   1200
         Width           =   1215
      End
      Begin VB.Label Label8 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00FFFFFF&
         BackStyle       =   0  'Transparent
         Caption         =   "Address  :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   120
         TabIndex        =   20
         Top             =   1560
         Width           =   1215
      End
      Begin VB.Label Label9 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "City :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   240
         TabIndex        =   19
         Top             =   1920
         Width           =   1095
      End
      Begin VB.Label Label11 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Home Phone :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   120
         TabIndex        =   18
         Top             =   1200
         Width           =   1215
      End
      Begin VB.Label Label14 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "High School :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   0
         TabIndex        =   17
         Top             =   2280
         Width           =   1335
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00FFFFFF&
         Index           =   5
         X1              =   120
         X2              =   7800
         Y1              =   4935
         Y2              =   4935
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00808080&
         Index           =   4
         X1              =   120
         X2              =   7800
         Y1              =   4920
         Y2              =   4920
      End
      Begin VB.Label Label15 
         BackStyle       =   0  'Transparent
         Caption         =   "  If Yes, What Type Of Job  Are You Applying For :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         Height          =   615
         Left            =   360
         TabIndex        =   16
         Top             =   5040
         Width           =   2535
      End
      Begin VB.Label Label17 
         Alignment       =   1  'Right Justify
         BackColor       =   &H00808000&
         Caption         =   "Birthday :"
         BeginProperty Font 
            name            =   "MS Sans Serif"
            charset         =   1
            weight          =   700
            size            =   8.25
            underline       =   0   'False
            italic          =   0   'False
            strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00FFFFFF&
         Height          =   255
         Left            =   360
         TabIndex        =   15
         Top             =   2640
         Width           =   975
      End
      Begin VB.Line Line1 
         BorderColor     =   &H00808080&
         Index           =   0
         X1              =   120
         X2              =   7800
         Y1              =   4440
         Y2              =   4440
      End
   End
   Begin VB.CommandButton cmdSearch 
      Caption         =   "&Search"
      Height          =   375
      Left            =   3720
      TabIndex        =   2
      Top             =   120
      Width           =   975
   End
   Begin VB.TextBox txtSearch 
      Alignment       =   2  'Center
      Appearance      =   0  'Flat
      BorderStyle     =   0  'None
      BeginProperty Font 
         name            =   "MS Sans Serif"
         charset         =   1
         weight          =   700
         size            =   9.75
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   2040
      MaxLength       =   9
      TabIndex        =   0
      Top             =   120
      Width           =   1455
   End
   Begin VB.Label lblTodayDate 
      ForeColor       =   &H00FFFFFF&
      Height          =   255
      Left            =   6720
      TabIndex        =   3
      Top             =   120
      Width           =   1095
   End
   Begin VB.Label lblEnterSS 
      Alignment       =   2  'Center
      BackColor       =   &H00808000&
      Caption         =   "Enter Student's Social Security : "
      BeginProperty Font 
         name            =   "MS Sans Serif"
         charset         =   1
         weight          =   700
         size            =   9.75
         underline       =   0   'False
         italic          =   0   'False
         strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00C00000&
      Height          =   495
      Left            =   -120
      TabIndex        =   1
      Top             =   120
      Width           =   2175
   End
   Begin VB.Menu mnuReturn 
      Caption         =   "&Back"
   End
   Begin VB.Menu mnuExit 
      Caption         =   "E&xit"
   End
End
Attribute VB_Name = "frmSearch"
Attribute VB_Creatable = False
Attribute VB_Exposed = False
Option Explicit


Private Sub cmdNext_Click()

Display_Next_3

End Sub

Private Sub cmdPrevious_Click()

    Display_Previous_3

End Sub

Private Sub cmdPrint_Click()

frmSearch.Hide
frmPrintSS.Show

'Print Report
Print_Current_Record

End Sub

Public Sub cmdSearch_Click()

Clear_Search_Screen
SearchItem = frmSearch.txtSearch.Text
Search_SS

End Sub


Private Sub cmdSearchRecord_Click()

 BSearch
 
End Sub

Private Sub Text4_Change()
Text4.Text = Today()
'Print frmsSearch.Text4; Today
End Sub


Private Sub Command1_Click()

frmSearch.Hide
frmPrintSS.Show

Print_Current_Record

End Sub

Private Sub Form_Load()
        
'  Set todays date on the form frmSearch
   lblTodayDate = Format$(Date, "mm/d/yyyy")

' Center Form On Screen
  CenterForm Me

End Sub


Private Sub mnuExit_Click()

Exit_Program

End Sub

Private Sub mnuReturn_Click()

Close #1
frmSearch.Hide
frmReports.Show
End Sub



