import os
from google import genai


def analyze_test_failure(test_name, stack_trace, page_source=None):
    """
    Sends a test failure stack trace to Gemini to get an automated root-cause analysis.
    """
    # Ensure you have set your GEMINI_API_KEY in your environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gemini API Key not found. Please set the GEMINI_API_KEY environment variable."

    client = genai.Client(api_key=api_key)

    # Construct a structured prompt for the model
    prompt = f"""
    You are an expert SDET and QA Automation Engineer. Analyze the following automated test failure and provide a concise summary.
    
    Test Name: {test_name}
    
    Stack Trace / Error:
    {stack_trace}
    """

    if page_source:
        prompt += f"\nHTML Snippet / Page Source at time of failure:\n{page_source[:2000]}"  # Limit size

    prompt += "\n\nProvide your analysis in the following format:\n1. **Root Cause Summary**\n2. **Likely Reason (Bug vs. Flaky Test vs. Broken Locator)**\n3. **Recommended Fix Code**"

    try:
        # Using gemini-2.5-flash as it is fast, highly capable, and has a great free tier
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Failed to generate analysis from Gemini: {str(e)}"
