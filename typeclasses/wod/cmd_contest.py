from evennia import Command
from evennia.utils.search import search_object
import random

class CmdContest(Command):
    """
    +contest <your traits> vs <target trait> of <target>

    Rolls an opposed check between you and another character.

    Example:
        +contest manipulation+dominate vs willpower of Sol
    """

    key = "+contest"
    locks = "cmd:all()"
    help_category = "Rolls"

    def func(self):
        caller = self.caller
        args = self.args.strip().lower()

        if "vs" not in args or "of" not in args:
            caller.msg("Usage: +contest trait1+trait2 vs trait of target")
            return

        try:
            your_part, rest = args.split("vs", 1)
            their_trait, target_name = [x.strip() for x in rest.split("of", 1)]
        except ValueError:
            caller.msg("Incorrect format. Try: +contest <traits> vs <trait> of <target>")
            return

        your_traits = [t.strip() for t in your_part.split("+")]
        their_traits = [t.strip() for t in their_trait.split("+")]

        target = search_object(target_name)
        if not target:
            caller.msg(f"Target '{target_name}' not found.")
            return
        target = target[0]

        def get_pool(char, trait_list):
            pool = 0
            used = []
            specialties = set()
            missing = []

            for trait in trait_list:
                trait = trait.lower()
                found = False

                for db_field in ("attributes", "virtues", "disciplines"):
                    traits = getattr(char.db, db_field) or {}
                    if trait in traits:
                        val = traits[trait]
                        pool += val
                        used.append(f"{trait.title()}({val})")
                        if val >= 4:
                            specialties.add(trait)
                        found = True
                        break

                if not found and trait == "willpower":
                    val = char.db.willpower or 0
                    pool += val
                    used.append(f"Willpower({val})")
                    if val >= 4:
                        specialties.add("willpower")
                    found = True

                if not found:
                    missing.append(trait)

            return pool, used, specialties, missing

        you_pool, you_used, you_specs, you_missing = get_pool(caller, your_traits)
        them_pool, them_used, them_specs, them_missing = get_pool(target, their_traits)

        if you_missing or them_missing:
            msg = "|rTrait Error(s):|n\n"
            if you_missing:
                msg += f"Your missing traits: {', '.join(you_missing)}\n"
            if them_missing:
                msg += f"{target.key}'s missing traits: {', '.join(them_missing)}"
            caller.msg(msg)
            return

        if you_pool == 0 or them_pool == 0:
            caller.msg("One or both pools are 0. Check your traits.")
            return

        def roll(pool, specialties):
            rolls = [random.randint(1, 10) for _ in range(pool)]
            successes = 0
            for r in rolls:
                if r >= 6:
                    successes += 2 if r == 10 and specialties else 1
            botches = rolls.count(1)
            net = max(successes - botches, 0)
            return rolls, successes, botches, net

        you_rolls, you_succ, you_botch, you_net = roll(you_pool, you_specs)
        them_rolls, them_succ, them_botch, them_net = roll(them_pool, them_specs)

        result = f"|wOpposed Roll|n: You vs {target.key}\n"
        result += f"You rolled: {you_net} net successes | Dice: {you_rolls} | {', '.join(you_used)}\n"
        result += f"{target.key} rolled: {them_net} net successes | Dice: {them_rolls} | {', '.join(them_used)}\n"

        if you_net > them_net:
            result += f"|gYou win the contest by {you_net - them_net} successes.|n"
        elif them_net > you_net:
            result += f"|r{target.key} wins the contest by {them_net - you_net} successes.|n"
        else:
            result += f"|yThe contest is a tie.|n"

        caller.msg(result)
        target.msg(f"{caller.key} rolled an opposed test against you!\n" + result)
