import builtins
import json
import os
import re
from pathlib import Path
from typing import Any, TypeVar, cast

import yaml

T = TypeVar("T")


def read_file(filepath: Path) -> dict[str, Any]:
    """Read JSON or YAML file and expand any environment variables.

    :param filepath: A JSON or YAML file with model data.
    :returns: File content as dict with environment variables expanded.
    """
    filepath = filepath.resolve(strict=True)
    if filepath.suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(filepath.read_text(encoding="utf-8"))
    elif filepath.suffix == ".json":
        data = json.loads(filepath.read_text(encoding="utf-8"))
    else:
        raise ValueError(f"Invalid file extension: {filepath.suffix}.")

    # expand environment variables
    return expand_env_vars(data)


def _expand_windows_style_vars(value: str) -> str:
    """Expand Windows-style %NAME% environment variables on any platform."""

    pattern = re.compile(r"%([^%]+)%")

    def replace(match: re.Match) -> str:  # type: ignore[type-arg]
        """Replace matched environment variable with its value."""
        return os.environ.get(match.group(1), match.group(0))

    return pattern.sub(replace, value)


def expand_env_vars(value: T) -> T:
    """Return the input with environment variables expanded. This applies to (nested) string fields. Substrings of the
    form $name or ${name} are replaced by the value of environment variable name. Malformed variable names and
    references to non-existing variables are left unchanged.

    On Windows, %name% expansions are supported in addition to $name and ${name}.

    Example:

        >>> expand_env_vars({"x": [1, 2, "${USER}"]})
        {'x': [1, 2, 'my-username']}

    :param value: Input object to search for environment variables.
    :returns: The same type as input.
    """
    if isinstance(value, dict):
        # recursive call for dicts and nested dicts
        return cast(T, {k: expand_env_vars(v) for k, v in value.items()})

    if isinstance(value, list | tuple | builtins.set):
        # recursive call for sequences and nested sequences
        return cast(T, type(value)([expand_env_vars(v) for v in value]))

    if isinstance(value, str):
        # actual environment variable expansion

        # First expand POSIX-style vars ($NAME or ${NAME})
        expanded = os.path.expandvars(value)
        # Then expand Windows-style vars (%NAME%)
        expanded = _expand_windows_style_vars(expanded)
        return cast(T, expanded)

    # otherwise do nothing and return the value
    return value


def parse_query_and_args(args):
    """
    Parse command arguments into query and additional arguments.
    
    Format: query text -- key value key value
    
    Returns:
        tuple: (query_string, args_dict)
    """
    if not args:
        return "", {}
    
    # Convert all args to strings and join
    str_args = [str(arg) for arg in args]
    full_text = " ".join(str_args)
    
    # Split on -- to separate query from additional args
    if " -- " in full_text:
        query_part, args_part = full_text.split(" -- ", 1)
        query = query_part.strip()
        
        # Parse additional arguments as key-value pairs
        args_dict = {}
        if args_part.strip():
            arg_tokens = args_part.split()
            for i in range(0, len(arg_tokens), 2):
                if i + 1 < len(arg_tokens):
                    key = arg_tokens[i]
                    value = arg_tokens[i + 1]
                    args_dict[key] = value
        
        return query, args_dict
    else:
        # No -- separator, everything is query
        return full_text.strip(), {}
