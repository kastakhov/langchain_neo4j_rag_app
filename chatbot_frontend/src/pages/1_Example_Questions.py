import streamlit as st


with st.sidebar:
    st.header("About")
    st.markdown(
        """
        The following are example questions that can be asked to the chatbot.
        """
    )

st.header("Example Questions")
st.markdown("- Which hospitals are in the hospital system?")
st.markdown(
    """- Compare the salary of physicians: Crystal Cruz and Logan Diaz. Who's salary is bigger?"""
)
st.markdown(
    """- What is the current wait time at wallace-hamilton hospital?"""
)
st.markdown(
    """- At which hospitals are patients complaining about billing and
    insurance issues?"""
)
st.markdown(
    "- What is the average duration in days for closed emergency visits?"
)
st.markdown(
    """- What are patients saying about the nursing staff at
    Castaneda-Hardy?"""
)
st.markdown(
    "- What was the total billing amount charged to each payer for 2023?"
)
st.markdown("- What is the average billing amount for medicaid visits?")
st.markdown(
    "- Which physician has the lowest average visit duration in days?"
)
st.markdown("- How much was billed for patient 789's stay?")
st.markdown(
    """- Which state had the largest percent increase in medicaid visits
    from 2022 to 2023?"""
)
st.markdown(
    "- What is the average billing amount per day for Aetna patients?"
)
st.markdown(
    """- How many reviews have been written from
            patients in Florida?"""
)
st.markdown(
    """- For visits that are not missing chief complaints,
    what percentage have reviews?"""
)
st.markdown(
    """- What is the percentage of visits that have reviews for
    each hospital?"""
)
st.markdown(
    """- Which physician has received the most reviews for this visits
    they've attended?"""
)
st.markdown("- What is the ID for physician James Cooper?")
st.markdown(
    """- List every review for visits treated by physician 270.
    Don't leave any out."""
)
