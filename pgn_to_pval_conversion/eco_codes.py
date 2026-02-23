# ECO code to opening name mapping based on https://en.wikipedia.org/wiki/List_of_ECO_codes
# It is very likely that there are errors in this file (blame Claude, not me).
# I did not end up using any ECO codes or opening names in my final analysis but it is definitely a potential area to explore.

ECO_CODES = {
    # A00-A39: Irregular Openings and English Opening
    "A00": "Uncommon Opening", 
    "A01": "Nimzowitsch-Larsen Attack", 
    "A02": "Bird's Opening", "A03": "Bird's Opening", 
    "A04": "Reti Opening", "A05": "Reti Opening", "A06": "Reti Opening", 
    "A07": "King's Indian Attack", "A08": "King's Indian Attack",
    "A09": "Reti Opening", 
    "A10": "English Opening", 
    "A11": "English Opening, Caro-Kann Defensive System",
    "A12": "English Opening", "A13": "English Opening", "A14": "English Opening, Neo-Catalan",
    "A15": "English Opening", "A16": "English Opening", "A17": "English Opening",
    "A18": "English Opening, Mikenas-Carls", "A19": "English Opening, Mikenas-Carls",
    "A20": "English Opening", "A21": "English Opening", "A22": "English Opening",
    "A23": "English Opening", "A24": "English Opening", "A25": "English Opening",
    "A26": "English Opening", "A27": "English Opening", "A28": "English Opening",
    "A29": "English Opening", "A30": "English Opening", "A31": "English Opening",
    "A32": "English Opening", "A33": "English Opening", "A34": "English Opening",
    "A35": "English Opening", "A36": "English Opening", "A37": "English Opening",
    "A38": "English Opening", "A39": "English Opening",

    # A40-A44: Queen's Pawn Game
    "A40": "Queen's Pawn Game", "A41": "Queen's Pawn Game", "A42": "Modern Defense",
    "A43": "Old Benoni Defense", "A44": "Old Benoni Defense",

    # A45-A49: Indian Game and Trompowsky
    "A45": "Indian Game", "A46": "Queen's Pawn Game", "A47": "Queen's Indian Defense",
    "A48": "King's Indian", "A49": "King's Indian",

    # A50-A79: Indian Defenses
    "A50": "Queen's Pawn Game", "A51": "Budapest Gambit", "A52": "Budapest Gambit",
    "A53": "Old Indian Defense", "A54": "Old Indian Defense", "A55": "Old Indian Defense",
    "A56": "Benoni Defense", "A57": "Benko Gambit", "A58": "Benko Gambit",
    "A59": "Benko Gambit", "A60": "Benoni Defense", "A61": "Benoni Defense",
    "A62": "Benoni Defense", "A63": "Benoni Defense", "A64": "Benoni Defense",
    "A65": "Benoni Defense", "A66": "Benoni Defense", "A67": "Benoni Defense",
    "A68": "Benoni Defense", "A69": "Benoni Defense", "A70": "Benoni Defense",
    "A71": "Benoni Defense", "A72": "Benoni Defense", "A73": "Benoni Defense",
    "A74": "Benoni Defense", "A75": "Benoni Defense", "A76": "Benoni Defense",
    "A77": "Benoni Defense", "A78": "Benoni Defense", "A79": "Benoni Defense",

    # A80-A99: Dutch Defense
    "A80": "Dutch Defense", "A81": "Dutch Defense", "A82": "Dutch Defense",
    "A83": "Dutch Defense", "A84": "Dutch Defense", "A85": "Dutch Defense",
    "A86": "Dutch Defense", "A87": "Dutch Defense", "A88": "Dutch Defense",
    "A89": "Dutch Defense", "A90": "Dutch Defense", "A91": "Dutch Defense",
    "A92": "Dutch Defense", "A93": "Dutch Defense", "A94": "Dutch Defense",
    "A95": "Dutch Defense", "A96": "Dutch Defense", "A97": "Dutch Defense",
    "A98": "Dutch Defense", "A99": "Dutch Defense",

    # B00-B09: King's Pawn Game and Defenses
    "B00": "King's Pawn Opening", "B01": "Scandinavian Defense", "B02": "Alekhine's Defense",
    "B03": "Alekhine's Defense", "B04": "Alekhine's Defense", "B05": "Alekhine's Defense",
    "B06": "Modern Defense", "B07": "Pirc Defense", "B08": "Pirc Defense",
    "B09": "Pirc Defense",

    # B10-B19: Caro-Kann Defense
    "B10": "Caro-Kann Defense", "B11": "Caro-Kann Defense", "B12": "Caro-Kann Defense",
    "B13": "Caro-Kann Defense", "B14": "Caro-Kann Defense", "B15": "Caro-Kann Defense",
    "B16": "Caro-Kann Defense", "B17": "Caro-Kann Defense", "B18": "Caro-Kann Defense",
    "B19": "Caro-Kann Defense",

    # B20-B99: Sicilian Defense
    "B20": "Sicilian Defense", "B21": "Sicilian Defense", "B22": "Sicilian Defense",
    "B23": "Sicilian Defense", "B24": "Sicilian Defense", "B25": "Sicilian Defense",
    "B26": "Sicilian Defense", "B27": "Sicilian Defense", "B28": "Sicilian Defense",
    "B29": "Sicilian Defense", "B30": "Sicilian Defense", "B31": "Sicilian Defense",
    "B32": "Sicilian Defense", "B33": "Sicilian Defense", "B34": "Sicilian Defense",
    "B35": "Sicilian Defense", "B36": "Sicilian Defense", "B37": "Sicilian Defense",
    "B38": "Sicilian Defense", "B39": "Sicilian Defense", "B40": "Sicilian Defense",
    "B41": "Sicilian Defense", "B42": "Sicilian Defense", "B43": "Sicilian Defense",
    "B44": "Sicilian Defense", "B45": "Sicilian Defense", "B46": "Sicilian Defense",
    "B47": "Sicilian Defense", "B48": "Sicilian Defense", "B49": "Sicilian Defense",
    "B50": "Sicilian Defense", "B51": "Sicilian Defense", "B52": "Sicilian Defense",
    "B53": "Sicilian Defense", "B54": "Sicilian Defense", "B55": "Sicilian Defense",
    "B56": "Sicilian Defense", "B57": "Sicilian Defense", "B58": "Sicilian Defense",
    "B59": "Sicilian Defense", "B60": "Sicilian Defense", "B61": "Sicilian Defense",
    "B62": "Sicilian Defense", "B63": "Sicilian Defense", "B64": "Sicilian Defense",
    "B65": "Sicilian Defense", "B66": "Sicilian Defense", "B67": "Sicilian Defense",
    "B68": "Sicilian Defense", "B69": "Sicilian Defense", "B70": "Sicilian Defense",
    "B71": "Sicilian Defense", "B72": "Sicilian Defense", "B73": "Sicilian Defense",
    "B74": "Sicilian Defense", "B75": "Sicilian Defense", "B76": "Sicilian Defense",
    "B77": "Sicilian Defense", "B78": "Sicilian Defense", "B79": "Sicilian Defense",
    "B80": "Sicilian Defense", "B81": "Sicilian Defense", "B82": "Sicilian Defense",
    "B83": "Sicilian Defense", "B84": "Sicilian Defense", "B85": "Sicilian Defense",
    "B86": "Sicilian Defense", "B87": "Sicilian Defense", "B88": "Sicilian Defense",
    "B89": "Sicilian Defense", "B90": "Sicilian Defense", "B91": "Sicilian Defense",
    "B92": "Sicilian Defense", "B93": "Sicilian Defense", "B94": "Sicilian Defense",
    "B95": "Sicilian Defense", "B96": "Sicilian Defense", "B97": "Sicilian Defense",
    "B98": "Sicilian Defense", "B99": "Sicilian Defense",

    # C00-C19: French Defense
    "C00": "French Defense", "C01": "French Defense", "C02": "French Defense",
    "C03": "French Defense", "C04": "French Defense", "C05": "French Defense",
    "C06": "French Defense", "C07": "French Defense", "C08": "French Defense",
    "C09": "French Defense", "C10": "French Defense", "C11": "French Defense",
    "C12": "French Defense", "C13": "French Defense", "C14": "French Defense",
    "C15": "French Defense", "C16": "French Defense", "C17": "French Defense",
    "C18": "French Defense", "C19": "French Defense",

    # C20-C29: Open Games (King's Pawn)
    "C20": "King's Pawn Game", "C21": "Danish Gambit", "C22": "Center Game",
    "C23": "Bishop's Opening", "C24": "Bishop's Opening", "C25": "Vienna Game",
    "C26": "Vienna Game", "C27": "Vienna Game", "C28": "Vienna Game",
    "C29": "Vienna Game",

    # C30-C39: King's Gambit
    "C30": "King's Gambit", "C31": "King's Gambit", "C32": "King's Gambit",
    "C33": "King's Gambit", "C34": "King's Gambit", "C35": "King's Gambit",
    "C36": "King's Gambit", "C37": "King's Gambit", "C38": "King's Gambit",
    "C39": "King's Gambit",

    # C40-C49: Open Games
    "C40": "King's Knight Opening", "C41": "Philidor Defense", "C42": "Petrov's Defense",
    "C43": "Petrov's Defense", "C44": "King's Pawn Game", "C45": "Scotch Game",
    "C46": "Three Knights Game", "C47": "Four Knights Game", "C48": "Four Knights Game",
    "C49": "Four Knights Game",

    # C50-C59: Italian Game
    "C50": "Italian Game", "C51": "Italian Game", "C52": "Italian Game",
    "C53": "Italian Game", "C54": "Italian Game", "C55": "Two Knights Defense",
    "C56": "Two Knights Defense", "C57": "Two Knights Defense", "C58": "Two Knights Defense",
    "C59": "Two Knights Defense",

    # C60-C99: Ruy Lopez (Spanish Game)
    "C60": "Ruy Lopez", "C61": "Ruy Lopez", "C62": "Ruy Lopez",
    "C63": "Ruy Lopez", "C64": "Ruy Lopez", "C65": "Ruy Lopez",
    "C66": "Ruy Lopez", "C67": "Ruy Lopez", "C68": "Ruy Lopez",
    "C69": "Ruy Lopez", "C70": "Ruy Lopez", "C71": "Ruy Lopez",
    "C72": "Ruy Lopez", "C73": "Ruy Lopez", "C74": "Ruy Lopez",
    "C75": "Ruy Lopez", "C76": "Ruy Lopez", "C77": "Ruy Lopez",
    "C78": "Ruy Lopez", "C79": "Ruy Lopez", "C80": "Ruy Lopez",
    "C81": "Ruy Lopez", "C82": "Ruy Lopez", "C83": "Ruy Lopez",
    "C84": "Ruy Lopez", "C85": "Ruy Lopez", "C86": "Ruy Lopez",
    "C87": "Ruy Lopez", "C88": "Ruy Lopez", "C89": "Ruy Lopez",
    "C90": "Ruy Lopez", "C91": "Ruy Lopez", "C92": "Ruy Lopez",
    "C93": "Ruy Lopez", "C94": "Ruy Lopez", "C95": "Ruy Lopez",
    "C96": "Ruy Lopez", "C97": "Ruy Lopez", "C98": "Ruy Lopez",
    "C99": "Ruy Lopez",

    # D00-D05: Queen's Pawn Game
    "D00": "Queen's Pawn Game", "D01": "Veresov Opening", "D02": "Queen's Pawn Game",
    "D03": "Torre Attack", "D04": "Queen's Pawn Game", "D05": "Queen's Pawn Game",

    # D06-D69: Queen's Gambit
    "D06": "Queen's Gambit", "D07": "Queen's Gambit", "D08": "Queen's Gambit",
    "D09": "Queen's Gambit", "D10": "Queen's Gambit", "D11": "Queen's Gambit",
    "D12": "Queen's Gambit", "D13": "Queen's Gambit", "D14": "Queen's Gambit",
    "D15": "Queen's Gambit", "D16": "Queen's Gambit", "D17": "Queen's Gambit",
    "D18": "Queen's Gambit", "D19": "Queen's Gambit", "D20": "Queen's Gambit",
    "D21": "Queen's Gambit", "D22": "Queen's Gambit", "D23": "Queen's Gambit",
    "D24": "Queen's Gambit", "D25": "Queen's Gambit", "D26": "Queen's Gambit",
    "D27": "Queen's Gambit", "D28": "Queen's Gambit", "D29": "Queen's Gambit",
    "D30": "Queen's Gambit", "D31": "Queen's Gambit", "D32": "Queen's Gambit",
    "D33": "Queen's Gambit", "D34": "Queen's Gambit", "D35": "Queen's Gambit",
    "D36": "Queen's Gambit", "D37": "Queen's Gambit", "D38": "Queen's Gambit",
    "D39": "Queen's Gambit", "D40": "Queen's Gambit", "D41": "Queen's Gambit",
    "D42": "Queen's Gambit", "D43": "Queen's Gambit", "D44": "Queen's Gambit",
    "D45": "Queen's Gambit", "D46": "Queen's Gambit", "D47": "Queen's Gambit",
    "D48": "Queen's Gambit", "D49": "Queen's Gambit", "D50": "Queen's Gambit",
    "D51": "Queen's Gambit", "D52": "Queen's Gambit", "D53": "Queen's Gambit",
    "D54": "Queen's Gambit", "D55": "Queen's Gambit", "D56": "Queen's Gambit",
    "D57": "Queen's Gambit", "D58": "Queen's Gambit", "D59": "Queen's Gambit",
    "D60": "Queen's Gambit", "D61": "Queen's Gambit", "D62": "Queen's Gambit",
    "D63": "Queen's Gambit", "D64": "Queen's Gambit", "D65": "Queen's Gambit",
    "D66": "Queen's Gambit", "D67": "Queen's Gambit", "D68": "Queen's Gambit",
    "D69": "Queen's Gambit",

    # D70-D99: Grunfeld and Indian Defenses
    "D70": "Neo-Grunfeld Defense", "D71": "Neo-Grunfeld Defense", "D72": "Neo-Grunfeld Defense",
    "D73": "Neo-Grunfeld Defense", "D74": "Neo-Grunfeld Defense", "D75": "Neo-Grunfeld Defense",
    "D76": "Neo-Grunfeld Defense", "D77": "Neo-Grunfeld Defense", "D78": "Neo-Grunfeld Defense",
    "D79": "Neo-Grunfeld Defense", "D80": "Grunfeld Defense", "D81": "Grunfeld Defense",
    "D82": "Grunfeld Defense", "D83": "Grunfeld Defense", "D84": "Grunfeld Defense",
    "D85": "Grunfeld Defense", "D86": "Grunfeld Defense", "D87": "Grunfeld Defense",
    "D88": "Grunfeld Defense", "D89": "Grunfeld Defense", "D90": "Grunfeld Defense",
    "D91": "Grunfeld Defense", "D92": "Grunfeld Defense", "D93": "Grunfeld Defense",
    "D94": "Grunfeld Defense", "D95": "Grunfeld Defense", "D96": "Grunfeld Defense",
    "D97": "Grunfeld Defense", "D98": "Grunfeld Defense", "D99": "Grunfeld Defense",

    # E00-E09: Catalan and Indian Systems
    "E00": "Queen's Pawn Game", "E01": "Catalan Opening", "E02": "Catalan Opening",
    "E03": "Catalan Opening", "E04": "Catalan Opening", "E05": "Catalan Opening",
    "E06": "Catalan Opening", "E07": "Catalan Opening", "E08": "Catalan Opening",
    "E09": "Catalan Opening",

    # E10-E19: Queen's Indian Defense
    "E10": "Queen's Indian Defense", "E11": "Queen's Indian Defense", "E12": "Queen's Indian Defense",
    "E13": "Queen's Indian Defense", "E14": "Queen's Indian Defense", "E15": "Queen's Indian Defense",
    "E16": "Queen's Indian Defense", "E17": "Queen's Indian Defense", "E18": "Queen's Indian Defense",
    "E19": "Queen's Indian Defense",

    # E20-E59: Nimzo-Indian Defense
    "E20": "Nimzo-Indian Defense", "E21": "Nimzo-Indian Defense", "E22": "Nimzo-Indian Defense",
    "E23": "Nimzo-Indian Defense", "E24": "Nimzo-Indian Defense", "E25": "Nimzo-Indian Defense",
    "E26": "Nimzo-Indian Defense", "E27": "Nimzo-Indian Defense", "E28": "Nimzo-Indian Defense",
    "E29": "Nimzo-Indian Defense", "E30": "Nimzo-Indian Defense", "E31": "Nimzo-Indian Defense",
    "E32": "Nimzo-Indian Defense", "E33": "Nimzo-Indian Defense", "E34": "Nimzo-Indian Defense",
    "E35": "Nimzo-Indian Defense", "E36": "Nimzo-Indian Defense", "E37": "Nimzo-Indian Defense",
    "E38": "Nimzo-Indian Defense", "E39": "Nimzo-Indian Defense", "E40": "Nimzo-Indian Defense",
    "E41": "Nimzo-Indian Defense", "E42": "Nimzo-Indian Defense", "E43": "Nimzo-Indian Defense",
    "E44": "Nimzo-Indian Defense", "E45": "Nimzo-Indian Defense", "E46": "Nimzo-Indian Defense",
    "E47": "Nimzo-Indian Defense", "E48": "Nimzo-Indian Defense", "E49": "Nimzo-Indian Defense",
    "E50": "Nimzo-Indian Defense", "E51": "Nimzo-Indian Defense", "E52": "Nimzo-Indian Defense",
    "E53": "Nimzo-Indian Defense", "E54": "Nimzo-Indian Defense", "E55": "Nimzo-Indian Defense",
    "E56": "Nimzo-Indian Defense", "E57": "Nimzo-Indian Defense", "E58": "Nimzo-Indian Defense",
    "E59": "Nimzo-Indian Defense",

    # E60-E99: King's Indian Defense
    "E60": "King's Indian Defense", "E61": "King's Indian Defense", "E62": "King's Indian Defense",
    "E63": "King's Indian Defense", "E64": "King's Indian Defense", "E65": "King's Indian Defense",
    "E66": "King's Indian Defense", "E67": "King's Indian Defense", "E68": "King's Indian Defense",
    "E69": "King's Indian Defense", "E70": "King's Indian Defense", "E71": "King's Indian Defense",
    "E72": "King's Indian Defense", "E73": "King's Indian Defense", "E74": "King's Indian Defense",
    "E75": "King's Indian Defense", "E76": "King's Indian Defense", "E77": "King's Indian Defense",
    "E78": "King's Indian Defense", "E79": "King's Indian Defense", "E80": "King's Indian Defense",
    "E81": "King's Indian Defense", "E82": "King's Indian Defense", "E83": "King's Indian Defense",
    "E84": "King's Indian Defense", "E85": "King's Indian Defense", "E86": "King's Indian Defense",
    "E87": "King's Indian Defense", "E88": "King's Indian Defense", "E89": "King's Indian Defense",
    "E90": "King's Indian Defense", "E91": "King's Indian Defense", "E92": "King's Indian Defense",
    "E93": "King's Indian Defense", "E94": "King's Indian Defense", "E95": "King's Indian Defense",
    "E96": "King's Indian Defense", "E97": "King's Indian Defense", "E98": "King's Indian Defense",
    "E99": "King's Indian Defense",
}

# Function to convert ECO code to opening name
def eco_code_to_opening_name(eco_code):
    """
    Convert ECO code to opening name.

    Args:
        eco_code: ECO code string (e.g., "C00", "E60")

    Returns:
        str: Opening name (e.g., "French Defense", "King's Indian Defense")
             Returns "Unknown" if ECO code is not found
    """
    if eco_code is None or eco_code == "":
        return "Unknown"

    return ECO_CODES.get(eco_code, "Unknown")
