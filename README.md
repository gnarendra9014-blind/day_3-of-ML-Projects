# 🔒 Privacy Tester: Local LLM vs Cloud LLM

A Streamlit application that provides a practical demonstration of data privacy when using Artificial Intelligence. This tool compares responses from a local LLM running on your machine against a cloud-based LLM in real-time, highlighting exactly what data leaves your system and calculating a "Privacy Score" based on the sensitivity of your prompts.

## ✨ Features

- **Side-by-Side Comparison**: Run prompts simultaneously through a Local LLM (Ollama) and a Cloud LLM (Groq).
- **Privacy Analysis**: Automatically scans prompts for sensitive information (passwords, medical info, PII) before sending them.
- **Privacy Dashboard**: Visualizes the privacy risks of different prompts with an interactive gauge chart.
- **Performance Metrics**: Compares latency and response length between local inference and cloud APIs.

## 🛠️ Tech Stack

- **Frontend Visualization**: [Streamlit](https://streamlit.io/) & [Plotly](https://plotly.com/python/)
- **Local AI Inference**: [Ollama](https://ollama.com/) (running LLaMA 3.2 locally)
- **Cloud AI API**: [Groq](https://groq.com/) (running LLaMA 3.3 for high-speed cloud inference)

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com/download) installed on your machine
- A [Groq API Key](https://console.groq.com/keys)

### 2. Prepare Local Model
Start Ollama and pull the LLaMA 3.2 model:
```bash
ollama run llama3.2
```

### 3. Install Dependencies
Clone this repository and explore the directory. Then, set up your Python environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file based on `.env.example` in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application
Start the Streamlit dashboard:
```bash
streamlit run app.py
```

## 🧠 Why Does This Matter?

When using cloud-based AI models, your prompts and data are sent over the internet to remote servers. If you are handling sensitive user data, internal corporate code, medical history, or personal keys, a Local LLM ensures that **zero bytes of data leave your machine**. This project visualizes the trade-offs in speed, quality, and complete privacy guarantee.
