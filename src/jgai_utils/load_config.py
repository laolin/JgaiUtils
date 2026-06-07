# Copyright (c) 2026 laolin. See LICENSE for details.
import json
import os
import sys
from collections.abc import Mapping, Sequence

try:
    import tomllib as toml  # type: ignore
except ImportError:
    try:
        import tomli as toml
    except ImportError as exc:
        raise ImportError("Please install tomli first: pip install tomli") from exc

from .printWithTime import printWithTime


def _normalize_config_files(config_file):
    if isinstance(config_file, (str, bytes, os.PathLike)):
        return [os.fspath(config_file)]
    if isinstance(config_file, Sequence):
        return [os.fspath(item) for item in config_file]
    return [os.fspath(config_file)]


def _merge_dict(base, extra):
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _merge_dict(base[key], value)
        else:
            base[key] = value
    return base


def _config_path(config_filename, base_dir, suffix):
    if not config_filename.endswith(suffix):
        config_filename += suffix
    if os.path.isabs(config_filename):
        return config_filename
    return os.path.join(base_dir, config_filename)


def load_config(
    toml_file="config",
    json_file=None,
    override_config=None,
    info: str = "",
    bar="-",
    width=60,
    base_dir=None,
    verbose=True,
):
    """Load TOML, optional JSON, and optional runtime configuration.

    `toml_file` supports one file or a sequence of files. Files are merged into a
    single dict in the given order. If `json_file` is provided, it is merged after
    TOML files, so JSON values override TOML values. If `override_config` is
    provided, it is merged last and has the highest priority.

    Args:
        toml_file (str | Sequence[str], optional): TOML config file path(s).
            A missing `.toml` suffix is added automatically.
        json_file (str | None, optional): Optional JSON config file path. A
            missing `.json` suffix is added automatically.
        override_config (dict | None, optional): Runtime config values merged
            after TOML and JSON.
        info (str, optional): Optional title printed before loading.
        bar (str, optional): Fill character for the title line.
        width (int, optional): Width for the title line.
        base_dir (str | os.PathLike | None, optional): Base directory for
            relative config paths. Defaults to the main script directory.
        verbose (bool, optional): Print loaded-file messages when True.

    Returns:
        dict: Merged configuration values.
    """
    if len(info) > 0:
        print(f"[+]{f' {info} ':{bar}^{width}}[+]")

    if base_dir is None:
        main_script_path = os.path.abspath(sys.argv[0])
        base_dir = os.path.dirname(main_script_path)
    else:
        base_dir = os.fspath(base_dir)

    config_dict = {}

    for config_filename in _normalize_config_files(toml_file):
        config_path = _config_path(config_filename, base_dir, ".toml")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"TOML config file not found: {config_path}")

        try:
            with open(config_path, "rb") as f:
                _merge_dict(config_dict, toml.load(f))
            if verbose:
                printWithTime(f"Config [ {config_filename} ] Loaded.")
        except Exception as exc:
            raise RuntimeError(f"Read or parse TOML error: {config_path}") from exc

    if json_file is not None:
        json_filename = os.fspath(json_file)
        json_path = _config_path(json_filename, base_dir, ".json")
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"JSON config file not found: {json_path}")

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
            _merge_dict(config_dict, json_data)
            if verbose:
                printWithTime(f"Config [ {json_filename} ] Loaded.")
        except Exception as exc:
            raise RuntimeError(f"Read or parse JSON error: {json_path}") from exc

    if override_config is not None:
        if not isinstance(override_config, Mapping):
            raise TypeError("override_config must be a dict-like mapping")
        _merge_dict(config_dict, dict(override_config))

    return config_dict


if __name__ == "__main__":
    cfg = load_config(info=" Config Load Test ")
    print(cfg)
