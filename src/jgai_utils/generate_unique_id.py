# Copyright (c) 2026 laolin. See LICENSE for details.

import os
import platform  
import hashlib
import time,threading,uuid

_lock = threading.Lock()
_last_timestamp = None
_sequence = 0
def _to_base36(n, length):
    """将整数 n 转为指定长度的 base36 字符串（小写，左补0）"""
    BASE36 = "0123456789abcdefghijklmnopqrstuvwxyz"
    s = ""
    while n:
        s = BASE36[n % 36] + s
        n //= 36
    s = s or "0"
    return s.rjust(length, "0")[-length:]


# 生成机器指纹（尽量唯一）
def generate_machine_id(n=4,mac=True,rnd=False):
    # 组合多个本地信息
    machine_info = (
        platform.system()  # Windows/Linux/Darwin
        + platform.release()  # 内核版本
        + platform.machine()  # x86_64, arm64 等
        + platform.node()  # 主机名
        + platform.processor()  # 可能为空，但无妨
    )
    if mac:
        machine_info += str(uuid.getnode())
    if rnd:
        machine_info += str(os.getpid())+ str(os.urandom(8))  # 加点随机性避免完全相同环境重复

    # 取 hash 的低16位（对应36^4 ≈ 1.6M，16位足够）
    hash_val = int(hashlib.sha1(machine_info.encode()).hexdigest()[:8], 16)
    machine_id = hash_val % (36**4)
    return _to_base36(machine_id,n)

def generate_unique_id(n_ms=3, n_seq=2, n_machine=3, zip_year_month=True):
    global _last_timestamp, _sequence

    # 为提高效率，不检查
    # if n_ms<2:
    #     n_ms = 2
    # if n_ms >4: #  36**4 > 60,000 用来表示毫秒最多4位就够了
    #     n_ms = 4
    # if n_seq<1:
    #     n_seq=1

    fc_ms=pow(36,n_ms)//60  #秒小数放大此倍数后取整
    with _lock:
        # 获取当前时间
        now = time.time()
        timetuple = time.localtime(now)

        # 2位 年，月，
        year_month = (timetuple.tm_year - 2025) * 12 + timetuple.tm_mon
        ym_part = _to_base36(year_month, 2)

        # 6位：DDHHMM
        time_part = time.strftime("%d%H%M", timetuple)

        # xx.xxx秒
        ms10 = int(((now - int(now)) + int(now) % 60) * fc_ms)
        # xx.xxx秒部分（n_ms位数字）
        ms_part = _to_base36(ms10, n_ms)

        current_ts = ym_part+time_part + ms_part  # 12位：时间

        if current_ts == _last_timestamp:
            _sequence = (_sequence + 1) % (36**n_seq)
        else:
            _sequence = 0
            _last_timestamp = current_ts

        # 机器ID（n_machine位base36）
        machine_part = generate_machine_id(n_machine)
        # 序列号（n_seq位base36）
        seq_part = _to_base36(_sequence, n_seq)

        return ym_part + time_part + ms_part + seq_part + machine_part


if __name__ == "__main__":
    print("machine_id =", generate_machine_id(6))
    for i in range(37):
        print(f' {i} uid =',generate_unique_id(n_ms=2,n_machine=2,n_seq=2))
    print("OK")
