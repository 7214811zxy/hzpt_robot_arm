@echo off
echo 正在设置静态IP地址...
netsh interface ip set address "以太网" static 192.168.10.100 255.255.255.0
echo 静态IP设置完成！
pause