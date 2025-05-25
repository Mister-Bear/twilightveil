"""
All commands in the game must be grouped in a cmdset. A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.
"""

from evennia import default_cmds
from evennia.commands.default.building import CmdTeleport
from commands.chargen_commands import CmdSetAbility
from typeclasses.wod.cmd_sheet import CmdSheet
from typeclasses.wod.cmd_setvirtue import CmdSetVirtue
from typeclasses.wod.cmd_setattr import CmdSetAttr
from typeclasses.wod.cmd_setpath import CmdSetPath
from typeclasses.wod.cmd_setmerits import CmdSetMerit, CmdSetFlaw
from typeclasses.wod.cmd_xp import CmdXP
from typeclasses.wod.cmd_vote import CmdVote
from typeclasses.wod.cmd_raise import CmdRaise
from typeclasses.wod.cmd_roll import CmdRoll
from typeclasses.wod.cmd_contest import CmdContest
from commands.cmd_sheet import CmdSheet
from commands.cmd_setattr import CmdSetAttr
from commands.cmd_setpowers import CmdSetDiscipline, CmdSetBackground, CmdSetVirtue
from commands.cmd_setidentity import CmdSetClan, CmdSetConcept, CmdSetNature, CmdSetDemeanor


class PatchedTeleport(CmdTeleport):
    def func(self):
        super().func()

        # After teleport completes, check location type
        if self.caller.location and self.caller.location.is_typeclass("typeclasses.rooms.CharGenRoom", exact=False):
            self.caller.db.is_chargen = True
            self.caller.msg("|g(Chargen mode activated by teleport override.)|n")
        else:
            self.caller.db.is_chargen = False
            self.caller.msg("|y(Chargen mode cleared by teleport override.)|n")


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        self.add(CmdSheet())
        self.add(CmdSetVirtue())
        self.add(CmdSetAttr())
        self.add(CmdSetPath())
        self.add(CmdSetMerit())
        self.add(CmdSetFlaw())
        self.add(CmdXP())
        self.add(CmdVote())
        self.add(CmdRaise())
        self.add(CmdRoll())
        self.add(CmdContest())
        self.add(CmdSetAbility())
        self.add(PatchedTeleport())  # This replaces the default @tel
        self.add(CmdSheet())
        self.add(CmdSetAttr())
        self.add(CmdSetDiscipline())
        self.add(CmdSetBackground())
        self.add(CmdSetVirtue())
        self.add(CmdSetClan())
        self.add(CmdSetConcept())
        self.add(CmdSetNature())
        self.add(CmdSetDemeanor())


class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """

    key = "DefaultAccount"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.
    """

    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in.
    """

    key = "DefaultSession"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
