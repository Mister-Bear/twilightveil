from evennia import Command

class CmdSetAbility(Command):
    """
    Sets an ability rating during character generation.

    Usage:
        +setability <ability> = <rating>

    Example:
        +setability athletics = 3
    """
    key = "+setability"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller

        # Allow Staff override
        if caller.locks.check_lockstring(caller, "perm(Builder)"):
            in_chargen = True
        else:
            in_chargen = caller.db.is_chargen

        if not in_chargen:
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
            caller.msg("|rAbility rating must be between 0 and 3 during chargen.|n")
            return

        # Get or create ability dict
        abilities = caller.db.abilities or {}
        abilities[ability] = value
        caller.db.abilities = abilities

        caller.msg(f"|gSet {ability.title()} to {value} dots.|n")
