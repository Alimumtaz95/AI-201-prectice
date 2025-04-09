# pr1 Project

This project demonstrates the use of the `crewai` and `litellm` libraries to create workflows and generate fun facts about cities in Pakistan. The project consists of two main Python scripts: `main.py` and `main1.py`. Below is a step-by-step guide to understanding and running the project.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [Understanding the Code](#understanding-the-code)
   - [main.py](#mainpy)
   - [main1.py](#main1py)
4. [Running the Project](#running-the-project)
5. [Output](#output)
6. [Notes](#notes)

---

## Project Overview

The project contains two workflows:

1. **SimpleFlow** (in `main.py`): A basic workflow with three sequential steps.
2. **CityFunFact** (in `main1.py`): A workflow that generates a random city name, fetches a fun fact about it, and saves the fact to a file.

---

## Setup Instructions

1. **Python Version**: Ensure you have Python 3.10 installed. You can check the version using:
   ```bash
   python3 --version
   ```

2. **Install Dependencies**: Install the required libraries using `pip`:
   ```bash
   pip install crewai>=0.108.0 litellm>=1.60.2 python-dotenv>=1.0.0
   ```

3. **API Key**: The `main1.py` script uses the `litellm` library, which requires an API key. Add your API key to the `.env` file:
   ```
   API_KEY=your_api_key_here
   ```

---

## Understanding the Code

### main.py

This script defines a simple workflow using the `crewai` library. The workflow consists of three steps executed sequentially.

#### Code Explanation

```python
from crewai.flow.flow import Flow, start, listen
import time

class SimpleFlow(Flow):

    @start()
    def function1(self):
        print("Step1...")
        time.sleep(3)

    @listen(function1)
    def function2(self):
        print("Step2...")
        time.sleep(3)

    @listen(function2)
    def function3(self):
        print("Step3...")
        time.sleep(3)

def kickoff():
    obj = SimpleFlow()
    obj.kickoff()
```

- **`@start()`**: Marks the starting point of the workflow.
- **`@listen()`**: Defines the dependency between steps.
- **`kickoff()`**: Initiates the workflow.

---

### main1.py

This script defines a more complex workflow that interacts with the `litellm` library to generate a random city name, fetch a fun fact about it, and save the fact to a file.

#### Code Explanation

```python
from crewai.flow.flow import Flow, start, listen
from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

class CityFunFact(Flow):

    @start()
    def generate_random_city(self):
        result = completion(
            model="gemini/gemini-1.5-flash",
            api_key=API_KEY,
            messages=[{"content": "Generate a random city name of Pakistan.", "role": "user"}],
        )
        city = result['choices'][0]['message']['content']
        print(city)
        return city

    @listen(generate_random_city)
    def generate_fun_fact(self, city):
        result = completion(
            model="gemini/gemini-1.5-flash",
            api_key=API_KEY,
            messages=[{"content": f"Generate a fun fact about {city}.", "role": "user"}],
        )
        fun_fact = result['choices'][0]['message']['content']
        print(fun_fact)
        self.state['fun_fact'] = fun_fact

    @listen(generate_fun_fact)
    def Save_fun_fact(self):
        with open("fun_fact.md", "w") as file:
            file.write(self.state['fun_fact'])
            return self.state['fun_fact']

def kickoff():
    obj = CityFunFact()
    result = obj.kickoff()
    print(result)
```

- **`generate_random_city`**: Uses the `litellm` library to generate a random city name.
- **`generate_fun_fact`**: Fetches a fun fact about the generated city.
- **`Save_fun_fact`**: Saves the fun fact to a file named `fun_fact.md`.

---

## Running the Project

1. **Run SimpleFlow**:
   ```bash
   python3 src/pr1/main.py
   ```

2. **Run CityFunFact**:
   ```bash
   python3 src/pr1/main1.py
   ```

---

## Output

### SimpleFlow
When you run `main.py`, you will see the following output:
```
Step1...
Step2...
Step3...
```

### CityFunFact
When you run `main1.py`, the script will:
1. Generate a random city name.
2. Fetch a fun fact about the city.
3. Save the fun fact to `fun_fact.md`.

Example output:
```
Karachi
Karachi is known as the "City of Lights" due to its vibrant nightlife and cultural diversity.
```

The `fun_fact.md` file will contain:
```md
Karachi is known as the "City of Lights" due to its vibrant nightlife and cultural diversity.
```

---

## Notes

- Ensure you have a valid API key for the `litellm` library.
- The `fun_fact.md` file will be overwritten each time you run the `CityFunFact` workflow.
- The `.env` file is used to securely store the API key.

---

## Author

**Mumtaz Ali**  
Email: [mumtazalipintto@gmail.com](mailto:mumtazalipintto@gmail.com)
