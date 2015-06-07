setlocal enabledelayedexpansion
cd barinel
for %%l in (*.csv) do (
echo %%l >>..\log.txt.txt
echo %%l >>..\error.txt.txt
java -jar ..\Tom.jar  %%l 2500 ..\out\DIFG_check_%%l  >> ..\log.txt.txt 2>> ..\error.txt.txt
)
endlocal