@echo off
REM Portable Google App Engine Command Line Rewriter
REM Written by David Lambert (http://www.codepenguin.com)
 
REM Execute the command line rewriting script
apppython.exe _cmdrewrite.py %0 %*
REM Execute the new command line batch file
_cmdrewrite.bat