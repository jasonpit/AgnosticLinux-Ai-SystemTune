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
cd AgnosticLinux-Ai-SystemTune
```

Create a `.env` file with your OpenAI key:
```env
OPENAI_API_KEY=your-api-key-here
```

Run the tool:
```bash
python SystemTune.py
```

You’ll be guided through:
- System summary generation
- Log analysis (from journalctl and dmesg)
- AI-assisted diagnostics via OpenAI API
- Selection-based optimization options

---

## 🌐 Usage Notes

- Requires `sudo` for full diagnostic access (journal logs, hardware probing, swapfile creation)
- Interactive CLI prompts will walk you through available issues and proposed fixes
- Works best in a Python virtual environment
- Your API key can be provided through `.env`, environment variable, or prompted input

---

## 🧪 What Happens When You Run It

When executed, `SystemTune.py` performs the following steps:
1. **System Summary**: Displays OS, kernel, model, firmware, and CPU info.
2. **Log Collection**: Pulls data from `journalctl`, `dmesg`, and hardware lister tools.
3. **AI Querying**: Sends anonymized hardware and log info to OpenAI’s GPT model to analyze issues and suggest optimizations.
4. **Interactive Resolution**:
   - You’re prompted to pick an issue to fix
   - Common fixes include: adding swap, fixing Broadcom drivers, or tuning Mac-specific packages (like `macfanctld`)
   - If an issue can’t be fixed automatically (e.g., permission denied on `/etc/fstab`), you’ll be notified

All actions are logged and suggestions are presented with actionable insight.

---

Let me know if you want to export results to a file or add screenshot/GIF support for GitHub viewers.

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
