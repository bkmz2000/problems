# Simple Codeforces-like Judge with Python Backend and Judge0

## Features

- Problem statement on the left, code editor on the right
- Upload file and submit solution
- Python backend (no Flask) serves static files and handles submissions
- Judge0 runs in Docker to evaluate code

## Usage

1. **Build and start the system:**
   ```
   docker-compose up --build
   ```

2. **Open the site:**
   Visit [http://localhost:5000](http://localhost:5000) in your browser.

3. **Submit a solution:**
   - Write code in the editor or upload a file.
   - Click "Submit Solution" to run your code against the sample input.

## File Structure

- `codeforces-clone/` — Frontend files and backend code
- `docker-compose.yml` — Orchestrates backend and Judge0

## Notes

- The backend uses Python's built-in http.server (no Flask or external dependencies).
- Judge0 is used for code execution and evaluation in a secure container.
- The default problem expects two integers as input and outputs their sum.
