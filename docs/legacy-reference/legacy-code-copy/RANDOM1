Attribute VB_Name = "Module1"
Option Explicit


Global MaxRec As Integer  'Max Record
Global I As Integer
Global RecBuf As Query_File
Global CurrentRec As Integer  'Current Record
Global FileName As String
Global MyRecord As Query_File
Global RecNum As Integer

Global MaxRec2 As Integer
Global I2 As Integer
Global RecBuf2 As Student_File
Global MyRecord2 As Student_File
Global CurrentRec2 As Integer
Global RecNum2 As Integer
Global FileName2 As String

Global MaxRec3 As Integer
Global I3 As Integer
Global RecBuf3 As Employment_File
Global MyRecord3 As Employment_File
Global CurrentRec3 As Integer
Global RecNum3 As Integer
Global FileName3 As String


Global CurrentRec4 As Integer

' Low and High point to the first and last
' element of a range of elements

Global Low As Integer
Global High As Integer
Global Md As Integer
Global Rslt As Integer
Global position As Integer

Global Result As Integer
Global Result2 As Integer
Global Result3 As Integer

Global j As Integer

'Array for Multiple Record Report
Dim Print_Rec(1 To 10) As String
Global k As Integer
Global l As Integer

'Variable to capture SS value to search
Global SearchItem As String

'Variable to capture Company Code to search for
Global Search_Company_Code As String


' -------------------------------------------------

' Define user-defined types.

' --------------------------------------------------

Type Student_File

    Program_Code As String * 7
    Date As String * 9
    Program_Name As String * 31
    SS_Number As String * 10
    Last_Name As String * 16
    First_Name As String * 16
    Home_Phone As String * 16
    Work_Phone As String * 16
    Address As String * 31
    City As String * 31
    State As String * 3
    Zip As String * 11
    High_School As String * 31
    Date_Graduated As String * 11
    Month As String * 3
    Day As String * 3
    YesNo As String * 2
    Description As String * 101
    Company_Code As String * 9

End Type


'Define Query File

Type Query_File

    SS_Number As String * 10

End Type


'Define Current Employment File

Type Employment_File
    
    Company_Code As String * 9
    Company_Name As String * 31
    Address As String * 26
    City As String * 31
    State As String * 3
    Zip As String * 11
    Job_Title As String * 31
    Current_Supervisor As String * 31
    Phone_Number As String * 16
    Hours_per_Week As String * 3
    Amount As String * 16
    Company_Type As String * 30

End Type


Sub Clear_Employment_Fields()
  
   frmSearch.txtCompany_Name = ""
   frmSearch.txtAddress_E = ""
   frmSearch.txtCity_E = ""
   frmSearch.txtSTate_E = ""
   frmSearch.txtZip_E = ""
   frmSearch.txtJob_Title = ""
   frmSearch.txtCurrent_Supervisor = ""
   frmSearch.txtPhone_Number = ""
   frmSearch.txtHours_per_Week = ""
   frmSearch.txtAmoun = ""
   frmSearch.txtCompany_Type = ""
 
 End Sub

'---------------------------------------------

Sub Clear_Search_Screen()

    frmSearch.txtSS = ""
    frmSearch.txtProgram_Name = ""
    frmSearch.txtProgram_Code = ""
    frmSearch.txtProgram_Name = ""
    frmSearch.txtLast_Name = ""
    frmSearch.txtFirst_Name = ""
    frmSearch.txtHome_Phone = ""
    frmSearch.txtWork_Phone = ""
    frmSearch.txtAddress = ""
    frmSearch.txtCity = ""
    frmSearch.txtSState = ""
    frmSearch.txtZip = ""
    frmSearch.txtHigh_School = ""
    frmSearch.txtDate_Graduated = ""
    frmSearch.txtMonth = ""
    frmSearch.txtDay = ""
    frmSearch.txtYesNo = ""
    frmSearch.txtDescription = ""
    
    
    frmSearch.txtSearch.SetFocus
    
End Sub

Sub Display_Next()

 
    'Get the next record in the file
    '
    If CurrentRec <> MaxRec Then
        '
        'Increment the record Number
        CurrentRec = CurrentRec + 1
        
        'Retrieve and display
        GetRecord (CurrentRec)
    Else
        MsgBox "End of file. No next record."
    End If

End Sub


Sub Display_Next_2()



    'Get the next record in the file
    '
    If CurrentRec2 <> MaxRec2 Then
        '
        'Increment the record Number
        CurrentRec2 = CurrentRec2 + 1
        
        'Retrieve and display
        ObtainRecord (CurrentRec2)
    Else
        MsgBox "End of file. No next record."
    End If


