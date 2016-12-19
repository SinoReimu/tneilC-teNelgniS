Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run("rasphone -a ""HSingleNet""") 
WScript.Sleep 1000 
WshShell.SendKeys "R" 
WScript.Sleep 30 
WshShell.SendKeys "{ENTER}" 
WScript.Sleep 30 
WshShell.SendKeys "{ENTER}" 
WScript.Sleep 50