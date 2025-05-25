from evennia import Command

def safe_split_args(raw_args):
    """
    Splits arguments like: +setdiscipline auspex = 3
    Returns ('auspex', 3) or raises ValueError.
    """
    if "=" not in raw_args:
        raise ValueError("Missing '=' symbol.")
    name, value = raw_args.split("=", 1)
    name = name.strip().lower()
    value = int(value.strip().strip("'\""))  # Remove quotes and whitespace
    return name, value

def validate_access(caller):
    return caller.attributes.get("is_chargen", default=False) or caller.locks.check_lockstring(caller, "perm(Builder)")

class CmdSetDiscipline(Command):
    key = "+setdiscipline"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        try:
            name, value = safe_split_args(self.args)
        except Exception:
            caller.msg("|rValue must be a number.|n")
            return

        if not validate_access(caller):
            caller.msg("|rYou are not in character generation.|n")
            return
        if caller.attributes.get("is_chargen", default=False) and value > 3:
            caller.msg("|rMax 3 dots per Discipline in chargen.|n")
            return
        if value < 0 or value > 5:
            caller.msg("|rDots must be between 0 and 5.|n")
            return

        data = caller.db.disciplines or {}
        data[name] = value
        caller.db.disciplines = data
        caller.msg(f"|gSet {name.title()} to {value} dots in Disciplines.|n")

class CmdSetBackground(Command):
    key = "+setbackground"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        try:
            name, value = safe_split_args(self.args)
        except Exception:
            caller.msg("|rValue must be a number.|n")
            return

        if not validate_access(caller):
            caller.msg("|rYou are not in character generation.|n")
            return
        if caller.attributes.get("is_chargen", default=False) and value > 3:
            caller.msg("|rMax 3 dots per Background in chargen.|n")
            return
        if value < 0 or value > 5:
            caller.msg("|rDots must be between 0 and 5.|n")
            return

        data = caller.db.backgrounds or {}
        data[name] = value
        caller.db.backgrounds = data
        caller.msg(f"|gSet {name.title()} to {value} dots in Backgrounds.|n")

class CmdSetVirtue(Command):
    key = "+setvirtue"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        try:
            name, value = safe_split_args(self.args)
        except Exception:
            caller.msg("|rValue must be a number.|n")
            return

        if not validate_access(caller):
            caller.msg("|rYou are not in character generation.|n")
            return
        if caller.attributes.get("is_chargen", default=False) and value > 5:
            caller.msg("|rMax 5 dots per Virtue in chargen.|n")
            return
        if value < 0 or value > 5:
            caller.msg("|rDots must be between 0 and 5.|n")
            return

        data = caller.db.virtues or {}
        data[name] = value
        caller.db.virtues = data
        caller.msg(f"|gSet {name.title()} to {value} dots in Virtues.|n")
