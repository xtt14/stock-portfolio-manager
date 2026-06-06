# Stock Portfolio Manager - Offline Setup Guide

## للعمل بدون إنترنت / For Offline Installation

### الخطوة 1: من جهاز فيه نت / Step 1: From a computer with internet:

```bash
pip download PyQt6 -d ./packages
```

هذا بيحمل كل المكتبات المطلوبة في مجلد `packages`

This will download all required libraries to the `packages` folder

### الخطوة 2: انقل مجلد packages لجهازك / Step 2: Transfer packages folder to your offline computer

انسخ المجلد `packages` إلى مجلد المشروع

Copy the `packages` folder to your project directory

### الخطوة 3: على جهازك بدون نت / Step 3: On your offline computer:

اضغط مرتين على `setup_and_run.bat` (Windows) أو شغل `./setup_and_run.sh` (Mac/Linux)

Double-click `setup_and_run.bat` (Windows) or run `./setup_and_run.sh` (Mac/Linux)

---

## Online Installation (مع النت)

إذا كان عندك نت، فقط اضغط على `setup_and_run.bat` أو `setup_and_run.sh`

If you have internet, just double-click `setup_and_run.bat` or run `setup_and_run.sh`

---

## محتويات المشروع / Project Structure:

- `main.py` - البرنامج الرئيسي / Main application
- `ui.py` - واجهة المستخدم / User interface
- `database.py` - إدارة قاعدة البيانات / Database management
- `calculator.py` - حسابات الأرباح والخسائر / Profit/Loss calculations
- `installer.py` - برنامج التثبيت / Setup installer
- `setup_and_run.bat` - بدء التطبيق على Windows
- `setup_and_run.sh` - بدء التطبيق على Mac/Linux
- `requirements.txt` - المكتبات المطلوبة / Required libraries

---

تم صنعه بواسطة xtt14
Created by xtt14
