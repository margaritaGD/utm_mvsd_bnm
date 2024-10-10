from pathlib import Path


class LLMUtils:
    assistant_id = "asst_ZtVaE6uARJSHjrorD2sEBzMe"


class LLMModels:
    gpt_4 = "gpt-4"
    gpt_4o = "gpt-4o"
    gpt_4o_mini = "gpt-4o-mini"
    o1_preview = "o1-preview"


class PathUtils:
    _PROJECT_DIR = Path(__file__).resolve().parent.parent.parent.parent
    _SRC_DIR = _PROJECT_DIR / "src"
    _MAIN_DIR = _SRC_DIR / "main"
    DOT_ENV_FILE = _MAIN_DIR / ".env"
    RESOURCES_DIR = _MAIN_DIR / "resources"
