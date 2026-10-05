# project-genai-post-generator

This tool analyzes the past LinkedIn posts of an influencer and helps them create new posts that match their writing style.

Let's say Mohan is a LinkedIn influencer and he needs help writing his future posts. He can feed his past LinkedIn posts to this tool, which extracts key topics from them. He can then select a topic, length, and language, and hit **Generate** to create a new post that matches his writing style.

## How it works

1. **Stage 1 — Preprocessing** (`preprocess.py`): collect raw LinkedIn posts (`data/raw_posts.json`) and use an LLM to extract `line_count`, `language`, and `tags` from each one, saving the enriched result to `data/processed_posts.json`.
2. **Stage 2 — Generation** (`post_generator.py`): given a selected topic, language, and length, the app pulls a couple of matching past posts as few-shot examples and asks the LLM to write a new post in that same style.

A small set of sample posts is already included in `data/` so the app works out of the box — swap in your own posts and re-run `preprocess.py` to personalize it.

## Project structure

```
.
├── main.py              # Streamlit UI
├── post_generator.py    # Prompt construction + generation
├── few_shot.py           # Loads & filters past posts for few-shot examples
├── preprocess.py         # One-off script: raw posts -> enriched posts
├── llm_helper.py         # Groq LLM client
├── data/
│   ├── raw_posts.json        # Your original posts (input to preprocess.py)
│   └── processed_posts.json  # Enriched posts (input to the app)
├── requirements.txt
└── .env.example
```

## Set-up

1. **Get an API key**: create a free key at [console.groq.com/keys](https://console.groq.com/keys).
2. **Configure your environment**: copy `.env.example` to `.env` and paste in your key:
   ```commandline
   cp .env.example .env
   ```
3. **Install dependencies**:
   ```commandline
   pip install -r requirements.txt
   ```
4. **Run the app**:
   ```commandline
   streamlit run main.py
   ```

## Using your own posts

1. Put your raw posts into `data/raw_posts.json`, each as `{"text": "..."}`.
2. Run the preprocessing step to extract metadata and tags:
   ```commandline
   python preprocess.py
   ```
   This regenerates `data/processed_posts.json`, which the app reads from.
3. Restart the Streamlit app — your topics will now show up in the **Topic** dropdown.

## Notes

- The model used is `openai/gpt-oss-120b` on Groq (configurable via `GROQ_MODEL_NAME` in `.env`). Groq model ids change fairly often as they retire older models — check [console.groq.com/docs/deprecations](https://console.groq.com/docs/deprecations) if you ever get a `model_not_found`/`model_decommissioned` error, and [console.groq.com/docs/models](https://console.groq.com/docs/models) for the current list.
- Requires Python 3.10+. If `pip install` tries to *build* a package (e.g. pandas) from source instead of using a precompiled wheel, your Python version is likely too new or too old for a pinned dependency — run `python --version` and, if needed, `pip install --upgrade pip` before retrying.

---

Copyright (C) Codebasics Inc. All rights reserved.

**Additional Terms:**
This software is licensed under the MIT License. However, commercial use of this software is strictly prohibited without prior written permission from the author. Attribution must be given in all copies or substantial portions of the software.
