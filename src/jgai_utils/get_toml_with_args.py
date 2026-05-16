#Copyright (c) 2026 laolin. See LICENSE for details.
import os
import sys
import argparse

# 兼容 Python 3.11+ 的内置库，以及旧版本的 tomli

try:
    import tomllib as toml # type: ignore  # 忽略这一行的导入检查
except ImportError:
    try:
        import tomli as toml
    except ImportError:
        print("[!] 请先安装 tomli 库: pip install tomli")
        sys.exit(1)

from .printWithTime import printWithTime

def str2bool(v):
    """ 安全的布尔值转换函数，防止 argparse 解析出错 """
    if isinstance(v, bool):
        return v
    if str(v).lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    if str(v).lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    raise argparse.ArgumentTypeError('期待传入布尔值 (True/False, 1/0)')

def get_toml_with_args(info:str="",bar="-",width=60):
    """(1) 读 config.toml配置文件。
    (2) 对于配置中简单类型的配置值，会自动生成对应命令行参数，通过命令行参数 --key VAL 在运行时修改配置。 函数返回命令行更新后的配置。
    (3) 默认配置文件名为 和 .py 同目录下config.toml。 可以通过 --config test 指定别的toml配置文件。

    Args:
        info (str, optional): _description_. Defaults to "".

    Returns:
        dict:返回的配置值
    """
    if len(info)>0:
        print(f"[+]{f' {info} ':{bar}^{width}}[+]")

    # ==========================================
    # 阶段 1：临时解析器，仅用于抓取 --config
    # ==========================================
    init_parser = argparse.ArgumentParser(add_help=False)
    init_parser.add_argument("--config", type=str, default="config", help="指定 TOML 配置文件名 (可省略 .toml)")
    
    init_args, remaining_argv = init_parser.parse_known_args()

    # ==========================================
    # 阶段 2：定位并读取 TOML 配置文件
    # ==========================================
    config_filename = init_args.config
    
    # 自动补全 .toml 扩展名
    if not config_filename.endswith('.toml'):
        config_filename += '.toml'

    main_script_path = os.path.abspath(sys.argv[0])
    main_dir = os.path.dirname(main_script_path)    
    config_path = os.path.join(main_dir, config_filename)

    if not os.path.exists(config_path):
        print(f"[!] ERROR! FILE NOT FOUND: {config_filename}")
        sys.exit(1)
    config_dict = {}
    try:
        # TOML 解析器要求必须用二进制 'rb' 模式读取
        with open(config_path, "rb") as f:
            config_dict = toml.load(f)
        printWithTime(f"Cofing [ {config_filename} ] Loaded.")
    except Exception as e:
        print(f"[!] Read of parse TOML ERROR: {e}")
        sys.exit(1)

    # ==========================================
    # 阶段 3：创建正式解析器，并动态生成参数
    # ==========================================
    parser = argparse.ArgumentParser(description="JieGouAi Model")
    # 把 config 加回来，以便 -h 帮助文档中能正常显示
    parser.add_argument("--config", type=str, default="config", help="指定 TOML 配置文件名 (可省略 .toml)")

    cfg = {}  # 用于专门存放列表和字典
    for key, value in config_dict.items():
        # 分流逻辑：如果是列表或字典，存入暂存区，跳过 argparse
        if isinstance(value, (list, dict)):
            cfg[key] = value
            continue
            
        # 根据 TOML 严格的类型，动态分配给 argparse
        if isinstance(value, bool):
            parser.add_argument(f"--{key}", type=str2bool, default=value, help=f"[动态生成] bool 值")
        else:
            val_type = type(value) if value is not None else str
            parser.add_argument(f"--{key}", type=val_type, default=value, help=f"[动态生成] {val_type.__name__} 类型")

    # ==========================================
    # 阶段 4：执行最终解析与业务逻辑
    # ==========================================
    # 此时，如果用户在终端显式指定了参数（如 --n_xspan 10），它会覆盖 TOML 里的默认值
    args = parser.parse_args()

    cfg.update(vars(args))

    # 移除不需要传入核心运算逻辑的 config 字段
    if 'config' in cfg:
        del cfg['config']

    return cfg

if __name__ =="__main__":
    cfg=get_toml_with_args(' Toml Config Test ')
    print(cfg)