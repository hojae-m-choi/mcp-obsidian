import importlib.resources
import yaml

_spec = None


def _load() -> dict:
    global _spec
    if _spec is None:
        try:
            ref = importlib.resources.files("mcp_obsidian").joinpath("openapi.yaml")
            with importlib.resources.as_file(ref) as path:
                with open(path) as f:
                    _spec = yaml.safe_load(f)
        except Exception:
            _spec = {}
    return _spec


def get_patch_parameters() -> dict:
    """Return {header-name: parameter-dict} for the PATCH /vault/{filename} endpoint."""
    spec = _load()
    try:
        params = spec["paths"]["/vault/{filename}"]["patch"]["parameters"]
        return {p["name"]: p for p in params}
    except (KeyError, TypeError):
        return {}
