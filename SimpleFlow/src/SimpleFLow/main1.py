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
        # return fun_fact

    @listen(generate_fun_fact)
    def Save_fun_fact(self):
        with open("fun_fact.md", "w") as file:
            file.write(self.state['fun_fact'])
            return self.state['fun_fact']
    
def kickoff():
    obj=CityFunFact()
    result = obj.kickoff()
    print(result)
