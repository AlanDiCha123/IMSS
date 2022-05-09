import re
import random

# We import re module to use regular expressions (avoiding special chars)
# We define chatbot's answer method with the input user


def feedback(text):
    # We define answer chatbot
    split_msg = re.split(r'\s|[,:;.?-_]\s*', text.lower())
    answer = msg_checking(split_msg)
    return answer


# user_message: User's messages
# known_words: List of recognized words
# required_words: In case what there is a word, it requires a specific word
# We define a method to calc the probability of an answer


def probab_msg(user_message, known_words, sample_word=False, required_words=[]):
    certain_msg = 0
    contain_required_words = True

    # We travel through user's word messages to search recognized words
    for word in user_message:
        if word in known_words:
            certain_msg += 1

    # We get the percentage of security message
    percentage = float(certain_msg) / float(len(known_words))

    # We search if the message contains the required word, if it contains we break the loop

    for word in required_words:
        if word not in user_message:
            contain_required_words = False
            break
    # If that contains it or having a sample_word we return the major probability
    if contain_required_words or sample_word:
        return int(percentage * 100)
    else:
        return 0


# We define message checking method

def msg_checking(msg):
    high_prob = {}

    # We define the bot's answer method
    def response(bot_aswr, word_list, sample_word=False, needed_words=[]):
        nonlocal high_prob
        # We calc the bot's message probability
        high_prob[bot_aswr] = probab_msg(
            msg, word_list, sample_word, needed_words)

    # We define the bot's answer
    response('Bienvenid@ al chatbot del IMMS. ¿En que puedo ayudarte?',
             ['hola', 'saludos', 'buenas', 'saludo'], sample_word=True)
    response('Para realizar el alta de tu UMF deberas acudir a tu clinica mas cercana a tu domicilio con tu identificación oficial, comprobante de domicilio, NSS, una fotografia infantil y acta de nacimiento.\n¿Hay algo más en lo que le pueda ayudar?',
             ['alta', 'clinica', 'umf', 'resgistrar', 'registrarme', 'dar', 'darme'], needed_words=['alta'])
    response('Para realizar la baja de un UMF deberas acudir a tu clinica mas cercana a tu domicilio con tu identificación oficial, NSS, CURP y acta de defuncion en caso de muerte o acta de divorcio en caso de baja por divorcio.\n¿Hay algo más en lo que le pueda ayudar?',
             ['baja', 'umf', 'clinica', 'dar', 'darme'], needed_words=['baja'])
    response('Para realizar la actualización de tu UMF deberas acudir a tu clinica mas cercana a tu domicilio con tu identificación oficial, comprobante de domicilio, NSS y una fotografia infantil.\n¿Hay algo más en lo que le pueda ayudar?',
             ['actualizar', 'cambiar', 'clinica', 'umf', 'modificar'])
    response('Para obtener tu aviso para calificación de accidente o enfermedad de trabajo ante el IMSS deberas acudir a tu clinica que te corresponda de acuerdo a tu domicilio con tu identificación oficial, cartilla nacional de salud, aviso de atención médica inicial y calificación de probable accidente de trabajo ST-7 y ST-9. En caso de defunción sera acta de defunción, certificado de necropsia que incluya examen toxicológico copia certificada de la Averiguación Previa del Ministerio Público y resumen medico de atención inicial de servicios en caso de tenerlo.\n¿Hay algo más en lo que le pueda ayudar?',
             ['trabajo', 'laboral', 'calificacion', 'accidente', 'enfermedad'])
    response('Para incribir a tu hijo a las guarderias del IMSS deberas acudir a la guarderia de tu interes o entrar al siguiente link:\nhttps://stigi.imss.gob.mx/\nen un horario de lunes a viernes de 7 a 19 horas con los siguientes datos de tu hijo/a: Nombre completo Fecha de nacimiento Acta de nacimiento Cartilla Nacional de Salud Examen Medico requisitado Tambien deberas presentar tu nombre, NSS, domicilio, datos de contacto, UMA, parentesco, CURP, identificación oficial con fotografia, solicitud de inscripción y constancia de platica de nuevo ingreso. Ademas deberas presentar el nombre o razon social, domicilio y telefono y extensiones de tu lugar de trabajo.\n¿Hay algo más en lo que le pueda ayudar?',
             ['incripcion', 'inscribir', 'hijo', 'hija', 'guarderia'], needed_words=['guarderia'])
    response('Estoy para servirle',
             ['gracias', 'te lo agradezco', 'adios', 'nos vemos'], sample_word=True)

    # We define the best answer
    best_coincidence = max(high_prob, key=high_prob.get)
    # We return the answer, if there is no a good coincidence, shows the answers by default
    return default() if high_prob[best_coincidence] < 1 else best_coincidence


# We define the method to give default answers
def default():
    # Permite mostrar varias respuestas al azar
    reply = ['¿Puedes volver a repetirlo?', 'No estoy seguro de lo quieres',
             'No cuento con la información que necesitas'][random.randrange(3)]
    return reply
