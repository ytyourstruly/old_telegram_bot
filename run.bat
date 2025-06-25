
call %~dp0my_python_env\Scripts\activate.bat
cd %~dp0\layers
set API_KEY=
python telegram_server.py
pause
