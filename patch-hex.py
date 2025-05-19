import intelhex
import struct
import re

def hex_to_bin(hex_path, bin_path):
    try:
        # 指定编码为 'utf-8' 或 'ascii' 以避免解码错误
        ih = intelhex.IntelHex()
        with open(hex_path, 'r', encoding='utf-8') as f:
            ih.fromfile(f, format='hex')
        
        max_address = ih.maxaddr()
        if max_address is not None:
            ih.tobinfile(bin_path)
            print(f"HEX文件已成功转换为BIN文件: {bin_path}")
            return max_address
        else:
            print("HEX文件为空")
            return None
    except Exception as e:
        print(f"转换HEX到BIN时出错: {e}")
        return None


def bin_to_hex_with_special_records(bin_path, hex_path, start_address=0x0000):
    try:
        ih = intelhex.IntelHex()
        ih.loadbin(bin_path, offset=start_address)

        # 读取原始文件的第一行和最后一行
        with open('oray_mcu_firmware.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            first_line = lines[0].strip()
            last_two_lines = lines[-2:]

        # 写入HEX文件，先写入第一行，再写入特殊记录，最后写入最后一行
        with open(hex_path, 'w', encoding='utf-8') as f:
            f.write(first_line + '\n')  # 写入第一行
            ih.write_hex_file(f, write_start_addr=False)
            f.writelines(last_two_lines)  # 写入最后两行

        print(f"BIN文件已成功转换为HEX文件: {hex_path}")
    except Exception as e:
        print(f"转换BIN到HEX时出错: {e}")

def find_and_modify(data, target_bytes, replacement_bytes, description):
    pos = data.find(target_bytes)
    if pos != -1:
        data[pos:pos+len(target_bytes)] = replacement_bytes
        print(f"{description} 已从 {target_bytes.hex()} 修改为 {replacement_bytes.hex()}，位于地址 {pos:#06x}")
        return True
    else:
        print(f"警告: 未找到 {description}: {target_bytes.hex()}")
        return False

def convert_pid_vid(pid_vid_str):
    parts = pid_vid_str.split(':')
    if len(parts) != 2 or any(len(part) != 4 for part in parts):
        raise ValueError("PID/VID 格式不正确，应为 'XXXX:YYYY'")
    
    pid = int(parts[0], 16)
    vid = int(parts[1], 16)
    
    packed = struct.pack('<HH', pid, vid)
    return packed.hex().upper()

def modify_bin(bin_path, output_bin_path, old_vid_pid, new_vid_pid, old_string, new_string, old_string2, new_string2):
    with open(bin_path, 'rb') as f:
        data = bytearray(f.read())

    # 修改VID和PID，使用查找方式
    old_vid_pid_bytes = bytes.fromhex(old_vid_pid)
    new_vid_pid_bytes = bytes.fromhex(new_vid_pid)
    find_and_modify(data, old_vid_pid_bytes, new_vid_pid_bytes, "VID和PID")

    # 修改第一个字符串
    old_string_bytes = old_string.encode('ascii')
    new_string_bytes = new_string.encode('ascii').ljust(len(old_string_bytes), b' ')
    find_and_modify(data, old_string_bytes, new_string_bytes, f"字符串 '{old_string}'")

    # 修改第二个字符串
    old_string2_bytes = old_string2.encode('ascii')
    new_string2_bytes = new_string2.encode('ascii').ljust(len(old_string2_bytes), b' ')
    find_and_modify(data, old_string2_bytes, new_string2_bytes, f"字符串 '{old_string2}'")

    # 将修改后的数据写回二进制文件
    with open(output_bin_path, 'wb') as f:
        f.write(data)

if __name__ == "__main__":
    # 定义所有需要修改的值，并进行转换
    old_vid_pid_input = "0483:572b"  # 原始VID和PID，用户提供的格式
    new_vid_pid_input = "17ef:6099"  # 新的VID和PID，用户提供的格式
    
    try:
        old_vid_pid = convert_pid_vid(old_vid_pid_input)
        new_vid_pid = convert_pid_vid(new_vid_pid_input)
    except ValueError as e:
        print(e)
        exit(1)

    old_string = 'OrayKVM Mouse Keyboard'    # 原始字符串
    new_string = 'Lenovo Wired Keyboard '    # 新字符串
    old_string2 = 'STMicroelectronics'      # 原始字符串2
    new_string2 = 'LiteOn            '      # 新字符串2

    print(f"原始VID和PID: {old_vid_pid_input} -> {old_vid_pid}")
    print(f"新的VID和PID: {new_vid_pid_input} -> {new_vid_pid}")

    # 转换HEX到BIN，并获取最大地址
    max_address = hex_to_bin('oray_mcu_firmware.txt', 'temp.bin')

    if max_address is not None:
        # 修改BIN文件中的VID、PID和字符串
        modify_bin(
            'temp.bin',
            'modified.bin',
            old_vid_pid,
            new_vid_pid,
            old_string,
            new_string,
            old_string2,
            new_string2
        )

        # 再次转换BIN到HEX，同时添加原始特殊记录
        bin_to_hex_with_special_records('modified.bin', 'output.hex')

        print("所有操作已完成，请检查生成的HEX文件。")
    else:
        print("无法继续，因为HEX文件转换失败。")

