from evennia import Command

class CmdSetMerit(Command):
    """
    +setmerit <name>

    Add a Merit to your sheet.

    Example:
        +setmerit acute senses
    """

    key = "+setmerit"
    locks = "cmd:all()"
    help_category = "Chargen"

    def func(self):
        caller = self.caller
        merit = self.args.strip().title()

        if not merit:
            caller.msg("Usage: +setmerit <name>")
            return

        merits = caller.db.merits or []

        if merit in merits:
            caller.msg(f"You already have the merit: {merit}.")
            return

        merits.append(merit)
        merits.sort()
        caller.db.merits = merits
        caller.msg(f"Merit added: {merit}")

class CmdSetFlaw(Command):
    """
    +setflaw <name>

    Add a Flaw to your sheet.

    Example:
        +setflaw deep sleeper
    """

    key = "+setflaw"
    locks = "cmd:all()"
    help_category = "Chargen"

    def func(self):
        caller = self.caller
        flaw = self.args.strip().title()

        if not flaw:
            caller.msg("Usage: +setflaw <name>")
            return

        flaws = caller.db.flaws or []

        if flaw in flaws:
            caller.msg(f"You already have the flaw: {flaw}.")
            return

        flaws.append(flaw)
        flaws.sort()
        caller.db.flaws = flaws
        caller.msg(f"Flaw added: {flaw}")