End Sub



Sub Display_Next_3()

Close #1

Open_Student

'Get the next record in the file
        
       
    If CurrentRec3 <> MaxRec2 Then
        '
        'Increment the record Number
        CurrentRec3 = CurrentRec3 + 1
               
        'Retrieve and display
        Obtain_Rec3 (CurrentRec3)
        
        frmSearch.txtSearch = RecBuf2.SS_Number
        
        'Keep Company Code to Search Employment File
        
        Search_Company_Code = Trim$(RecBuf2.Company_Code)
       
        'Search Employment File
        
        Open_Employment
                     
        
        Query_Employment
    
    Else
    
        MsgBox "End of file. No next record."
    
    End If

End Sub


Sub Display_Next_4()

'Get the next record in the file
        
       
    If CurrentRec3 <> MaxRec3 Then  'Check Current Rec3 maybe 4
        '
        'Increment the record Number
        CurrentRec3 = CurrentRec3 + 1
               
        'Retrieve and display
        ObtainRec_4 (CurrentRec3)
        
    Else
    
        MsgBox "End of file. No next record."
    
    End If

End Sub


Sub Display_Previous_3()

'Close Employment File and Open Student File

Close #1
Open_Student


'Get the previous record in the file
    '
    If CurrentRec3 > 1 Then
        '
        'Decrement the record Number
        CurrentRec3 = CurrentRec3 - 1
        
        'Retrieve and display
        Obtain_Rec3 (CurrentRec3)
    
        frmSearch.txtSearch = RecBuf2.SS_Number
        
        'Keep Company Code to Search Employment File
        
        Search_Company_Code = Trim$(RecBuf2.Company_Code)
        
        'Search Employment File
                
        Open_Employment
        Query_Employment
    
    
    
    
    Else
        MsgBox "Start of file. No previous record."
    End If



End Sub




Sub Display_Previous()

'Get the previous record in the file
    '
    If CurrentRec > 1 Then
        '
        'Decrement the record Number
        CurrentRec = CurrentRec - 1
        
        'Retrieve and display
        GetRecord (CurrentRec)
    Else
        MsgBox "Start of file. No previous record."
    End If
    
End Sub

Sub Display_Previous_4()

'Get the previous record in the file
    '
    If CurrentRec3 > 1 Then
        '
        'Decrement the record Number
        CurrentRec3 = CurrentRec3 - 1
        
        'Retrieve and display
        ObtainRec_4 (CurrentRec3)
    Else
        MsgBox "Start of file. No previous record."
    End If
    
End Sub

Sub Display_Previous_2()

'Get the previous record in the file
    '
    If CurrentRec2 > 1 Then
        '
        'Decrement the record Number
        CurrentRec2 = CurrentRec2 - 1
        
        'Retrieve and display
        ObtainRecord (CurrentRec2)
    Else
        MsgBox "Start of file. No previous record."
    End If


End Sub



Sub Exit_Program()

Dim ExitP%

'Display message box to end program

ExitP% = MsgBox("Are you sure you want to exit?", 1, "Exit Program")

    If ExitP% = 1 Then
    
        End

    End If

End Sub     ' Exit_Program



Sub Multiple_Rec_rep()

'Print Multiple Records Report


'Transfer value of text boxes to array elements

Print_Rec(1) = Trim$(frmSelect_Rec.txtRec1.Text)
Print_Rec(2) = Trim$(frmSelect_Rec.txtRec2.Text)
Print_Rec(3) = Trim$(frmSelect_Rec.txtRec3.Text)
Print_Rec(4) = Trim$(frmSelect_Rec.txtRec4.Text)
Print_Rec(5) = Trim$(frmSelect_Rec.txtRec5.Text)
Print_Rec(6) = Trim$(frmSelect_Rec.txtRec6.Text)
Print_Rec(7) = Trim$(frmSelect_Rec.txtRec7.Text)
Print_Rec(8) = Trim$(frmSelect_Rec.txtRec8.Text)
Print_Rec(9) = Trim$(frmSelect_Rec.txtRec9.Text)
Print_Rec(10) = Trim$(frmSelect_Rec.txtRec10.Text)


