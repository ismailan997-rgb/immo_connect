@echo off
title Immo Connect - Serveur Local
cd /d "%~dp0"
chcp 65001 >nul
color 0B
cls
echo ========================================================
echo             IMMO CONNECT - SERVEUR LOCAL
echo ========================================================
echo.
echo   Application disponible sur :
echo     * Sur ce PC        : http://127.0.0.1:5000
echo     * Sur ce PC        : http://localhost:5000
echo     * Sur smartphone   : http://192.168.1.3:5000 (même Wi-Fi)
echo.
echo   (Ne fermez pas cette fenêtre pendant que vous naviguez)
echo   Appuyez sur Ctrl + C pour arrêter le serveur.
echo ========================================================
echo.
"C:\Users\Win 11 Pro\AppData\Local\Programs\Python\Python314\python.exe" app.py
if errorlevel 1 (
    echo.
    echo Une erreur est survenue lors du lancement de l'application.
    pause
)
