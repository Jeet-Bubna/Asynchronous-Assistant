from modules import music, timer, search

FUNCTIONS_LIST = {
    "functions": [
        {
            "name": "music",
            "func": music.main
        },
        {
            "name": "time",
            "func": timer.main
        },
        {
            "name": "search",
            "func": search.main
        }
    ]
}

EMBEDDING_FILE = "stored_embeddings.npy"

ACCEPTABLE_RATIO = 0.5

CATEGORIES  = {'music': 'music player', 'timer':'timer', 'search':'search', 'end':'end the program'}  

MODEL_PATH = "./local_model"

MODEL_NAME ="sentence-transformers/all-MiniLM-L6-v2"

TIME_TO_JOIN_THREAD = 5