'Print Report Header
frmPrintSS.Show
frmPrintSS.FontBold = True
frmPrintSS.Print
frmPrintSS.Print Tab(2); "Social"; Tab(36); "Prog"; Tab(43); "Company"; Tab(58); "Work"; Tab(71); "Company"
frmPrintSS.Print Tab(1); "Security"; Tab(13); "Student Name"; Tab(36); "Code"; Tab(58); "Phone"; Tab(73); "Code"
frmPrintSS.Print "-------------------------------------------------------------------------------------------------------------"
 
'Find and Print Record for each Student

l = k

For j = 1 To k

SearchItem = Print_Rec(j)

If SearchItem = "" Then
    
    frmPrintSS.Print Tab(1); "-"
    
Else


'Search_SS

Search_PSocial


Result = StrComp(SearchItem, Trim$(RecBuf.SS_Number))

If Result <> 0 Then
 
'Display Not Found Message
 Not_Found_Msg
   
    
Else
 

'*************Query_Student
Search_PStudent

Result2 = StrComp(SearchItem, Trim(RecBuf2.SS_Number))

 
If Result2 <> 0 Then
 
   Not_Found2_Msg
 
Else
 
'MsgBox "It Found Student!!!"
    
   
    
       
    
    ' Keep position count in case View Previous or View Next are
    ' required
    
    CurrentRec3 = position

    ' Keep Company Code to Search Employment

    Search_Company_Code = Trim$(RecBuf2.Company_Code)
        
    
    'Initiate Employment File Search based on Company Code
    'in Student Record
    
    '********Query Employment
    Srch_PEmp

    Result3 = StrComp(Search_Company_Code, Trim$(RecBuf3.Company_Code))


    If Result3 <> 0 Then
   
        Employment_Not_Found_Msg
 
    Else
    
 
        'Print Records
 
        frmPrintSS.FontBold = False
        frmPrintSS.Print Tab(1); RecBuf2.SS_Number; Tab(13); Trim$(RecBuf2.First_Name); " "; Trim$(RecBuf2.Last_Name); Tab(36); Trim$(RecBuf2.Program_Code); Tab(43); Trim$(RecBuf3.Company_Name); Tab(58); Trim$(RecBuf2.Work_Phone); Tab(72); RecBuf2.Company_Code
  
  End If
    
    End If
   
End If

End If

'**** End Next
Next

End Sub


Sub Not_Found2_Msg()

Dim NotFound%

'Display message box to end program


NotFound% = MsgBox("Number Not Found in Student File! Enter another number", 48, "Not Found")

'frmSelect_Rec.txtRec1 = ""
'frmSearch.txtSearch.SetFocus

End Sub



Sub Obtain_Rec3(RecNum3 As Integer)
'
'Read the specfied record from the file and display on the form

    
    'Read the first record and place in the form
    Get #1, RecNum3, RecBuf2
    
    
    frmSearch.txtSS = RecBuf2.SS_Number
    frmSearch.txtProgram_Code = RecBuf2.Program_Code
    frmSearch.txtProgram_Name = RecBuf2.Program_Name
    frmSearch.txtLast_Name = RecBuf2.Last_Name
    frmSearch.txtFirst_Name = RecBuf2.First_Name
    frmSearch.txtHome_Phone = RecBuf2.Home_Phone
    frmSearch.txtWork_Phone = RecBuf2.Work_Phone
    frmSearch.txtAddress = RecBuf2.Address
    frmSearch.txtCity = RecBuf2.City
    frmSearch.txtSState = RecBuf2.State
    frmSearch.txtZip = RecBuf2.Zip
    frmSearch.txtHigh_School = RecBuf2.High_School
    frmSearch.txtDate_Graduated = RecBuf2.Date_Graduated
    frmSearch.txtMonth = RecBuf2.Month
    frmSearch.txtDay = RecBuf2.Day
    frmSearch.txtYesNo = RecBuf2.YesNo
    frmSearch.txtDescription = RecBuf2.Description
    frmSearch.txtCompany_Code = RecBuf2.Company_Code

   
End Sub

Sub Open_Employment()

'Close Student File
Close #1

'Open Employment File

'FileName = App.Path & "\employment.txt"
Open "a:\employment.txt" For Random As #1 Len = Len(MyRecord3)

End Sub

