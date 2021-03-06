def about():
    window.location = "./pages/about.html"


def sendMsg():
    textfield = document.getElementById("input")
    textfield.focus()
    text = textfield.value
    if text:  # ignore empty field
        window.webxdc.sendUpdate(
            {
                "payload": {
                    "sender": window.webxdc.selfName,
                    "text": text,
                }
            },
            f'someone typed "{text}"',
        )
    textfield.value = ""


def receiveUpdate(update):
    msg = update.payload
    msgs = document.getElementById("msgs")
    msgs.innerHTML += f"<strong>&lt;{msg['sender']}&gt;</strong> {msg['text']}<br>"


def onInput():
    if event.key == "Enter":
        sendMsg()


def _onload():
    body = document.getElementsByTagName("body")[0]
    body.innerHTML += (
        '<input id="input" type="text" onkeydown="app.onInput();"/>'
        + '<button onclick="app.sendMsg();">Send</button>'
        + ' <button onclick="app.about();">About</button>'
        + '<p id="msgs"></p>'
    )

    window.webxdc.setUpdateListener(receiveUpdate, 0)  # process incoming messages


window.onload = _onload
