@echo off
:: CREATING REQUIREMENTS FOR Python MODULE
rem call conda activate pdf-reader
rem call pip freeze>requirements.txt

:: LOG PREVIOUS COMMITS
call git log -3 --oneline --reverse

:: INPUTS
set /p branch=Branch: 
set /p message=Message: 

:: ADD
call git add .
echo added to stack

:: COMMIT
call git commit -m "%message%"
echo commited!

:: PUSH
call git push origin %branch%
echo pushed to origin on %branch% branch!!

pause