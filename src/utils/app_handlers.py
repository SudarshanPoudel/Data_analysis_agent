import os
import re
from typing import Literal


def process_question(
    app,
    file: str,
    query: str = "",
    metadata: str = "",
    report: Literal["yes", "no"] = "no",
) -> dict:
    """
    Process the question and generate the final output.

    Args:
        app: The graph app to process the question.
        file: The file name of the data.
        query: The question to be processed. Defaults to "".
        metadata: The metadata of the data. Defaults to "".
        report: Whether to generate a report. Defaults to "no".

    Returns:
        dict: A dictionary containing the response, including an answer and charts if available.
    """
    data_path = os.path.join("data", file)
    inputs = {
        "query": query,
        "data_path": data_path,
        "metadata": metadata,
        "report": report,
    }

    try:
        for output in app.stream(inputs):
            for key, value in output.items():
                print(f"Node '{key}':")
            print("====== END OF NODE ======\n")

        print("====== FINAL GENERATION ======")
        return value.get(
            "generation", {"answer": "Unable to answer your query", "charts": []}
        )
    except Exception as e:
        return {"answer": f"Error processing request: {e}", "charts": []}


def display_markdown_with_images(markdown_content: str, st):
    """
    Display markdown content using st.markdown() and display images separately.

    Args:
        markdown_content: Markdown content to be displayed.
    """
    image_pattern = r"!\[.*?\]\((.*?)\)"
    images = re.findall(image_pattern, markdown_content)
    parts = re.split(image_pattern, markdown_content)

    for i, part in enumerate(parts):
        if i % 2 == 0:
            st.markdown(part)
        else:
            st.image(part.replace("%20", " "))  # Convert URL-encoded spaces
