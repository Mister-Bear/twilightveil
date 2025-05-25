from evennia import Command

class CmdSetPath(Command):
    """
    +setpath <path> = <value>

    Set your moral path and current path rating.

    Examples:
        +setpath humanity = 7
        +setpath path of night = 5
    """

    key = "+setpath"
    locks = "cmd:all()"
    help_category = "Chargen"

    def func(self):
        caller = self.caller

        if not self.args or "=" not in self.args:
            caller.msg("Usage: +setpath <path> = <value>")
            return

        path_name, value = [part.strip() for part in self.args.split("=", 1)]

        try:
            value = int(value)
            if not 0 <= value <= 10:
                raise ValueError
        except ValueError:
            caller.msg("Value must be a number between 0 and 10.")
            return

        # Store as a dict: {name, rating}
        caller.db.path = {
            "name": path_name.title(),
            "rating": value
        }

        caller.msg(f"Set Path to {path_name.title()} ({value}/10).")
