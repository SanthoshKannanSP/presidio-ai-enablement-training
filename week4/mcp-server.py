from langchain_community.document_loaders import GoogleDriveLoader
from fastmcp import FastMCP
from pathlib import Path

app = FastMCP("mcpTool")

credentials_path = str(Path(__file__).parent / "credentials.json")
tokens_path = str(Path(__file__).parent / "token.json")


@app.tool(name="load_insurance_details")
def load_insurance_details() -> str:
    """
    Load insurance policy details of Presidio from Google Docs.

    Use this tool for:
    - Answering Insurance Related Queries regarding to Presidio

    Returns:
        insurance_policy: String of entire insurance policy details
    """
    try:
        loader = GoogleDriveLoader(
            credentials_path=credentials_path,
            token_path=tokens_path,
            document_ids=[""],
        )

        docs = loader.load()
        return docs[0].page_content

    except Exception as e:
        raise e


if __name__ == "__main__":
    app.run(transport="stdio", show_banner=False)
