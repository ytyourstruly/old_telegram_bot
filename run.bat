
call %~dp0my_python_env\Scripts\activate.bat
cd %~dp0\layers
set API_KEY=5237237654:AAH1HqwlF1ZUzMBSYglSq0Omw9nE7ryb9Hg
python telegram_server.py
pause