# ENVY AGENT

**A Siri-style voice assistant for your laptop.** Say "open Chrome" and it opens Chrome.

Envy listens to your voice, turns speech into text with [Whisper](https://github.com/SYSTRAN/faster-whisper), figures out what you want, and runs the matching action on your computer. It is built from small, swappable parts so each stage (speech recognition, intent understanding, actions) can be improved independently.

> **Status:** early development. The core pipeline works end to end (voice or text → intent → open an app). See the [roadmap](#roadmap) for what is done and what is next.

---

## How it works

```
 ┌────────────┐   ┌────────────────┐   ┌───────────────┐   ┌──────────────────┐   ┌──────────┐
 │ Microphone │ → │ Speech-to-text │ → │ Intent router │ → │ Action executor  │ → │ Feedback │
 │  (record)  │   │   (Whisper)    │   │ (text → skill)│   │ (skill registry) │   │  (reply) │
 └────────────┘   └────────────────┘   └───────────────┘   └──────────────────┘   └──────────┘
```

1. **Listen**: records audio from the microphone (16 kHz, mono).
2. **Transcribe**: [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) converts the audio to text, fully offline after the first model download.
3. **Understand**: the router maps text like `"open chrome"` to a skill name and arguments: `open_app` + `{"name": "chrome"}`.
4. **Act**: the skill registry looks up the skill by name and runs it. For `open_app`, that means asking the operating system to start the program.
5. **Respond**: the result is printed (text-to-speech is planned).

### The skill registry

Every capability is a plain Python function registered with a decorator. Adding a new skill means writing one function:

```python
from skills.registry import skill

@skill("tell_time")
def tell_time() -> str:
    from datetime import datetime
    return datetime.now().strftime("It is %I:%M %p.")
```

The router only needs to return `("tell_time", {})`, and the registry takes care of the rest. The router and the skills never import each other directly, so either side can change without breaking the other.

---

## Getting started

### Requirements

- Python 3.10 or newer
- A working microphone
- Windows (primary target). macOS and Linux branches exist in `skills/apps.py` but are less tested.
- Internet access on first run only, to download the Whisper model (~140 MB for `base`)

### Installation

```bash
git clone https://github.com/ArrushiTripathi2429/Envy-Agent.git
cd Envy-Agent

python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

> If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process RemoteSigned` and try again.

### Run

```bash
python main.py
```

- Press **Enter** to speak. Envy records for 4 seconds, then runs your command.
- Or **type** a command directly, for example `open notepad`.
- Type `quit` to exit.

Example session:

```
Envy ready. Enter = bolo, ya type karo. 'quit' = exit.
You (Enter = speak):
Listening for 4s... bolo!
Envy ne suna: Open Chrome.
Envy: Opening chrome.
```

### Microphone not working?

On Windows, go to **Settings → Privacy & security → Microphone** and enable *Let desktop apps access your microphone*.

---

## Supported commands

| Command                              | What it does              |
| ------------------------------------ | ------------------------- |
| `open chrome` / `launch chrome`      | Opens Google Chrome       |
| `open notepad`                       | Opens Notepad             |
| `open calculator`                    | Opens Calculator          |
| `open vscode`                        | Opens Visual Studio Code  |

App names are mapped to real executables in `APP_ALIASES` inside `skills/apps.py`. To teach Envy a new app, add one line there.

---

## Project structure

```
envy/
├── main.py              # main loop: input → parse → run skill
├── config.yaml          # settings (model size, aliases) — in progress
├── audio/
│   └── listener.py      # microphone recording
├── stt/
│   └── whisper_stt.py   # speech-to-text (faster-whisper)
├── brain/               # intent router (rules, then LLM) — in progress
├── skills/
│   ├── registry.py      # @skill decorator + run_skill()
│   └── apps.py          # open_app skill
├── tts/                 # text-to-speech — planned
├── core/                # safety checks, logging — planned
└── tests/               # planned
```

---

## Roadmap

- [x] Skill registry with decorator-based registration
- [x] `open_app` skill (Windows, with macOS/Linux branches)
- [x] Push-to-talk voice input
- [x] Speech-to-text with Whisper (offline)
- [ ] Rule-based intent router with typo tolerance (regex + fuzzy matching)
- [ ] More skills: volume, brightness, screenshot, web search, open files
- [ ] LLM tool-calling fallback for flexible phrasing
- [ ] Text-to-speech replies
- [ ] Voice activity detection (stop recording when you stop talking)
- [ ] Wake word ("Hey Envy")
- [ ] Safety layer: confirmation for risky actions like shutdown or delete
- [ ] Hinglish voice commands
- [ ] Command logging and latency metrics
- [ ] Tests

---

## Design notes

- **Text first, voice on top.** The same `parse → run_skill` path handles typed and spoken commands, which makes debugging easy: if a command fails by voice, try typing it.
- **Skills never crash.** Every skill catches its own errors and returns a message, so one bad command cannot take the assistant down.
- **Non-blocking launches.** Apps are started with `subprocess.Popen`, so Envy keeps listening while Chrome runs.
- **Normalised text.** Whisper returns text like `"Open Chrome."` (capitalised, with punctuation), so input is lowercased and stripped before matching.

---

## Tech stack

- Python
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) for speech recognition
- [sounddevice](https://python-sounddevice.readthedocs.io/) and NumPy for audio capture
- Standard library: `subprocess`, `platform`

---

## Author

Built by [Arushi](https://github.com/ArrushiTripathi2429) as a learning-by-building project in speech systems and agentic AI.
