' HS 29Jan21
' Excel Visual Basic code for cell content replacement
' Code Information source: https://stackoverflow.com/questions/25530193/excel-find-and-replace-macro-one-column-only
' search query "excel vba find and replace text in column"

Sub ReplaceVirtual()
    Columns("A").Replace What:="ltm virtual ", _
                            Replacement:="", _
                            LookAt:=xlPart, _
                            SearchOrder:=xlByRows, _
                            MatchCase:=False, _
                            SearchFormat:=False, _
                            ReplaceFormat:=False
							
    Columns("A").Replace What:=" {", _
                            Replacement:="", _
                            LookAt:=xlPart, _
                            SearchOrder:=xlByRows, _
                            MatchCase:=False, _
                            SearchFormat:=False, _
                            ReplaceFormat:=False
							
							
    Columns("B").Replace What:="    description ", _
                            Replacement:="", _
                            LookAt:=xlPart, _
                            SearchOrder:=xlByRows, _
                            MatchCase:=False, _
                            SearchFormat:=False, _
                            ReplaceFormat:=False

    Columns("C").Replace What:="    destination ", _
                            Replacement:="", _
                            LookAt:=xlPart, _
                            SearchOrder:=xlByRows, _
                            MatchCase:=False, _
                            SearchFormat:=False, _
                            ReplaceFormat:=False

    Columns("D").Replace What:="    partition ", _
                            Replacement:="", _
                            LookAt:=xlPart, _
                            SearchOrder:=xlByRows, _
                            MatchCase:=False, _
                            SearchFormat:=False, _
                            ReplaceFormat:=False

    Columns("E").Replace What:="    pool ", _
                            Replacement:="", _
                            LookAt:=xlPart, _
                            SearchOrder:=xlByRows, _
                            MatchCase:=False, _
                            SearchFormat:=False, _
                            ReplaceFormat:=False
End Sub
