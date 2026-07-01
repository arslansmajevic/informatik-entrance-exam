"""Streamlit entrance-exam quiz application.

Run it locally with::

    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from quiz.loader import Part, load_parts

st.set_page_config(page_title="Informatik Entrance Exam", page_icon="📝", layout="centered")


@st.cache_data
def get_parts() -> list[Part]:
    """Load quiz parts once and cache them for the session."""
    return load_parts()


def render_question(part_key: str, index: int, question) -> list[int]:
    """Render a single question and return the indices the user selected."""
    st.markdown(f"**{index + 1}. {question.text}**")

    if question.image:
        st.image(question.image, use_container_width=True)

    widget_key = f"{part_key}:{question.id}"

    if question.multiple:
        st.caption("Select all answers that apply.")
        selected: list[int] = []
        for opt_index, option in enumerate(question.options):
            if st.checkbox(option, key=f"{widget_key}:{opt_index}"):
                selected.append(opt_index)
        return selected

    choice = st.radio(
        "Choose one answer",
        options=list(range(len(question.options))),
        format_func=lambda i: question.options[i],
        index=None,
        key=widget_key,
        label_visibility="collapsed",
    )
    return [] if choice is None else [choice]


def render_results(part: Part, answers: dict[str, list[int]]) -> None:
    """Show grading feedback after the quiz has been submitted."""
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
                marker = " *(your answer)*" if is_selected else ""
                st.markdown(f"{prefix}{option}{marker}")
            if question.explanation:
                st.info(question.explanation)

    total = len(part.questions)
    st.subheader(f"Score: {score} / {total}")
    st.progress(score / total if total else 0.0)


def main() -> None:
    parts = get_parts()

    st.title("📝 Informatik Entrance Exam")
    st.write("Pick a part of the exam, answer the questions and submit to see your score.")

    if not parts:
        st.warning("No question files found in the `questions/` directory.")
        return

    part_titles = {part.title: part for part in parts}
    selected_title = st.sidebar.radio("Exam part", list(part_titles.keys()))
    part = part_titles[selected_title]

    st.sidebar.metric("Questions in this part", len(part.questions))

    st.header(part.title)
    if part.description:
        st.caption(part.description)

    submitted_key = f"submitted:{part.key}"

    with st.form(f"form:{part.key}"):
        answers: dict[str, list[int]] = {}
        for index, question in enumerate(part.questions):
            answers[question.id] = render_question(part.key, index, question)
            st.divider()
        submitted = st.form_submit_button("Submit answers")

    if submitted:
        st.session_state[submitted_key] = answers

    if st.session_state.get(submitted_key) is not None:
        st.divider()
        render_results(part, st.session_state[submitted_key])


if __name__ == "__main__":
    main()