Sub Print_Current_Record()

 
    frmPrintSS.Print
    frmPrintSS.FontBold = True
    frmPrintSS.Font = "MS Sans Serif"
    frmPrintSS.Print Tab(2); "---------------------------------------------------------------------------------------------"
    frmPrintSS.Print Tab(22); "STUDENT RECORD"
    frmPrintSS.Print Tab(2); "---------------------------------------------------------------------------------------------"
    frmPrintSS.Print Tab(2); "Social Security Number: "; Tab(26); RecBuf2.SS_Number
    frmPrintSS.Print Tab(2); "Student Name:   "; Tab(26); Trim$(RecBuf2.First_Name); " "; Trim$(RecBuf2.Last_Name)
    frmPrintSS.Print Tab(2); "---------------------------------------------------------------------------------------------"
    
    frmPrintSS.Print Tab(2); "Program Code: "; Tab(17); RecBuf2.Program_Code
    frmPrintSS.Print Tab(2); "Program Name:"; Tab(17); RecBuf2.Program_Name
    frmPrintSS.Print Tab(2); "Home Phone:   "; RecBuf2.Home_Phone; Tab(37); "Work Phone:"; Tab(51); RecBuf2.Work_Phone
    frmPrintSS.Print Tab(2); "Address:   "; Tab(17); RecBuf2.Address
    frmPrintSS.Print Tab(17); Trim$(RecBuf2.City); Tab(37); RecBuf2.State; Tab(42); RecBuf2.Zip
    frmPrintSS.Print Tab(2); "High School:  "; Tab(17); RecBuf2.High_School
    frmPrintSS.Print Tab(2); "Graduated on:  "; Tab(17); RecBuf2.Date_Graduated
    frmPrintSS.Print Tab(2); "Birthday  "; Tab(17); "Month:   "; RecBuf2.Month; Tab(37); "Day:   "; RecBuf2.Day
    frmPrintSS.Print Tab(2); "Currently looking for a Job?:   "; RecBuf2.YesNo
    frmPrintSS.Print Tab(2); "Type of Job:  "; Tab(17); RecBuf2.Description
    frmPrintSS.Print Tab(2); "---------------------------------------------------------------------------------------------"
    frmPrintSS.Print Tab(2); "Company:   "; Tab(17); RecBuf3.Company_Name
    frmPrintSS.Print Tab(2); "Address:   "; Tab(17); RecBuf3.Address
    frmPrintSS.Print Tab(17); Trim$(RecBuf3.City); Tab(37); RecBuf3.State; Tab(42); RecBuf3.Zip
    frmPrintSS.Print Tab(2); "Job Title:   "; Tab(17); RecBuf3.Job_Title; Tab
    frmPrintSS.Print Tab(2); "Supervisor:   "; Tab(17); Trim$(RecBuf3.Current_Supervisor); Tab(45); "Phone:   "; Tab(54); RecBuf3.Phone_Number
    frmPrintSS.Print Tab(2); "Hours/Week:   "; Tab(17); RecBuf3.Hours_per_Week; Tab(37); "Hourly Rate:  "; Tab(54); RecBuf3.Amount
    frmPrintSS.Print Tab(2); "Company Type:"; Tab(17); RecBuf3.Company_Type
    frmPrintSS.Print Tab(2); "---------------------------------------------------------------------------------------------"
    frmPrintSS.Font = "Courier New"

End Sub


Sub ObtainRecord(RecNum2 As Integer)
'
'Read the specfied record from the file and display on the form

    
    'Read the first record and place in the form
    Get #1, RecNum2, RecBuf2
    
    
    frmDisplay.txtSS_Number = RecBuf2.SS_Number
    frmDisplay.txtProgram_Code = RecBuf2.Program_Code
    frmDisplay.txtDate = RecBuf2.Date
    frmDisplay.txtProgram_Name = RecBuf2.Program_Name
    frmDisplay.txtLast_Name = RecBuf2.Last_Name
    frmDisplay.txtFirst_Name = RecBuf2.First_Name
    frmDisplay.txtHome_Phone = RecBuf2.Home_Phone
    frmDisplay.txtWork_Phone = RecBuf2.Work_Phone
    frmDisplay.txtAddress = RecBuf2.Address
    frmDisplay.txtCity = RecBuf2.City
    frmDisplay.txtSState = RecBuf2.State
    frmDisplay.txtZip = RecBuf2.Zip
    frmDisplay.txtHigh_School = RecBuf2.High_School
    frmDisplay.txtDate_Graduated = RecBuf2.Date_Graduated
    frmDisplay.txtMonth = RecBuf2.Month
    frmDisplay.txtDay = RecBuf2.Day
    frmDisplay.txtYesNo = RecBuf2.YesNo
    frmDisplay.txtDescription = RecBuf2.Description
    frmDisplay.txtCompany_Code = RecBuf2.Company_Code
    
   

    
    
End Sub

Sub ObtainRec_4(RecNum3 As Integer)

