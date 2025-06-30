# Overview of all the things that needed to be done

1. Integrate litellm for llm api calling (also remove genai from the package list)
2. Add multiple models such as OpenAI, Google, Anthorpic, Openrouter model, Openrouter free model
3. Setup api key in the env file using argparser or something like that
4. for now 4 seperate argument can be use openai, google, anthorpic, openrouter to setup the api key
5. Initially set the default llm to an free openrouter llm
6. another cmd argument to set a defualt model so that that model will be choose at the starting.
7. Try to write a more better prompt
8. Handle the argument passing from a deb installed program
9. Handle proper exception handling (suppose the structure output is wrong, the api key is not there, the connection is closed or etc etc )
10. Create a bash script to automate the deb package building process
11. If possible write a cicd yaml to automate the package publication on github
12. Create a proper readme and push to github with proper instruction
13. Finally if possible create a makefile so that anyone can compile from the source.


# Thing to do (in depth) 

1. Integrate LiteLLM for universal model call:
    - We were using `genai` library from google and from there we were calling gemini models
    - we will switch to LiteLLM and utilize an universal integration of LLM.
    - First we update `LLM_Integration.py` with litellm
    - look in the `litellm_testing.py` file for example how the litellm is being used and strcture output is being handled
    - get all the api key from the `.env` and store each of them in a variable.
    - then after updating to litellm we first test them with the current model (gemini)
    - We pass the `GEMINI_API_KEY` key in the completion of `litellm`

2. **Adding more model from different providers:**
    - In this phase we'll increase the total number of model
    - Available model is going to be
        - Existing gemini model
        - New gemini model
            - gemini/gemini-2.5-flash-lite-preview-06-17
            - gemini/gemini-2.5-flash
        - OpenAI models
            - openai/gpt-4o-mini
            - openai/gpt-4.1
            - openai/gpt-4.1-mini
            - openai/gpt-4.1-nano
            - openai/gpt-4o
        - Anthropic
            - anthropic/claude-sonnet-4
            - anthropic/claude-3.7-sonnet
            - anthropic/claude-3.5-sonnet
        - Openrouter (free)
            - openrouter/deepseek/deepseek-chat:free
            - openrouter/qwen/qwen3-32b:free
            - openrouter/mistralai/mistral-small-3.1-24b-instruct:free
            - openrouter/mistralai/mistral-small-3.2-24b-instruct:free
            - openrouter/mistralai/devstral-small:free
            - openrouter/qwen/qwen3-14b:free
            - openrouter/qwen/qwen3-8b:free
            - openrouter/google/gemma-3-27b-it:free
    - Create a seperate file  (inside app folder) and put all these value inside a list
    - import that list inside the `app.py` file
    - update the `self.llm_list` with that list
    - update the default llm (`self.model`) with the `openrouter/mistralai/devstral-small:free`



# Task Progress

- [x] litellm integration for universal LLM integration
- [x] update the LLM provider list