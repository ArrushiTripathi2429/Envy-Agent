import platform
import subprocess
from skills.registry import skill

APP_ALIASES = {
    "Windows": {"chrome": "chrome", "notepad": "notepad", "calculator": "calc", "vscode": "code"},
    "Darwin":  {"chrome": "Google Chrome", "notes": "Notes", "calculator": "Calculator", "vscode": "Visual Studio Code"},
    "Linux":   {"chrome": "google-chrome", "calculator": "gnome-calculator", "vscode": "code"},
}

@skill("open_app")
def open_app(name: str) -> str:
    system = platform.system()
    target = APP_ALIASES.get(system, {}).get(name.lower().strip())
    if target is None:
        return f"I don't know an app called '{name}'."
    try:
        if system == "Windows":
            subprocess.Popen(["cmd", "/c", "start", "", target])
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", target])
        else:
            subprocess.Popen([target])
        return f"Opening {name}."
    except Exception as e:
        return f"Couldn't open {name}: {e}"