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
index.html                 # stlite entry page for GitHub Pages
scripts/build_site.py      # Builds the static dist/ site
.github/workflows/deploy.yml  # Deploys to GitHub Pages on push to main
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

## Host on GitHub Pages

GitHub Pages only serves static files, so the normal Streamlit server can't run
there. Instead the app is deployed with [stlite](https://github.com/whitphx/stlite),
which runs Streamlit **entirely in the browser** via WebAssembly (Pyodide). No
backend server is involved — every visitor runs the quiz locally in their tab.

### How it works

- [index.html](index.html) loads stlite from a CDN, reads `manifest.json` and
  mounts `app.py` plus the `quiz/` and `questions/` files into the in-browser
  virtual file system.
- [scripts/build_site.py](scripts/build_site.py) assembles a `dist/` folder
  (the app files, `index.html`, a generated `manifest.json` and a `.nojekyll`
  marker).
- [.github/workflows/deploy.yml](.github/workflows/deploy.yml) rebuilds `dist/`
  and deploys it to GitHub Pages on **every push to `main`**.

### One-time setup

1. Push this repository to GitHub.
2. In the repo, go to **Settings → Pages** and set **Source** to
   **GitHub Actions**.
3. Push to `main` (or run the workflow manually from the **Actions** tab). The
   app is published at `https://<user>.github.io/<repo>/`.

### Preview the static build locally

```bash
python scripts/build_site.py
python -m http.server -d dist 8000
# open http://localhost:8000
```

> The first load downloads the Python runtime in the browser and can take a
> little while; subsequent loads are cached.