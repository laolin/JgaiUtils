#Copyright (c) 2026 laolin. See LICENSE for details.

import numpy as np
from scipy.stats import truncnorm as _tr 

# 生成截断正态分布随机数
def truncnorm(mean,std,lower,upper,n,n_round=2):

    # 计算标准正态分布的截断边界
    a = (lower - mean) / std
    b = (upper - mean) / std

    return np.around(_tr.rvs(a, b, loc=mean, scale=std, size=n), n_round)