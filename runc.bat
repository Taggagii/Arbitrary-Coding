@ECHO OFF

IF "%~1" == "" GOTO NoInput
IF "%~2" == "" GOTO NoName
GOTO Name


:RunC
	GCC %1 -o "%name%"
	"%name%.exe"

	IF NOT "%~3" == "False" IF EXIST "%name%.exe" ( rm "%name%.exe" )


GOTO End

:NoInput
	ECHO You must enter a filename parameter when running this command
GOTO End


:NoName
	set name=%~n1
GOTO RunC


:Name
	set name=%~2
GOTO RunC


:End
