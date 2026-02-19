import streamlit as st
import requests
import random
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

if "result" not in st.session_state:
    st.session_state.result = None


def show_list(items):
    for i, item in enumerate(items, 1):
        st.write(f"{i}. {item}")

def convert_to_markdown(data):
    md = "# Interview Kit\n\n"

    md += "## Technical Questions\n"
    for q in data["technical_questions"]:
        md += f"- {q}\n"

    md += "\n## Behavioral Questions\n"
    for q in data["behavioral_questions"]:
        md += f"- {q}\n"

    md += "\n## Evaluation Rubric\n"
    for r in data["evaluation_rubric"]:
        md += f"### {r['criteria']} — {r['weight']}%\n{r['what_to_look_for']}\n\n"

    return md

def create_pdf(md_text):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate("interview_kit.pdf")
    story = [Paragraph(line, styles["Normal"]) for line in md_text.split("\n")]
    doc.build(story)
    return "interview_kit.pdf"


st.set_page_config(page_title="AI Interview Kit Generator", page_icon="🤖")

st.title("AI Interview Kit Generator")

role = st.text_input("Job Role", placeholder="Machine Learning Engineer")
experience = st.selectbox("Experience Level", ["Intern", "Junior", "Mid", "Senior"])
skill_focus = st.text_input(
    "Skill Focus (optional)",
    placeholder="e.g. APIs, System Design, NLP, Leadership"
)


generate_btn = st.button("Generate Interview Kit")

tips = [
    "Analyzing job requirements...",
    "Designing technical questions...",
    "Generating behavioral scenarios...",
    "Building evaluation rubric..."
]


if generate_btn:

    if not role.strip():
        st.warning("Please enter a job role.")
        st.stop()

    job_description = f"{role} - {experience}"
    if skill_focus.strip():
        job_description += f" - Focus on {skill_focus}"


    with st.spinner(random.choice(tips)):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/generate",
                json={"job_description": job_description},
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()

                if "technical_questions" in data:
                    st.session_state.result = data
                else:
                    st.error("Backend returned unexpected response.")
                    st.json(data)

            else:
                st.error(f"Backend error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to FastAPI server.")

        except requests.exceptions.Timeout:
            st.error("LLM took too long. Try again.")

        except Exception as e:
            st.error("Unexpected error.")
            st.exception(e)


data = st.session_state.result

if data:
    st.success("Interview kit generated!")

    st.subheader("Technical Questions")
    show_list(data["technical_questions"])

    st.subheader("Behavioral Questions")
    show_list(data["behavioral_questions"])

    st.subheader("Evaluation Rubric")
    for item in data["evaluation_rubric"]:
        st.markdown(f"**{item['criteria']} — {item['weight']}%**")
        st.write(item["what_to_look_for"])
        st.write("")

    st.subheader("Download")

    md_text = convert_to_markdown(data)

    st.download_button("Download Markdown", md_text, file_name="interview_kit.md")

    pdf_file = create_pdf(md_text)
    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", f, file_name="interview_kit.pdf")