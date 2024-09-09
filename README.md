# Chat Assistant with Google Slides Integration

This is a simple chat interface built using Flask and the OpenAI API that adds a custom tool called `push_to_google_slide`. This tool allows the chatbot to automatically replace placeholder text (e.g., `<TK>`) in a Google Slide presentation with the information that the user requests through the chat interface.

## Features

- **OpenAI Chatbot Integration**: A simple conversational agent powered by OpenAI that responds to user input.
- **Google Slides Automation**: The chatbot can automatically replace text in a specified Google Slide presentation. It uses Google Slides API to search for a placeholder text (`<TK>`) and replace it with the requested information.
- **Persistent Chat Threads**: Chat threads are persistent, allowing for ongoing conversations to be tracked.

## Prerequisites

1. **Python 3.x** installed on your machine.
2. **OpenAI API key**: Sign up at [OpenAI](https://openai.com) to get an API key.
3. **Google Cloud credentials**: Set up a new OAuth 2.0 Client ID credential in Google Cloud, with the Slides API enabled and type "Desktop".

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://www.github.com/americanjournalismproject/slider
cd slider
```

### 2. Install Dependencies

Ensure you have `pip` installed, then run:

```bash
pip install -r requirements.txt
```

### 3. Set Up OpenAI and Google Slides

- **Create an OpenAI assistant**: make a new assistant in the [OpenAI playground](https://platform.openai.com/playground/assistants).
- **Add a function to your assistant** called `push_to_google_slides`. See example in `app.py`.
- **Find or create the Google Slides presentation** that you want to edit. Add `<TK>` to a text field in the presentation.

### 4. Set Up Environment Variables

Create a `.env` file in the root of the project with the following environment variables:

```env
OPENAI_API_KEY=your-openai-api-key
ASSISTANT_ID=your-openai-assistant-id
GOOGLE_SLIDES_PRESENTATION_ID=your-presentation-id
```

- `OPENAI_API_KEY`: Your OpenAI API key.
- `ASSISTANT_ID`: The ID of your assistant in OpenAI.
- `GOOGLE_SLIDES_PRESENTATION_ID`: The ID of the Google Slides presentation you want to modify.

### 5. Google OAuth Setup

- Download the `credentials.json` file from your Google Cloud OAuth instance. Put it in this project's root directory.
- When you first run the app, it will prompt you to authenticate with your Google account and generate a `token.json` file.

### 6. Run the Application

To start the application, run:

```bash
python app.py
```

This will launch the Flask app on `http://127.0.0.1:5000/`.

## Usage

1. **Access the Chat Interface**: Open your browser and go to `http://127.0.0.1:5000/`.
2. **Chat with the Assistant**: Type in your message. For example, you can ask the assistant to replace the placeholder `<TK>` in a Google Slide with any specific information you provide.
3. **Google Slides Automation**: When the assistant receives a request to update the Google Slide, it will replace the placeholder `<TK>` with the provided text.

## Example Interaction

- **User**: "Please update the slide with a talking point about how our audience loves cats."
- **Assistant**: Automatically replaces the `<TK>` placeholder in the designated Google Slide with talking points about cats.

## Files Overview

- `app.py`: The main application file. It handles routes, assistant interactions, and Google Slides API calls.
- `templates/index.html`: The front-end template for the chat interface.
- `.env`: Holds sensitive environment variables.
- `credentials.json` and `token.json`: Google Cloud OAuth credentials and token for accessing Google Slides API. `token.json` is automatically generated after the first login with your credentials.

## Limitations

- The placeholder text in Google Slides is currently hardcoded as `<TK>`. You may need to modify the code if you use different placeholders.
- The app assumes that the Google Slides presentation ID is provided in the `.env` file.

## License

This project is open source and available under the MIT License.
