"""
This script defines code to automate the process of building prompts for GPT-4o.
"""

from pathlib import Path
from typing import Dict, List

from file_utils import load_examples

constitutional_examples: List[Dict] = load_examples(Path("data/constitutional_examples.jsonl"))

def build_prompt_draft_example(examples: List[str]):
    """
    Build prompt to generate a new constitutional example from previosly given examples.

    Args:
        examples (List[str]): previosly edited and loaded constitutional examples.
    Returns:
        str: prompt to generate a new constitutional example.
    """

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
    return final_prompt

def build_prompt_constitutional(examples: List[str], prompt_text: str, student_response: str) -> str:
    """
    Function to build final prompt that will be send to GPT-4o in order to get
    critique and rewrite for the input prompt text and student response.

    Args:
        examples (List[Dict]): list of constitutional examples utilized to build few-shot prompt.
        prompt_text (str): input user text that is sent to the student model.
        student_response (str): output response of the student model

    Returns:
        (str): final prompt with the constitutional examples (few-shot) plus the input user prompt
        and the response of the student model.
    """
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
    return final_prompt
