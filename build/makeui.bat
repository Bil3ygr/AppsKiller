@echo off

set PYUIC5=C:\Python36\Scripts\pyuic5.exe
set PYLUPDATE5=C:\Python36\Scripts\pylupdate5.exe
set PYRCC5=C:\Python36\Scripts\pyrcc5.exe

pushd %~dp0\..

@REM for %%I IN ( res\*.ui ) DO (
@REM     echo making UI %%I
@REM     %PYUIC5% %%I -x -o res\ui_%%~nI.py
@REM     if errorlevel 1 (
@REM         echo makeUI failed, check PyQt5 and file path.
@REM         goto:end
@REM     )
@REM )
@REM %PYLUPDATE5% -noobsolete translate.py res\ui_makelink_tab.py res\ui_makelinkwindow.py res\ui_svn_tab.py -ts translate\trans_zh_CN.ts

%PYRCC5% -o src/resources_rc.py res/resources.qrc

:end
popd
pause
