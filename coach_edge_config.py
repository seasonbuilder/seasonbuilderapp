"""Small, framework-independent helpers for Coach Edge launch configuration."""


TRUE_VALUES = {"true", "1", "yes", "y", "on"}
FALSE_VALUES = {"false", "0", "no", "n", "off"}


def parse_bool_parameter(value, *, default: bool = False) -> bool:
    """Parse a URL/environment boolean while safely preserving a launcher default."""
    if value is None:
        return default

    normalized = str(value).strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    return default
