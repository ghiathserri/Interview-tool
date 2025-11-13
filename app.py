import streamlit as st
from openai import OpenAI
from streamlit_js_eval import streamlit_js_eval

# Setting a title for the page, and an icon
st.set_page_config(page_title="Streamlit Chat", page_icon="💬")

# if setup_complete is not exists, it will be created with the value False
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False

# now we need to count the messages that user write, otherwise it will be infenite
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0

# we need to track if a user see a feedback after the interview, so we will track that by creating a session for that
if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False

# for the chat history, we need to track that by using session_state too
if "messages" not in st.session_state:
    st.session_state.messages = []

# to track if the chat complete we can create a session for that
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False

# set a header (big text)

st.title("Chatbot")


# a function to change the setup_complete state to True
def complete_setup():
    st.session_state.setup_complete = True


# a function to change the feedback_shown state to True, when we want to show the feedback
def show_feedback():
    st.session_state.feedback_shown = True


# if you didn't add your name and info, you will see the form to do so, and if you did already, you won't see the form
if not st.session_state.setup_complete:
    # set a subheader with a text and an hr looks like a rainbow
    st.subheader("Personal information", divider="rainbow")

    # for each value we will make (name, experience, skills), if they are not exists in the session_state, we will create them with a value of "" empty string
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "experience" not in st.session_state:
        st.session_state.experience = ""
    if "skills" not in st.session_state:
        st.session_state.skills = ""

    # creating an input with streamlit for the name
    st.session_state.name = st.text_input(
        label="Name",
        max_chars=40,
        value=st.session_state.name,
        placeholder="Enter your name",
    )

    # creating a text area input for the experiences
    st.session_state.experience = st.text_area(
        label="Experience",
        value=st.session_state.experience,
        height=None,
        max_chars=200,
        placeholder="Describe your experience",
    )

    # creating a text area input for the skills
    st.session_state.skills = st.text_area(
        label="Skills",
        value=st.session_state.skills,
        height=None,
        max_chars=200,
        placeholder="List your skills",
    )

    # output the value for testing
    # st.write(f"**Your Name**: {st.session_state.name}")
    # st.write(f"**Your Experience**: {st.session_state.experience}")
    # st.write(f"**Your Skills**: {st.session_state.skills}")

    # set a subheader with a text and an hr looks like a rainbow
    st.subheader("Company and Position", divider="rainbow")

    # for each value we will make (level, position, company), if they are not exists in the session_state, we will create them with a value of "" empty string
    if "level" not in st.session_state:
        st.session_state.level = "Junior"
    if "position" not in st.session_state:
        st.session_state.position = "Data Scientist"
    if "company" not in st.session_state:
        st.session_state.company = "Amazon"
    # creating a layout with two columns (something like grid)
    col1, col2 = st.columns(2)

    # creating the first column in the layout with a radio from st
    with col1:
        st.session_state.level = st.radio(
            "Choose level", key="visibility", options=["Junior", "Mid-Level", "Senior"]
        )

    # creating the second column in the layout with a selectbox from st
    with col2:
        st.session_state.position = st.selectbox(
            "Choose a position",
            (
                "Data Scientist",
                "Data Engineer",
                "ML Engineer",
                "BI Analyst",
                "Financial Analyst",
            ),
        )

    # creating a selectbox for the user to select a company
    st.session_state.company = st.selectbox(
        "Choose a company",
        ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify"),
    )

    # testing if it works by outputing the value of the selectbox for company
    # st.write(
    #     f"**Your information**: {st.session_state.level} {st.session_state.position} at {st.session_state.company}"
    # )

    # creating a button when you click on it, it will call the complete_setup function that will change the session_state for the setup_complete to True, that will couse the form to esapeer
    if st.button("Start Interview", on_click=complete_setup):
        st.write("Setup Complete. Starting interview...")

# after the setup_complete is done, then the interview will start, and you will see the input to write your question and call the ai
if (
    st.session_state.setup_complete
    and not st.session_state.feedback_shown
    and not st.session_state.chat_complete
):
    # creating a connection with openai api after passing our api key

    # to help the user to know what to do, we can use the st.info from streamlit
    st.info(
        """
     Start by introducing yourself.
    """,
        icon="👋",  # to add emoji in vscode, press win+.
    )

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # choosing the model to use from openai
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4o"

    # saving the entire history to our chat (user, assistant)
    if not st.session_state.messages:
        st.session_state.messages = [
            {
                "role": "system",
                "content": f"You are an HR executive for the company {st.session_state.company} and are interviewing user named {st.session_state.name} for the position {st.session_state.position} and level {st.session_state.level} The interviewee has the following experience: {st.session_state.experience} The interviewee has the skills: {st.session_state.skills}",
            }
        ]

    # showing the messages that happens between the user and the assistant
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # before taking the answer from the user, we need to check if the answers from the user are smaller than 5 answers
    if st.session_state.user_message_count < 5:
        # := it's assigns the value to the prompt object, checks if the input is not empty
        if prompt := st.chat_input("Your answer.", max_chars=1000):
            st.session_state.messages.append({"role": "user", "content": prompt})
            # when the user write a message
            with st.chat_message("user"):
                st.markdown(prompt)
            # to let the assistant to stop asking after 3 answers from user, if it is more than 4, the assistant will stop responding
            if st.session_state.user_message_count < 4:
                with st.chat_message("assistant"):
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            st.session_state.user_message_count += 1

    # now we need to check if user send 5 answers, we set chat_complete in session to True
    if st.session_state.user_message_count >= 5:
        st.session_state.chat_complete = True

# now we need to create a button, when it clicked, it will show the feedback, we need to make sure that the button will be showen after the chat_complete, and the feedback is not showen yet
if st.session_state.chat_complete and not st.session_state.feedback_shown:
    if st.button("Get feedback", on_click=show_feedback):
        st.write("Fetching feedback...")


# Show feedback screen
if st.session_state.feedback_shown:
    st.subheader("Feedback")

    conversation_history = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]
    )

    # Initialize new OpenAI client instance for feedback
    feedback_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Generate feedback using the stored messages and write a system prompt for the feedback
    feedback_completion = feedback_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful tool that provides feedback on an interviewee performance.
             Before the Feedback give a score of 1 to 10.
             Follow this format:
             Overal Score: //Your score
             Feedback: //Here you put your feedback
             Give only the feedback do not ask any additional questins.
              """,
            },
            {
                "role": "user",
                "content": f"This is the interview you need to evaluate. Keep in mind that you are only a tool. And you shouldn't engage in any converstation: {conversation_history}",
            },
        ],
    )

    st.write(feedback_completion.choices[0].message.content)

    # Button to restart the interview
    if st.button("Restart Interview", type="primary"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
