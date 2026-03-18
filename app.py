import streamlit as st
import plotly.graph_objects as go
from local_llm import get_local_response
from cloud_llm import get_cloud_response
from analyzer import analyze_privacy, compare_quality

st.set_page_config(page_title="Privacy Tester", layout="wide")
st.title("🔒 Local LLM vs Cloud LLM — Privacy Tester")
st.caption("See exactly what data leaves your machine when you use AI")

EXAMPLE_PROMPTS = {
    "Safe": "What is the capital of France?",
    "Mildly sensitive": "My name is John. What career advice do you have?",
    "Very sensitive": "My password is abc123. Is that secure?",
    "Medical": "I have a diagnosis of anxiety. How do I manage it?",
}

col_left, col_right = st.columns([2, 1])
with col_left:
    example = st.selectbox("Try an example", list(EXAMPLE_PROMPTS.keys()))
    prompt = st.text_area(
        "Your prompt",
        value=EXAMPLE_PROMPTS[example],
        height=100
    )
with col_right:
    is_sensitive = "sensitive" in prompt.lower() or "medical" in prompt.lower() or "password" in prompt.lower()
    st.metric("Data sent to internet",
        "None (local recommended)" if is_sensitive else "Your prompt")

if st.button("🔍 Analyze Privacy + Compare", use_container_width=True):
    privacy = analyze_privacy(prompt)

    # Privacy warning
    if privacy["detected_sensitive"]:
        st.warning(f"⚠️ Sensitive data detected: {', '.join(privacy['detected_sensitive'])}. Cloud will receive this!")
    else:
        st.success("✅ No sensitive data detected in this prompt.")

    # Run both models
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖥️ Local (Ollama)")
        with st.spinner("Running locally..."):
            local = get_local_response(prompt)
            if local.get("error"):
                st.error(local["text"])
            else:
                st.success(local["text"])
                st.metric("Latency", f"{local['latency_ms']}ms")
                st.metric("Data sent outside", "None ✅")

    with col2:
        st.subheader("☁️ Cloud (Groq)")
        with st.spinner("Calling Groq cloud..."):
            cloud = get_cloud_response(prompt)
            if cloud.get("error"):
                st.error(cloud["text"])
            else:
                st.info(cloud["text"])
                st.metric("Latency", f"{cloud['latency_ms']}ms")
                st.metric("Data sent outside", "Your prompt ⚠️")

    # Privacy score gauge
    if not local.get("error") and not cloud.get("error"):
        st.divider()
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=privacy["cloud_privacy_score"],
            delta={"reference": 100},
            title={"text": "Cloud Privacy Score (100 = fully safe)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#1D9E75"},
                "steps": [
                    {"range": [0, 40], "color": "#FCEBEB"},
                    {"range": [40, 70], "color": "#FAEEDA"},
                    {"range": [70, 100], "color": "#EAF3DE"},
                ],
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        quality = compare_quality(local["text"], cloud["text"])
        st.subheader("Quality Comparison")
        st.dataframe({
            "Metric": ["Word count", "Latency (ms)", "Privacy score"],
            "Local": [quality["local_words"], local["latency_ms"], "100%"],
            "Cloud": [quality["cloud_words"], cloud["latency_ms"], f"{privacy['cloud_privacy_score']}%"],
        }, use_container_width=True)