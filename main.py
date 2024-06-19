from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.query_pipeline import QueryPipeline
from prompts import context, code_parser_template
from dotenv import load_dotenv
from code_reader import code_reader
import ast,os

def llamaLLM():

    load_dotenv()   # checks for .env file and loads the contents

    llm = Ollama(model="mistral", request_timeout=300.0)    # create mistral model llm in Ollama

    parser = LlamaParse(result_type='markdown')
    # create a parser that takes the pdf, pushes it to cloud, parses it and returns parsed output

    file_extractor = {'.pdf': parser}   # all pdfs present will be parsed using file_extractor

    documents = SimpleDirectoryReader('./data', file_extractor=file_extractor).load_data()  # load files from directory and load the data

    embed_model = resolve_embed_model('local:BAAI/bge-m3')
    # a local model to create the vector store index instead of default OpenAImodel

    vector_index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    # create the vector index from the documents we loaded and embed using the embed model

    query_engine = vector_index.as_query_engine(llm=llm)    # create query engine to interact with llm

    tools = [
         QueryEngineTool(
             query_engine=query_engine,
             metadata=ToolMetadata(
                 name='api_documentation',
                 description='this gives documentation about code for an API. Use this for reading docs for the API',
             ),
         ),
        code_reader,    # tool to read the python code
     ]
    code_llm = Ollama(model='codellama', request_timeout=300.0) # codellama for code generation

    agent = ReActAgent.from_tools(tools, llm=code_llm, verbose=True, context=context)
    #verbose - thoughts of the agent
    # agent reads, analyzes and answers questions about code

    class CodeOutput(BaseModel):    # pydantic BaseModel object
        code: str
        description: str
        filename: str

    parser = PydanticOutputParser(CodeOutput)   # parse the code output
    json_prompt_str = parser.format(code_parser_template)   # reads string from prompts, takes pydantic format and injects it in parser
    json_prompt_template = PromptTemplate(json_prompt_str)  # injects the response in prompt template
    output_pipeline = QueryPipeline(chain=[json_prompt_template, llm])  # output chain with mistral llm


    while (prompt := input("Enter a prompt (q to quit): ")) != 'q':
        retries = 0

        while retries < 3:
            try:
                result = agent.query(prompt)    # send prompt to agent
                next_result = output_pipeline.run(response=result)  # feed the response to the output pipeline
                cleaned_json = ast.literal_eval(str(next_result).replace('assistant:',''))  # convert to valid python code as a dictionary
                break
            except Exception as e:
                retries += 1
                print(f'Error occured, retry #{retries}:', e)   # print retry number and error message

        if retries >= 3:
            print('Unable to process req, try again.....')
            continue
        print(cleaned_json)
        print("Code Generated")
        print(cleaned_json['code'])
        print("\nDescription:\n", cleaned_json['description'])

        filename = cleaned_json['filename']

        try:
            with open(os.path.join('output', filename), 'w') as f:
                f.write(cleaned_json['code'])   # writing code in file
            print('Saved File', filename)
        except:
            print('Error saving file...')

if __name__ == '__main__':
    llamaLLM()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
