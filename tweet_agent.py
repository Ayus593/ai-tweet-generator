from typing import TypedDict, Literal, Annotated
import operator
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not configured.")


evaluator = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GOOGLE_API_KEY
)

generator = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GOOGLE_API_KEY
)

optimizer = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GOOGLE_API_KEY
)
class TweetEvaluation(BaseModel):

    evaluation: Literal[
        "approved",
        "needs_improvement"
    ] = Field(
        ...,
        description="Final evaluation result."
    )

    feedback: str = Field(
        ...,
        description="Feedback for the tweet."
    )


structured_evaluator_llm = evaluator.with_structured_output(
    TweetEvaluation
)



class TweetState(TypedDict):

    topic: str
    tweet: str

    evaluation: Literal[
        "approved",
        "needs_improvement"
    ]

    feedback: str

    iteration: int
    max_iteration: int

    tweet_history: Annotated[
        list[str],
        operator.add
    ]

    feedback_history: Annotated[
        list[str],
        operator.add
    ]



def generate_tweet(state: TweetState):

    messages = [

        SystemMessage(
            content=(
                "You are a funny and clever "
                "Twitter/X influencer."
            )
        ),

        HumanMessage(
            content=f"""
Write a short, original, and hilarious tweet
on the topic: "{state['topic']}".

Rules:

- Do NOT use question-answer format.
- Maximum 280 characters.
- Use observational humor, irony, sarcasm,
  or cultural references.
- Think in meme logic, punchlines, or relatable takes.
- Use simple, day-to-day English.
"""
        )
    ]

    response = generator.invoke(messages)

    return {
        "tweet": response.content,
        "tweet_history": [response.content]
    }



def evaluate_tweet(state: TweetState):

    messages = [

        SystemMessage(
            content=(
                "You are a ruthless, no-laugh-given "
                "Twitter critic. "
                "You evaluate tweets based on humor, "
                "originality, virality, and tweet format."
            )
        ),

        HumanMessage(
            content=f"""
Evaluate the following tweet:

Tweet:
"{state['tweet']}"

Use these criteria:

1. Originality
2. Humor
3. Punchiness
4. Virality Potential
5. Format

Auto-reject if:

- It is question-answer format.
- It exceeds 280 characters.
- It reads like a traditional setup-punchline joke.
- It ends with generic or deflating lines.

Respond using the required structured format.
"""
        )
    ]

    response = structured_evaluator_llm.invoke(messages)

    return {
        "evaluation": response.evaluation,
        "feedback": response.feedback,
        "feedback_history": [response.feedback]
    }




def optimize_tweet(state: TweetState):

    messages = [

        SystemMessage(
            content=(
                "You punch up tweets for virality "
                "and humor based on given feedback."
            )
        ),

        HumanMessage(
            content=f"""
Improve the tweet based on this feedback:

"{state['feedback']}"

Topic:
"{state['topic']}"

Original Tweet:
"{state['tweet']}"

Rewrite it as a short, viral-worthy tweet.

Rules:

- Avoid Q&A style.
- Stay under 280 characters.
- Make it funny.
- Make it punchy.
- Do not add explanations.
"""
        )
    ]

    response = optimizer.invoke(messages)

    iteration = state["iteration"] + 1

    return {
        "tweet": response.content,
        "iteration": iteration,
        "tweet_history": [response.content]
    }




def route_evaluation(state: TweetState):

    if (
        state["evaluation"] == "approved"
        or state["iteration"] >= state["max_iteration"]
    ):
        return "approved"

    return "needs_improvement"



graph = StateGraph(TweetState)

graph.add_node(
    "generate",
    generate_tweet
)

graph.add_node(
    "evaluate",
    evaluate_tweet
)

graph.add_node(
    "optimize",
    optimize_tweet
)


graph.add_edge(
    START,
    "generate"
)

graph.add_edge(
    "generate",
    "evaluate"
)

graph.add_conditional_edges(
    "evaluate",
    route_evaluation,
    {
        "approved": END,
        "needs_improvement": "optimize"
    }
)

graph.add_edge(
    "optimize",
    "evaluate"
)


workflow = graph.compile()



def run_tweet_agent(
    topic: str,
    max_iterations: int
):

    initial_state = {
        "topic": topic,
        "iteration": 1,
        "max_iteration": max_iterations,
        "tweet": "",
        "evaluation": "needs_improvement",
        "feedback": "",
        "tweet_history": [],
        "feedback_history": []
    }

    result = workflow.invoke(initial_state)

    return result