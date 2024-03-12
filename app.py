import os
from dotenv import load_dotenv
from src.web_interface import WebInterface


def run_app(prevent_thread_lock: bool = False):
    # Load environment variables
    load_dotenv()

    # Instantiate the WebInterface class
    web_interface = WebInterface()

    # Create and launch the Gradio web interface
    app = web_interface.create_web_interface()
    app.launch(server_name=os.environ.get('GRADIO_SERVER_NAME'),
               server_port=int(os.environ.get('GRADIO_SERVER_PORT')),
               favicon_path="images/KnowNetQA_icon.png",
               prevent_thread_lock=prevent_thread_lock,
               )


if __name__ == "__main__":
    run_app()
