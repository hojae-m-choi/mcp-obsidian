import importlib.resources
import os
import requests
import yaml

_spec = None


def _fetch_live() -> dict:
    api_key = os.getenv("OBSIDIAN_API_KEY", "")
    protocol = os.getenv("OBSIDIAN_PROTOCOL", "https").lower()
    host = os.getenv("OBSIDIAN_HOST", "127.0.0.1")
    port = os.getenv("OBSIDIAN_PORT", "27124")
    url = f"{protocol}://{host}:{port}/openapi.yaml"
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {api_key}"},
        verify=False,
        timeout=(3, 6),
    )
    response.raise_for_status()
    return yaml.safe_load(response.text)


def _load_bundled() -> dict:
    ref = importlib.resources.files("mcp_obsidian").joinpath("openapi.yaml")
    with importlib.resources.as_file(ref) as path:
        with open(path) as f:
            return yaml.safe_load(f)


def _load() -> dict:
    global _spec
    if _spec is None:
        try:
            _spec = _fetch_live()
        except Exception:
            try:
                _spec = _load_bundled()
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
