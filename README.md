# CrowdWork - Combined Prompt Viewer

A web-based frontend for viewing combined prompts from the CrowdWork database.

## Features

- **Canvas Display**: View combined prompts in a resizable canvas area
- **Real-time Updates**: Refresh button to get the latest data from the database
- **Copy to Clipboard**: One-click copying of the combined prompt
- **Download**: Save the combined prompt as a text file
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask web server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

- `GET /` - Main frontend page
- `GET /api/combined-prompt` - Returns the combined prompt from the database

## Database Integration

The frontend automatically connects to your existing `agent_data.db` database and uses the `create_combined_prompt()` function to retrieve and display the combined content.

## Usage

1. **View Prompt**: The combined prompt will automatically load when you visit the page
2. **Refresh**: Click "Refresh Prompt" to get the latest data from the database
3. **Copy**: Click "Copy to Clipboard" to copy the prompt to your clipboard
4. **Download**: Click "Download as TXT" to save the prompt as a text file

## File Structure

```
CrowdWork/
├── app.py              # Flask web server
├── db.py              # Database functions
├── templates/
│   └── index.html     # Frontend HTML/CSS/JS
├── requirements.txt    # Python dependencies
└── agent_data.db      # SQLite database
``` 