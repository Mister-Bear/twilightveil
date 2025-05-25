"""
Room

Rooms are simple containers that have no location of their own.
"""

from evennia.objects.objects import DefaultRoom
from .objects import ObjectParent

class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects.
    """
    pass


class CharGenRoom(ObjectParent, DefaultRoom):
    """
    Final version — fully Evennia-compliant
    Triggers flag for both Characters and @tel scenarios.
    """

    def at_object_arrive(self, obj, source_location, move_type="teleport", **kwargs):
        if obj.has_account:
            obj.db.is_chargen = True
            obj.msg("|gYou have entered Character Generation mode.|n")

    def at_object_leave(self, obj, target_location, move_type="teleport", **kwargs):
        if obj.has_account:
            obj.db.is_chargen = False
            obj.msg("|yYou have exited Character Generation mode.|n")
