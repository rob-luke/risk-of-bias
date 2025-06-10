import base64
from pathlib import Path
from typing import Dict, List, Optional, Union


def pdf_to_base64(pdf_file_path: Path) -> str:
    """
    Convert a PDF file to a base64 encoded string.

    Args:
        pdf_file_path (Path): The path to the PDF file to be encoded.

    Returns:
        str: The base64 encoded string representation of the PDF file.
    """
    with open(pdf_file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")


def create_openai_message(
    role: str,
    text: Optional[str] = None,
    file_data: Optional[str] = None,
    filename: Optional[str] = None,
    content_type: str = "input",
) -> Dict[str, Union[str, List[Dict[str, str]]]]:
    """
    Create a message dictionary for chat input with proper type handling.

    Args:
        role: The role of the message ('system', 'user', 'assistant')
        text: Text content for the message
        file_data: Base64 encoded file data (with data: prefix)
        filename: Name of the file being attached
        content_type: Type of content ('input' for user messages,
                     'output' for assistant)

    Returns:
        Dictionary formatted for chat input
    """
    if role == "system":
        if text is None:
            raise ValueError("System messages require text content")
        return {"role": "system", "content": text}

    content_list = []

    # Add file data if provided
    if file_data and filename:
        content_list.append(
            {
                "type": f"{content_type}_file",
                "filename": filename,
                "file_data": file_data,
            }
        )

    # Add text if provided
    if text:
        content_list.append({"type": f"{content_type}_text", "text": text})

    if not content_list:
        raise ValueError("Message must have either text or file data content")

    return {"role": role, "content": content_list}
