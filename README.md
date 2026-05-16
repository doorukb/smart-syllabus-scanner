Syllabus Parser

This is a command-line tool that reads a plain-text syllabus file and extracts structured information from it using the Anthropic Claude API. It returns a clean JSON object containing the course code, instructor email, grading weights, important dates, and key policy statements. The output is validated with Pydantic, and the tool automatically retries once if the model returns malformed output.

INPUT : 
```
CS 101: Introduction to Computer Science
Fall 2025

Instructor: Dr. Jane Smith
Email: j.smith@university.edu
Office Hours: Monday/Wednesday 2–3 PM, Room 304

Course Description:
An introduction to the fundamentals of computer science, covering
algorithms, data structures, and basic programming concepts.

Grading:
  Homework Assignments: 30%
  Midterm Exam:         25%
  Final Exam:           35%
  Participation:        10%

Important Dates:
  Midterm Exam:            October 15, 2025
  Last day to withdraw:    November 1, 2025
  Final Exam:              December 10, 2025

Policies:
- Late submissions will be penalized 10% per day, up to a maximum of 50%.
- Attendance is expected at all lectures and recitations.
- Academic dishonesty (plagiarism, cheating) will result in a zero for
  the assignment and may be referred to the academic integrity office.
- Students requiring accommodations should contact the instructor within
  the first two weeks of the semester.
- All electronic devices must be silenced during lectures.

```

OUTPUT : 
```
stop_reason=end_turn
{
  "course_code": "CS 101",
  "instructor_email": "j.smith@university.edu",
  "grading_weights": [
    {
      "component": "Homework Assignments",
      "percent": 30.0
    },
    {
      "component": "Midterm Exam",
      "percent": 25.0
    },
    {
      "component": "Final Exam",
      "percent": 35.0
    },
    {
      "component": "Participation",
      "percent": 10.0
    }
  ],
  "important_dates": [
    {
      "label": "Midterm Exam",
      "date_iso": "2025-10-15",
      "raw_text": ""
    },
    {
      "label": "Last day to withdraw",
      "date_iso": "2025-11-01",
      "raw_text": ""
    },
    {
      "label": "Final Exam",
      "date_iso": "2025-12-10",
      "raw_text": ""
    }
  ],
  "policy_bullets": [
    "Late submissions will be penalized 10% per day, up to a maximum of 50%.",
    "Attendance is expected at all lectures and recitations.",
    "Academic dishonesty (plagiarism, cheating) will result in a zero for the assignment and may be referred to the academic integrity office.",
    "Students requiring accommodations should contact the instructor within the first two weeks of the semester.",
    "All electronic devices must be silenced during lectures."
  ]
}
```

<br><br>

INSTALLATION : 
Requires Python 3.10 or higher.

1. Clone the repository and enter the folder.
  
2. Create and activate a virtual environment:
   python -m venv .venv
   .venv\Scripts\activate
   
3. Install dependencies:
   pip install -r requirements.txt

4. Copy the environment file template and add your API key:
   copy .env.example .env
   Open .env and replace the placeholder with your real Anthropic API key.
   Get a key at: https://console.anthropic.com/settings/keys
   Your .env file is listed in .gitignore and will never be committed.

<br><br>

USAGE :

Feel free to change syllabus.txt with any text file but you might want to change the prompts in the source code too- keep an eye on that. As a good example, you can test how the algorithm will behave given syllabus.txt with following constraints however you desire : 

Run against the included sample syllabus :
   python demo_extract.py --file syllabus.txt

Run with debug output (prints stop reason and error class names to stderr, never your document):
   python demo_extract.py --file syllabus.txt --debug

Pipe text from stdin (press Ctrl+Z then Enter on Windows to signal end of input):
   type syllabus.txt | python demo_extract.py

Limit how much of a long document is sent (default cap is 50,000 characters):
   python demo_extract.py --file syllabus.txt --max-chars 20000

The extracted JSON is printed to stdout. You can redirect it to a file:
   python demo_extract.py --file syllabus.txt > output.json

<br><br>
   
OUTPUT : 

Given a syllabus (which is hard coded to the project) the tool always returns a JSON object with these fields : 
   course_code        - course identifier, e.g. CS 101, or null if not found
   instructor_email   - primary instructor email, or null if not found
   grading_weights    - list of objects with component name and percent value
   important_dates    - list of objects with a label, an ISO-8601 date if parseable, and the raw text phrase
   policy_bullets     - list of policy statements as plain strings
   
Doing what with this JSON file is totally up to you.

<br><br>
   
ENVIRONMENT VARIABLES :  

   ANTHROPIC_API_KEY   Required. Your Anthropic API key. Read from .env or set directly in your shell.

<br><br>

Roadmap :
   - Accept PDF files directly as input using a PDF-to-text conversion step
   - Add a simple web interface so users can paste or upload a syllabus in a browser
   - Wrap the extractor in a FastAPI endpoint for use as a microservice
   - Support batch processing of multiple syllabus files in one run
   - Add an output flag to write JSON directly to a file instead of stdout
   - Validate instructor_email as a properly formatted email address
