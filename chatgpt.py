from openai import OpenAI

client = OpenAI()

def get_keywords(career: str, model: str) -> str:
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"""Get domain-specific keywords associated with {career} and return the result in a comma delimited string.
                
                For example, you would return the domain-specific keywords associated with software engineer as follows:
                Python,Java,Javascript,Big O Notation,Agile Methodology,RESTful APIs,Design Patterns,Data Structures,Object-Oriented Programming,Continuous Integration/Continuous Deployment,Version Control Systems,Test-Driven Development,Microservices,Containerization"""
            }
        ]
    )

    print(f"Keywords: {completion.choices[0].message.content}")
    return completion.choices[0].message.content