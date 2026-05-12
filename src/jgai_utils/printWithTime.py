# Copyright (c) 2026 laolin. See LICENSE for details.

from datetime import datetime

def printWithTime(*args, **kwargs):
    # 使用 pop 一步完成获取和删除，如果不存在则返回空字符串
    begin_val = kwargs.pop('begin', '')
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    # 强制加上 flush=True，专治进度条光标乱跳和显示延迟
    kwargs['flush'] = True
    # 将前缀和时间戳拼接后作为第一个参数打印
    print(f"{begin_val}{timestamp}", *args, **kwargs)

if __name__ == "__main__":
    printWithTime("Start")
    printWithTime("hellllo", 10, 3.14, [1, 2, 3], (5, 6, 7))

    printWithTime("abc,", end=" ")
    printWithTime("DEF,", end="")
    print("Ghi.")

    printWithTime("123,", end="")
    print("456.", end="")
    print("789!")
    printWithTime("End")
