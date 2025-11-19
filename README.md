# Implementação de Produtor/Consumidor com AWS SQS

Este projeto é uma implementação prática de um sistema distribuído utilizando o padrão **Produtor-Consumidor** via **Amazon Simple Queue Service (SQS)**. O projeto foi desenvolvido como parte da disciplina de Sistemas Distribuídos.

## Descrição

O sistema consiste em dois scripts Python independentes que se comunicam de forma assíncrona:
1.  **Produtor (`producer.py`):** Envia mensagens JSON simulando pedidos para uma fila SQS.
2.  **Consumidor (`consumer.py`):** Monitora a fila, recupera as mensagens, processa os dados e remove a mensagem da fila para evitar reprocessamento.

# Pré-requisitos
Para executar este projeto, é necessário ter:

* **Python 3.8+** instalado.
* Uma conta ativa na **AWS**.

# Dependências
O projeto utiliza a biblioteca `boto3` para interagir com a AWS.

```bash
pip install boto3
```
