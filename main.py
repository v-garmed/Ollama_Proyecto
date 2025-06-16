from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from infonegocio import info

template = """
Answer the question below in spanish.

Here is the business information about the company: 
{infonegocio}

Question: {question}

Answer:

""" 

model = OllamaLLM(model = "llama3.1")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def chat():
    print("Hola, te saluda tu asistente de venta BOTin, ¿Cómo puedo ayudarte el día de hoy?.")
    context = ""
    while True:
        question = input("You: ")
        if question == "stop":
            break

        result = chain.invoke({"infonegocio":info, "context": context, "question": question})
        print("Bot:", result)
        context += f"Bot: {result}\nYou: {question}\n"


if __name__ == "__main__":
    chat()