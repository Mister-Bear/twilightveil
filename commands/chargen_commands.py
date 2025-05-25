from evennia import Command

# Define categories and their abilities
TALENTS = {"alertness", "athletics", "awareness", "brawl", "empathy", "expression", "intimidation", "leadership", "streetwise", "subterfuge"}
SKILLS = {"animal ken", "crafts", "drive", "etiquette", "firearms", "melee", "performance", "security", "stealth", "survival"}
KNOWLEDGES = {"academics", "computer", "finance", "investigation", "law", "linguistics", "medicine", "occult", "politics", "science"}

CATEGORY_LIMITS = {
    "talents": 13,
    "skills": 9,
    "knowledges": 5,
}

def categorize(ability):
    if ability in TALENTS:
        return "talents"
    if ability in SKILLS:
        return "skills"
    if ability in KNOWLEDGES:
        return "knowledges"
    return None

class CmdSetAbility(Command):
    """
    Sets an ability rating during character generation.

    Usage:
        +setability <ability> = <rating>
    """

    key = "+setability"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller

        # Check chargen flag or staff override
        flag = caller.attributes.get("is_chargen", default=False)
        if not (flag or caller.locks.check_lockstring(caller, "perm(Builder)")):
            caller.msg("|rYou are not in character generation. This command is disabled.|n")
            return

        if not self.args or "=" not in self.args:
            caller.msg("Usage: +setability <ability> = <rating>")
            return

        ability, value = [a.strip().lower() for a in self.args.split("=", 1)]

        try:
            value = int(value)
        except ValueError:
            caller.msg("|rRating must be a number.|n")
            return

        if not (0 <= value <= 3):
            caller.msg("|rDuring chargen, ability ratings must be between 0 and 3.|n")
            return

        category = categorize(ability)
        if not category:
            caller.msg("|rUnknown ability: '{}'. Make sure it's a valid WoD ability.|n".format(ability.title()))
            return

        # Calculate current total for this category
        abilities = caller.db.abilities or {}
        new_total = value
        for ab, val in abilities.items():
            if categorize(ab) == category and ab != ability:
                new_total += val

        if new_total > CATEGORY_LIMITS[category]:
            caller.msg(f"|rYou've exceeded the maximum {CATEGORY_LIMITS[category]} dots in {category.title()}. "
                       f"Current total would be {new_total}.|n")
            return

        abilities[ability] = value
        caller.db.abilities = abilities

        caller.msg(f"|gSet {ability.title()} to {value} dots in {category.title()}.|n")
