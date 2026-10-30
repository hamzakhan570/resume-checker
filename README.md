AI ATS Resume Analyzer
A Streamlit application that extracts text from a PDF, DOCX, or TXT resume, calculates a transparent heuristic ATS-readiness estimate, and uses Google Gemini Flash to provide actionable improvement suggestions.
The score is an estimate based on a simple checklist. It is not an actual score from an employer's ATS, and it cannot predict whether a recruiter will select a candidate.

Features
- Upload PDF, DOCX, and TXT resumes (10 MB maximum).
- Optional job description comparison.
- Heuristic score with a visible category breakdown.
- Gemini-generated review with prioritized improvements, summary rewrite, bullet examples, supported keywords, and formatting tips.
- Download the feedback as a Markdown file.
- API key can be entered in the sidebar or supplied through Streamlit Secrets.
Project files
ats_resume_analyzer/
├── app.py
├── requirements.txt
└── README.md
1. Requirements
- Python 3.10 or newer
- A Google Gemini API key from Google AI Studio
2. Run locally on Windows
Open Command Prompt or PowerShell in the project folder.
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
If py is not recognized, install Python from python.org and enable Add Python to PATH during installation. Close and reopen the terminal afterwards.

If requirements.txt cannot be found, first change directory to the folder that contains the file:
cd path\to\ats_resume_analyzer
dir
The dir command should show app.py, requirements.txt, and README.md.
3. Add your Gemini API key
Option A — Sidebar (quick test)
Run the app and paste your key into Google Gemini API key in the sidebar. The key is not written into the source code.
Option B — Streamlit Secrets (recommended for deployment)
Create a folder named .streamlit and inside it create secrets.toml:
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
Add .streamlit/secrets.toml to .gitignore. Never upload API keys to GitHub.

Optional: choose another supported Gemini model by setting the GEMINI_MODEL environment variable. The default is gemini-2.5-flash.
4. Push to GitHub using the website UI
1. Sign in at GitHub and click New repository.
2. Name it ats-resume-analyzer. Choose Public or Private, then click Create repository.
3. In the repository page, choose Add file → Upload files.
4. Upload app.py, requirements.txt, and README.md.
5. Do not upload .streamlit/secrets.toml, API keys, .venv, or private resumes.
6. Enter a commit message such as Add Streamlit ATS resume analyzer.
7. Click Commit changes.
Recommended .gitignore contents:
.venv/
__pycache__/
.streamlit/secrets.toml
.env
5. Deploy on Streamlit Community Cloud
1. Push the three project files to GitHub.
2. Open Streamlit Community Cloud and sign in with GitHub.
3. Click Create app (or New app).
4. Select the repository, branch (usually main), and main file path app.py.
5. Open Advanced settings → Secrets and add:
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
6. Click Deploy and wait for the app to build.
7. Open the app URL and upload a test resume.
When you update the files in GitHub, Streamlit Cloud normally redeploys the app automatically.
Troubleshooting
- ModuleNotFoundError: No module named 'docx': confirm python-docx is present in requirements.txt, commit the change, then reboot/redeploy the app. The import is from docx import Document, but the package name is python-docx.
- No module named streamlit locally: activate .venv, then run python -m pip install -r requirements.txt using the same Python interpreter.
- requirements.txt not found: use cd to enter the project directory before installing.
- No text extracted from PDF: it may be a scanned/image-only PDF. OCR it first, or upload a text-based PDF or DOCX.
- Gemini API error: verify the key, model availability, API quota, and billing/region restrictions in Google AI Studio.
- App build error: open Manage app → Logs in Streamlit Cloud. Check that the repository root contains app.py and requirements.txt.
Privacy and limitations
- When you click Analyze, extracted resume text and the optional job description are sent to Google's Gemini API for analysis.
- The app does not save uploaded resumes to a database.
- PDF text extraction does not perform OCR.
- The score is a basic heuristic. ATS products differ, and formatting, parsing, job requirements, and recruiter decisions vary.
- The app's AI feedback must be reviewed by the candidate; it should not add skills or achievements that are not true.
