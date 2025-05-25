from evennia import Command

class CmdXP(Command):
    """
    +xp [gain/spend] <amount> = <reason>

    Track XP earned and spent. Use:
        +xp                : View totals
        +xp gain <amt> = <reason>  : ST gives XP
        +xp spend <amt> = <reason> : Log XP spent
    """

    key = "+xp"
    locks = "cmd:all()"
    help_category = "XP"

    def func(self):
        caller = self.caller

        if not caller.db.xp:
            caller.db.xp = {"earned": 0, "spent": 0, "freebie": 0}

        args = self.args.strip()

        if not args:
            earned = caller.db.xp.get("earned", 0)
            spent = caller.db.xp.get("spent", 0)
            freebie = caller.db.xp.get("freebie", 0)
            available = earned - spent
            msg = "|wXP Tracker|n\n"
            msg += f"Earned : {earned}\n"
            msg += f"Spent  : {spent}\n"
            msg += f"Freebie: {freebie}\n"
            msg += f"|wAvailable|n: {available}"
            caller.msg(msg)
            return

        if "=" not in args:
            caller.msg("Usage: +xp gain/spend <amount> = <reason>")
            return

        left, reason = [part.strip() for part in args.split("=", 1)]
        parts = left.split()
        if len(parts) != 2:
            caller.msg("Format: +xp gain/spend <amount> = <reason>")
            return

        action, amount = parts[0].lower(), parts[1]

        if action not in ("gain", "spend"):
            caller.msg("You must specify either 'gain' or 'spend'.")
            return

        try:
            amount = int(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            caller.msg("Amount must be a positive number.")
            return

        if action == "gain":
            caller.db.xp["earned"] += amount
            caller.msg(f"Gained {amount} XP. Reason: {reason}")
        elif action == "spend":
            available = caller.db.xp["earned"] - caller.db.xp["spent"]
            if available < amount:
                caller.msg(f"Not enough available XP. You have {available}.")
                return
            caller.db.xp["spent"] += amount
            caller.msg(f"Spent {amount} XP. Reason: {reason}")