'
'Read the specfied record from the file and display on the form

    
    'Read the first record and place in the form
    Get #1, RecNum3, RecBuf3
    
    
   frmEmployment.txtCompany_Code = RecBuf3.Company_Code
   frmEmployment.txtCompany_Name = RecBuf3.Company_Name
   frmEmployment.txtAddress = RecBuf3.Address
   frmEmployment.txtCity = RecBuf3.City
   frmEmployment.txtState = RecBuf3.State
   frmEmployment.txtZip = RecBuf3.Zip
   frmEmployment.txtJob_Title = RecBuf3.Job_Title
   frmEmployment.txtCurrent_Supervisor = RecBuf3.Current_Supervisor
   frmEmployment.txtPhone_Number = RecBuf3.Phone_Number
   frmEmployment.txtHours_per_Week = RecBuf3.Hours_per_Week
   frmEmployment.txtAmoun = RecBuf3.Amount
   frmEmployment.txtCompany_Type = RecBuf3.Company_Type
    
      
    
End Sub







Sub GetRecord(RecNum As Integer)
'
'Read the specfied record from the file and display on the form

    'Read the first record and place in the form
    Get #1, RecNum, RecBuf
    
    
    frmRandom.txtSS = RecBuf.SS_Number
    
    


End Sub



Sub Open_File()

'FileName = App.Path & "\random.txt"
Open "a:\random.txt" For Random As #1 Len = Len(MyRecord)

End Sub


Sub Open_Student()

Close #1

'FileName = App.Path & "\student.txt"
Open "a:\student.txt" For Random As #1 Len = Len(MyRecord2)

End Sub


Sub Print_All_SS()

frmRandom.Hide
frmPrintSS.Show

frmPrintSS.Print
frmPrintSS.Print
frmPrintSS.Print ; Tab(12); "All Social Security Numbers"
frmPrintSS.Print

I = 0
CurrentRec = 1

For I = 1 To MaxRec
        
        'Retrieve and display
        GetRecord (CurrentRec)
  
        'Print Record
        frmPrintSS.Print ; Tab(20); RecBuf.SS_Number
        
        'Increment Current Record
        CurrentRec = CurrentRec + 1

Next

CurrentRec = 0

End Sub

Sub Print_Current()

Dim Current_SS As String

frmRandom.Hide
frmPrintSS.Show

frmPrintSS.Print
frmPrintSS.Print
frmPrintSS.Print ; Tab(12); "Social Security Number"
frmPrintSS.Print



'Retrieve value from text box
Current_SS = frmRandom.txtSS.Text

        'Print Record
        frmPrintSS.Print ; Tab(18); Current_SS

End Sub





Sub Query_Employment()
' Subroutine to Search for the social security in the Student
' Information File after it is found in the


'Parameters:
  
    'Search Item - Item to tbe found - variant ype
    'MaxRec - Number of items in the array
    'Position - 0 if item not found,
    '      equal to subscript of item,
    '      otherwise assume item will not be
    '      found
    
'Open Student Information File

Open_Employment

MaxRec3 = LOF(1) / Len(MyRecord3)


Dim Result As Integer

' Low and High point to the first and last
' element of a range of elements

' Start with entire range of array values

Low = 1
High = MaxRec3

Do While Low <= High

    Md = (Low + High) \ 2   'an inter division
   
        'Retrieve and display
        
        Get #1, Md, RecBuf3
               
        
    Rslt = StrComp(Search_Company_Code, Trim$(RecBuf3.Company_Code))
 
Select Case Rslt

    Case 0
        position = Md
        Exit Do    ' search is over
        
    Case -1        ' search item is in first half of list
        High = Md - 1
        
    Case 1         ' search item is in last half of list
        Low = Md + 1

End Select

  Loop

Result = StrComp(Search_Company_Code, Trim$(RecBuf3.Company_Code))


'Else
 
 If Result <> 0 Then
   
    Employment_Not_Found_Msg
 
 Else
    
   frmSearch.txtCompany_Name = RecBuf3.Company_Name
   frmSearch.txtAddress_E = RecBuf3.Address
   frmSearch.txtCity_E = RecBuf3.City
   frmSearch.txtSTate_E = RecBuf3.State
   frmSearch.txtZip_E = RecBuf3.Zip
   frmSearch.txtJob_Title = RecBuf3.Job_Title
   frmSearch.txtCurrent_Supervisor = RecBuf3.Current_Supervisor
   frmSearch.txtPhone_Number = RecBuf3.Phone_Number
   frmSearch.txtHours_per_Week = RecBuf3.Hours_per_Week
   frmSearch.txtAmoun = RecBuf3.Amount
   frmSearch.txtCompany_Type = RecBuf3.Company_Type
        
    
 End If
    
 frmSearch.txtSearch.SetFocus

 End Sub

