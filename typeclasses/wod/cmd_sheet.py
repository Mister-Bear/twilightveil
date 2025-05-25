from evennia import Command

class CmdSheet(Command):
    """
    +sheet

    Display your character sheet.
    """

    key = "+sheet"
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        caller = self.caller

        # Safeguard: default fallbacks
        attributes = caller.db.attributes or {}
        willpower = caller.db.willpower or 0
        backgrounds = caller.db.backgrounds or {}
        disciplines = caller.db.disciplines or {}
        virtues = caller.db.virtues or {}
        humanity = caller.db.humanity or 7
        path = caller.db.path or None
        health = caller.db.health or {
            "bruised": False,
            "hurt": False,
            "injured": False,
            "wounded": False,
            "mauled": False,
            "crippled": False,
            "incapacitated": False,
        }
        merits = caller.db.merits or []
        flaws = caller.db.flaws or []

        # Build output
        sheet = "|cCharacter Sheet|n\n"
        sheet += "-" * 40 + "\n"

        # Attributes
        sheet += "|wAttributes|n\n"
        for attr in ("strength", "dexterity", "stamina",
                     "charisma", "manipulation", "appearance",
                     "perception", "intelligence", "wits"):
            value = attributes.get(attr, 0)
            dots = "*" * value + "-" * (5 - value)
            sheet += f"{attr.title():<13}: {dots}\n"

        # Willpower
        sheet += "\n|wWillpower|n\n"
        dots = "*" * willpower + "-" * (10 - willpower)
        sheet += f"Willpower     : {dots}\n"

        # Backgrounds
        sheet += "\n|wBackgrounds|n\n"
        if not backgrounds:
            sheet += "None\n"
        else:
            for name, value in backgrounds.items():
                dots = "*" * value + "-" * (5 - value)
                sheet += f"{name.title():<13}: {dots}\n"

        # Disciplines
        sheet += "\n|wDisciplines|n\n"
        if not disciplines:
            sheet += "None\n"
        else:
            for name, value in disciplines.items():
                dots = "*" * value + "-" * (5 - value)
                sheet += f"{name.title():<13}: {dots}\n"

        # Virtues
        sheet += "\n|wVirtues|n\n"
        for virtue in ("conscience", "self_control", "courage"):
            value = virtues.get(virtue, 0)
            dots = "*" * value + "-" * (5 - value)
            sheet += f"{virtue.replace('_', ' ').title():<13}: {dots}\n"

        # Path or Humanity
        if isinstance(path, dict):
            pname = path.get("name", "Unknown")
            prating = path.get("rating", 0)
            sheet += f"\n|wPath|n: {pname} ({prating}/10)\n"
        else:
            sheet += f"\n|wHumanity|n: {humanity}/10\n"

        # Merits
        sheet += "\n|wMerits|n\n"
        if merits:
            for merit in merits:
                sheet += f"- {merit}\n"
        else:
            sheet += "None\n"

        # Flaws
        sheet += "\n|wFlaws|n\n"
        if flaws:
            for flaw in flaws:
                sheet += f"- {flaw}\n"
        else:
            sheet += "None\n"

        # Health
        sheet += "\n|wHealth|n\n"
        penalties = {
            "bruised": "",
            "hurt": "-1",
            "injured": "-1",
            "wounded": "-2",
            "mauled": "-2",
            "crippled": "-5",
            "incapacitated": ""
        }
        for level in ("bruised", "hurt", "injured", "wounded",
                      "mauled", "crippled", "incapacitated"):
            mark = "[X]" if health.get(level, False) else "[-]"
            penalty = f"  {penalties[level]}" if penalties[level] else ""
            sheet += f"{mark} {level.title():<13}{penalty}\n"

        caller.msg(sheet)
