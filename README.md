# 💬 Chatbot — Multi-Thread AI Chat with Persistent Memory

**A ChatGPT-style chatbot that never forgets a conversation, even after you close the tab.**

Most demo chatbots lose everything on refresh. This one doesn't: every conversation is checkpointed to a local SQLite database via LangGraph, so you can start new chats, switch between old ones, and pick up right where you left off — all from a simple Streamlit sidebar.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Memory-1C3C3C)
![Gemini](https://img.shields.io/badge/Gemini-2.5--flash--lite-4285F4?logo=googlegemini&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Persistence-003B57?logo=sqlite&logoColor=white)

---

## Why This Project

Most tutorial chatbots are single-turn or lose state the moment you refresh the page. This project uses LangGraph's `SqliteSaver` checkpointer to persist every message to disk per conversation thread, so chat history survives restarts, and multiple separate conversations can exist side by side — much closer to how a real chat product behaves.

## How It Works

```
User message
     │
     ▼
Streamlit chat input
     │
     ▼
LangGraph StateGraph ("chat_node")
     │
     ▼
Gemini 2.5 Flash-Lite generates a response
     │
     ▼
SqliteSaver checkpoints the full message state to Chatbot.db
     │
     ▼
Response streamed back to the Streamlit UI
```

Each conversation is tracked by a unique `thread_id`. Starting a "New Chat" generates a fresh thread; picking a thread from the sidebar reloads its full message history from the database.

## Key Features

- **Persistent conversation memory** — chat history is checkpointed to a local SQLite database (`Chatbot.db`) via LangGraph's `SqliteSaver`, so nothing is lost between sessions
- **Multi-thread chat** — start new conversations and revisit old ones from the sidebar, each with its own isolated message history
- **Streamed responses** — assistant replies are streamed token-by-token into the UI using `chatbot.stream(...)`
- **Minimal, hackable core** — the entire agent is a single-node LangGraph graph (`chat_node`), making it a clean starting point for adding tools, RAG, or multi-step reasoning
- **Simple, chat-native UI** — built with Streamlit's native `st.chat_message` and `st.chat_input` components

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Agent orchestration | LangGraph (`StateGraph`) |
| Conversation memory | LangGraph `SqliteSaver` checkpointer + SQLite |
| LLM | Google Gemini `2.5-flash-lite` via `langchain-google-genai` |

## Repo Structure

```
Chatbot/
├── Chatbot.py         # LangGraph agent: state, chat node, SQLite checkpointer
├── Frontend.py         # Streamlit UI: sidebar threads, chat input, streaming responses
├── Chatbot.db           # SQLite database (auto-created, stores conversation checkpoints)
└── requirements.txt
```

## Setup

### Prerequisites
- Python 3.10+
- A [Google Gemini API key](https://makersuite.google.com/app/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/PalTrivedi/Chatbot.git
cd Chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the repo root:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

## Run

```bash
streamlit run Frontend.py
```

The app opens in your browser (default `http://localhost:8501`). Click **New Chat** to start a conversation, and revisit any past thread from the **Previous Conversations** sidebar.

## Limitations & Future Work

- Single-node graph — no tool use, retrieval, or multi-step reasoning yet
- Thread list is derived by scanning all checkpoints on load, which won't scale well with a very large number of conversations
- No thread titles/labels — conversations are identified by raw UUID in the sidebar
- No authentication — anyone with access to the app can see all stored chat threads
- Next steps: named/auto-titled threads, tool-calling nodes (web search, RAG), and swapping SQLite for a hosted store for multi-user deployments

## License

MIT — feel free to fork and adapt.

## Author

Built by **Pal Trivedi**. Feedback and PRs welcome.
