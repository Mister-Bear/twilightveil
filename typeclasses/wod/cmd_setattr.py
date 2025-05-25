from evennia import Command

class CmdSetAttr(Command):
    """
    +setattr <trait> = <value>

    Set attributes, backgrounds, or disciplines.

    Examples:
        +setattr strength = 3
        +setattr celerity = 2
        +setattr allies = 1
    """

    key = "+setattr"
    locks = "cmd:all()"
    help_category = "Chargen"

    def func(self):
        caller = self.caller

        if not self.args or "=" not in self.args:
            caller.msg("Usage: +setattr <trait> = <value>")
            return

        trait, val = [part.strip().lower() for part in self.args.split("=", 1)]

        # Valid core attributes
        attributes = [
            "strength", "dexterity", "stamina",
            "charisma", "manipulation", "appearance",
            "perception", "intelligence", "wits"
        ]

        # Determine which pool this trait belongs to
        if trait in attributes:
            db_field = "attributes"
        elif trait in (caller.db.disciplines or {}):
            db_field = "disciplines"
        elif trait in (caller.db.backgrounds or {}):
            db_field = "backgrounds"
        else:
            # Default to disciplines unless user overrides later
            db_field = "disciplines"

        # Validate the dot value
        try:
            val = int(val)
            if not 0 <= val <= 5:
                raise ValueError
        except ValueError:
            caller.msg("Value must be a number between 0 and 5.")
            return

        # Make sure the dictionary exists before assignment
        if not getattr(caller.db, db_field, None):
            setattr(caller.db, db_field, {})

        # Store the trait
        getattr(caller.db, db_field)[trait] = val
        caller.msg(f"Set {trait.title()} to {val} ({db_field}).")
