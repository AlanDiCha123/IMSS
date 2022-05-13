# We define the greetings
def greetings(message):
    text = evaluate(message)
    return text


def evaluate(text):
    if text == "Menor de edad" or text == "Mayor de edad":
        return "¿Qué desea realizar?"
    else:
        return "Selecciona el trámite deseado"
