::-----------------------------------------------------------------------------::
:: Name .........: make.cmd
:: Project ......: WSPR Analytics
:: Description ..: Windows Makefile (make.cmd)
:: Project URL ..: https://github.com/KI7MT/wsprana
::
:: Author .......: Greg, Beam, KI7MT, <ki7mt@yahoo.com>
:: Copyright ....: Copyright (C) 2020 Greg Beam, KI7MT
:: License ......: Apache 2.0
::
:: make.cmd is free software: you can redistribute it and/or modify it
:: under the terms of the GNU General Public License as published by the Free
:: Software Foundation either version 3 of the License, or (at your option) any
:: later version. 
::
:: make.cmd is distributed in the hope that it will be useful, but WITHOUT
:: ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
:: FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
:: details.
::
:: You should have received a copy of the GNU General Public License
:: along with this program.  If not, see <http://www.gnu.org/licenses/>.
::-----------------------------------------------------------------------------::
@ECHO OFF

:: Requirements:
::     python
::     setuptools
::     twine
::
:: NOTES:
::
::   For Package Requirements
::     If you have runtime package requirements, add the file "requirements.txt"
::     to the root of the distribution.
::
::   For Development Requirements
::     For development requirements, use the requirements-dev.txt

:: Make File Variables
SET app_name=wsprana
SET app_ver=0.0.1
SET pypitest=--repository-url https://test.pypi.org/legacy/ dist/*
SET test_install=-i https://test.pypi.org/simple/ wsprana
SET prod_install=-i https://pypi.org/simple/ wspr
SET pubprod=twine upload dist/*
SET requirements=%CD%\requirements.txt
SET requirements-dev=%CD%\requirements-dev.txt

:: Get Command line Options %1
IF /I [%1]==[clean] ( GOTO _CLEAN )
IF /I [%1]==[distclean] ( GOTO _DISTCLEAN )
IF /I [%1]==[dist] ( GOTO _DIST )
IF /I [%1]==[install] ( GOTO _INSTALL )
IF /I [%1]==[uninstall] ( GOTO _UNINSTALL )
IF /I [%1]==[pubtest] ( GOTO _PUBTEST )
IF /I [%1]==[publish] ( GOTO _PUBLISH )
IF /I [%1]==[setup] ( GOTO _SETUP )
IF /I [%1]==[setupdev] ( GOTO _SETUPDEV )
IF /I [%1]==[help] ( GOTO _HELP )
GOTO _HELP

:: Clean the source tree
:_CLEAN
CLS
ECHO ----------------------------------------
ECHO  Clean Solution %app_name%
ECHO ----------------------------------------
ECHO.
python setup.py clean ^-a
GOTO EOF

:: Clean the source tree
:_DISTCLEAN
CLS
ECHO ----------------------------------------
ECHO  Clean Distribution %app_name%
ECHO ----------------------------------------
ECHO.
python setup.py clean ^-a
rmdir /s /q .\dist > NUL 2>&1
rmdir /s /q .\%app_name%.egg-info > NUL 2>&1
rmdir /s /q .\%app_name%\__pycache__ > NUL 2>&1
rmdir /s /q .\tools > NUL 2>&1
rmdir /s /q .\src > NUL 2>&1
rmdir /s /q .\scripts > NUL 2>&1
rmdir /s /q .\tmp > NUL 2>&1
GOTO EOF

:: Install application
:_INSTALL
CLS
ECHO ----------------------------------------
ECHO  Installing %app_name% locally with pip
ECHO ----------------------------------------
ECHO.
ECHO Installing Package: %app_name%
pip install ^-e .
ECHO.
ECHO Finished
GOTO EOF

:: Uninstall application
:_UNINSTALL
CLS
ECHO --------------------------------------------
ECHO  Installing %app_name% with pip
ECHO --------------------------------------------
ECHO.
pip uninstall ^-y %app_name%
ECHO.
GOTO EOF

:: Run pip install -r %requirements.txt%
:: TODO: this should check os the file is "empty" also
:: for /F %%A in (%requirements%) do If %%~zA equ 0 echo "File Is Empty" 
:_SETUP
CLS
ECHO ----------------------------------------
ECHO  Setup Requirements
ECHO ----------------------------------------
ECHO.
IF EXIST %requirements% (
    ECHO Installing Requirements using pip
    pip install ^-r %requirements%
) else (
    ECHO Nothing to do, no requirements file
)
IF %ERRORLEVEL% NEQ 0 ( 
   GOTO _ERROR_EXIT 
)
ECHO.
ECHO Finished
GOTO EOF

:: Run pip install -r %requirements-dev.txt%
:: TODO: this should check os the file is "empty" also
:: for /F %%A in (%requirements-dev%) do If %%~zA equ 0 echo "File Is Empty" 
:_SETUPDEV
CLS
ECHO ----------------------------------------
ECHO  Setup Developer Requirements
ECHO ----------------------------------------
ECHO.
IF EXIST %requirements-dev% (
    ECHO Installing Developer Requirements using pip
    pip install ^-r %requirements-dev%
) ELSE (
    ECHO Nothing to do, no developer requirments file
)
IF %ERRORLEVEL% NEQ 0 (
   GOTO _ERROR_EXIT
)
ECHO.
ECHO Finished
GOTO EOF

:: Run Python setuptools to package app
:_DIST
CLS
ECHO ----------------------------------------
ECHO  Distribution Package ^: %app_name%
ECHO ----------------------------------------
ECHO.
ECHO Creating Package: %app_name%
python setup.py sdist bdist_wheel
ECHO.
ECHO Finished
GOTO EOF

:: Run Python twine to publish to test.pypi.org
:_PUBTEST
CLS
ECHO ----------------------------------------
ECHO  Publishing to PyPi test Site
ECHO ----------------------------------------
ECHO.
ECHO Plublishing Package: %app_name%
twine upload %pypitest%

:: If the esit status was not 0, for to test publish error
IF %ERRORLEVEL% NEQ 0 (
   GOTO _TEST_PUBLISH_ERROR
)
ECHO.
ECHO To install ^[ %app_name% ^] from ^( test.pypi.org ^)^, run the
ECHO following command ^:
ECHO.
ECHO pip install %test_install%
ECHO.
ECHO.
ECHO Finished
GOTO EOF

:: Run Python twine to publish to test.pypi.org
:_PUBLISH
CLS
ECHO ----------------------------------------
ECHO  Publishing to PyPi Production Site
ECHO ----------------------------------------
ECHO.
ECHO Plublishing Package: %app_name%
twine upload %pypiprod%

:: If the exit status was not 0, goto publish error
IF %ERRORLEVEL% NEQ 0 (
   GOTO _PUBLISH_ERROR
)
ECHO.
ECHO To install ^[ %app_name% ^] from ^( pypi.org ^)^, run the
ECHO following command ^:
ECHO.
ECHO pip install %prod_install%
ECHO.
ECHO.
ECHO Finished
GOTO EOF

:: Finished installation
ECHO   Finished
GOTO EOF

:: ----------------------------------------------------------------------------
::  HELP MESSAGE
:: ----------------------------------------------------------------------------
:_HELP
CLS
ECHO.
ECHO ----------------------------------------
ECHO  %app_name% Make Help
ECHO ----------------------------------------
ECHO.
ECHO  The build script takes one option^:
ECHO.
ECHO    make ^<option^>
ECHO.
ECHO    clean      :  clean the build tree
ECHO    distclean  :  clean distribution files adn folders
ECHO    dist       :  generate distribution wheel
ECHO    install    :  install the application locally
ECHO    uninstall  :  uninstall the application
ECHO    pubtest    :  publish app to test.pypi.org
ECHO    publish    :  publish app to pypi.org
ECHO    setup      :  pip install requirements.txt
ECHO    setupdev   :  pip install requirements-dev.txt
ECHO.
ECHO    Example:
ECHO      make setup
ECHO      make clean
ECHO      make install
ECHO.
GOTO EOF

:_TEST_PUBLISH_ERROR
ECHO.
ECHO  Publishing to ^( test.pypi.org ^) failed.
ECHO  Check error messages on the screen, resolve
ECHO  the issue, and republish.
ECHO.
GOTO _ERROR_EXIT

:_PUBLISH_ERROR
ECHO.
ECHO  Publishing to ^( pypi.org ^) failed.
ECHO  Check error messages on the screen, resolve
ECHO  the issue, and republish.
ECHO.
GOTO _ERROR_EXIT

:EOF
EXIT /b 0

:_ERROR_EXIT
EXIT /B %ERRORLEVEL%
