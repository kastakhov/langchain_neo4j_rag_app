# Build an LLM RAG Chatbot With LangChain

Note: This repo originally based on the source code from [Build an LLM RAG Chatbot With LangChain](https://realpython.com/build-llm-rag-chatbot-with-langchain/#demo-a-llm-rag-chatbot-with-langchain-and-neo4j).

Create a `.env` file from `sample.env` in the root directory.

Update API and NEO4J secrets:

* *_MODEL_API_BASE
* *_MODEL_API_KEY
* NEO4J_URI
* NEO4J_USERNAME
* NEO4J_PASSWORD

It's possible to use LangFuse to debug RAG app. Fill the next env variable in .env and restart the chatbot_api container.

* LANGFUSE_SECRET_KEY
* LANGFUSE_PUBLIC_KEY
* LANGFUSE_HOST

Default bot configuration stored in [configuration.yaml.default](chatbot_api/src/chatbot_api/configuration.yaml.default). This configuration will be loaded if `configuration.yaml` doesn't exist (this file will be created after first update request).

This secrets are not populated to the configuration.yaml which could be updated in runtime with `CHATBOT_URL/config/update` POST request with JSON in data.

Current configuration could be obtained with `CHATBOT_URL/config/show` GET request (all fields could be changed, some have validation).

Note: "apoc" plugin have to be installed into neo4j database (already done for docker-compse)

For docker env the next value for chatbot fronted url should be used:

```env
CHATBOT_URL=http://chatbot_api:8000
```

The either [debug](https://python.langchain.com/v0.2/docs/how_to/debugging/#set_debugtrue) or [verbose](https://python.langchain.com/v0.2/docs/how_to/debugging/#set_verbosetrue) output for langchain chains could be enable with the next variables, by default False.

```env
LANGCHAIN_DEBUG=True
LANGCHAIN_VERBOSE=True
```

The next variable should be configured to load data presets localy, otherwise set `_CSV_PATH` variables with http/https urls to csv files.

```env
#NEO4J_ETL_URL=<neo4j_etl container hostname>
NEO4J_ETL_URL=http://neo4j_etl:8000
```

Once you have a running Neo4j instance, and have filled out all the environment variables in `.env`, you can run the entire project with [Docker Compose](https://docs.docker.com/compose/). You can install Docker Compose by following [these directions](https://docs.docker.com/compose/install/).

Once you've filled in all of the environment variables, and installed Docker Compose, open a terminal and run:

```shell
make build
make start
```

After each container finishes building, you'll be able to access the chatbot api at `http://localhost:8000/docs` and the Streamlit app at `http://localhost:8501/`.

## Change models

Changing model names and their configs can be done online like this, note we connect to the `chatbot-api` to tertive & update [chatbot_api/models.config.json](chatbot_api/models.config.json).

While changing the LLM provider endpoints requires restarting chatbot-api container: update the `.env` for the docker.

![Demo](./langchain_rag_chatbot_demo.gif)

## Examples and materials

* [ ] [RAG Explanation](https://towardsdatascience.com/intro-to-llm-agents-with-langchain-when-rag-is-not-enough-7d8c08145834)
* [ ] [Knowlage Graph Explanation](https://medium.com/stackademic/using-neo4j-and-langchain-for-knowledge-graph-creation-a-detailed-guide-84e7a74495eb)

## Ideas for reasoning improvement

* [ ] [Reflexion](https://arxiv.org/abs/2303.11366)
* [ ] [Chain of Hindsight](https://arxiv.org/abs/2302.02676)
* [ ] [Tree of Thought example + Yutube](https://github.com/Rachnog/intro_to_llm_agents)

## LocalAI and Ollama issues

* Ollama cannot be used as llm for Agent as the model cannot access to the mock data for some reason, the only `localai` or `openai` can be used for AGENT_MODEL_ENGINE. Also, ChatOpenAI is being used internally instead of ChatOllama due to [Langchain issue 21479](https://github.com/langchain-ai/langchain/issues/21479)
* For some reason LocalAI has an issue with embeddings, the only `ollama` or `openai` can be used for EMBEDDINGS_MODEL_ENGINE.

### Examples of API request to LocalAI

<https://mudler.pm/posts/localai-question-answering/>
