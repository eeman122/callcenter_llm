import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "https://callcenter-llm.onrender.com")

def process_audio(file_path):
    """Send audio to backend for processing"""
    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                f"{BACKEND_URL}/analyze",
                files={"file": f}
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": str(e)}

def update_ui(result):
    """Update Gradio UI with results"""
    if "error" in result:
        return result["error"], None, None, None
    
    # You'll need to adapt this to match your backend response
    transcription = result.get("transcription", "")
    sentiment = result.get("sentiment", {})
    tonal = result.get("tonal", {})
    evaluation = result.get("evaluation", {})
    
    # You'll need to implement these plotting functions in the frontend
    sentiment_plot = create_sentiment_plot(sentiment)
    tonal_plot = create_tonal_plot(tonal)
    
    return transcription, sentiment_plot, tonal_plot, evaluation

with gr.Blocks() as demo:
    gr.Markdown("# 🎧 Advanced Call Center QA System")
    gr.Markdown("Upload a call recording to analyze agent performance with transcription, sentiment analysis, and quality evaluation.")
    
    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="🎙️ Upload Call Recording")
        analyze_button = gr.Button("🚀 Analyze Call", variant="primary")
    
    with gr.Tabs():
        with gr.TabItem("📄 Transcription & Diarization"):
            transcription_output = gr.Textbox(label="Transcription", lines=15)
        
        with gr.TabItem("📊 Sentiment Analysis"):
            sentiment_plot = gr.Plot(label="Sentiment Analysis Results")
        
        with gr.TabItem("🎭 Tonal Analysis"):
            tonal_plot = gr.Plot(label="Tonal Emotion Distribution")
        
        with gr.TabItem("🧠 Quality Evaluation"):
            evaluation_output = gr.JSON(label="Evaluation Results")
    
    analyze_button.click(
        fn=process_audio,
        inputs=[audio_input],
        outputs=[transcription_output, sentiment_plot, tonal_plot, evaluation_output]
    )

if __name__ == "__main__":
    demo.launch(server_port=int(os.getenv("PORT", 7860)))
