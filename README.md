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


---

## 开源协议与免责声明

### 开源协议

本仓库的**原创内容**（`patch-hex.py` 及本文档）以 [MIT 协议](LICENSE) 开源。

### 第三方内容与版权

| 文件 | 来源 | 版权归属 |
|---|---|---|
| `oray_mcu_firmware.hex` | 向日葵控控原厂 MCU 固件备份 | 深圳市贝锐科技（Oray / 向日葵） |
| `output.hex` | 基于原厂固件修改 VID/PID 的衍生版本 | 原厂部分版权归贝锐，修改部分见本仓库 MIT 协议 |
| `ChipGenius_v4_17_0413.exe` | 第三方工具「芯片精灵」 | 其原作者 |

以上第三方文件**不受本仓库 MIT 协议约束**，仅作个人技术研究留存；若权利人认为不宜分发，请提交 Issue 或联系作者，将立即移除。

### 免责声明

1. **刷机风险**：向 MCU 刷写固件可能导致设备变砖、功能异常、失去官方保修及后续更新支持——**风险自负，后果自担**
2. **非官方项目**：本项目为第三方技术研究，**与深圳市贝锐科技 / 向日葵（Sunlogin）官方无关联**，非其官方出品
3. **合规使用**：请仅在**自有设备**上操作；修改 USB VID/PID 应出于合法技术目的，**不得**用于冒充他人设备、规避授权、侵害第三方权益或其他违法违规用途
4. **无担保**：本仓库按 MIT 协议「按现状」提供，不附带任何明示或默示担保；作者不对使用本项目造成的任何直接或间接损失负责
5. **商标声明**：Oray、向日葵、Sunlogin 等名称与标识归其权利人所有，本项目仅作描述性使用

### 致谢

- [SwimmingTiger/oraykvm](https://github.com/SwimmingTiger/oraykvm) —— 上游参考项目
