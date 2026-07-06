import streamlit as st
import pandas as pd
from google import genai

st.title("Lesson Planner")

database = pd.read_excel(
    "database.xlsx",
    sheet_name=None
)

levels = list(database.keys())
num_classes = st.number_input(
    "How many classes do you want to include?",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)
selected_lessons = []

for i in range(num_classes):

    st.subheader(f"Class {i+1}")

    level = st.selectbox(
        "Level",
        levels,
        key=f"level_{i}"
    )

    df = database[level]

    unit = st.selectbox(
        "Unit",
        sorted(df["UNIT"].unique()),
        key=f"unit_{i}"
    )

    lesson = st.selectbox(
        "Class",
        sorted(df[df["UNIT"] == unit]["CLASS"].unique()),
        key=f"class_{i}"
    )

    selected = df[
        (df["UNIT"] == unit) &
        (df["CLASS"] == lesson)
    ].iloc[0]

    selected_lessons.append(selected)

    st.divider()
if st.button("Generate Lesson Plan"):

    prompt = ""
    prompt = """
You are an experienced ESL teacher.

Create ONE integrated lesson plan.

The lesson must contain exactly four stages:

1. Warm Up
2. Individual Approach
3. Group Approach
4. Assessment

Each activity should naturally connect all the selected lessons.

The lesson should last approximately 90 minutes.

Use communicative language teaching.

Avoid simply teaching grammar.

Prioritize meaningful communication.

Here is the curriculum information:

"""

    for i, lesson in enumerate(selected_lessons):

        prompt += f"""
CLASS {i+1}

LEVEL: {lesson['NIVEL']}
UNIT: {lesson['UNIT']}
CLASS: {lesson['CLASS']}

TOPIC:
{lesson['TOPIC']}

GOAL:
{lesson['GOAL']}

GRAMMAR:
{lesson['GRAMMAR']}

COMMUNICATIVE FUNCTIONS:
{lesson['COMMUNICATIVE FUNCTIONS']}

----------------------------------------

"""

    st.code(prompt, language=None)
from google import genai
import streamlit as st

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

lesson = response.text

st.write(lesson)
