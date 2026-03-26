from modules import music, timer, search

ASSISTANT_NAME = "jarvis"

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

CATEGORIES  = {
    "music":{
        "general description":"commands for playing, pausing, stopping, and ressuming music playback",
        "commands":{
            "play":["play music", "start the music", "put on some tunes"],
            "stop":["stop the music"],
            "resume":["resume", "resume music", "restart music"],
            "switch":["change song", "switch song", "change music"]
        }
    },
    "end":{
        "general description":"command to end the program"
    }
}

MODEL_PATH = "./local_model"

MODEL_NAME ="sentence-transformers/all-MiniLM-L6-v2"

TIME_TO_JOIN_THREAD = 5