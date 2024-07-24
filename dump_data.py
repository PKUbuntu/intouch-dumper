""" Dump the data from the lgh file """

import datetime
import struct

# 从字符数组中获取 8 bytes 长的 Win 格式时间戳
def get_time_from_bytes(bytes: bytes) -> datetime:
    # 字节转整数
    seconds_since_epoch = int.from_bytes(bytes, byteorder='little')

    # 整数表示的秒数
    seconds_since_epoch = seconds_since_epoch / 10000000

    # 将秒数转换为 UTC 时间
    utc_time = datetime.datetime.utcfromtimestamp(seconds_since_epoch)
    utc_time = datetime.datetime(1601, 1, 1) + datetime.timedelta(seconds=seconds_since_epoch)
    return utc_time


# Open binary file "./data/24072300.lgh"
with open("./data/24072300.lgh", "rb") as f:
    # 512 字节作为 block 单元
    content = f.read(512)
    while content:
        if content[:4].hex() in ['ec130300', 'ec130200', 'ec130100']:
            # 将后 [4:8] 字节作为整数读取 --> 
            num_record = int.from_bytes(content[4:8], byteorder='little')
            op_time = get_time_from_bytes(content[8:16])
            # 从后面的 40 字节中读取 tag 名称
            tag_name = content[16:56].decode('utf-8').strip('\x00')
            
            records_remains = num_record

            # 数据起始的偏移位置
            records_offset = 56

            while records_remains > 0:
                # 读取 8 字节的整数 timestamp
                timestamp = get_time_from_bytes(content[records_offset:records_offset+8])

                # 读取 8 字节的浮点数 value
                value = struct.unpack('<d', content[records_offset+8:records_offset+16])[0]
                
                records_offset += 16
                records_remains -= 1

                if content[:4].hex() == 'ec130300':
                    print(f'{tag_name}\t\t{value:.2f}\t{timestamp}')    
                else:
                    # int / bool , 截断小数部分即可
                    print(f'{tag_name}\t\t{value:.0f}\t{timestamp}')

                # value_average = struct.unpack('<d', content[records_offset:records_offset+8])[0]
            print(f'\t\t----- Above are {num_record} records -----\n')
                

        content = f.read(512)
