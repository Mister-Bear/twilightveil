from evennia import Command
from evennia.utils.utils import datetime_format
from datetime import datetime

class CmdVote(Command):
    """
    +vote <player> = <reason>

    Give someone a vote of respect. They gain 0.25 XP.
    Max 4 votes per player per day.

    Example:
        +vote @Sol = Amazing Elysium RP
    """

    key = "+vote"
    locks = "cmd:all()"
    help_category = "XP"

    def func(self):
        caller = self.caller

        if "=" not in self.args:
            caller.msg("Usage: +vote <player> = <reason>")
            return

        targetname, reason = [part.strip() for part in self.args.split("=", 1)]
        target = caller.search(targetname)
        if not target:
            return

        if target == caller:
            caller.msg("You can't vote for yourself.")
            return

        if not reason:
            caller.msg("Please include a reason for the vote.")
            return

        now = datetime.now().date()

        # Track vote history on VOTER
        if not caller.db.vote_log:
            caller.db.vote_log = []

        for entry in caller.db.vote_log:
            if entry.get("target") == target.key and entry.get("date") == str(now):
                caller.msg(f"You've already voted for {target.key} today.")
                return

        # Track daily vote count on RECIPIENT
        if not target.db.vote_received:
            target.db.vote_received = []

        today_votes = [v for v in target.db.vote_received if v.get("date") == str(now)]
        if len(today_votes) >= 4:
            caller.msg(f"{target.key} has already received 4 votes today.")
            return

        # Grant 0.25 XP
        if not target.db.xp:
            target.db.xp = {"earned": 0, "spent": 0, "freebie": 0}

        target.db.xp["earned"] += 0.25

        # Log for voter
        caller.db.vote_log.append({
            "target": target.key,
            "reason": reason,
            "date": str(now)
        })

        # Log for recipient
        target.db.vote_received.append({
            "source": caller.key,
            "reason": reason,
            "date": str(now)
        })

        caller.msg(f"You voted for {target.key}. They gained 0.25 XP.")
        target.msg(f"You received a vote from {caller.key}: {reason}")
