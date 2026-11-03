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
            "disabled": True,
            "fr": "Tout mélanger"
        },
        "logic": {
            "default": "casual",
            "options": {
                "none": ["Aucune logique", "No Logic"],
                "casual": ["Logique de base", "Basic Logic"],
                "medium_logic": ["Logique complète", "Full Logic"]
            },
            "fr": "Logique"
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
                    "dev": ["Version de développement", "Dev Build"]
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
    for p in list(SETTINGS.keys()):
        m_settings = SETTINGS[p].copy()
        for p2 in list(SETTINGS[p].keys()):
            if "options" in SETTINGS[p][p2]:
                for p3 in list(SETTINGS[p][p2]["options"].keys()):
                    if isinstance(SETTINGS[p][p2]["options"][p3], dict):
                        m_settings[p2]["options"][CATS_BY_LANG[p3][lang_index]] = SETTINGS[p][p2]["options"][p3]
                        del m_settings[p2]["options"][p3]
        settings[CATS_BY_LANG[p][lang_index]] = m_settings
    return json.dumps(settings)