Sub Query_Student()


' Subroutine to Search for the social security in the Student
' Information File after it is found in the


'Close #1


SearchItem = frmSearch.txtSearch.Text

'Dim position As Integer

'Parameters:
  
    'Search Item - Item to tbe found - variant ype
    'MaxRec - Number of items in the array
    'Position - 0 if item not found,
    '      equal to subscript of item,
    '      otherwise assume item will not be
    '      found
    
'Open Student Information File

Open_Student

MaxRec2 = LOF(1) / Len(MyRecord2)


Dim Result As Integer

' Low and High point to the first and last
' element of a range of elements

'Dim Low As Integer
'Dim High As Integer
'Dim Md As Integer

'Dim Rslt As Integer

' Start with entire range of array values

Low = 1
High = MaxRec2

Do While Low <= High

    Md = (Low + High) \ 2   'an inter division
    
             
        'Retrieve and display
        
        Get #1, Md, RecBuf2
               
        
    Rslt = StrComp(SearchItem, Trim$(RecBuf2.SS_Number))
 
Select Case Rslt

    Case 0
        position = Md
        Exit Do    ' search is over
        
    Case -1        ' search item is in first half of list
        High = Md - 1
        
    Case 1         ' search item is in last half of list
        Low = Md + 1

End Select

  Loop

Result = StrComp(SearchItem, Trim(RecBuf2.SS_Number))

'If Result = 0 Then
 'frmSearch.txtSS = RecBuf.SS_Number

'Else
 
 If Result <> 0 Then
 
    frmSearch.txtSS = ""
    Not_Found_Msg
 
 Else
 
    frmSearch.txtSS = RecBuf2.SS_Number
    frmSearch.txtProgram_Name = RecBuf2.Program_Name
    frmSearch.txtProgram_Code = RecBuf2.Program_Code
    frmSearch.txtProgram_Name = RecBuf2.Program_Name
    frmSearch.txtLast_Name = RecBuf2.Last_Name
    frmSearch.txtFirst_Name = RecBuf2.First_Name
    frmSearch.txtHome_Phone = RecBuf2.Home_Phone
    frmSearch.txtWork_Phone = RecBuf2.Work_Phone
    frmSearch.txtAddress = RecBuf2.Address
    frmSearch.txtCity = RecBuf2.City
    frmSearch.txtSState = RecBuf2.State
    frmSearch.txtZip = RecBuf2.Zip
    frmSearch.txtHigh_School = RecBuf2.High_School
    frmSearch.txtSState = RecBuf2.State
    frmSearch.txtZip = RecBuf2.Zip
    frmSearch.txtHigh_School = RecBuf2.High_School
    frmSearch.txtDate_Graduated = RecBuf2.Date_Graduated
    frmSearch.txtMonth = RecBuf2.Month
    frmSearch.txtDay = RecBuf2.Day
    frmSearch.txtYesNo = RecBuf2.YesNo
    frmSearch.txtDescription = RecBuf2.Description
    frmSearch.txtCompany_Code = RecBuf2.Company_Code
    
    
    
    'activate Previous, Next and Print Buttons

    frmSearch.cmdPrevious.Enabled = True
    frmSearch.cmdNext.Enabled = True
    frmSearch.cmdPrint.Enabled = True
    
    ' Keep position count in case View Previous or View Next are
    ' required
    
    CurrentRec3 = position

    ' Keep Company Code to Search Employment

    Search_Company_Code = Trim$(RecBuf2.Company_Code)
        
    
    'Initiate Employment File Search based on Company Code
    'in Student Record
    
       
    Query_Employment
    
    

End If

End Sub


Sub Scroll_SS()
 
 On Error GoTo rand_err
    '
    'Set up file name
    'FileName = App.Path & "\random.txt"

    ' Open sample file for random access.
    Open "a:\random.txt" For Random As #1 Len = Len(MyRecord)

    'Write some records to the file
    '
    
    'For RecNum = 1 To 8
     '   MyRecord.SS = "59509693" & Str$(RecNum)
        
        'Write the record to the file
      '  Put #1, RecNum, MyRecord

    'Next RecNum
    '
    'Determine the number of records in the file
    '
    MaxRec = LOF(1) / Len(MyRecord)

    'Read the first record and place in the form
    GetRecord (1)

    'Initialize the Current Record
    CurrentRec = 1

