"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.
"""

from evennia.objects.objects import DefaultCharacter

class Character(DefaultCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.
    """

    def at_after_move(self, source_location, **kwargs):
        super().at_after_move(source_location, **kwargs)

        # Automatically detect CharGen room
        if self.location and self.location.is_typeclass("typeclasses.rooms.CharGenRoom", exact=False):
            self.db.is_chargen = True
            self.msg("|gYou have entered Character Generation mode.|n")
        else:
            self.db.is_chargen = False
            self.msg("|yYou have exited Character Generation mode.|n")
