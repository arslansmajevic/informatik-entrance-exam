# Entrance exam application

A simple [Streamlit](https://streamlit.io/) quiz app for practising an
informatics entrance exam. Pick a part of the exam, answer multiple-choice
questions (single or multiple correct answers, optionally with images) and get
an instant score.

## Features

- Multiple-choice questions with **one or many** correct answers.
- Optional **images** attached to questions.
- Questions organised into **parts**, one JSON file per part.
- No authentication or registration — just run it and answer.

## Project structure

```
app.py                     # Streamlit application
quiz/loader.py             # Loads & validates question files
questions/                 # One JSON file per exam part
  part1_mathematics.json
  part2_computer_science.json
  README.md                # Question file format reference
images/                    # Images referenced by questions
requirements.txt
```

## Run locally

Requires Python 3.10+.

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
streamlit run app.py
```

Streamlit opens the app in your browser (default: http://localhost:8501).

## Adding questions

Edit an existing file in `questions/` or add a new `*.json` file for a new part.
The app picks up every `*.json` file automatically. See
[questions/README.md](questions/README.md) for the full file format.