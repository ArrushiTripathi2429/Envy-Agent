from skills.registry import run_skill
import skills.apps  # noqa: F401  (import karne se decorators run hote hain)

def parse(text: str):
    text = text.lower().strip()
    for verb in ("open ", "launch ", "start "):
        if text.startswith(verb):
            return "open_app", {"name": text[len(verb):]}
    return None, {}

def main():
    print("Envy ready. Type 'quit' to exit.")
    while True:
        text = input("You: ")
        if text.strip().lower() in ("quit", "exit"):
            break
        skill_name, args = parse(text)
        if skill_name is None:
            print("Envy: Sorry, samajh nahi aaya.")
            continue
        print("Envy:", run_skill(skill_name, **args))

if __name__ == "__main__":
    main()