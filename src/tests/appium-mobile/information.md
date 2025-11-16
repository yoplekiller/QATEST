kurly_launcher.bat: adb -s <디바이스ID> shell cmd package resolve-activity --brief <패키지명>

@echo off
echo === 디바이스 목록 ===
adb devices

echo === 마켓컬리 앱 런처 액티비티 확인 ===
adb -s R3CX70ALSLB shell cmd package resolve-activity --brief com.dbs.kurly.m2

echo === 현재 실행 중 액티비티 ===
adb -s R3CX70ALSLB shell dumpsys window | findstr mCurrentFocus

pause

#appium dump 파일 소스 추출
adb shell uiautomator dump
adb pull /sdcard/window_dump.xml C:\Users\jmlim\OneDrive\Desktop