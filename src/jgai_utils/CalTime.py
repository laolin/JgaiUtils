# Copyright (c) 2026 laolin. See LICENSE for details.

import time
from typing import Optional

class CalTime:
    """
    CalTime 用于返回一个表示过了多长时间的字符串    
    """ 
    def __init__(self,en=True):
        self.en=en
        self.reset()
    def reset(self):
        self._t0=time.time()
    def set_en(self):
        self.en=True
    def set_cn(self):
        self.en=False

        
    def use(self, en: Optional[bool] = None) -> str:
        """获取从初始化(或上次重置)到当前经过的时间时长。
        
        Args:
            en (bool, optional): 指定输出语言。
                - True: 英文输出 (如 1hr2min)
                - False: 中文输出 (如 1小时2分钟)
                - None: 默认值，沿用上一次的语言设置。
                
        Returns:
            str: 格式化后的时长字符串
        """
        # 1. 计算总秒数
        seconds = time.time() - self._t0

        # 2. 处理语言状态
        if en is not None:
            self.en = en
            
        # 注意：这里必须判断 self.en，而不是局部变量 en
        if self.en:
            dy, hr, mn, sec = 'd', 'hr', 'min', 's'
        else:
            dy, hr, mn, sec = '天', '小时', '分', '秒'

        # 3. 如果时间很短（小于1分钟），保留小数并直接返回
        if seconds < 60:
            return f"{seconds:.1f}{sec}" if seconds > 10 else f"{seconds:.2f}{sec}"

        # 4. 使用 divmod 优雅地计算天、时、分、秒
        # divmod(a, b) 返回一个包含商和余数的元组 (a // b, a % b)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)

        # 5. 根据时间长短进行格式化输出
        if d > 0:
            return f"{int(d)}{dy}{int(h)}{hr}{int(m)}{mn}{s:.0f}{sec}"
        elif h > 0:
            return f"{int(h)}{hr}{int(m)}{mn}{s:.0f}{sec}"
        else:
            return f"{int(m)}{mn}{s:.0f}{sec}"
