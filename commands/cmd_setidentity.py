from evennia import Command

def is_chargen_or_staff(caller):
    return caller.attributes.get("is_chargen", default=False) or caller.locks.check_lockstring(caller, "perm(Builder)")

class CmdSetClan(Command):
    key = "+setclan"
    locks = "cmd:all()"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: +setclan <clan>")
            return
        if not is_chargen_or_staff(self.caller):
            self.caller.msg("|rYou are not in character generation.|n")
            return
        self.caller.db.clan = self.args.strip().title()
        self.caller.msg(f"|gClan set to {self.caller.db.clan}.|n")

class CmdSetConcept(Command):
    key = "+setconcept"
    locks = "cmd:all()"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: +setconcept <concept>")
            return
        if not is_chargen_or_staff(self.caller):
            self.caller.msg("|rYou are not in character generation.|n")
            return
        self.caller.db.concept = self.args.strip().title()
        self.caller.msg(f"|gConcept set to {self.caller.db.concept}.|n")

class CmdSetNature(Command):
    key = "+setnature"
    locks = "cmd:all()"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: +setnature <nature>")
            return
        if not is_chargen_or_staff(self.caller):
            self.caller.msg("|rYou are not in character generation.|n")
            return
        self.caller.db.nature = self.args.strip().title()
        self.caller.msg(f"|gNature set to {self.caller.db.nature}.|n")

class CmdSetDemeanor(Command):
    key = "+setdemeanor"
    locks = "cmd:all()"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: +setdemeanor <demeanor>")
            return
        if not is_chargen_or_staff(self.caller):
            self.caller.msg("|rYou are not in character generation.|n")
            return
        self.caller.db.demeanor = self.args.strip().title()
        self.caller.msg(f"|gDemeanor set to {self.caller.db.demeanor}.|n")
