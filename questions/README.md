# Question files

Each `*.json` file in this directory describes **one part of the exam**. The app
loads every file automatically (sorted by file name) and shows one entry per
part in the sidebar.

The current question banks are written in **German** and are based on the book
*Abenteuer Informatik* (Jens Gallenbacher). There is one part per chapter, e.g.
shortest paths, sorting, the knapsack problem, recognition/decision trees,
networks/routing, hashing, IT security/cryptography, error correction and
computability. Each question comes with an `explanation` that is also shown by
the per-question **"Antwort anzeigen"** (show answer) button in the app.

## File format

```json
{
  "title": "Teil 1: Kürzeste Wege & Graphen",
  "description": "Optionaler Text unter dem Titel des Prüfungsteils.",
  "questions": [
    {
      "id": "kw01",
      "question": "Woraus besteht ein Graph?",
      "image": "images/optional.png",
      "options": ["Knoten und Kanten", "Zeilen und Spalten", "Bits und Bytes"],
      "correct": [0],
      "explanation": "Ein Graph besteht aus Knoten und Kanten."
    }
  ]
}
```

### Fields

| Field         | Required | Description                                                                 |
| ------------- | -------- | --------------------------------------------------------------------------- |
| `title`       | no       | Part title (defaults to the file name).                                     |
| `description` | no       | Short description shown under the title.                                    |
| `questions`   | yes      | List of question objects.                                                   |
| `id`          | no       | Unique id for the question (auto-generated if omitted).                     |
| `question`    | yes      | The question text.                                                          |
| `image`       | no       | Path (relative to the repo root) to an image, e.g. `images/tree.png`.       |
| `options`     | yes      | List of answer strings.                                                     |
| `correct`     | yes      | List of **0-based** indices into `options` marking the correct answers.     |
| `explanation` | no       | Text shown after the quiz is submitted.                                     |

### Multiple correct answers

If `correct` contains more than one index, the question automatically switches
to checkboxes and the user must select **all** correct answers to score the
point. A single index renders as radio buttons. Every question always has at
least one correct answer.

### Show answer

In the app each question has a **"Antwort anzeigen"** button that reveals the
correct answer(s) and the `explanation` for that single question, independently
of the final grading. The button toggles the answer on and off.

### Images

Put image files in the `images/` folder and reference them with a path relative
to the repository root, e.g. `"image": "images/my_diagram.png"`. Missing images
are ignored gracefully.
