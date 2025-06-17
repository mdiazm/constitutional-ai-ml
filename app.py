"""
This script defined app code to run streamlit application for validating and editing constitutional
AI examples.

To run the app: uv run streamlit run app.py
"""


import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

from prompts import build_prompt_constitutional, build_prompt_draft_example, constitutional_examples
from models.constitutional_example import ConstitutionalExample

from file_utils import load_examples, generate_jsonl
from pathlib import Path

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

st.set_page_config(page_title="Constitutional AI Critique Tool", layout="wide")

st.title("🧠 Constitutional AI. Critique & Rewrite Tool")

validation_tab, edition_tab = st.tabs(["Validation", "Editing"])

with validation_tab: 
    examples = load_examples(Path("data/dev.jsonl"))
    example_idx = st.number_input("Select an example", 0, len(examples) - 1, 0)
    example = examples[example_idx]
    
    st.subheader("📝 Original prompt: ")
    st.markdown(f"**{example['user']}**")

    st.subheader("🤖 Student model response:")
    st.markdown(f"> {example['bot']}")

    if st.button("🔍 Call GPT-4o for testing"):
        with st.spinner("Calling GPT-4o for testing..."):

            full_prompt = build_prompt_constitutional(
                examples=constitutional_examples,
                prompt_text=example["user"],
                student_response=example["bot"]
            )

            st.text(f"Full prompt: {full_prompt}")

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful AI teacher."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7
            )

            output = response.choices[0].message.content
            st.markdown("### 🧠 Teacher model response (GPT-4o):")
            st.text(output)

            # Validate received rewrite
            if "Rewrite:" in output:
                critique_part, rewrite_part = output.split("Rewrite:", 1)

                try:
                    valid_example = ConstitutionalExample(
                        prompt=example["user"],
                        student_response=example["bot"],
                        critique=critique_part.strip(),
                        rewrite=rewrite_part.strip()
                    )
                    st.success("Received 'rewrite' is valid after using Pydantic")
                except Exception as e:
                    st.error(e)

with edition_tab:
    st.header("Constitutional examples management (critique+rewrite)")
    ex_list = constitutional_examples

    # Mostrar y editar cada ejemplo
    for i, ex in enumerate(ex_list):
        with st.expander(f"Example #{i+1}"):
            ex["prompt"]           = st.text_input("Prompt", ex["prompt"], key=f"prompt_{i}")
            ex["student_response"] = st.text_area("Student response", ex["student_response"], key=f"stud_{i}")
            ex["critique"]         = st.text_area("Critique", ex["critique"], key=f"crit_{i}", height=100)
            ex["rewrite"]          = st.text_area("Rewrite", ex["rewrite"], key=f"rew_{i}",  height=120)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Delete", key=f"del_{i}"):
                    ex_list.pop(i)
                    st.rerun()
            with col2:
                if st.button("🔄 Validate rewrite", key=f"val_{i}"):

                    try:
                        valid_example = ConstitutionalExample(**ex)
                        st.success("✅ ADAPTIVE-compliant")
                    except ValueError as e:
                        st.error("❌ ADAPTIVE non-compliant")

    st.markdown("---")

    # Initialize session state
    for key in ["gen_prompt", "gen_student", "gen_critique", "gen_rewrite"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    if st.button("Draft example (GPT)"):
        full_prompt = build_prompt_draft_example(constitutional_examples)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful AI teacher."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7
        )

        output = response.choices[0].message.content

        rest, st.session_state.gen_rewrite = output.split("Rewrite:")
        rest, st.session_state.gen_critique = rest.split("Critique:")
        st.session_state.gen_prompt, st.session_state.gen_student = rest.split("Student response:", 1)
        st.session_state.gen_prompt = st.session_state.gen_prompt.replace("Prompt:", "")

    st.subheader("Add new constitutional example")
    new_prompt   = st.text_input("New Prompt", key="new_prompt", value=st.session_state["gen_prompt"])
    new_student  = st.text_area ("New Student response", key="new_stud", value=st.session_state["gen_student"])
    new_critique = st.text_area ("New Critique", key="new_crit", value=st.session_state["gen_critique"], height=100)
    new_rewrite  = st.text_area ("New Rewrite",  key="new_rew", value=st.session_state["gen_rewrite"], height=120)

    if st.button("Add example"):
        if not (new_prompt and new_student and new_critique and new_rewrite):
            st.warning("Please, do fill four fields below")
        else:

            try:
                ex = {
                    "prompt": new_prompt,
                    "student_response": new_student,
                    "critique": new_critique,
                    "rewrite": new_rewrite
                }

                valid_example = ConstitutionalExample(**ex)
                st.success("Example was added")
                
                # Clean input fields
                st.session_state["gen_prompt"] = ""
                st.session_state["gen_student"]   = ""
                st.session_state["gen_critique"]   = ""
                st.session_state["gen_rewrite"]    = ""

                ex_list.append(ex)
                st.rerun()
            except Exception as e:
                st.error("Example is not valid, try addressing issues")

    st.markdown("---")
   
    # Save all the changes
    if st.button("Generate examples file"):
        jsonl_data = generate_jsonl(constitutional_examples)

        st.download_button(
            label="Download JSONL",
            data=jsonl_data,
            file_name="constitutional_examples.jsonl",
            mime="application/json"
        )
