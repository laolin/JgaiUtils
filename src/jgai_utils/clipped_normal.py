# Copyright (c) 2026 laolin. See LICENSE for details.

def clipped_normal(mean:float, std:float, low:float, high:float, size:int, around:int=2):
    try:
        import numpy as np
        from scipy.stats import truncnorm
    except ImportError as exc:
        raise ImportError("clipped_normal requires numpy and scipy") from exc

    if std <= 0:
        return np.full(size, mean)
    a = (low - mean) / std
    b = (high - mean) / std
    return np.around(truncnorm.rvs(a, b, loc=mean, scale=std, size=size), around)
