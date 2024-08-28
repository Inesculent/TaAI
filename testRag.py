from interface import query_rag
#from langchain_community.llms.ollama import Ollama

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def test_question():
  #question = "How many equations will there be in the linear system to determine the natural spline that passes through these points?"
  question = "a two-input AND gate, with output y and inputs x1 and x2, is denoted as"
  response = query_rag(question)

  print(response)


