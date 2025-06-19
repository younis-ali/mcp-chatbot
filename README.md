
# MCP Agntic AI for Research Papers

This project implements a chatbot using the Model Context Protocol (MCP) to search and retrieve information about research papers from arXiv. The chatbot allows us to query papers by topic and extract detailed information about specific papers.

## Overview

The system consists of two main components:

1. **Server**: A FastMCP server that provides tools for searching arXiv papers and extracting paper information.
2. **Client**: An MCP client that integrates with OpenAI's GPT model to process user queries and interact with the server.

The server stores paper information in JSON files organized by topic, while the client provides an interactive chat interface for users to input queries.

## Features

- **Search Papers**: Search for papers on arXiv by topic, with configurable maximum results.
- **Extract Paper Info**: Retrieve detailed information (title, authors, summary, PDF URL, publication date) for a specific paper using its arXiv ID.
- **Persistent Storage**: Paper information is saved in JSON files under a `papers` directory, organized by topic.
- **Interactive Chatbot**: Users can interact with the chatbot via a command-line interface, with support for natural language queries powered by OpenAI's GPT model.

## Requirements

- Python 3.8+
- Dependencies (install via `uv`):
  - `arxiv`
  - `mcp`
  - `openai`
  - `nest_asyncio`
  - `python-dotenv`
- OpenAI API key (stored in `src/keys.json`)
- `uv` (optional, for running the server)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies using `uv` (recommended) or `pip`:

3. Create a `src/keys.json` file with your OpenAI API key:
   ```json
   {
       "open_ai_api": "your-openai-api-key"
   }
   ```

4. Ensure the MCP configuration file (`mcp_config.json`) is set up correctly in the project root:
   ```json
   {
       "mcpServers": {
           "filesystem": {
               "command": "npx",
               "args": [
                   "-y",
                   "@modelcontextprotocol/server-filesystem",
                   "."
               ]
           },
           "research": {
               "command": "uv",
               "args": ["run", "research_server.py"]
           },
           "fetch": {
               "command": "uvx",
               "args": ["mcp-server-fetch"]
           }
       }
   }
   ```

## Usage

1. Start the MCP server:
   ```bash
   uv run src/research_server.py
   ```
   This runs the server with the `research` configuration, providing tools for paper search and extraction.

2. Run the client in a separate terminal:
   ```bash
   uv run main.py
   ```
   The client connects to the server, initializes the chatbot, and starts the interactive chat loop.

3. Interact with the chatbot:
   - Enter a query like "Search for papers on quantum computing" or "Get info for paper 1234.56789".
   - Ctrl+ C to exit.

<video controls src="MCP Server.mp4" title="Title"></video>

## Project Structure

```
├── papers/                   # Directory for storing paper information (auto-created)
├── src/
│   ├── client.py             # MCP client with chatbot implementation
│   ├── research_server.py    # FastMCP server with arXiv search tools
│   ├── keys.json             # API keys (not tracked in git)
├── mcp_config.json           # MCP server configuration
├── README.md
├── main.py                   # Entry point                   
```

## Example Queries

- Search for papers:
  ```
  Query: Find 3 papers on machine learning
  ```
  Output: List of paper IDs, with details saved in `papers/machine_learning/papers_info.json`.

- Extract paper information:
  ```
  Query: Get info for paper 2103.12345
  ```
  Output: JSON-formatted paper details (title, authors, summary, etc.) if found.

## Notes

- The server creates a `papers` directory to store JSON files containing paper information, organized by topic (e.g., `papers/quantum_computing/papers_info.json`).
- The client uses `gpt-4o-mini` by default. Update the model in `client.py` if needed.
- The system assumes `uv` is installed for running scripts. Modify the `command` in `mcp_config.json` if using a different tool (e.g., `python`).

## Future Improvements

- Add support for filtering papers by date, author, or category.
- Implement paper PDF download and storage.
- Enhance the chatbot with more natural language understanding for complex queries.
- Add a web-based UI for better user interaction.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

