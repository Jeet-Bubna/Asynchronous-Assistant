from modules import music, timer, search

FUNCTIONS_LIST = {
    "functions": [
        {
            "name": "music",
            "args": ["text"],
            "func": music.main
        },
        {
            "name": "time",
            "args": ["text"],
            "func": timer.main
        },
        {
            "name": "search",
            "args": ["text"],
            "func": search.main
        }
    ]
}

EMBEDDING_FILE = "stored_embeddings.npy"

ACCEPTABLE_RATIO = 0.3

CATEGORIES  = {'music': 'music player', 'timer':'timer', 'search':'search', 'end':'end the program'}  

MODEL_PATH = "./local_model"

MODEL_NAME ="sentence-transformers/all-MiniLM-L6-v2"