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
    choiceButton.addEventListener('click', e => this.buttonClicked(chatBox, [].slice.call(choiceButton.querySelectorAll('.options')).indexOf(e.target)));
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
              "tag": "Trámite relacionado con UMF",
              "next": [
                "Darse de alta en su UMF",
                "Darse de baja en su UMF",
                "Actualizar o cambiar su UMF", 
                "Terminar conversación"
              ]
            },
            {
              "tag":"Trámite relacionado con guarderías",
              "next": [
                "Inscribir a tu hijo a guarderias IMSS",
                "Terminar conversación"
              ]
            },
            {
              "tag":"Trámite relacionado con prótesis externa, ortesis o ayuda técnica",
              "next": [
                "Solicitar prótesis externa, ortesis o ayuda técnica",
                "Terminar conversación"
            ]
            },
            {
              "tag": "Terminar conversación"
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
                "Actualizar o cambiar su UMF",
                "Terminar conversación"
              ]
            },
            {
              "tag":"Trámite relacionado con no derechohabientes",
              "next": [
                "Constancia de no derechohabiente",
                "Inscripción a cursos representativos IMSS no derechohabiente",
                "Terminar conversación"
              ]
            },
            {
              "tag":"Trámite relacionado con tu trabajo",
              "next": [
                "Aviso de calificación para accidente o enfermedad de trabajo",
                "Dictamen de incapacidad",
                "Certificado de discapacidad con fines de aplicación del árticulo 186",
                "Terminar conversación"
              ]
            },
            {
              "tag":"Trámite relacionado con tu familia",
              "next": [
                "Incorporar a su familia al seguro de salud del IMSS",
                "Terminar conversación"
              ]
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
            },
            {
              "tag": "Terminar conversación"
            }
          ]
        }
      ]
    }`;


    const obj = JSON.parse(intents);
    var html = '';
    var textField = chatbox.querySelector('.chatbox__options');
    let text1 = document.getElementsByClassName('options')[index].innerText;
    console.log(index);
    if (text1 === "Terminar conversación") {
      this.clearContent(chatbox);
      return 0;
    }
    let band = false;
    for (let i = 0; i < 2; i++) {
      if (obj.content[i].tag === text1) band = true;
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
    if (band) {
      for (var i = 0; i < textField.children.length; i++) {
        if (obj.content[i].tag === textField.getElementsByClassName('options')[index].innerText) {
          for (let k = 0; k < obj.content[i].next.length; k++) {
            html += `<div class="options messages__item messages__item--selector"> 
              ${obj.content[i].next[k].tag} </div>`;
          }
          break;
        }
      }
    } else {
      for (var i = 0; i < obj.content.length; i++) {
        for (var j = 0; j < obj.content[i].next.length; j++) {
          if (obj.content[i].next[j].tag === textField.getElementsByClassName('options')[index].innerText) {
            for (let k = 0; k < obj.content[i].next[j].next.length; k++) {
              html += `<div class="options messages__item messages__item--selector"> 
                ${obj.content[i].next[j].next[k]} </div>`;
            }
            break;
          }
        }
      }
    }
    var div = document.getElementById('choices');
    while (div.firstChild) {
      div.removeChild(div.firstChild);
    }
    textField.innerHTML = html;
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
    var band = false;
    this.messages.slice().reverse().forEach(function (item) {
      if (item.name === "Sam") {
        html += `<div class="messages__item messages__item--visitor"> ${item.message} </div>`;
        if (item.message === "Estoy para servirle") band = true;
      } else {
        html += `<div class="messages__item messages__item--operator"> ${item.message} </div>`;
      }
    });
    const chatmessage = chatbox.querySelector('.chatbox__messages');
    chatmessage.innerHTML = html;
    if (band) setTimeout(() => this.clearContent(chatbox), 4000);
  }

  clearContent(chatbox) {
    var html = ` <div class="messages__item messages__item--visitor">
					Bienvenido al chatbot del IMSS. Puedo ayudarte a
					resolver tus dudas sobre algún trámite. Para empezar
					quisiera saber a quien está dirigido tu trámite.</div> `;

    const chatmessage = chatbox.querySelector('.chatbox__messages');
    chatmessage.innerHTML = html;

    var options = `<div class="options messages__item messages__item--selector">
					Menor de edad </div>
					<div class="options messages__item messages__item--selector">
					Mayor de edad </div> `;

    const chatoptions = chatbox.querySelector('.chatbox__options');
    chatoptions.innerHTML = options;
  }
}

const myChatbot = new Chatbot();
myChatbot.display();