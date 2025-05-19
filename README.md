# 向日葵控控硬件OrayKVM固件修改指南

## 主要功能
修改贝锐向日葵控控硬件OrayKVM原固件，实现修改为指定厂商的设备硬件ID

> **注意**：只是提供一种思路和技术实现，风险自担。

## 操作步骤

### 1. 登录设备
- 控控网口默认启用DHCP
- 连接路由器，在路由器后台查看分配的IP地址
- 使用SSH登录：
  ```bash
  ssh -p 44033 root@设备IP
  密码：xxoo
  ```

### 2. 查看版本信息
```bash
root@OrayKVM:~# /usr/sbin/oraymcu_helper -v
oray mcu model:stm32f103c8t6, version:1.4.2

root@OrayKVM:~# cat /etc/version
cpu:1.4.0
mcu:1.4.2
kernel:1.1.2
uboot:1.1.0
```

### 3. 查看USB硬件ID
建议使用ChipGenius查看USB设备ID（Windows系统无法直接查看硬件ID）

控控的现有USB设备ID：
```
Bus 004 Device 002: ID 0483:572b
```

示例设备信息：

**联想键盘**：
```
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
```

**联想鼠标**：
```
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
```

### 4. 修改USB硬件ID
**原理**：
1. 将备份的`oray_mcu_firmware.hex`文件转换为二进制bin文件
2. 搜索替换USB设备ID
3. 转换回HEX文件
4. 刷入修改后的固件

脚本`patch-hex.py`实现了上述功能，可根据需要修改为任意厂商的硬件ID。

> **HEX文件说明**：  
> Intel HEX是一种由英特尔公司设计的ASCII文本格式，广泛用于存储和传输嵌入式系统中的二进制数据，如微控制器固件。HEX文件通过编码二进制数据为可读文本，并包含地址、校验和等信息，确保数据完整性和正确性。

### 5. 刷入固件
SSH到设备执行刷固件命令：
```bash
/usr/sbin/oraymcu_helper -f /usr/share/oray_mcu_firmware.hex
```

刷机后USB设备ID示例：
```
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
```

## 相关参考
- [OrayKVM项目](https://github.com/SwimmingTiger/oraykvm)
