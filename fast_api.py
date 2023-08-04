from fastapi import FastAPI, Request
from protobuf.ticket.ticket import Ticket, Medicamento, MedicamentoType

app = FastAPI()
ticket = Ticket

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/prototype")
async def read_user(request: Request):
    message_p = await request.body()
    
    obj_ticket = ticket.FromString(message_p)
    print(obj_ticket)
    for med in obj_ticket.medicamentos:
        print(med.name, med.quantidade, med.tipo)

    return 'teste'

@app.get("/request")
async def read_user():
    ticket = Ticket()
    medicine_1 = Medicamento()
    medicine_2 = Medicamento()

    medicine_1.name = 'Paracetamol'
    medicine_1.quantidade = 2
    medicine_1.tipo = MedicamentoType.PACOTE

    medicine_2.name = 'Dipirona'
    medicine_2.quantidade = 1
    medicine_2.tipo = MedicamentoType.AMPOLA

    ticket.medicamentos.append(medicine_1)
    ticket.medicamentos.append(medicine_2)

    return ticket.SerializeToString()
