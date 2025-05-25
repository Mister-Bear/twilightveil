from evennia import Command

# Attribute groups
PHYSICAL = {"strength", "dexterity", "stamina"}
SOCIAL = {"charisma", "manipulation", "appearance"}
MENTAL = {"perception", "intelligence", "wits"}

CATEGORY_LIMITS = {
    "physical": 7,
    "social": 5,
    "mental": 3,
}

def categorize(attr):
    if attr in PHYSICAL:
        return "physical"
    if attr in SOCIAL:
        return "social"
    if attr in MENTAL:
        return "mental"
    return None

class CmdSetAttr(Command):
    """
    Sets an attribute during character generation.

    Usage:
        +setattribute <attribute> = <value>
    """

    key = "+setattribute"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller

        if not self.args or "=" not in self.args:
            caller.msg("Usage: +setattribute <attribute> = <value>")
            return

        try:
            attr_raw, value_raw = self.args.split("=", 1)
            attr = attr_raw.strip().lower()
            value = int(value_raw.strip().strip("\"'"))
        except Exception as e:
            caller.msg("|rValue must be a number.|n")
            caller.msg(f"(DEBUG: {e})")
            return

        if not (1 <= value <= 5):
            caller.msg("|rDuring chargen, attributes must be between 1 and 5 dots.|n")
            return

        category = categorize(attr)
        if not category:
            caller.msg(f"|r'{attr}' is not a valid attribute.|n")
            return

        flag = caller.attributes.get("is_chargen", default=False)
        is_allowed = flag or caller.locks.check_lockstring(caller, "perm(Builder)")

        if not is_allowed:
            caller.msg("|rYou are not in character generation. This command is disabled.|n")
            return

        attrs = caller.db.attributes or {}
        new_total = value
        for a, v in attrs.items():
            if categorize(a) == category and a != attr:
                new_total += v

        if new_total > CATEGORY_LIMITS[category]:
            caller.msg(f"|rToo many points in {category.title()} (limit: {CATEGORY_LIMITS[category]}). "
                       f"Current total would be {new_total}.|n")
            return

        attrs[attr] = value
        caller.db.attributes = attrs
        caller.msg(f"|gSet {attr.title()} to {value} dots in {category.title()}.|n")
