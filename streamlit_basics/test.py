import streamlit as st

st.set_page_config(page_title="User Profiles", layout="wide")

# basic elements
st.title("Streamlit Basics")
st.write("This is where we will learn about streamlit basics")

# divider
st.divider()

# more interactive elements

# text input
name = st.text_input("What is your name?")
mood = None
if name:
    st.write(f"Welcome {name}, how are you doing today?")
    mood = st.radio("select mood", ("good", "okay", "no-talking"), horizontal=True)

# divider
st.divider()

# radio button
gender = st.radio("Gender", ("Male", "Female"))

# slider
age = st.slider("Your age", 0, 100)

# select box
interest = st.selectbox(
    "What are your interests?",
    ("Computer vision", "Natural language processing", "Deep Learning"),
)

# button
if st.button("Current Profile"):
    st.write(
        f"Name is: {name}, Age is: {age}, Gender is: {gender}, Interest is: {interest}"
    )

# whenever you interact with streamlit elements (like buttons), streamlit reruns the entire page from top to bottom.
# So values of all variables are lost as they are reinitialized, but it smartly preserves the values of widget states
# The values of streamlit widgets like slider, radio button, selectbox however are retained.
# If you want to retain the value of the variables use streamlit session state.

# implementation without session_state
# all_profiles = []

# new_profile = {"Name": name, "Age": age, "Gender": gender, "Interest": interest}

# all_profiles.append(new_profile)

# if st.button("Show all profiles"):
#     st.write(all_profiles)


# implementation with session_state
if "profiles" not in st.session_state:
    st.session_state.profiles = []

new_profile = {
    "Name": name,
    "Age": age,
    "Gender": gender,
    "Interest": interest,
    "Mood": mood,
}

if st.button("Save and show all profiles"):
    st.session_state.profiles.append(new_profile)
    st.write(st.session_state.profiles)
