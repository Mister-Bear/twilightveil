from evennia import Command

class CmdSetVirtue(Command):
    """
    +setvirtue <virtue> = <value>

    Set your virtue ratings. Valid virtues:
    - conscience
    - self_control
    - courage

    Example:
        +setvirtue conscience = 3
    """

    key = "+setvirtue"
    locks = "cmd:all()"
    help_category = "Chargen"

    def func(self):
        caller = self.caller

        if not self.args or "=" not in self.args:
            caller.msg("Usage: +setvirtue <virtue> = <value>")
            return

        arg, val = [part.strip().lower() for part in self.args.split("=", 1)]

        valid = ["conscience", "self_control", "courage"]

        if arg not in valid:
            caller.msg(f"Invalid virtue. Choose one of: {', '.join(valid)}.")
            return

        try:
            val = int(val)
            if not 0 <= val <= 5:
                raise ValueError
        except ValueError:
            caller.msg("Value must be a number between 0 and 5.")
            return

        if not caller.db.virtues:
            caller.db.virtues = {}

        caller.db.virtues[arg] = val
        caller.msg(f"Set {arg.title()} to {val}.")
