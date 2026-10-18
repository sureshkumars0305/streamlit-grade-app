import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #4F46E5;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #6B7280;
        margin-top: 0px;
        margin-bottom: 30px;
    }

    .welcome-box {
        background: linear-gradient(90deg, #EEF2FF, #F5F3FF);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #4F46E5;
        margin-bottom: 20px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }

    div[data-testid="stMetric"]:hover {
        border-color: #4F46E5;
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.12);
    }
</style>
""", unsafe_allow_html=True)

# Main heading
st.markdown(
    '<div class="main-title">🎓 Student Grade Manager</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">A simple and smart dashboard to manage student performance.</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="welcome-box">
    <b>📚 Grade Dashboard</b><br>
    Add student marks, calculate grades, and monitor overall class performance.
</div>
""", unsafe_allow_html=True)


# Function to calculate grade
def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"


# Initialize student list in session state
if "students" not in st.session_state:
    st.session_state.students = []


# Add Student
st.subheader("➕ Add Student")

with st.form("add_student_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Student Name")

    with col2:
        mark = st.number_input(
            "Mark",
            min_value=0,
            max_value=100,
            value=75
        )

    submitted = st.form_submit_button("Add Student")

    if submitted:
        if name.strip():
            grade = get_grade(mark)

            st.session_state.students.append({
                "Name": name.strip(),
                "Mark": mark,
                "Grade": grade
            })

            st.success(f"✅ {name} added successfully!")
        else:
            st.warning("⚠️ Please enter the student's name.")


# Display class statistics and student results
if st.session_state.students:

    # Get all student marks
    marks = [student["Mark"] for student in st.session_state.students]

    # Calculate statistics
    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)

    # Class Overview
    st.subheader("📊 Class Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📈 Average", f"{average:.1f}")

    with col2:
        st.metric("🏆 Highest", highest)

    with col3:
        st.metric("📉 Lowest", lowest)

    # Student Results
    st.subheader("📋 Student Results")

    # Grade color function
    def color_grade(grade):
        colors = {
            "A": "background-color: #DCFCE7; color: #166534; font-weight: bold;",
            "B": "background-color: #DBEAFE; color: #1E40AF; font-weight: bold;",
            "C": "background-color: #FEF3C7; color: #92400E; font-weight: bold;",
            "D": "background-color: #FFEDD5; color: #9A3412; font-weight: bold;",
            "F": "background-color: #FEE2E2; color: #991B1B; font-weight: bold;"
        }

        return colors.get(grade, "")

    # Convert students into DataFrame
    df = pd.DataFrame(st.session_state.students)

    # Apply grade colors
    styled_df = df.style.map(
        color_grade,
        subset=["Grade"]
    )

    # Display results
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

    # Clear student records
    st.write("")

    if st.button("🗑️ Clear All Students"):
        st.session_state.students = []
        st.rerun()