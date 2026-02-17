# AiFlix: Distributed Cinematic Intelligence

AiFlix is an autonomous multi-agent studio that turns a one-line concept into a fully visualized cinematic sequence.

## 🚀 How to Run

### prerequisites
1. Python 3.10+
2. API Keys for **Groq** and **Replicate**.

### Setup
1. Clone the repo.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your keys in `.env`:
   ```env
   GROQ_API_KEY=gsk_...
   
   # Option A: Free Open Source Models (Recommended)
   HF_TOKEN=hf_...
   # Note: Free tier supports robust FLUX.1 Image Generation. 
   # Video generation (SVD) may be rate-limited or unavailable on the free router.
   
   # Option B: Replicate (Paid/Cloud)
   REPLICATE_API_TOKEN=r8_...
   ```

### 🎬 Run Studio
To generate a movie sequence from a concept:

```bash
python3 src/main.py "A cyberpunk detective investigating a neon-lit alleyway."
```

**Options:**
- `--max_shots N`: Limit generation to N shots (saves money/time).
  ```bash
  python3 src/main.py "A cowboy dual at sunset" --max_shots 1
  ```

## 🏗 System Architecture

- **Studio Head (Orchestrator)**: Manages the workflow.
- **Screenwriter**: Writes the script (Groq/Llama3).
- **DOP**: Plans the shots (Groq/Llama3).
- **Identity Manager**: Maintains character consistency.
- **Visual Engine**: Generates media (Replicate: FLUX.1 + CogVideoX).

## 📦 Production
See `PRODUCTION.md` for details on deploying as an API with Docker and Databases.
