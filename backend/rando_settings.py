import json
import copy

SETTINGS = {
    0: {
        "shuffle_dungeons": {
            "default": False,
            "disabled": True,
            "description": ["Modifie les portails d'une entrée de donjon pour qu'ils mènent à un autre donjon. Par exemple, l'extérieur du donjon d1 peut mener à l'intérieur du donjon d2, etc.", "Changes the warps of a dungeon entrance to lead to another dungeon. For example, outside d1 can lead to inside d2, or etc."],
            "fr": "Mélanger les donjons"
        },
        "shuffle_items": {
            "default": True,
            "description": ["Lorsque cette option est activée, tous les objets du jeu seront mélangés.", "When enabled, all ingame items will be shuffled around."],
            "fr": "Mélanger les objets"
        },
        "keysanity": {
            "default": False,
            "disabled": True,
            "description": ["Lorsque cette option est activée, les clés de boss et les petites clés seront mélangées en dehors des donjons.", "When enabled, boss and small keys will be shuffled outside dungeons."],
            "fr": "La clé de la santé mentale"
        },
        "shuffle_bosses": {
            "default": False,
            "disabled": True,
            "description": ["Lorsque cette option est activée, tous les boss des donjons seront mélangés. Par exemple, la salle du boss d1 pourrait accueillir le boss d2, et ainsi de suite.", "When enabled, all dungeon bosses will be shuffled around. For example, the d1 boss room could have a d2 boss or etc."],
            "fr": "Mélanger les boss"
        },
        "shuffle_all": {
            "default": False,
            "description": ["Lorsque cette option est activée, absolument tout sera mélangé.", "When enabled, absolutely everything will be shuffled around."],
            "fr": "Tout mélanger"
        },
        "guarentee_sword": {
            "default": True,
            "disabled": True,
            "description": ["Lorsque cette option est activée, un ouvrier portant un casque de chantier sur l'île de Mist aura toujours une épée sur lui, quelles que soient les conditions logiques.", "When enabled, a hardhat worker on mist island will always have a sword on him, no matter the logic conditions."],
            "fr": "Assurer une épée"
        },
        "logic": {
            "default": "casual",
            "options": {
                "none": ["Aucune logique", "No Logic"],
                "casual": ["Logique de base", "Basic Logic"],
                "medium_logic": ["Logique moyenne", "Medium Logic"]
            },
            "description": ["À utiliser lorsque vous vous déplacez d'un endroit à l'autre dans le jeu.\n\nAucune logique : aucun « softlock » n'est pris en compte lors de la génération aléatoire d'une partie.\n\nLogique de base : vous êtes censé connaître l'itinéraire que vous avez emprunté spontanément lors de votre précédente partie du romhack. Aucune astuce n'est requise.\n\nLogique moyenne : vous êtes censé connaître le fonctionnement du moteur Oracle, ce qui implique de connaître les astuces du jeu. Aucun bug n'est requis.", "Used when shuffling around locations in the game.\n\nNo Logic: no softlocks are put into mind when randomizing a game.\n\nBasic Logic: You are expected to know the route you took casually in the romhack before. No tricks will be required.\n\nMedium Logic: You are expected to know how the oracles engine works, that means knowing tricks ingame. No glitches are required."],
            "fr": "Logique"
        },
        "dream_timer": {
            "default": 7,
            "min": 3,
            "max": 1092, # Crazy number for a time, but unless you really take a long time exploring a dream, don't use this.
            "description": ["Une fois configuré, ce paramètre modifiera la durée pendant laquelle vous pourrez rêver dans le jeu. Ce compte à rebours est calculé en ajoutant 60 images un nombre défini de fois, tel que configuré ici. Par défaut, cette valeur est fixée à 7 pour une expérience normale. N'hésitez pas à la modifier à votre guise.", "When configured, this will change how long you can dream for in the game. This timer is calculated by adding 60 frames a set number of times configured here. By default, this will stay at 7 for the normal experience. Feel free to change it as long as you like."],
        },
        "disable_dream_timer": {
            "default": False,
            "fr": "Désactiver Dream Timer",
            "description": ["Lorsque cette option est activée, deux octets seront mis à 0, ce qui empêchera l'affichage du chronomètre sur le HUD et rendra ainsi ce dernier totalement inactif. Si vous souhaitez explorer le rêve sans subir de ralentissements dans le jeu, utilisez plutôt cette fonctionnalité.", "When enabled, 2 bytes will be set to 0 which will prevent the timer from being shown on the HUD, thus causing the timer to not have any effect on all. If you want to explore the dream while not lagging out the game, use this feature instead."]
        }
    },
    1: {
        "show_ballade_cutscenes": {
            "default": False,
            "description": ["Lorsque cette fonctionnalité est activée, vous découvrirez des cinématiques mettant en scène Marin la mouette et d'autres personnages au sein de l'objet d'interaction « Ballade ». Par défaut, cette fonctionnalité est désactivée, car son implémentation dans un contexte aléatoire n'a pas de sens. N'activez cette fonctionnalité que si c'est la première fois que vous jouez à « Gulls of Life ».", "When enabled, you will be greeted with cutscenes from marin the seagull and others within the ballade interaction object. By default, this feature is disabled because it dosen't make sense to have that implemented in rando context. Only enable this feature if this is your first time playing gulls of life."],
            "fr": "Afficher les cinématiques de Ballade"
        },
        "vanilaize_rom": {
            "default": False,
            "description": ["Lorsque cette option est activée, toutes les corrections de bugs identifiées pour la version romhack seront supprimées, y compris le « warp to start » ! Assurez-vous d'être certain de votre choix avant de sélectionner cette option, car vous risquez davantage de vous retrouver bloqué définitivement dans le jeu si vous choisissez ce paramètre.", "When enabled, any bugfixes found for the romhack version will be removed, including warp to start! please be certain before selecting this option as you'll have more chance of being softlocked into the game entirely if you select this setting."],
            "fr": "ROM Vanilaize"
        },
        "romhack_version": {
            "default": "latest",
            "description": ["Version du romhack « Gulls of Life » utilisée lors de la randomisation du jeu. Veuillez noter que les corrections de bugs seront intégrées le cas échéant ; la version du romhack n'est donc peut-être pas tout à fait originale, mais elle s'en rapproche suffisamment.", "Version of the gulls of life romhack used during game randomization. Please keep in mind that bugfixes will be included if there are any, so the romhack version may not be completely original, but close enough."],
            "options": {
                2: {
                    "1.0_1.1": ["v1.0/1.1 (Dernière)", "v1.0/1.1 (Latest)"],
                    "1.0_1": "v1.0/1",
                },
                3: {
                    "1.0_2": "v1.0/2"
                },
                4: {
                    "dev": ["Version de développement", "Dev Build"]
                }
            },
            "fr": "Version Romhack"
        },
    },
    5: {
        "max_out_dream_timer": {
            "default": False,
            "description": ["Permet de régler le « dream timer » au maximum en modifiant les 2 octets qui le contrôlent pour leur attribuer la valeur 0xff, au lieu de celle calculée à partir du réglage du « dream timer ». Ce réglage entraînera inévitablement des ralentissements dans votre jeu, que ce soit sur une Game Boy originale ou sur l'émulateur BGB ou tout autre émulateur similaire. Veuillez ne pas cocher cette option, sauf si vous souhaitez faire vos propres essais.", "Maxes out the dream timer by modifying 2 bytes responsible for the dream timer to be 0xff instead of what's calculated from the dream timer setting. This setting will absolutely lag your game on a real gameboy and on the bgb emulator or others similar to it. Please do not check this setting unless you want to experiment for yourself."]
        }
    }
}

CATS_BY_LANG = [
    ["Options logiques", "Logic Options"],
    ["Divers", "Misc"],
    ["Versions stables", "Stable Builds"],
    ["Versions bêta", "Beta Builds"],
    ["Versions pour développeurs", "Developer Builds"],
    ["Options expérimentales", "Experimental Options"]
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