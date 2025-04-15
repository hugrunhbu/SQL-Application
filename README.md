Chat-Based CSV Data Explorer with LLM + SQLite

Interactive AI-powered assistant that lets users explore spreadsheet data (CSV files) using natural language instead of SQL. Combining SQLite, pandas, and OpenAI's API to do it.

### What It Does:

- loads '.csv' files into a SQLite database
- lets users:
  - list tables
  - write raw SQL queries (e.g. SELECT \* FROM sales WHERE revenue > 50)
  - Ask questions in natural language (e.g. "what are my top 3 products by revenue?")
- uses OpenAI to convert natural language to SQL
- Runs everything through a command-line interface

### Features

- Dynamic table creation from any CSV file
- Schema conflict handling (overwrite, rename, skip)
- AI-based SQL generation using OpenAI API
- CLI commands: `load`, `list`, `query`, `ask`, `exit`
- Error logging to `error_log.txt`

### Tech Stack

- Python 3
- SQLite
- pandas
- openai (LLM API)
- python-dotenv (for managing API keys)

### setup

1. clone repo
2. create a virtual environment
3. install required packages by typing: "pip install -r requirements.txt"
4. create a '.env' file with OpenAI key
