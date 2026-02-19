# AI Interview Question Generator

A Streamlit-based application that generates structured interview questions and evaluation rubrics using an LLM. The app helps recruiters, educators, and candidates quickly create role-specific interview material tailored to skills, job descriptions, and difficulty levels.

---

## 🚀 Features

* Generate interview questions based on:

  * Role
  * Experience Level
  * Skills(optional to put in)
    
* Produces structured outputs including:

  * Technical Question
  * Behavioral Question
  * Evaluation rubric
    
* Simple UI built with Streamlit
* Python and FastAPI backend

---

## 🧠 Application Architecture

```
User Input (Streamlit UI)
        ↓
Prompt Builder (Python)
        ↓
LLM Engine (Groq API)
        ↓
Structured Output Formatter
        ↓
Streamlit Display
```

**Main Components**

| File               | Purpose                         |
| ------------------ | ------------------------------- |
| `app.py`           | Frontend UI                     |
| `llm_engine.py`    | LLM integration + prompt design |
| `api.py`           | Routing Endpoints               |
| `.env`             | API key storage                 |

---

## 🛠️ Tech Stack

* **Backend / Logic:** Python & FastAPI
* **LLM:** Groq API (model: llama-3.3-70b-versatile)
* **Frontend:** Streamlit

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/SatyamJha402/Interview-Question-Generator.git
cd project
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API key

Create a `.env` file in the project root:

```
GROQ_API_KEY= write own api key here
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
uvicorn api:app --reload
```

App will open in browser at:

```
http://localhost:8501
```

---

## 🧩 How It Works

### 1. Input Collection

User provides:

* Role (e.g., ML Engineer)
* Experience level
* Skills (e.g., Python, Deep Learning)

### 2. Prompt Engineering

The system builds a structured prompt ensuring:

* Questions focus on Role, Experience level and skills
* Balanced difficulty calibration
* Consistent output format

### 3. LLM Generation

The model returns structured JSON containing:

* Questions
* Rubrics

---

## 🎯 Difficulty Calibration Strategy

| Level  | Behavior                          |
| ------ | --------------------------------- |
| Easy   | Conceptual + basic implementation |
| Medium | Applied scenarios + tradeoffs     |
| Hard   | System design + Achitectures      |

---

## 🔍 Prompt Design Highlights

* Combines **skills + description** to avoid skill-only bias
* Enforces structured JSON output
* Encourages realistic interview-style questions
* Prevents vague or generic responses

---

## ⚠️ Limitations

* Requires internet connection for API calls
* Not a replacement for human interview design as question cannot be designed on candidates resume/project or previous experiences.

---


## 📌 Future Improvements

* Multi-role sessions
* Question bank storage
* Ability to refine and regenerate questions

---

## 📄 License

MIT License
