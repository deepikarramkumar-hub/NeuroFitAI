# NeuroFit AI – Personal Fitness Coach

A beginner-friendly full-stack project built with:
- Frontend: HTML, CSS and JavaScript
- Backend: Python Flask
- Database: SQLite

## Features
1. Personalised starter fitness plan based on goal, experience, available equipment, time and weekly schedule.
2. General balanced meal ideas.
3. Fitness assistant chat endpoint with simple topic-based responses.
4. SQLite storage for generated plan history.
5. Responsive dashboard.

> The recommendation logic in this student project is a simple rule-based prototype. It is not a trained medical AI model and does not provide medical advice.

## Requirements
- Python 3.9 or newer
- VS Code
- Internet connection only if you want the Google Fonts used in the design (the app itself works without them).

## Run in VS Code (Windows)

1. Extract `NeuroFitAI.zip`.
2. Open the extracted `NeuroFitAI` folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:

   ```powershell
   py -m venv venv
   ```

5. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt terminal and run:

   ```cmd
   venv\Scripts\activate.bat
   ```

6. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

7. Start the application:

   ```powershell
   py app.py
   ```

8. Open this address in your browser:

   `http://127.0.0.1:5000`

## Project structure

```text
NeuroFitAI/
│   app.py
│   requirements.txt
│   README.md
│   .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── app.js
```

The SQLite database `neurofit.db` is created automatically the first time the app runs.

## Troubleshooting
- If `py` is not recognised, install Python and select **Add Python to PATH** during installation. You can also try `python` instead of `py`.
- If port 5000 is already in use, close the other app using it, then run the project again.
- Keep the terminal running while you use the website. Press `Ctrl + C` to stop the server.

## Project explanation for presentation
NeuroFit AI is a personal fitness coaching web application. Users enter their fitness goal, experience level, equipment availability and daily schedule. The Flask backend processes these inputs and generates a starter workout outline and balanced meal ideas. The generated plan is stored in an SQLite database, and users can view their recent plans on the dashboard.
