"# LLM_project" 
"# llm_project" 
"# callcenter_llm" 

# 📞 Call Center Agent Evaluation System using AI

An end-to-end AI pipeline for evaluating customer service calls using speech transcription, speaker diarization, sentiment & emotion analysis, and LLM-based rulebook evaluation. This system helps identify agent performance issues and compute key performance indicators (KPIs) automatically.

---

## 🚀 Features

- 🔊 **Automatic Speech Transcription** using WhisperX  
- 🧍‍♂️ **Speaker Diarization** to separate customer and agent voices  
- 😊 **Sentiment & Emotion Analysis** for each speaker using Hugging Face models  
- 📖 **Rulebook Evaluation** using Retrieval-Augmented Generation (RAG) and chunking  
- 📊 **Agent KPI Scoring** based on tone, compliance, and conduct  

---

## 🧠 Tech Stack

| Component        | Tool/Library                             |
|------------------|-------------------------------------------|
| Transcription    | [WhisperX](https://github.com/m-bain/whisperx) |
| Diarization      | WhisperX + PyAnnote                      |
| Sentiment Model  | `cardiffnlp/twitter-roberta-base-sentiment` |
| Emotion Model    | HuBERT-based audio emotion detection     |
| LLM Evaluation   | LangChain + FAISS                        |
| Rulebook Format  | Markdown / JSON                          |
| Language Models  | Mistral / OpenAI (optional)              |

