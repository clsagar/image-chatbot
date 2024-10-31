from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

load_dotenv()


# Main function to run the Streamlit app
def main():
    genai.configure(api_key = st.secrets["your-API-KEY"])
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    # Initialize chat session in Streamlit if not already present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Configuring page
    st.set_page_config(
        page_title="ImageBot",
        page_icon="💬",
        layout="centered"
    )

    st.title("Integrated Chatbot and Image Processing App")

    # Display boxes for navigation
    col1, col2 = st.columns(2)

    with col1:
        st.header("Text Chatbot")
        text_chatbot = st.button("Text ChatBot📝")

    with col2:
        st.header("Image Chatbot")
        image_chatbot = st.button("Image Chatbot")

    if text_chatbot:
        st.session_state.active_chat = "text"  # Track which chatbot is active

    elif image_chatbot:
        st.session_state.active_chat = "image"  # Track which chatbot is active

    if st.session_state.get("active_chat") == "text":
        st.header("📝Text🦾Chatbot💻")
        st.text("Text-to-Text Chatbot, where you can ask any real questions and get real-time, intelligent responses...")
        for message in st.session_state.chat_history:
            with st.chat_message(message['role']):
                st.markdown(message["content"])

        # Input field for user's message
        user_prompt = st.chat_input("Ask ChatBot...")

        def get_gemini_response(prompt):
            try:
                response = model.generate_content(prompt, stream=True)
                response.resolve()
                return response.text
            except Exception as e:
                return f"An error occurred: {e}"

        if user_prompt:
            # Add user's message to chat and display it
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            st.chat_message("user").markdown(user_prompt)

            with st.spinner("Generating response..."):
                assistant_response = get_gemini_response(user_prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

            # Display ChatBot response
            with st.chat_message("assistant"):
                st.markdown(assistant_response)

    elif st.session_state.get("active_chat") == "image":
        st.header("🖼️Image🦾Chatbot💻")
        st.text("This is an image-based project capable of answering questions or giving detailed "
                "descriptions of the input images, demonstrating proficiency in computer vision and natural language processing...")
        input_prompt = st.text_input("Input Prompt: ", key="input")

        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", 'png', 'gif'])
        image = None
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

        submit = st.button("Submit")

        if submit:
            if input_prompt == "":
                input_prompt = "describe the image"
            response = model.generate_content([input_prompt, image])
            st.subheader("The response is")
            st.write(response.text)


# Run the Streamlit app
if __name__ == "__main__":
    main()











#
# text = st.button("Text ChatBot📝")
# st.text("Text-to-Text Chatbot, where you can ask any real questions and get real-time, intelligent responses...")
# img = st.button("Image ChatBot🖼️")
# st.text("This is an image-based project capable of answering questions or giving detailed "
#         "descriptions of the input images, demonstrating proficiency in computer vision and natural language processing...")
