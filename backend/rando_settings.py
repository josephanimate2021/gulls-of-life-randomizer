import json
import copy

SETTINGS = {
    0: {
        "shuffle_dungeons": {
            "default": False,
            "disabled": True,
            "fr": "Mélanger les donjons"
        },
        "shuffle_items": {
            "default": True,
            "fr": "Mélanger les objets"
        },
        "keysanity": {
            "default": False,
            "disabled": True,
            "fr": "La clé de la santé mentale"
        },
        "shuffle_bosses": {
            "default": False,
            "disabled": True,
            "fr": "Mélanger les boss"
        },
        "shuffle_all": {
            "default": False,
            "fr": "Tout mélanger"
        }
    },
    1: {
        "romhack_version": {
            "default": "latest",
            "options": {
                2: {
                    "latest": ["v1.0/1.1 (Dernière version, stable)", "v1.0/1.1 (Latest, stable)"],
                },
                3: {},
                4: {
                    "dev": ["Dev Build", "Version de développement"]
                }
            }
        }
    }
}

CATS_BY_LANG = [
    ["Options logiques", "Logic Options"],
    ["Divers", "Misc"],
    ["Versions stables", "Stable Builds"],
    ["Versions bêta (à venir)", "Beta Builds (Coming Soon)"],
    ["Versions pour développeurs", "Developer Builds"]
]

def stringify_settings(lang_index):
    settings = {}
    for p in SETTINGS.keys():
        settings[CATS_BY_LANG[p][lang_index]] = SETTINGS[p]
    return json.dumps(settings)