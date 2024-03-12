import os
from dotenv import load_dotenv
import gradio as gr
from src import dirs
from src.document_extractor import DocumentExtractor
from src.chatbot import ChatBot


class WebInterface:
    def __init__(self):
        self.document_extractor = DocumentExtractor()
        self.chatbot = ChatBot()
        self.chatbot.setup_chatbot()

    def get_chatbot_response(self, question, history, url, keywords):
        user_keywords = None
        if keywords:
            # Split keywords by comma and strip spaces
            user_keywords = [keyword.strip() for keyword in keywords.split(",")]

        # Extract text from the provided URL and save it
        if url:
            self.document_extractor.crawl_and_extract(
                documents_dir=str(dirs.DOCUMENTS_DIR),
                url=url,
                query=question,
                user_keywords=user_keywords,
            )

            # Set up the chatbot with the configuration
            self.chatbot.setup_chatbot()

        # Get response from the chatbot
        response = self.chatbot.ask_question(question)
        return response

    def create_web_interface(self):
        app = gr.ChatInterface(
            fn=self.get_chatbot_response,
            additional_inputs_accordion=gr.Accordion(label="Additional Inputs", open=True),
            additional_inputs=[
                gr.Textbox(label="url", lines=2, placeholder="Enter Website URL here..."),
                gr.Textbox(label="keywords", lines=2,
                           placeholder="[Optional] Enter Keywords here separated by commas..."),
            ],
            title="KnowNetQA",
            description=
            """Provide a URL and keywords to extract documents for the chatbot to learn from, then ask any question.""",
            examples=[
                [
                    "What is Python ?",
                    "https://en.wikipedia.org/wiki/Python_(programming_language)",
                    "python, programming, example"
                ]
            ],
        )
        return app


if __name__ == "__main__":
    load_dotenv()
    web_interface = WebInterface()
    app = web_interface.create_web_interface()
    app.launch(server_name=os.environ.get('GRADIO_SERVER_NAME'),
               server_port=int(os.environ.get('GRADIO_SERVER_PORT')),
               )
