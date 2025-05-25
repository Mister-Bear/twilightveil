from evennia import Command
import random

class CmdRoll(Command):
    """
    +roll <trait1>+<trait2> [vs <difficulty>]

    Example:
        +roll dexterity+stealth
        +roll wits+alertness vs 7
    """

    key = "+roll"
    locks = "cmd:all()"
    help_category = "Rolls"

    def func(self):
        caller = self.caller
        args = self.args.strip().lower()

        if not args:
            caller.msg("Usage: +roll <trait1>+<trait2> [vs <difficulty>]")
            return

        if "vs" in args:
            traits_part, diff_part = [x.strip() for x in args.split("vs", 1)]
            try:
                difficulty = int(diff_part)
                if not 2 <= difficulty <= 10:
                    raise ValueError
            except ValueError:
                caller.msg("Difficulty must be a number between 2 and 10.")
                return
        else:
            traits_part = args
            difficulty = 6

        traits = [t.strip() for t in traits_part.split("+")]
        if not traits:
            caller.msg("No traits specified.")
            return

        pool = 0
        details = []
        specialties = set()
        missing = []

        for trait in traits:
            trait_value = 0
            found = False

            for category in ("attributes", "virtues", "disciplines", "abilities"):
                trait_dict = getattr(caller.db, category) or {}
                if trait in trait_dict:
                    trait_value = trait_dict.get(trait, 0)
                    pool += trait_value
                    details.append(f"{trait.title()}({trait_value})")
                    if trait_value >= 4:
                        specialties.add(trait)
                    found = True
                    break

            if not found and trait == "willpower":
                trait_value = caller.db.willpower or 0
                pool += trait_value
                details.append(f"Willpower({trait_value})")
                if trait_value >= 4:
                    specialties.add("willpower")
            elif not found:
                missing.append(trait)

        if missing:
            caller.msg(f"Could not find trait(s): {', '.join(missing)}")
            return

        if pool == 0:
            caller.msg("Your total dice pool is 0.")
            return

        rolls = [random.randint(1, 10) for _ in range(pool)]
        successes = 0
        for r in rolls:
            if r >= difficulty:
                successes += 2 if r == 10 and specialties else 1
        botches = rolls.count(1)
        net_success = max(successes - botches, 0)

        roll_report = ", ".join(str(r) for r in rolls)

        caller.msg(
            f"|wRoll|n: {' + '.join(details)} vs {difficulty}\n"
            f"Dice: {roll_report}\n"
            f"Successes: {successes} | Botches: {botches} | Net: {net_success}"
        )
