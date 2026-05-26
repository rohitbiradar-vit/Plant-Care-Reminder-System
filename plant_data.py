PLANT_PROFILES = {
    "rosa": {
        "common_name": "Rose",
        "care_tasks": {
            "watering":    0,
            "fertilizing": 30,
            "pruning":     14,
            "pest_check":  7,
            "repotting":   365,
        },
        "tips": "Roses love sunlight. Water at the base, not the leaves."
    },
    "cactaceae": {
        "common_name": "Cactus",
        "care_tasks": {
            "watering":    14,
            "fertilizing": 60,
            "pruning":     90,
            "pest_check":  30,
            "repotting":   730,
        },
        "tips": "Cactus needs very little water. Overwatering will kill it."
    },
    "ficus": {
        "common_name": "Ficus",
        "care_tasks": {
            "watering":    5,
            "fertilizing": 21,
            "pruning":     30,
            "pest_check":  14,
            "repotting":   365,
        },
        "tips": "Keep away from cold drafts. Wipe leaves to remove dust."
    },
    "aloe vera": {
        "common_name": "Aloe Vera",
        "care_tasks": {
            "watering":    0,
            "fertilizing": 60,
            "pruning":     30,
            "pest_check":  21,
            "repotting":   548,
        },
        "tips": "Aloe stores water in its leaves. Let soil dry completely before watering."
    },
    "monstera": {
        "common_name": "Monstera",
        "care_tasks": {
            "watering":    7,
            "fertilizing": 21,
            "pruning":     30,
            "pest_check":  14,
            "repotting":   365,
        },
        "tips": "Loves indirect light. Wipe leaves weekly for better growth."
    },
    "lavandula": {
        "common_name": "Lavender",
        "care_tasks": {
            "watering":    10,
            "fertilizing": 45,
            "pruning":     14,
            "pest_check":  21,
            "repotting":   365,
        },
        "tips": "Lavender loves full sun and dry conditions. Do not overwater."
    },
    "tulipa": {
        "common_name": "Tulip",
        "care_tasks": {
            "watering":    3,
            "fertilizing": 14,
            "pruning":     7,
            "pest_check":  7,
            "repotting":   180,
        },
        "tips": "Water regularly during growth. Let bulbs dry out after flowering."
    },
    "Mango": {
        "common_name": "Mango",
        "care_tasks": {
            "watering":    5,
            "fertilizing": 30,
            "pruning":     21,
            "pest_check":  14,
            "repotting":   365,
        },
        "tips": "No specific profile found. Using general care schedule."
    }
}

def get_plant_profile(species):
    key = species.strip().lower()
    for profile_key in PLANT_PROFILES:
        if profile_key in key or key in profile_key:
            return PLANT_PROFILES[profile_key]
    return PLANT_PROFILES["default"]