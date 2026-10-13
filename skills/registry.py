SKILLS = {}

def skill(name):
    def decorator(func):
        SKILLS[name] = func
        return func
    return decorator

def run_skill(skill_name, /, **kwargs):
    if skill_name not in SKILLS:
        return f"Unknown skill: {skill_name}"
    return SKILLS[skill_name](**kwargs) 