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
    response('Para obtener tu constancia de no derechohabiente deberas ingresar al siguiente link http://www.imss.gob.mx/constancia-no-derechohabiencia con tu CURP y correo electronico donde se te enviara tu constancia con una validez de un día.\n¿Hay algo más en lo que le pueda ayudar?',
             ['obtener', 'constancia', 'no', 'derechohabiente', 'sacar', 'sacarme'], needed_words=['no'])
    response('Para realizar tu inscripción a cursos para representativos IMSS no derechohabientes deberas acudir a tu clinica mas cercana a tu domicilio con tu identificación oficial, comprobante de domicilio, carta de autorización de padres o tutor en caso de ser menor de edad y contancia firmada por el director de la unidad que lo acredite como representativo. Además deberas presentar un pago de 80.00 pesos en el momento de tu tramite.\n¿Hay algo más en lo que le pueda ayudar?',
             ['inscribir', 'incribirme', 'curso', 'cursos', 'representativos', 'inscripcion', 'no', 'derechohabientes', 'derechohabiente'], needed_words=['no'])
    response('Para reposición de tu credencial para usuarios de prestamos sociales deberas presentarte en ventanilla y mencionar que deseas reponer tu credencial. Recibiras una ficha de deposito para realizar el pago de tu reposición con un valor de 40.00 pesos  y deberas presentar tu ficha ya pagada nuevamente en ventanilla para recoger tu credencial.\n¿Hay algo más en lo que le pueda ayudar?',
             ['reposicion', 'reponer', 'credencial', 'prestamo', 'social', 'usuarios', 'usuario', 'prestamos', 'sociales'], needed_words=['credencial'])
    response('Para obtener tu dictamen de incapacidad deberas acudir a tu clinica mas cercana a tu domicilio con tu Cartilla Nacinal de Salud, identificación oficial, solicitud de beneficiario incapacitado ante el Control de Prestaciones de la Unidad de Medicina Familiar y pase del servicio de medicina familiar o de especialista médico de segundo ó tercer nivel de Atención a Salud en el Trabajo\n¿Hay algo más en lo que le pueda ayudar?',
             ['obtener', 'sacar', 'dictamen', 'incapacidad', 'trabajo'], needed_words=['incapacidad'])
    response('Para incribirte en alguno de los cursos que ofrece el IMSS deberas acudir a tu clinica más cercano a tu domicilio y presentar identificación oficial, carta de autorización de tutor, ficha de deposito y en caso de ser derechohabiente credencial escolar y comprobante de domicilio. El pago que deberas de realizar sera de un valor de 80.00 pesos.\n¿Hay algo más en lo que le pueda ayudar?',
             ['inscribir', 'incribirme', 'curso', 'cursos', 'inscripcion'])
    response('Para realizar la regularización y/o corrección de sus datos acudir a su clinica o presentar su tramite desde internet a travez del siguiente link:\nhttps://serviciosdigitales.imss.gob.mx/correcciondatosasegurado-web-ciudadano/wizard/correccionDatosAsegurado/\n con los siguientes documentos a la mano: CURP, acta de nacimiento, identificación oficial y un documento expedido por el IMSS que contenga su NSS. Además en caso de realizar su tramite en linea debera tener un correo electronico donde se le hara llegar la confirmación del tramite y en caso de tramite presencial debera presentar la solicitud de regularización y/o corrección de datos personales del asegurado que se encuentra en el siguinete link:\nhttp://www.imss.gob.mx/sites/all/statics/pdf/formatos/SolicRegCorreDatosPerso.pdf \n¿Hay algo más en lo que le pueda ayudar?',
             ['datos', 'corregir', 'correcion', 'personales', 'regularizar', 'regularizacion', 'cambiar', 'cambio'], needed_words=['datos'])
    response('Para solicitar prótesis externa, ortesis o ayuda técnica debera acudir a su clinica asiganada con su identificación oficial, Cartilla Nacional de Salud y orden para la dotación o reparación de prótesis, ortesis o ayudas funcionales en un horario de: 8 a 20 horas de lunes a viernes.\n¿Hay algo más en lo que le pueda ayudar?', [
             'solucitud', 'solicitar', 'protesis', 'ortesis', 'ayuda', 'tecnica'])
    response('Este tramite cuenta con modalidad tanto presencial como en linea. Para realizar el tramite en linea debera entrar al siguiente link y tener a la mano un correo electronico donde le llegara toda la información y su CURP.\nhttps://serviciosdigitales.imss.gob.mx/gestionAsegurados-web-externo/asignacionNSS;JSESSIONIDASEGEXTERNO=Wmle4dHJBfUuckhnc0tp3p26Yf0mShg7udNAfPlNHRuL28mPSKA4!-1100133577\n Si desea realizar el tramite presencial debera acudir a su clinica más cercana de lunes a viernes de 8 a 15 horas con su acta de nacimeinto identificación oficial, CURP y poder notarial en caso de que el registro de nacimiento se haya realizado por Autoridad Civil (DIF y PGR).\n¿Hay algo más en lo que le pueda ayudar?',
             ['asignacion', 'asignar', 'nss', 'localizar', 'obtener', 'saber', 'asignen', 'den', 'pedir', 'localicen', 'numero', 'seguro', 'social'])
    response('Para obetner su certificado de discapacidad con fines de aplicación del artículo 186 de la Ley del Impuesto Sobre la Renta debera acudir a su clinica asignada de lunes a vierns en un horario de 8 a 19 horas con los siguientes documentos: Solicitud de Certificado de Discapacidad que obtendra en el siguiente link: http://www.imss.gob.mx/sites/all/statics/pdf/tramites-varios/certif-186-solicitud-instructivo.pdf Identificación oficial con fotografia y firma Copia del aviso de inscripción al IMSS del trabajador de la liquidación del pago de cuotas obrero-patronales del Sistema Único de Autodeterminación (SUA) o Emisión Mensual Anticipada (EMA).\n¿Hay algo más en lo que le pueda ayudar?',
             ['obtener', 'sacar', 'certificado', 'discapacidad', 'articulo', '186'], needed_words=['certificado'])
    response('Para solicitar la entrega de bienes rematados en una subasta del IMSS deberas presnetarte en la Oficina para Cobros donde se realizo la subasa de lunes a viernes de 8 a 15 con el acta de remates como postor ganador, recibo de pago efectuado del 90% del importe ofrecido en la puja e identificación oficial. En caso de realizar el tramite un representante legal este debera traer poder notarial , carta poder ratificada y su identificación oficial.\n¿Hay algo más en lo que le pueda ayudar?', [
             'solicitar', 'entrega', 'bienes', 'subasta', 'rematados'], needed_words=['subasta'])
    response('Para incorporar a su familia al seguro de salud del IMSS sin contar con un esquema de seguridad social podras realizar el tramite tanto en linea como en fisico. Para realizar tu tramite en linea deberas tener a la mano tu NSS y un correo electronico y entrar al siguiente enlace: https://serviciosdigitales.imss.gob.mx/portal-ciudadano-web-externo/home En caso de realizar tu tramite en fisico deberas acudir a tu clinica más cercana con  acta de matrimonio, identificación oficial, CURP, comprobante de pago de anualidad anticipada, Acta de nacimeinto, comprobante de domicilio y cuestionario medico proporcionado por el IMSS.\n¿Hay algo más en lo que le pueda ayudar?',
             ['familia', 'incorporacion', 'incorporar', 'seguro', 'imss'], needed_words=['familia'])
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
