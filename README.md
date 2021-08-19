#   ip-monitor
Public IP monitoring bot.

##  Usage
- Install required packages:
  - requests;
  - smtplib.
- Run the script.

```shell
python -m pip install requests
python -m pip install smtplib
python main.py
```

##  Build the binary
- Install pyinstaller.
- Build the script.

```shell
python -m pip install pyinstaller
pyinstaller main.py -n ip-monitor -w -F
```
