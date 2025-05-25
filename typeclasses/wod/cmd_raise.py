from evennia import Command

class CmdRaise(Command):
    """
    +raise <trait>

    Spend XP to increase a trait by 1 dot.

    Supports: Attributes, Backgrounds, Disciplines, Willpower

    XP Costs:
    Attribute: current x4
    Background: current x2
    Discipline: current x5
    Willpower: new rating
    """

    key = "+raise"
    locks = "cmd:all()"
    help_category = "XP"

    def func(self):
        caller = self.caller
        trait = self.args.strip().lower()

        if not trait:
            caller.msg("Usage: +raise <trait>")
            return

        if not caller.db.xp:
            caller.msg("You have no XP record.")
            return

        xp = caller.db.xp
        available = xp["earned"] - xp["spent"]

        # Trait categories
        attributes = [
            "strength", "dexterity", "stamina",
            "charisma", "manipulation", "appearance",
            "perception", "intelligence", "wits"
        ]

        # Pull trait pools
        attr_pool = caller.db.attributes or {}
        back_pool = caller.db.backgrounds or {}
        disc_pool = caller.db.disciplines or {}
        willpower = caller.db.willpower or 0

        # Determine trait type
        if trait in attributes:
            rating = attr_pool.get(trait, 0)
            cost = rating * 4
            if available < cost:
                caller.msg(f"Not enough XP. Need {cost}, have {available}.")
                return
            attr_pool[trait] = rating + 1
            caller.db.attributes = attr_pool
            xp["spent"] += cost
            caller.msg(f"{trait.title()} raised to {rating + 1} for {cost} XP.")
            return

        elif trait in back_pool:
            rating = back_pool.get(trait, 0)
            cost = rating * 2
            if available < cost:
                caller.msg(f"Not enough XP. Need {cost}, have {available}.")
                return
            back_pool[trait] = rating + 1
            caller.db.backgrounds = back_pool
            xp["spent"] += cost
            caller.msg(f"{trait.title()} raised to {rating + 1} for {cost} XP.")
            return

        elif trait in disc_pool:
            rating = disc_pool.get(trait, 0)
            cost = rating * 5  # Adjust to 7 if out-of-clan in future
            if available < cost:
                caller.msg(f"Not enough XP. Need {cost}, have {available}.")
                return
            disc_pool[trait] = rating + 1
            caller.db.disciplines = disc_pool
            xp["spent"] += cost
            caller.msg(f"{trait.title()} raised to {rating + 1} for {cost} XP.")
            return

        elif trait == "willpower":
            cost = willpower + 1
            if available < cost:
                caller.msg(f"Not enough XP. Need {cost}, have {available}.")
                return
            caller.db.willpower = willpower + 1
            xp["spent"] += cost
            caller.msg(f"Willpower raised to {willpower + 1} for {cost} XP.")
            return

        else:
            caller.msg(f"Unknown or unsupported trait: {trait}.")
