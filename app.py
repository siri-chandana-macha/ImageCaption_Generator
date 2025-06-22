import streamlit as st
from PIL import Image
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

# Set page config FIRST
st.set_page_config(page_title="🖼️ Image Caption Generator", layout="centered")

# Load model components
@st.cache_resource
def load_model():
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    return model, processor, tokenizer

model, processor, tokenizer = load_model()

# App UI
st.title("🖼️ Image Caption Generator")
st.write("Upload an image to get a caption!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Generate caption
    with st.spinner("Generating caption..."):
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        output_ids = model.generate(pixel_values, max_length=16, num_beams=4)
        caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    st.success("✅ Caption Generated:")
    st.write(f"📝 {caption}")
