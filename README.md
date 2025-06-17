# 🧠 Constitutional AI - Critique+Rewrite Tool

This tool helps users create, edit, validate, and test **Critique + Rewrite** examples based on the approach described in [Anthropic's Constitutional AI paper](https://arxiv.org/pdf/2212.08073). The goal is to facilitate building datasets that guide a teacher model in improving student responses to better follow predefined constitutional principles — for instance:  
**"Putting together the first letter of each sentence from the assistant's answer should spell 'ADAPTIVE'."**

---

## 🚀 Features

### 🧩 Example Editor
- View and edit existing examples (`prompt`, `student_response`, `critique`, `rewrite`).
- Manually add or delete examples.
- Automatically generate new examples using GPT-4o.
- Preview auto-generated fields before deciding whether to add them.

### ✅ Validator
- Load examples from a `.jsonl` file.
- Automatically validate whether the `rewrite` satisfies the "ADAPTIVE" acronym principle (one sentence per letter, in order).
- Call the teacher model to see how model outputs change depending on the examples provided.

---

## 📁 Project Structure
```yaml
.
├── app.py # Main Streamlit app
├── file_utils.py # File I/O helper functions
├── models # Pydantic validation models
├── data/ # Editable examples file
└── README.md
```

## ⚙️ Requirements
Python UV package and project manager is used to manage all the dependencies of this project. Ensure that `uv` is previosly installed by running: `pip install uv`.

- Python 3.8+
- Streamlit
- OpenAI SDK
- Pydantic

### 📦 Quick Install

```bash

    uv install
```

## 📋 Usage
```bash
    uv run streamlit run app.py
```

## ✨ Constitutional Principle Used
> "Putting together the first letter of each sentence from the assistant's answer should spell 'ADAPTIVE'."

The validator checks this automatically on each rewrite.