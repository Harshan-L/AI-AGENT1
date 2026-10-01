import os#myfirst

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import wikipedia_search, duckduckgo_search


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()



# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.5-flash-lite"


# ==========================================
# WIKIPEDIA TOOL
# ==========================================

wikipedia_tool = {
    "name": "wikipedia_search",
    "description": (
        "Search Wikipedia for information about people, "
        "places, historical events, concepts, or topics."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The topic or person to search for."
            }
        },
        "required": ["query"]
    }
}


# ==========================================
# DUCKDUCKGO TOOL
# ==========================================

duckduckgo_tool = {
    "name": "duckduckgo_search",
    "description": (
        "Search the internet using DuckDuckGo for current "
        "or general information."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query."
            }
        },
        "required": ["query"]
    }
}


# ==========================================
# CREATE GEMINI TOOLS
# ==========================================

tools = types.Tool(
    function_declarations=[
        wikipedia_tool,
        duckduckgo_tool
    ]
)


# ==========================================
# EXECUTE TOOL
# ==========================================

def execute_tool(function_name, arguments):

    if function_name == "wikipedia_search":

        query = arguments.get("query", "")

        return wikipedia_search(query)

    elif function_name == "duckduckgo_search":

        query = arguments.get("query", "")

        return duckduckgo_search(query)

    else:

        return "Unknown tool."


# ==========================================
# ASK GEMINI
# ==========================================

def ask_gemini(prompt):

    # --------------------------------------
    # STEP 1
    # Ask Gemini whether a tool is needed
    # --------------------------------------

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[tools]
        )
    )

    # --------------------------------------
    # Check if Gemini selected a tool
    # --------------------------------------

    function_calls = response.function_calls

    # --------------------------------------
    # No tool required
    # --------------------------------------

    if not function_calls:

        return response.text


    # --------------------------------------
    # STEP 2
    # Execute the selected tool
    # --------------------------------------

    tool_results = []

    for function_call in function_calls:

        function_name = function_call.name

        arguments = function_call.args

        query = arguments.get("query", "")

        print()
        print(f"🔧 Tool selected: {function_name}")
        print(f"🔎 Query: {query}")

        # Execute the tool
        result = execute_tool(
            function_name,
            arguments
        )

        # Store result
        tool_results.append(
            f"""
Tool: {function_name}

Search Result:
{result}
"""
        )


    # --------------------------------------
    # STEP 3
    # Combine tool results
    # --------------------------------------

    combined_results = "\n\n".join(tool_results)


    # --------------------------------------
    # STEP 4
    # Send results back to Gemini
    # --------------------------------------

    final_prompt = f"""
You are an AI assistant that can use external tools.

The user asked:

{prompt}


The following information was retrieved from external tools:

----------------------------------------
{combined_results}
----------------------------------------


Use the information above to answer the user's question.

IMPORTANT:
- Use the tool results when answering.
- Do not claim that you cannot access the internet.
- Do not mention a knowledge cutoff.
- Do not ignore the search results.
- Give the user a clear and useful answer.
"""


    # --------------------------------------
    # STEP 5
    # Generate final answer
    # --------------------------------------

    final_response = client.models.generate_content(
        model=MODEL,
        contents=final_prompt
    )


    return final_response.text


# ==========================================
# START AI AGENT
# ==========================================

print()
print("======================================")
print("        AI AGENT STARTED")
print("======================================")
print()
print("Available tools:")
print("1. Wikipedia")
print("2. DuckDuckGo Web Search")
print()
print("Type 'exit' or 'quit' to stop.")
print()


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    user_input = input("You: ")

    # Exit
    if user_input.lower() in ["exit", "quit"]:

        print()
        print("Goodbye!")
        break


    try:

        answer = ask_gemini(user_input)

        print()
        print("Agent:", answer)
        print()

    except Exception as e:

        print()
        print("Error:", str(e))
        print()