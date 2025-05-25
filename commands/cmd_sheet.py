from evennia import Command

# Ability categories
TALENTS = ["alertness", "athletics", "awareness", "brawl", "empathy", "expression", "intimidation", "leadership", "streetwise", "subterfuge"]
SKILLS = ["animal ken", "crafts", "drive", "etiquette", "firearms", "melee", "performance", "security", "stealth", "survival"]
KNOWLEDGES = ["academics", "computer", "finance", "investigation", "law", "linguistics", "medicine", "occult", "politics", "science"]

PHYSICAL = ["strength", "dexterity", "stamina"]
SOCIAL = ["charisma", "manipulation", "appearance"]
MENTAL = ["perception", "intelligence", "wits"]

CATEGORY_LIMITS = {
    "Talents": 13,
    "Skills": 9,
    "Knowledges": 5,
}

def dotline(value, max_dots=5):
    filled = "*" * value
    empty = "-" * (max_dots - value)
    return filled + empty

def format_columnar_traits(traits_dict, label=None):
    if not traits_dict:
        return f"|w{label}|n\n  None"
    keys = sorted(traits_dict.keys())
    left = keys[::2]
    right = keys[1::2]
    output = [f"|w{label}|n"]
    for l, r in zip(left, right + [""]):
        left_txt = f"{l.title():<15}: {dotline(traits_dict[l])}" if l else ""
        right_txt = f"{r.title():<15}: {dotline(traits_dict[r])}" if r else ""
        output.append(f"{left_txt:<30} {right_txt:<30}")
    return "\n".join(output)

def gather_traits(source, keys):
    return {key: source.get(key, 0) for key in keys if source.get(key, 0) > 0}

class CmdSheet(Command):
    """
    View your character sheet.

    Usage:
        +sheet
    """
    key = "+sheet"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller

        # Character identity block
        name = caller.key
        clan = caller.db.clan or "-"
        concept = caller.db.concept or "-"
        nature = caller.db.nature or "-"
        demeanor = caller.db.demeanor or "-"

        abilities = caller.db.abilities or {}
        attributes = caller.db.attributes or {}
        disciplines = caller.db.disciplines or {}
        backgrounds = caller.db.backgrounds or {}
        virtues = caller.db.virtues or {}

        output = [
            f"|cCharacter Sheet: {name}|n",
            "-" * 60,
            f"|wClan     :|n {clan:<15} |wConcept :|n {concept}",
            f"|wNature   :|n {nature:<15} |wDemeanor:|n {demeanor}",
            "-" * 60,
            format_columnar_traits(gather_traits(attributes, PHYSICAL + SOCIAL + MENTAL), "Attributes"),
            "",
            format_columnar_traits(gather_traits(abilities, TALENTS + SKILLS + KNOWLEDGES), "Abilities"),
            "",
            format_columnar_traits(disciplines, "Disciplines"),
            "",
            format_columnar_traits(backgrounds, "Backgrounds"),
            "",
            format_columnar_traits(virtues, "Virtues"),
            "-" * 60,
        ]

        caller.msg("\n".join(output))
