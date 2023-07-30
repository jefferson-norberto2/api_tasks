from flask import Flask, request, send_file

import protobuf.ticket.ticket as ticket
import io

app = Flask(__name__)
m_ticket = ticket.Ticket


@app.route('/prototype', methods=['POST'])
def prototype():
    message = request.data
    obj_ticket =  m_ticket.FromString(message)
    print(obj_ticket)
    return 'Received'

@app.route('/request', methods=['GET'])
def getTicket():
    print("Passou aqui")
    s_ticket = ticket.Ticket()
    medicamento = ticket.Medicamento()
    medicamento.tipo = ticket.MedicamentoType.AMPOLA
    medicamento.name = 'Dipirona'
    medicamento.quantidade = 7
    s_ticket.medicamentos.append(medicamento)
    return s_ticket.SerializeToString()

if __name__=='__main__':
    app.run(debug=True)