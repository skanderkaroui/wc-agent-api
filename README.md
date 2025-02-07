# wc-agent-api

## Project Overview
The `wc-agent-api` is an AI Agent designed to fetch and analyze information about the WorldChain coin. Utilizing OpenAI's language model and LangChain for orchestration, this agent generates insightful questions based on the fetched data. This project is intended for private use by members of the hackathon.

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/skanderkaroui/wc-agent-api
   cd wc-agent-api
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Required Packages**
   Create a `.env` file in the root directory of the project and add the necessary environment variables. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

   Example of `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   LANGCHAIN_API_KEY=your_langchain_api_key
   ```

## How to Use
1. Ensure your virtual environment is activated.
2. Run the main application:
   ```bash
   python main.py
   ```
3. Follow the prompts to input the name of the WorldChain coin and receive generated questions based on the fetched information.

## Contributing
This is a private repository for hackathon members. Please reach out to the project maintainers for access and contribution guidelines.

## License
This project is licensed for private use only during the hackathon.
