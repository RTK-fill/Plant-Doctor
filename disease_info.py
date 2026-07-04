# ============================================================
# Plant Doctor AI 3.0
# Disease Information Database
# ============================================================

disease_database = {

    # ========================================================
    # PEPPER
    # ========================================================

    "Pepper__bell___Bacterial_spot": {
        "plant": "Bell Pepper",
        "disease": "Bacterial Spot",

        "about":
        "A bacterial disease that causes dark brown or black circular spots on leaves and fruits. Severe infections lead to leaf drop and reduced fruit quality.",

        "symptoms": [
            "Small dark water-soaked spots",
            "Yellow halo around lesions",
            "Leaves turn yellow",
            "Leaves fall early",
            "Fruit develops rough scabby spots"
        ],

        "causes": [
            "Xanthomonas bacteria",
            "Warm humid weather",
            "Rain splash",
            "Infected seeds"
        ],

        "treatment": [
            "Remove infected leaves",
            "Spray copper-based bactericide",
            "Avoid overhead watering",
            "Disinfect gardening tools"
        ],

        "prevention": [
            "Use certified disease-free seeds",
            "Rotate crops every year",
            "Keep plants well spaced",
            "Avoid working with wet plants"
        ]
    },

    "Pepper__bell___healthy": {
        "plant": "Bell Pepper",
        "disease": "Healthy",

        "about":
        "The plant appears healthy with no visible signs of disease.",

        "symptoms": [
            "Bright green leaves",
            "No spots",
            "Healthy stem",
            "Good fruit growth"
        ],

        "causes": [
            "Proper nutrition",
            "Good watering",
            "Adequate sunlight"
        ],

        "treatment": [
            "No treatment required"
        ],

        "prevention": [
            "Continue proper watering",
            "Use balanced fertilizer",
            "Inspect plants regularly"
        ]
    },

    # ========================================================
    # POTATO
    # ========================================================

    "Potato___Early_blight": {
        "plant": "Potato",
        "disease": "Early Blight",

        "about":
        "A fungal disease that first appears on older leaves and gradually spreads throughout the plant.",

        "symptoms": [
            "Brown circular spots",
            "Concentric rings",
            "Yellow leaves",
            "Premature leaf drop"
        ],

        "causes": [
            "Alternaria fungus",
            "Warm temperatures",
            "High humidity"
        ],

        "treatment": [
            "Apply fungicide",
            "Remove infected leaves",
            "Improve air circulation"
        ],

        "prevention": [
            "Crop rotation",
            "Healthy seed potatoes",
            "Avoid overhead watering"
        ]
    },

    "Potato___Late_blight": {
        "plant": "Potato",
        "disease": "Late Blight",

        "about":
        "A serious fungal-like disease capable of destroying potato crops very quickly.",

        "symptoms": [
            "Large brown lesions",
            "White fungal growth",
            "Stem infection",
            "Rotting tubers"
        ],

        "causes": [
            "Phytophthora infestans",
            "Cool wet weather"
        ],

        "treatment": [
            "Remove infected plants",
            "Spray fungicide immediately",
            "Destroy infected debris"
        ],

        "prevention": [
            "Use resistant varieties",
            "Avoid excess irrigation",
            "Maintain good airflow"
        ]
    },

    "Potato___healthy": {
        "plant": "Potato",
        "disease": "Healthy",

        "about":
        "Healthy potato plant showing no disease symptoms.",

        "symptoms": [
            "Green leaves",
            "Strong stems",
            "Normal growth"
        ],

        "causes": [
            "Proper care",
            "Good soil",
            "Balanced nutrients"
        ],

        "treatment": [
            "No treatment needed"
        ],

        "prevention": [
            "Continue normal care",
            "Inspect regularly"
        ]
    },
        # ========================================================
        # TOMATO
        # ========================================================

        "Tomato_Bacterial_spot": {
            "plant": "Tomato",
            "disease": "Bacterial Spot",

            "about":
                "A bacterial disease that attacks leaves, stems, and fruits, reducing plant health and fruit quality.",

            "symptoms": [
                "Small dark leaf spots",
                "Yellow halos",
                "Leaf drop",
                "Raised fruit lesions"
            ],

            "causes": [
                "Xanthomonas bacteria",
                "Warm humid weather",
                "Rain splash",
                "Infected seeds"
            ],

            "treatment": [
                "Remove infected leaves",
                "Spray copper bactericide",
                "Avoid overhead watering"
            ],

            "prevention": [
                "Use disease-free seeds",
                "Rotate crops",
                "Disinfect tools"
            ]
     },


        "Tomato_Early_blight": {
            "plant": "Tomato",
            "disease": "Early Blight",

            "about":
                "A common fungal disease causing concentric brown spots on older tomato leaves.",

            "symptoms": [
                "Brown spots with concentric rings",
                "Yellow leaves",
                "Leaf drop",
                "Reduced fruit production"
            ],

            "causes": [
                "Alternaria solani fungus",
                "Warm humid conditions"
            ],

            "treatment": [
                "Remove infected leaves",
                "Apply fungicide",
                "Improve air circulation"
            ],

            "prevention": [
                "Crop rotation",
                "Mulching",
                "Avoid wet foliage"
            ]
        },

        "Tomato_Late_blight": {
            "plant": "Tomato",
            "disease": "Late Blight",

            "about":
                "A destructive disease capable of killing tomato plants within days under cool, wet conditions.",

            "symptoms": [
                "Large brown patches",
                "White fungal growth",
                "Stem lesions",
                "Fruit rot"
            ],

            "causes": [
                "Phytophthora infestans",
                "Cool humid weather"
            ],

            "treatment": [
                "Remove infected plants",
                "Spray fungicide immediately",
                "Destroy infected debris"
            ],

            "prevention": [
                "Plant resistant varieties",
                "Improve airflow",
                "Avoid overhead watering"
            ]
        },

        "Tomato_Leaf_Mold": {
            "plant": "Tomato",
            "disease": "Leaf Mold",

            "about":
                "A fungal disease that mainly affects greenhouse tomatoes by reducing photosynthesis.",

            "symptoms": [
                "Yellow patches",
                "Olive-green mold underneath leaves",
                "Leaf curling",
                "Premature leaf drop"
            ],

            "causes": [
                "High humidity",
                "Poor ventilation",
                "Cladosporium fungus"
            ],

            "treatment": [
                "Remove infected leaves",
                "Apply fungicide",
                "Increase ventilation"
            ],

            "prevention": [
                "Reduce humidity",
                "Space plants properly",
                "Avoid wet leaves"
            ]
        },

        "Tomato_Septoria_leaf_spot": {
            "plant": "Tomato",
            "disease": "Septoria Leaf Spot",

            "about":
                "A fungal disease that creates numerous tiny spots and gradually weakens tomato plants.",

            "symptoms": [
                "Tiny circular spots",
                "Dark borders",
                "Yellowing leaves",
                "Leaf drop"
            ],

            "causes": [
                "Septoria fungus",
                "Rain splash",
                "High humidity"
            ],

            "treatment": [
                "Remove infected leaves",
                "Spray fungicide",
                "Improve air circulation"
            ],

            "prevention": [
                "Crop rotation",
                "Mulching",
                "Avoid overhead watering"
            ]
        },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "plant": "Tomato",
        "disease": "Spider Mites",

        "about":
        "Spider mites are tiny pests that feed on leaf sap, causing yellow speckles and webbing.",

        "symptoms": [
            "Tiny yellow or white spots",
            "Fine webbing under leaves",
            "Leaf curling",
            "Dry, brittle leaves"
        ],

        "causes": [
            "Two-spotted spider mites",
            "Hot dry weather",
            "Low humidity"
        ],

        "treatment": [
            "Spray neem oil",
            "Use insecticidal soap",
            "Remove heavily infested leaves"
        ],

        "prevention": [
            "Maintain proper humidity",
            "Inspect plants regularly",
            "Encourage beneficial insects"
        ]
    },

    "Tomato__Target_Spot": {
        "plant": "Tomato",
        "disease": "Target Spot",

        "about":
        "A fungal disease producing circular brown lesions that resemble a target.",

        "symptoms": [
            "Brown circular spots",
            "Concentric rings",
            "Yellowing leaves",
            "Leaf drop"
        ],

        "causes": [
            "Corynespora fungus",
            "Warm humid weather"
        ],

        "treatment": [
            "Apply fungicide",
            "Remove infected leaves",
            "Improve airflow"
        ],

        "prevention": [
            "Crop rotation",
            "Avoid wet foliage",
            "Proper plant spacing"
        ]
    },

    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "plant": "Tomato",
        "disease": "Yellow Leaf Curl Virus",

        "about":
        "A viral disease spread by whiteflies that severely reduces tomato yield.",

        "symptoms": [
            "Yellow curled leaves",
            "Stunted growth",
            "Reduced flowering",
            "Poor fruit production"
        ],

        "causes": [
            "Tomato Yellow Leaf Curl Virus",
            "Whitefly insects"
        ],

        "treatment": [
            "Remove infected plants",
            "Control whiteflies",
            "Use sticky traps"
        ],

        "prevention": [
            "Grow resistant varieties",
            "Use insect netting",
            "Control whiteflies early"
        ]
    },

    "Tomato__Tomato_mosaic_virus": {
        "plant": "Tomato",
        "disease": "Tomato Mosaic Virus",

        "about":
        "A viral disease causing mottled leaves and poor fruit development.",

        "symptoms": [
            "Light and dark green mosaic pattern",
            "Leaf distortion",
            "Stunted plants",
            "Poor fruit quality"
        ],

        "causes": [
            "Tomato Mosaic Virus",
            "Contaminated tools",
            "Infected plant material"
        ],

        "treatment": [
            "Remove infected plants",
            "Disinfect tools",
            "Do not compost infected plants"
        ],

        "prevention": [
            "Wash hands before handling plants",
            "Use disease-free seeds",
            "Disinfect equipment"
        ]
    },

    "Tomato_healthy": {
        "plant": "Tomato",
        "disease": "Healthy",

        "about":
        "The tomato plant is healthy and free from visible disease symptoms.",

        "symptoms": [
            "Bright green leaves",
            "Strong stems",
            "Healthy flowers",
            "Normal fruit development"
        ],

        "causes": [
            "Proper nutrition",
            "Adequate watering",
            "Good sunlight"
        ],

        "treatment": [
            "No treatment required"
        ],

        "prevention": [
            "Continue regular watering",
            "Fertilize as needed",
            "Inspect plants weekly"
        ]
    }

}