# Copyright (c) 2026 laolin. See LICENSE for details.


def str_by_ints(tName:str, tIdx:int, *ints: int):
    """
    生成名称，支持不定长的索引参数。
    用法: str_by_ints("Beam", 1, 0, 2, 3) -> "Beam1_0_2_3"
    """
    # 基础名称部分 (tName 和 tIdx 之间没有下划线)
    base_name = f"{tName}{tIdx}"
    
    # 过滤掉小于 0 的索引，并转换为字符串列表
    # 如果你希望保留 0，只需判断 i >= 0
    valid_indices = [str(i) for i in ints if i >= 0]
    
    # 如果有有效索引，用下划线连接；否则直接返回基础名称
    if valid_indices:
        return f"{base_name}_{'_'.join(valid_indices)}"
    return base_name

if __name__ == "__main__":
    print(1, str_by_ints('node', 1,2,3))