rand_exit:
Exit Sub

'Error handler
rand_err:
    MsgBox Err.Description, vbCritical, "File I/O Error"
    Resume rand_exit

End Sub

Sub Scroll_Employment_Info()

Close #1

 On Error GoTo rand_err
    

    ' Open sample file for random access.
    Open "a:\employment.txt" For Random As #1 Len = Len(MyRecord3)

    'Write some records to the file
    '
    
    'For RecNum3 = 1 To 11
        
       
        'MyRecord3.Company_Code = "CC" & Str$(RecNum3)
        'MyRecord3.Company_Name = "CN" & Str$(RecNum3)
        'MyRecord3.Address = "A" & Str$(RecNum3)
        'MyRecord3.City = "C" & Str$(RecNum3)
        'MyRecord3.State = "S" & Str$(RecNum3)
        'MyRecord3.Zip = "Z" & Str$(RecNum3)
        'MyRecord3.Job_Title = "JT" & Str$(RecNum3)
        'MyRecord3.Current_Supervisor = "CS" & Str$(RecNum3)
        'MyRecord3.Phone_Number = "PN" & Str$(RecNum3)
        'MyRecord3.Hours_per_Week = "H" & Str$(RecNum3)
        'MyRecord3.Amount = "A" & Str$(RecNum3)
        'MyRecord3.Company_Type = "CT" & Str$(RecNum3)
        
               
    ' Write the record to the file
    'Put #1, RecNum3, MyRecord3
        
    
    'Next RecNum3
    '
    'Determine the number of records in the file
    '
    MaxRec3 = LOF(1) / Len(MyRecord3)

   
    'Read the first record and place in the form
    
    ObtainRec_4 (1)

    'Initialize the Current Record
    
    CurrentRec3 = 1

rand_exit:
Exit Sub

'Error handler
rand_err:
    MsgBox Err.Description, vbCritical, "File I/O Error"
    Resume rand_exit


End Sub

Sub Scroll_Student_Info()

Close #1

 On Error GoTo rand_err
    '
    'Set up file name
    'FileName2 = App.Path & "\student.txt"

    ' Open sample file for random access.
    Open "a:\student.txt" For Random As #1 Len = Len(MyRecord2)

    'Write some records to the file
    '
    
    'For RecNum2 = 1 To 11
        
       
     'MyRecord2.Program_Code = "PC" & Str$(RecNum2)
     'MyRecord2.Date = "Date" & Str$(RecNum2)
     'MyRecord2.Program_Name = "PN" & Str$(RecNum2)
     'MyRecord2.SS_Number = "59509693" & Str$(RecNum2)
     'MyRecord2.Last_Name = "LN" & Str$(RecNum2)
     'MyRecord2.First_Name = "FN" & Str$(RecNum2)
     'MyRecord2.Home_Phone = "HP" & Str$(RecNum2)
     'MyRecord2.Work_Phone = "WP" & Str$(RecNum2)
     'MyRecord2.Address = "A" & Str$(RecNum2)
     'MyRecord2.City = "C" & Str$(RecNum2)
     'MyRecord2.State = "S" & Str$(RecNum2)
     'MyRecord2.Zip = "Z" & Str$(RecNum2)
     'MyRecord2.High_School = "HS" & Str$(RecNum2)
     'MyRecord2.Date_Graduated = "DG" & Str$(RecNum2)
     'MyRecord2.Month = "M" & Str$(RecNum2)
     'MyRecord2.Day = "D" & Str$(RecNum2)
     'MyRecord2.YesNo = "Y" & Str$(RecNum2)
     'MyRecord2.Description = "Description" & Str$(RecNum2)
     'MyRecord2.Company_Code = "CC" & Str$(RecNum2)
          
    ' Write the record to the file
    'Put #1, RecNum2, MyRecord2
        
    
    'Next RecNum2
    
    '
    'Determine the number of records in the file
    '
    MaxRec2 = LOF(1) / Len(MyRecord2)

    'frmDisplay.Print MaxRec2
    'Read the first record and place in the form
    
    ObtainRecord (1)

    'Initialize the Current Record
    
    CurrentRec2 = 1

rand_exit:
Exit Sub

'Error handler
rand_err:
    MsgBox Err.Description, vbCritical, "File I/O Error"
    Resume rand_exit


End Sub

Sub Search_PSocial()
'Open_File

