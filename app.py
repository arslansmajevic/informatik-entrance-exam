"""Streamlit-App zum Üben für die Informatik-Aufnahmeprüfung.

Lokal starten mit::

    streamlit run app.py

Die Fragen stammen aus den JSON-Dateien im Ordner ``questions`` und basieren
auf dem Buch "Abenteuer Informatik". Jede Frage besitzt einen eigenen Button
"Antwort anzeigen", mit dem sich die richtige Loesung einzeln aufdecken laesst,
unabhaengig von der Gesamtauswertung am Ende.
"""

from __future__ import annotations

import streamlit as st

from quiz.loader import Part, load_parts

st.set_page_config(
    page_title="Informatik-Aufnahmeprüfung",
    page_icon="📝",
    layout="centered",
)


@st.cache_data
def get_parts() -> list[Part]:
    """Fragen-Teile einmal laden und für die Sitzung zwischenspeichern."""
    return load_parts()


def _selected_answers(part_key: str, question) -> list[int]:
    """Aktuelle Auswahl einer Frage aus dem Session-State auslesen."""
    widget_key = f"{part_key}:{question.id}"
    if question.multiple:
        selected: list[int] = []
        for opt_index in range(len(question.options)):
            if st.session_state.get(f"{widget_key}:{opt_index}"):
                selected.append(opt_index)
        return selected
    choice = st.session_state.get(widget_key)
    return [] if choice is None else [choice]


def _render_answer_reveal(question) -> None:
    """Die richtige(n) Antwort(en) und Erklärung einer Frage anzeigen."""
    correct_options = [question.options[i] for i in question.correct]
    if len(correct_options) == 1:
        st.success(f"✔️ Richtige Antwort: {correct_options[0]}")
    else:
        joined = "\n".join(f"- {option}" for option in correct_options)
        st.success(f"✔️ Richtige Antworten:\n{joined}")
    if question.explanation:
        st.info(question.explanation)


def render_question(part_key: str, index: int, question) -> None:
    """Eine einzelne Frage samt Eingabe und "Antwort anzeigen"-Button rendern."""
    st.markdown(f"**{index + 1}. {question.text}**")

    if question.image:
        st.image(question.image, use_container_width=True)

    widget_key = f"{part_key}:{question.id}"

    if question.multiple:
        st.caption("Mehrfachauswahl möglich – wähle alle zutreffenden Antworten.")
        for opt_index, option in enumerate(question.options):
            st.checkbox(option, key=f"{widget_key}:{opt_index}")
    else:
        st.radio(
            "Wähle eine Antwort",
            options=list(range(len(question.options))),
            format_func=lambda i: question.options[i],
            index=None,
            key=widget_key,
            label_visibility="collapsed",
        )

    reveal_key = f"reveal:{part_key}:{question.id}"
    if st.button("💡 Antwort anzeigen", key=f"btn:{reveal_key}"):
        st.session_state[reveal_key] = not st.session_state.get(reveal_key, False)

    if st.session_state.get(reveal_key):
        _render_answer_reveal(question)


def render_results(part: Part, answers: dict[str, list[int]]) -> None:
    """Auswertung nach dem Absenden anzeigen."""
    score = 0
    for question in part.questions:
        selected = answers.get(question.id, [])
        correct = question.is_correct(selected)
        score += int(correct)

        icon = "✅" if correct else "❌"
        with st.expander(f"{icon} {question.text}", expanded=not correct):
            for opt_index, option in enumerate(question.options):
                is_correct_option = opt_index in question.correct
                is_selected = opt_index in selected
                prefix = ""
                if is_correct_option:
                    prefix = "✔️ "
                elif is_selected:
                    prefix = "❌ "
                marker = " *(deine Antwort)*" if is_selected else ""
                st.markdown(f"{prefix}{option}{marker}")
            if question.explanation:
                st.info(question.explanation)

    total = len(part.questions)
    st.subheader(f"Ergebnis: {score} / {total}")
    st.progress(score / total if total else 0.0)


def main() -> None:
    parts = get_parts()

    st.title("📝 Informatik-Aufnahmeprüfung")
    st.write(
        "Wähle einen Prüfungsteil, beantworte die Fragen und werte sie aus, um "
        "dein Ergebnis zu sehen. Mit "
        '"Antwort anzeigen" kannst du die Lösung jeder Frage einzeln aufdecken.'
    )

    if not parts:
        st.warning("Im Ordner `questions/` wurden keine Fragen-Dateien gefunden.")
        return

    part_titles = {part.title: part for part in parts}
    selected_title = st.sidebar.radio("Prüfungsteil", list(part_titles.keys()))
    part = part_titles[selected_title]

    st.sidebar.metric("Fragen in diesem Teil", len(part.questions))

    st.header(part.title)
    if part.description:
        st.caption(part.description)

    submitted_key = f"submitted:{part.key}"

    for index, question in enumerate(part.questions):
        render_question(part.key, index, question)
        st.divider()

    if st.button("Antworten auswerten", key=f"submit:{part.key}", type="primary"):
        answers = {
            question.id: _selected_answers(part.key, question)
            for question in part.questions
        }
        st.session_state[submitted_key] = answers

    if st.session_state.get(submitted_key) is not None:
        st.divider()
        render_results(part, st.session_state[submitted_key])


if __name__ == "__main__":
    main()
