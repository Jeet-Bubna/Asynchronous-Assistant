# Subcategorization Problem

## Problem

The problem is that broad categorization for the categories belonging to the function module which is concerned with the task is not sufficient to determine the sub-action to be performed within that module. For example, if it detects that music, ie. music worker is the concerned thread for command, it cannot determine _what_ to do in music thread. Right now, we have initialised it such that it will always play music, and will end it if end command is sent. But it cannot distinguish between playing and stopping music, switching songs, finding the song name, etc.

  

## Possible Solutions

 - **In-function Categorization**: This involves categorization using a same (or different) onnx model in the sub-module itself. In this, the current functional architecture remains unchanged, and the categorisation will be handled exclusivly by the concerned modules.
**Benefits** : 
	 - Reduced code complexity as there is no need to incorportate all the different commands and sub commands in the main cateogirsation list
	 - No need to update the architecture and codebase to handle this. All can be done exclusively through the functions itself
	 - Modularity as the code will be reusable in other projects so it might be more helpful to other developers
	 - As all function related categorization is done in-house, reduces the execution speed (even though very slightly for a small sample) of the main categorization function, as less l1 and l2 normalization calculations need to be performed,

	**Drawbacks**
	

	 - Categorisation using embedding takes up a lot of CPU cycles, keeps the thread busy for more time and reduces the apparent speediness of the program.
	 - For same model, importing requires some tweaking in the arguments of the threads, so not a completely hands-off solution. For different model, if the same model (which is different from the main categorization model) is used, then a centralized function is required to load that model and pass it in parameters to the worker threads. If different models are used for different threads, then either give the parameters are locally override the parameters in the function itself or maintain a list of models and their corresponding threads.
	 - Realistically, no developers are going to be taking this codebase, especially modules to incorporate in their own codebase. If they are, they are exceptional and not the norm. Hence, it makes minimal sense to think about edge cases and prioritize this over better architecture and faster execution speed.
	 - Adding another function to the modules gives another possible point of error which needs to be tested and worried about.

 - **Global Categorization**: This involves categorization in the `init` function with the  `categories_list` from `settings.py`. In this, all the possible commands in all modules will be present in one list, and the best `argmax` value from there resulting matrix will be matched with the module and function. This is similar to what we are doing as of writing this, and will require significant structural change.
**Benefits**:

	 - It keeps the function of a worker thread to just working the given specified task and leaves the categorization part for the input function to handle. 
	 - In comparison to the previously mentioned solution, is more easily testable and doesnt introduce more friction and possible technical debt

	**Drawbacks**
	

	 - Increases program delays and setting up time as more information needs to be loaded and processed while calcualting the argmax score. Though minimal with a small set of modules and sub commands
	 - Implementation becomes tricky as existing framework of returns and paramters need to be altered drastically to accomodate multiple ways to access same thread, possibly by a tokenising function which breaks the target string by a seperator (most likely a full stop) and comapring the first token with predefined main categories. The second token is then passed on to the program which uses a lookup table to find the corresponding function and call it with required parameters, checking if parameters are met and putting a message in the listener queue if flow is obstructed by a bad request. 

 - **Regex-Based Sub-Categorisation**: Involves reaserching about pre-determined patterns in pre-defined sub commands per module and implementing a regex match with all possible sub-commands inside the module itslef. Simplest and most simple to implement, but limited in expandability and maintainability as lingo and slang evolve over time.
 - **Mixed Sub-Categorization**: Involves both regex and embedding based categorization to avoid unnecessary calculations. More of a supplement to the main in-function and global categorization argument.  

## Further Thought Process moved to `ImprovedCategorisation.md` after more Research