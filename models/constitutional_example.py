"""
Definition of PyDantic's model for the validation of constitutional examples.
"""

import re
from typing import List

from pydantic import BaseModel, field_validator


def extract_initials(text: str) -> List[str]:
    """
    Given a string as input, get initials of each sentence.

    Args: 
        text (str): input text with a set of sentences.

    Returns:
        List[str]: initial letters of the sentences that are present in text.
    """

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.lstrip()[0].upper() for s in sentences if s.strip()]


class ConstitutionalExample(BaseModel):
    prompt: str
    student_response: str
    critique: str
    rewrite: str

    @field_validator("rewrite")
    def validate_adaptive_rewrite(cls, v):
        expected = list("ADAPTIVE")
        initials = extract_initials(v)

        if initials[:len(expected)] != expected:
            raise ValueError(
                f"rewrite is not compliant with ADAPTIVE pattern.\n"
                f"Expected: {''.join(expected)}\n"
                f"Detected: {''.join(initials[:len(expected)])}"
            )
