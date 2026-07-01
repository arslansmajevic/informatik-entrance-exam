# Question files

Each `*.json` file in this directory describes **one part of the exam**. The app
loads every file automatically (sorted by file name) and shows one entry per
part in the sidebar.

## File format

```json
{
  "title": "Part 1: Mathematics",
  "description": "Optional text shown under the part title.",
  "questions": [
    {
      "id": "math-1",
      "question": "What is 7 + 8?",
      "image": "images/optional.png",
      "options": ["13", "14", "15", "16"],
      "correct": [2],
      "explanation": "Optional text shown after grading."
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
point. A single index renders as radio buttons.

### Images

Put image files in the `images/` folder and reference them with a path relative
to the repository root, e.g. `"image": "images/my_diagram.png"`. Missing images
are ignored gracefully.
