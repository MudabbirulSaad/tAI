# Overview of all the things that needed to be done

1. Integrate litellm for llm api calling (also remove genai from the package list) (done)
2. Add multiple models such as OpenAI, Google, Anthorpic, Openrouter model, Openrouter free model (done)
3. Setup api key in the env file using argparser or something like that  (done)
4. for now 4 seperate argument can be use openai, google, anthorpic, openrouter to setup the api key (done)
5. Initially set the default llm to an free openrouter llm (done set to devstrall free)
6. another cmd argument to set a defualt model so that model will be choose at the starting.
7. Add TUI settings for api and default model configuration.
7. Try to write a more better prompt
8. Handle the argument passing from a deb installed program
9. Handle proper exception handling (suppose the structure output is wrong, the api key is not there, the connection is closed or etc etc )
10. Create a bash script to automate the deb package building process
11. If possible write a cicd yaml to automate the package publication on github
12. Create a proper readme and push to github with proper instruction
13. Finally if possible create a makefile so that anyone can compile from the source.

-- Future Enhancement (later version)
- Context adding to LLM
    - current path
    - previous few commands
    - previous response
- TUI settings
    - default model from the TUI
    - API key setup from the TUI
    - Prompt configuration from the TUI
- Code refactoring
    - All the config (model name and default model name should be in a single json)
    - for argparser import should not happen (unnecessary) but only happen when using main


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

2.1. **Updating the modelname:**
    - The current model name contains `provider/model_name` this is necessary for api calling but can be too verbose in the TUI.
    - update the modelname with only the model and drop the provider name in the tui while showing only the model name
    - but we still need to map to the original name (that we have given earlier) so that we can pass those value to the api
    - instead of creating a list, create a dictionary where key contain the model name that will be showing in the TUI and value contains the api model name
    - we load the dictionary in the main.py and show all the key value
    - when that key value is selected instead of taking the value as it is we get the value (dict value) using that key (event.value) and then set the model name to that value

3. **Setup Api Key from cmd:**
    - Right now the api key is hardcoded and provided by me. But user will want to provide their own API key.
    - First we will take api key from the terminal or cmd argument (later will implement tui interface so that user can provide api key from their)
    - take api key value from the argument.
        - for gemini the argument will be `google`
        - for openai the argument will be `openai`
        - for anthropic the argument will be `anthorpic`
        - for openrouter the argument will be `openrouter`
    - Now after getting the values update the values in the .env folder (maybe use a separate module to handle this)
    - In the main.py do not run the app if user is providing any of these arguments. rather update the dotenv and getout of the program

4. **Setup Default Model Name:**
    - In this step we need to setup a default model so that user can change the default model
    - First default model will be a parameter (maybe in a config.json file) which will be loaded outside from the python script. Initial value will be the current value (devstral)
    - Then similar way (the way we created api key configurability) we need to create an argparser for `default-model` and which will take the `default-model` value
    - We also need another argparser `models` (thiw argparser won't take any values it is just a flag to show the available models) which will show all model name (with the provider name, the dictionary value of the models). 
    - We need to handle error handling for `default-model`. First the given string value we check with the available models in the system. If the available models and the given default value is a match then we update the default model. But if the available models doesn't match with default model then we say the user this model is not available please check the available model name and format of the name and then give the entire available model name





# Task Progress

- [x] litellm integration for universal LLM integration
- [x] update the LLM provider list
- [x] update the model name using key_value methodology (2.1)
- [x] Create a module to handle api key updation from the command line
- [x] Create a module to handle default model configuration and other steps define in `4` no points