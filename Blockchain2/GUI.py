import streamlit as st
import vote_chain


# Function to authenticate the admin
def authenticate_admin(username, password):
    # Replace with your authentication logic
    return username == "admin" and password == "admin123"


st.set_page_config(
    page_title="Blockchain-based Voting System",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)

is_admin_logged_in = st.session_state.get(
    "is_admin_logged_in", False
)  # Flag to track admin login status

st.title("Blockchain-based Voting System")

# Sidebar for admin authentication
if not is_admin_logged_in:
    st.sidebar.title("Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if authenticate_admin(username, password):
            st.session_state["is_admin_logged_in"] = True
            is_admin_logged_in = True
        else:
            st.sidebar.error("Invalid username or password")

if is_admin_logged_in:
    st.sidebar.header("Admin Interface")

    # Add Candidate Section
    st.sidebar.subheader("Add Candidate")
    new_candidate = st.sidebar.text_input("New Candidate Name:")
    if st.sidebar.button("Add Candidate"):
        new_candidate = new_candidate.strip()  # Remove leading/trailing whitespace
        if new_candidate:  # Check if the input is not empty
            vote_chain.chain.insert_vote(
                new_candidate, 0, ""
            )  # Insert candidate data into the votes table
            st.sidebar.success(f"Added candidate -> {new_candidate} successfully.")
        else:
            st.sidebar.warning("Please enter a valid candidate name.")

    # Remove Candidate Section
    st.sidebar.subheader("Remove Candidate")
    candidate_to_remove = st.sidebar.selectbox(
        "Select Candidate to Remove:", vote_chain.candidate
    )
    if st.sidebar.button("Remove Candidate"):
        vote_chain.candidates.remove(candidate_to_remove)
        st.sidebar.success(f"Removed candidate -> {candidate_to_remove} successfully.")

else:
    st.header("User Interface")
    # Display the current candidate
    st.subheader("Current Candidate")
    st.write(f"{vote_chain.candidate}")

    # voter data logic
    voter_name = st.text_input("Voter Name")  # get the voter name
    option_list = [_ for _ in vote_chain.candidate]
    voter_choose = st.selectbox("Choose your candidate to vote for", option_list)
    voter_key = st.text_input("Voter Key")

    if st.button("Vote"):
        vote_chain.chain.insert_vote(
            voter_name, int(vote_chain.voter_code), voter_choose
        )
        st.success(f"Voted for -> {voter_choose}")
