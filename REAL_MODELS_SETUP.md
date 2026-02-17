# Running AiFlix with Real Models

To switch from mock implementations to real AI models, follow these steps.

## 1. Environment Setup

Create a `.env` file in the project root:

```bash
# .env
GROQ_API_KEY=gsk_...
REPLICATE_API_TOKEN=r8_...
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Switch Logic to Groq

In `verify_workflow.py` or your notebook, initialize the Orchestrator with `groq`:

```python
orchestrator = Orchestrator(llm_provider="groq")
```

The system is configured to use `llama3-70b-8192` by default. You can change this in `src/llm.py`.

## 4. Enable Real Media Generation (Replicate)

To use **FLUX.1** and **CogVideoX** via Replicate, you need to verify `REPLICATE_API_TOKEN` is set.

I have updated the code to look for the token. If the token is present and valid, you can uncomment or enable the Replicate logic in `src/media/image_gen.py`.

*Currently, the code defaults to Mock mode to avoid accidental charges.*

To force enable it, modify `src/media/image_gen.py`:

```python
# Change this:
# MOCK IMPLEMENTATION...

# To this:
import replicate
output = replicate.run(...)
```
