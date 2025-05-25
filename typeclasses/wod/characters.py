from evennia import DefaultCharacter

class WoDCharacter(DefaultCharacter):
    def at_object_creation(self):
        super().at_object_creation()

        self.db.attributes = {
            "strength": 1,
            "dexterity": 1,
            "stamina": 1,
            "charisma": 1,
            "manipulation": 1,
            "appearance": 1,
            "perception": 1,
            "intelligence": 1,
            "wits": 1
        }

        self.db.abilities = {}
        self.db.backgrounds = {}

        self.db.willpower = 1
        self.db.health = {
            "bruised": 0,
            "hurt": 0,
            "injured": 0,
            "wounded": 0,
            "mauled": 0,
            "crippled": 0,
            "incapacitated": 0
        }

        self.db.total_attributes = 0
        self.db.total_abilities = 0
        self.db.total_backgrounds = 0
