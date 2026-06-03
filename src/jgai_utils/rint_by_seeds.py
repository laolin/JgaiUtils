# Copyright (c) 2026 laolin. See LICENSE for details.

import zlib

def rint_by_seeds(valueMax:int, *seedList):
    """
    根据seedList生成可复现的[0, iMax)随机整数
    """
    # 将所有种子转为字符串并拼接
    seed_str = "jgai"+"!".join(str(s) for s in seedList)        
    # zlib.crc32 返回一个固定的 32 位无符号整数
    hash_val = zlib.crc32(seed_str.encode('utf-8'))      
    return hash_val % (valueMax if valueMax>0 else (2**32-1))

if __name__ == "__main__":
    print(1, rint_by_seeds(100, 1,2,3))
    print(2, rint_by_seeds(200, 4,5,6,7,8,))
    print(3, rint_by_seeds(300))
    print(4, rint_by_seeds(400, 1,'aabbcc',[1,2,3],print))  # 可用任意变量做种子

    print(5, rint_by_seeds(100, 1,2,3))  # 可复现第1行的结果
    print(6, rint_by_seeds(300))  # 可复现第3行的结果
    print(7, rint_by_seeds(400, 1,'aabbcc',[1,2,3],print))  # 可复现第4行结果

    print(0, rint_by_seeds(0, 1,2,3))
