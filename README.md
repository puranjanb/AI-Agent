Topic :-
Building ai agent with retrieval augmented generation capabilities.
This project  uses multiple llms(mistral and codellama), connect them and parse the output of one llm using another.
Ollama and LlamaIndex has been used in this project.

Basic Idea :-
Llamaindex – llm framework – open source – load data, index data, query and evaluate llm application.
Llamaparse – retrieval augmented generation capability, part of llamaindex.
Ollama – allows running open source llm locally, open source alternative for chatgpt. 

What the project contains :-
Some data(an api documentation) is provided to the llm model - readme pdf in data directory.
test.py is an implementation of the api.
code_reader.py helps read the code from the file test.py and wrap it in a function tool for the llm.
api_interaction.py in output directory is the generated file.

The llm model reads api documentation and the test.py code, and generates some code based on that as per our prompt request.
Output.pdf is a snapshot of the output in the terminal.


Detailed description :-
LlamaParse breaks down input data into logical chunks.
The logical chunks are then used to create vector embeddings.
The data is stored in a multi dimensional space (vector embeddings) based on several parameters like sentiment, meaning, etc. 
The vector embeddings are stored in VectorStoreIndex that is a very fast database that helps query the vector embeddings as per requirement. 
Thus we don’t store the entire pdf file but just query and pick as per requirement. The parser injects the answer to our query, into the llm.
The llm processes the answer and provides the output (in this case the generated code). Then the output code is saved in an file.
