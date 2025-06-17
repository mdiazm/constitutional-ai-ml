# Solutions Engineer take-home task

This document explains the process followed to develop a tool that enables users to define and edit custom examples for constitutional AI. The developed tool just focuses on the first part of the constitutional AI process, that is about using few-shot prompting techniques to enable a teacher AI model to propose a pair critique+rewrite that will be used then to finetune a student model using RLHF techniques.

So, I will explain the process I followed in order to develop the tool.

## Few-shot prompting
First, it is important to define the constitutional principle that will head the prompt. On each time that a pair user_prompt+student_response is received, it has to generate a pair critique+rewrite following the principle: 

> "Putting together the first letter of each sentence from the assistant's answer should spell 'ADAPTIVE'."

With that, I defined a couple of examples manually, with the user prompt, some expected response from the model (invented), then a possible critique, and finally what the rewrite would be in order to meet the constitutional principle. The examples I wrote manually are the following: 

```json
    {"prompt":"Tell me about your features.","student_response":"Sure, I have many features.","critique":"The response does not follow the ADAPTIVE principle. The sentence structure is too short and lacks the pattern.","rewrite":"Absolutely! Delightfully, I provide context-aware help. Amazingly fast, I can generate responses. Promptly, I answer your queries. Thoroughly trained, I adapt. Intuitively, I learn from patterns. Versatile in tasks. Elegantly helpful always."}
    {"prompt":"What makes you special?","student_response":"I'm smart and can answer a lot of questions.","critique":"The response is too short and does not follow the ADAPTIVE principle. It lacks multiple sentences whose first letters spell out 'ADAPTIVE'.","rewrite":"Mabsolutely, I'm designed to assist with a wide range of topics. Delightfully responsive, I adapt to your needs. As a language model, I draw from extensive data. Promptness is key to my design. Thorough answers are my goal. Intelligently built, I learn continuously. Versatility defines my capabilities. Every interaction aims to help you."}
```

Once I had defined these examples, I used generative AI models to generate 4 more examples (GPT-4o, Gemini). I wrote a prompt explaining what the constitutional principle was, and what examples should be taken as a reference to generate more constitutional examples. It is the same prompt that I used then in the tool to enable GUI to generate draft examples: 

```python
    example_blocks = ""
    for ex in examples:
        example_blocks += f"""Prompt: {ex['prompt']}
        Student response: {ex['student_response']}

        Critique: {ex['critique']}
        Rewrite: {ex['rewrite']}

        """

    final_prompt = f"""You are a teacher model helping a student adhere to the following constitutional principle:

    "Putting together the first letter of each sentence from the assistant's answer should spell 'ADAPTIVE'."

    Below are some examples of critiques and rewrites:

    {example_blocks}
    Now write a new example following the same logic that previosly given examples. Content can be randomly chosen
    but critique and rewrite needs to be compliant with previous rules.

    Prompt: 
    Student response: 
    Critique:
    Rewrite: """
```

With that, all the constitutional examples that I needed were ready to write the final prompt, that will generate the pair of critique+rewrite for an input example of user_prompt+student_response.

The final prompt that is automatically build with code is the following:

```python
        example_blocks = ""
    for ex in examples:
        example_blocks += f"""Prompt: {ex['prompt']}
        Student response: {ex['student_response']}

        Critique: {ex['critique']}
        Rewrite: {ex['rewrite']}

        """

    final_prompt = f"""You are a teacher model helping a student adhere to the following constitutional principle:

    "Putting together the first letter of each sentence from the assistant's answer should spell 'ADAPTIVE'."

    Below are some examples of critiques and rewrites:

    {example_blocks}
    Now critique and rewrite the following:

    Prompt: {prompt_text}
    Student response: {student_response}

    Critique:
    Rewrite: """
```

In  the prompt, first explain what is the role that the model should play when generating a response. Then, the constitutional principle is clearly set. After that, it comes the few-shot part of the prompt, where the constitutional examples are defined according to what we explained previously. Last, the task comes, where it is requested that the model generates a pair of critique+rewrite taking the prompt and student response as input.

It it noticeable that the prompt is almost identical to the previous one, with the only difference being that instead of also generating Prompt: and Student response:, it's receiving them as input and only inferring Critique and Rewrite. This is the prompt which is sent to GPT-4o using OpenAI client.

All the defined constitutional examples are available in `data/constitutional_examples.jsonl`.

## Tool design
The next part, was to design a GUI that enables final users to edit and manage example, also validate them by calling OpenAI API. I decided to add 2 different tabs, according to two different features: 

- Validation: in the first tab, every single example in `dev.jsonl` is loaded and ready to be validated with GPT-4o. You are able to choose which example to validate by choosing the index of the example. When `Call GPT-4o for testing` button is pressed, the full prompt which is sent to GPT is shown. Then, when the response is received, it is validated using Pydantic BaseModel class, and if valid, a green message is displayed.
- Editing: in the second tab, the constitutional examples that were previously defined are shown. You are able to click and display each example, also modify them, remove a example or validate its rewrite content. Validation is done by using pydantic. Besides, a GPT-4o call can be done to generate a new constitutional example. Once response is received, you are able to edit and save a new example, or simply adding the new example. Before adding the example, pydantic validation is done to ensure that invalid constitutional examples are not added to the final prompt.

At the bottom of the website, you will find a button with 'Generate examples file'. Once this button is pressed, a second button will appear to confirm download. This will generate a `.jsonl` file with all the generated and edited constitutional examples, to enable easy migration of data to the second part of this system, that is about finetuning the student model.

## Tool development
To manage all the python packages, I decided to use [uv](https://github.com/astral-sh/uv) as package manager. It is extremely fast, coded in Rust, and per my experience, it's much better than using other package managers such as poetry or pipenv.

To install all the packages, assuming that `uv` is installed, please run `uv install`. Versions are locked in file `uv.lock` to ensure that they don't change in a production deployment. 

Code is mainly structure al follows:
- app.py: main script of the application, where the `streamlit` functionality is defined for the GUI.
- file_utils.py: some utility functions to centralize file loading.
- prompts.py: functions to define the input prompts to the GPT model.
- models/constitutional_example.py: pydantic BaseModel class to validate `rewrite` part of each example, and ensure it is **ADAPTIVE**-compliant.
- data/: where constitutional examples, and initial shared examples, are placed.

## Run the tool
It is mandatory to create a `.env` file with the `OPENAI_API_KEY` variable defined (with a real and valid OpenAI API Key) in order to run the tool. It can be directly defined as environment variable, as desired.

Then, just run:
```bash
    uv run streamlit run app.py
```

A local server will be automatically set up and the streamlit will be shown in a browser.