# ai-tweet-generator

# AI Tweet Generator

An AI-powered tweet generation and evaluation system built with **LangGraph, Google Gemini, LangChain, and Streamlit**.

The application generates a tweet from a given topic, evaluates it for quality, and automatically improves it based on evaluator feedback until the tweet is approved or the maximum number of evaluation attempts is reached.

## How It Works

The application uses an iterative generation-evaluation workflow:

```text
User enters topic
        ↓
   Generate Tweet
        ↓
    Evaluate Tweet
        ↓
   ┌────┴────┐
   │         │
Approved   Needs Improvement
   │         │
   ↓         ↓
  END     Optimize Tweet
             │
             ↓
          Evaluate
             │
             └─────── loop

## Features

- Generate original tweets from a given topic
- Evaluate tweets for:
  - Originality
  - Humor
  - Punchiness
  - Virality potential
  - Tweet format
- Automatically improve tweets using evaluator feedback
- Configurable maximum number of evaluation attempts
- Maintains tweet and feedback history
- Uses structured LLM evaluation with Pydantic
- LangGraph-based iterative workflow
- Streamlit user interface

## Tech Stack

- Python
- LangGraph
- LangChain
- Google Gemini
- Pydantic
- Streamlit
- python-dotenv