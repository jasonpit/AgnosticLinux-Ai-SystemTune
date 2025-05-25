# AgnosticLinux-Ai-SystemTune

AgnosticLinux-Ai-SystemTune is a lightweight Python utility that performs intelligent system diagnostics and optimization recommendations on any Linux system. It collects hardware information, system logs, and uses OpenAI's API to generate insightful, actionable tuning suggestions.

---

## 🧠 What It Does

- Gathers hardware, software, and kernel data
- Parses system logs for recent errors or warnings
- Sends anonymized diagnostics to OpenAI to get performance and stability tips
- Displays AI-generated suggestions to the user
- Prompts the user to manually or automatically apply improvements (manual execution only for now)

---

## 📦 Features

- Works on any Linux distro (Debian, Arch, Fedora, etc.)
- CLI-based, no GUI needed
- Secure: API key is not hardcoded
- AI-powered diagnostics via GPT-4
- Designed for extensibility and portability

---

## 🔧 Requirements

- Python 3.7+
- `openai` Python SDK
- Internet access for AI queries

Install dependencies:
```bash
pip install openai python-dotenv
```

---

## 🚀 Quick Start

Clone the repo:

```bash
git clone https://github.com/jasonpit/AgnosticLinux-Ai-SystemTune.git
cd AgnosticLinux-AgnosticLinux-Ai-SystemTune
```

Create a `.env` file with your OpenAI key:

```env
OPENAI_API_KEY=your-api-key-here
```

Run the tool:

```bash
python SystemTune.py
```

If the environment variable is not found, the script will prompt you securely for the API key.

---

## 🌐 Usage Notes

- Run from a terminal or over SSH
- You may need `sudo` for full diagnostics (e.g., `journalctl`)
- Use in a Python virtual environment to avoid conflicts:
  ```bash  
  mkdir -p SystemTune 
  cd SystemTune/
  curl -O https://raw.githubusercontent.com/jasonpit/AgnosticLinux-Ai-SystemTune/main/SystemTune.py
  python -m venv .venv
  source .venv/bin/activate
  ```

---

## ⚙️ Roadmap

- [ ] Auto-apply selected optimizations
- [ ] Export reports to Markdown or HTML
- [ ] Package as `.deb`, `.rpm`, and `AUR`
- [ ] GUI front-end (Web & GTK planned)
- [ ] Auto-update with GitHub releases

---

## 📜 License

MIT License © Jason Pit