Close #1
Open "a:\random.txt" For Random As #1 Len = Len(MyRecord)

'Determine Length of Record
MaxRec = LOF(1) / Len(MyRecord)


Dim Result As Integer

' Low and High point to the first and last
' element of a range of elements

' Start with entire range of array values

Low = 1
High = MaxRec

Do While Low <= High

    Md = (Low + High) \ 2   'an inter division
    
             
        'Retrieve and display
        
        Get #1, Md, RecBuf
               
        
    Rslt = StrComp(SearchItem, Trim$(RecBuf.SS_Number))
    
    'MsgBox Rslt
 
Select Case Rslt

    Case 0
        position = Md
        Exit Do    ' search is over
        
    Case -1        ' search item is in first half of list
        High = Md - 1
        
    Case 1         ' search item is in last half of list
        Low = Md + 1

End Select

  Loop

End Sub

Sub Search_PStudent()
Open_Student

MaxRec2 = LOF(1) / Len(MyRecord2)


Dim Result2 As Integer

' Low and High point to the first and last
' element of a range of elements


Low = 1
High = MaxRec2

Do While Low <= High

    Md = (Low + High) \ 2   'an inter division
    
             
        'Retrieve and display
        
        Get #1, Md, RecBuf2
               
        
    Rslt = StrComp(SearchItem, Trim$(RecBuf2.SS_Number))
 
Select Case Rslt

    Case 0
        position = Md
        Exit Do    ' search is over
        
    Case -1        ' search item is in first half of list
        High = Md - 1
        
    Case 1         ' search item is in last half of list
        Low = Md + 1

End Select

  Loop

End Sub

Sub Search_SS()

' Subroutine to search for the social security entered
' by System Administrator


Close #1


'Parameters:
  
    'Search Item - Item to tbe found - variant ype
    'MaxRec - Number of items in the array
    'Position - 0 if item not found,
    '      equal to subscript of item,
    '      otherwise assume item will not be
    '      found

Open_File

MaxRec = LOF(1) / Len(MyRecord)


Dim Result As Integer

' Low and High point to the first and last
' element of a range of elements

' Start with entire range of array values

Low = 1
High = MaxRec

Do While Low <= High

    Md = (Low + High) \ 2   'an inter division
    
             
        'Retrieve and display
        
        Get #1, Md, RecBuf
               
        
    Rslt = StrComp(SearchItem, Trim$(RecBuf.SS_Number))
 
Select Case Rslt

    Case 0
        position = Md
        Exit Do    ' search is over
        
    Case -1        ' search item is in first half of list
        High = Md - 1
        
    Case 1         ' search item is in last half of list
        Low = Md + 1

End Select

  Loop

Result = StrComp(SearchItem, Trim$(RecBuf.SS_Number))

'If Result = 0 Then
 'frmSearch.txtSS = RecBuf.SS_Number

'Else
 
 If Result <> 0 Then
 
 'Display Not Found Message
 Not_Found_Msg
   
 
 Else
 
' frmSearch.txtSS = RecBuf.SS_Number

 Query_Student
 
 
End If

End Sub

Sub Not_Found_Msg()

Dim NotFound%

'Display message box to end program


NotFound% = MsgBox("Number Not Found in SS File! Enter another number", 48, "Not Found")

'frmSelect_Rec.txtRec1 = ""
'frmSearch.txtSearch.SetFocus
    
End Sub


Sub Employment_Not_Found_Msg()

Dim NotFound%

'Display message box to end program


NotFound% = MsgBox("EMPLOYMENT RECORD NOT FOUND! ", 48, "Not Employment Data")
'frmSearch.txtSearch = ""
frmSearch.txtSearch.SetFocus

Clear_Employment_Fields



End Sub
Sub Srch_PEmp()

  'Query_Employment
    Open_Employment

'Determine Record Size

MaxRec3 = LOF(1) / Len(MyRecord3)




' Low and High point to the first and last
' element of a range of elements

' Start with entire range of array values

Low = 1
High = MaxRec3

Do While Low <= High

    Md = (Low + High) \ 2   'an inter division
   
        'Retrieve and display
        
        Get #1, Md, RecBuf3
               
        
    Rslt = StrComp(Search_Company_Code, Trim$(RecBuf3.Company_Code))
 
Select Case Rslt

    Case 0
        position = Md
        Exit Do    ' search is over
        
    Case -1        ' search item is in first half of list
        High = Md - 1
        
    Case 1         ' search item is in last half of list
        Low = Md + 1

End Select

  Loop

End Sub


