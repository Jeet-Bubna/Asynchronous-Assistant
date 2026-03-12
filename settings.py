from modules import music, timer, search

FUNCTIONS_LIST = {
    "functions": [
        {
            "name": "music",
            "args": ["text"],
            "func": music
        },
        {
            "name": "time",
            "args": ["text"],
            "func": timer
        },
        {
            "name": "search",
            "args": ["text"],
            "func": search
        }
    ]
}

EMBEDDING_FILE = "stored_embeddings.npy"

ACCEPTABLE_RATIO = 0.3

CATEGORIES  = {'music': 'music player', 'timer':'timer', 'search':'search', 'end':'end the program'}  