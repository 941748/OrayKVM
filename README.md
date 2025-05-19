# OrayKVM
主要作用：修改 贝锐向日葵 控控硬件OrayKVM原固件，实现修改为指定厂商的设备硬件ID


注意：只是提供一种思路和技术实现，风险自担。


1.登录设备
控控网口默认启用DHCP，可以连接路由器，在路由器后台查看分配的IP地址。然后用ssh登录。
ssh 端口：44033  用户名：root 密码：xxoo

2.查看版本
root@OrayKVM:~# /usr/sbin/oraymcu_helper -v
oray mcu model:stm32f103c8t6, version:1.4.2
root@OrayKVM:~# cat /etc/version
cpu:1.4.0
mcu:1.4.2
kernel:1.1.2
uboot:1.1.0

3.查看USB硬件ID
建议用ChipGenius 查看USB设备id，Windows系统看不到硬件ID，需要用ChipGenius查看。
控控的现有USB设备id：
Bus 004 Device 002: ID 0483:572b    

查看了一下我手边的联想的键盘、鼠标，如下：

　设备描述: USB Composite Device(LiteOn Lenovo Traditional USB Keyboard)
　设备类型: 人机接口设备
　协议版本: USB 2.00
　当前速度: 全速(FullSpeed)
　电力消耗: 100mA
 USB设备ID: VID = 17EF PID = 6099
设备供应商: LiteOn
　设备名称: Lenovo Traditional USB Keyboard
设备修订版: 0115
　主控型号: Unknown(未知)

　设备描述: USB 输入设备(PixArt Lenovo USB Optical Mouse)
　设备类型: 人机接口设备
　协议版本: USB 2.00
　当前速度: 全速(FullSpeed)
　电力消耗: 100mA
 USB设备ID: VID = 17EF PID = 608D
设备供应商: PixArt
　设备名称: Lenovo USB Optical Mouse
设备修订版: 0100
　主控型号: Unknown(未知)

所以，如果把控控的固件刷成  USB设备ID: VID = 17EF PID = 6099 ，那么第三方检测工具就可以识别为联想的键盘、鼠标了。

4.修改USB硬件ID
原理：
把备份出来的oray_mcu_firmware.hex格式文件转换成二进制bin文件，然后简单暴力的搜索替换掉USB设备ID，然后再转换回HEX文件，再刷回去。
脚本patch-hex.py 就是这个原理的实现。也可以根据自己需要，修改代码改成任意厂商的硬件ID。

‌HEX文件（Intel HEX）是一种由英特尔公司设计的ASCII文本格式，广泛用于存储和传输嵌入式系统中的二进制数据，如微控制器固件‌‌。HEX文件通过编码二进制数据为可读文本，并包含地址、校验和等信息，确保数据完整性和正确性‌。


5.刷固件
ssh到设备，执行命令刷固件：
/usr/sbin/oraymcu_helper -f /usr/share/oray_mcu_firmware.hex
刷后，再次查看USB设备id：

　设备描述: USB Composite Device(LiteOn Lenovo Wired Keyboard)
　设备类型: 人机接口设备
　协议版本: USB 2.00
　当前速度: 全速(FullSpeed)
 USB设备ID: VID = 17EF PID = 6099
设备序列号: 00000000001A
设备供应商: LiteOn
　设备名称: Lenovo Wired Keyboard
设备修订版: 0200
　主控型号: Unknown(未知)

6.收工


相关内容参考：
https://github.com/SwimmingTiger/oraykvm

