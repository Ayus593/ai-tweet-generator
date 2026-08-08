import streamlit as st

from tweet_agent import run_tweet_agent



st.set_page_config(
    page_title="AI Tweet Generator",
    page_icon="🐦",
    layout="centered"
)




st.title("🐦 AI Tweet Generator")

st.write(
    "Generate, evaluate, and improve tweets "
    "using a LangGraph workflow."
)



topic = st.text_input(
    "Enter a topic",
    placeholder="e.g. DK Shivakumar"
)


max_iterations = st.number_input(
    "Maximum number of evaluations",
    min_value=1,
    max_value=10,
    value=5,
    step=1
)



if st.button(
    "Generate Tweet",
    type="primary"
):

    if not topic.strip():

        st.warning(
            "Please enter a topic first."
        )

    else:

        with st.spinner(
            "Generating and evaluating tweet..."
        ):

            result = run_tweet_agent(
                topic=topic,
                max_iterations=max_iterations
            )


        

        st.subheader("Final Tweet")

        st.info(
            result["tweet"]
        )



        st.subheader("Evaluation")

        if result["evaluation"] == "approved":

            st.success(
                "✅ Tweet approved"
            )

        else:

            st.warning(
                "⚠️ Maximum evaluations reached"
            )


 

        st.subheader("Evaluator Feedback")

        st.write(
            result["feedback"]
        )


        

        st.subheader("Process Information")

        st.write(
            f"Evaluations performed: "
            f"{result['iteration']}"
        )

        st.write(
            f"Tweet versions generated: "
            f"{len(result['tweet_history'])}"
        )


        with st.expander(
            "View Tweet History"
        ):

            for i, tweet in enumerate(
                result["tweet_history"],
                start=1
            ):

                st.write(
                    f"**Version {i}**"
                )

                st.write(tweet)

                st.divider()


        with st.expander(
            "View Evaluation History"
        ):

            for i, feedback in enumerate(
                result["feedback_history"],
                start=1
            ):

                st.write(
                    f"**Evaluation {i}**"
                )

                st.write(feedback)

                st.divider()