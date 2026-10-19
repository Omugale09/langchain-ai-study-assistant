
# LangChain AI Study Assistant

A simple terminal-based AI study assistant built using LangChain, LangGraph, and a local language model running on LM Studio on another laptop.

## Features

- Ask questions and get AI-generated explanations.
- Maintain conversation history during a session.
- Search Google for current information using SerpApi.
- Connect to LM Studio over a local network.
- Clear conversation history or exit the application.

## Technologies Used

- Python
- LangChain
- LangGraph
- LM Studio
- SerpApi
- python-dotenv

## Project Structure

```text
langchain_ai_study_assistant/
├── main.py
├── local_openai.py
├── .env
├── .env.example
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or newer
- LM Studio installed on the server laptop
- A compatible model loaded in LM Studio
- Both laptops connected to the same accessible network
- A SerpApi key if you want Google search functionality

## Configuration

The LM Studio server is configured at:

`http://192.168.10.2:1234`

The `.env` file should contain:

```dotenv
LM_STUDIO_BASE_URL=http://192.168.10.2:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_CHAT_MODEL=prism-ml/bonsai-27b
SERPAPI_KEY=
```

Replace the model identifier with the exact ID returned by LM Studio if it differs.

Add your SerpApi key to `SERPAPI_KEY` if you want internet search. Keep the `.env` file private.

## Installation

### 1. Clone or extract the project

Open a terminal inside the project directory.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

If `.env` does not exist, create it from the example:

```bash
cp .env.example .env
```

Edit `.env` and verify the server IP, port, and model identifier.

## Configure LM Studio

On the laptop running LM Studio:

1. Load the required language model.
2. Enable **Serve on Local Network** in the server settings.
3. Start the local server on port `1234`.
4. Allow connections through the firewall from your trusted local network.

## Test the Connection

From the laptop running the Python application, execute:

```bash
curl http://192.168.10.2:1234/v1/models
```

If the connection works, the endpoint should return JSON containing model information.

If the request fails, check the server status, IP address, port, firewall, and network configuration.

## Run the Application

Activate the virtual environment and execute:

```bash
python main.py
```

## Commands

- `/clear` — Clear the current conversation.
- `/exit` — Exit the application.
- `quit` — Exit the application.

## Troubleshooting

### Connection refused

Ensure LM Studio is running and accepting network connections on port `1234`.

### Connection timed out

Check the IP address, firewall rules, and network connectivity between the laptops.

### Model not found

Verify the model identifier using the `/v1/models` endpoint and update `.env`.

### Unexpected endpoint or method

Confirm that `LM_STUDIO_BASE_URL` ends in `/v1`, not `/v1/chat/completions`.

### SerpApi search fails

Verify your `SERPAPI_KEY` and internet connectivity. Search functionality is separate from the LM Studio connection.

## Security

- Do not commit `.env` or API keys to GitHub.
- Restrict access to the LM Studio server to trusted devices on your local network.
- Do not expose the local model server directly to the public internet.

## Limitations

This is a basic conversational assistant. It does not currently implement document-based RAG, PDF ingestion, or persistent conversation storage.

Conversation history is maintained in memory while the application runs.
