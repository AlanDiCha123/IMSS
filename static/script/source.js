class Chatbot {
  constructor() {
    this.args = {
      openButton: document.querySelector('.chatbox__button'),
      chatBox: document.querySelector('.chatbox__support'),
      sendButton: document.querySelector('.send__button'),
      choiceButton: document.querySelector('.chatbox__options')
    }

    this.state = false;
    this.messages = [];
  }


  display() {
    const { openButton, chatBox, sendButton, choiceButton } = this.args;
    openButton.addEventListener('click', () => this.toggle(chatBox));
    var choices = [].slice.call(choiceButton.querySelectorAll('.options'));
    // choiceButton.addEventListener('click', function (e) {
    //   var index = choices.indexOf(e.target);
    //   if (index !== -1) {
    //     buttonClicked(chatBox, index);
    //   } else {
    //     console.log(index);
    //   }
    // });
    choiceButton.addEventListener('click', e => this.buttonClicked(chatBox, choices.indexOf(e.target)));
    sendButton.addEventListener('click', () => this.onSendButton(chatBox));
    // We listen to sending button
    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", ({ key }) => {
      if (key == "Enter") {
        this.onSendButton(chatBox);
      }
    })
  }

  toggle(chatbox) {
    this.state = !this.state;

    //show or hides the box
    if (this.state) {
      chatbox.classList.add('chatbox--active');
    } else {
      chatbox.classList.remove('chatbox--active');
    }
  }

  buttonClicked(chatbox, index) {
    let intents = `{
      "content": [
        {
          "tag": "Menor de edad",
          "next": [
            {
              "tag": "Trámite relacionado con UMF o clínica",
              "next": [
                "Darse de alta en su UMF",
                "Darse de baja en su UMF",
                "Actualizar o cambiar su UMF"
              ]
            },
            {
              "tag":"Trámite relacionado con guarderías",
              "next": "Inscribir a tu hijo a guarderias IMSS"
            },
            {
              "tag":"Trámite relacionado con prótesis externa, ortesis o ayuda técnica",
              "next": "Solicitar prótesis externa, ortesis o ayuda técnica"
            }
          ]
        },
        {
          "tag": "Mayor de edad",
          "next": [
            {
              "tag": "Trámite relacionado con UMF o clínica",
              "next": [
                "Darse de alta en su UMF",
                "Darse de baja en su UMF",
                "Actualizar o cambiar su UMF"
              ]
            },
            {
              "tag":"Trámite relacionado con no derechohabientes",
              "next": [
                "Constancia de no derechohabiente",
                "Inscripción a cursos representativos IMSS no derechohabiente"
              ]
            },
            {
              "tag":"Trámite relacionado con tu trabajo",
              "next": [
                "Aviso de calificación para accidente o enfermedad de trabajo",
                "Dictamen de incapacidad",
                "Certificado de discapacidad con fines de aplicación del árticulo 186"
              ]
            },
            {
              "tag":"Trámite relacionado con tu familia",
              "next": "Incorporar a su familia al seguro de salud del IMSS"
            },
            {
              "tag":"Otros trámites fuera de las categorías anteriores",
              "next": [
                "Reposición de credencial para usuarios de préstamos sociales",
                "Solicitar prótesis externa, ortesis o ayda técnica",
                "Inscripción a cursos ofrecidos por el IMSS",
                "Regularización o correción de tus datos personales",
                "Recuperación u obtención de tu NSS",
                "Solicitar la entrega de bienes resultados en una subasta del IMSS"
              ]
            }
          ]
        }
      ]
    }`;


    const obj = JSON.parse(intents);
    var html = '';
    var textField = chatbox.querySelector('.chatbox__options');
    let text1 = textField.getElementsByClassName('options')[index].innerText;
    let msg1 = { name: "User", message: text1 }
    this.messages.push(msg1);
    var count = textField.children.length;
    fetch('/predict', {
      method: 'POST',
      body: JSON.stringify({ message: text1 }),
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      },
    })
      .then(r => r.json())
      .then(r => {
        let msg2 = { name: "Sam", message: r.answer };
        this.messages.push(msg2);
        this.updateChatText(chatbox);
        textField.value = '';
      }).catch((error) => {
        console.error('Error', error);
        this.updateChatText(chatbox);
        textField.value = '';
      });
    for (var i = 0; i < textField.children.length; i++) {
      if (obj.content[i].tag === textField.getElementsByClassName('options')[index].innerText) {
        for (let k = 0; k < obj.content[i].next.length; k++) {
          html += `<div class="options messages__item messages__item--selector"> 
              ${obj.content[i].next[k].tag} </div>`;
        }
        break;
      }
    }
    var div = document.getElementById('choices');
    while (div.firstChild) {
      div.removeChild(div.firstChild);
    }
    // textField.innerHTML = html;
    chatbox.querySelector('.chatbox__options').innerHTML = html;
    html = '';
  }

  onSendButton(chatbox) {
    var textField = chatbox.querySelector('input');
    let text1 = textField.value;
    if (text1 === "") {
      return;
    }
    let msg1 = { name: "User", message: text1 }
    this.messages.push(msg1);
    fetch('/predict', {
      method: 'POST',
      body: JSON.stringify({ message: text1 }),
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      },
    })
      .then(r => r.json())
      .then(r => {
        let msg2 = { name: "Sam", message: r.answer };
        this.messages.push(msg2);
        this.updateChatText(chatbox);
        textField.value = '';
      }).catch((error) => {
        console.error('Error', error);
        this.updateChatText(chatbox);
        textField.value = '';
      });
    var div = document.getElementById('choices');
    while (div.firstChild) {
      div.removeChild(div.firstChild);
    }
  }

  updateChatText(chatbox) {
    var html = '';
    this.messages.slice().reverse().forEach(function (item) {
      if (item.name === "Sam") {
        html += `<div class="messages__item messages__item--visitor"> ${item.message} </div>`;
      } else {
        html += `<div class="messages__item messages__item--operator"> ${item.message} </div>`;
      }
    });
    const chatmessage = chatbox.querySelector('.chatbox__messages');
    chatmessage.innerHTML = html;
  }
}

const myChatbot = new Chatbot();
myChatbot.display();