import boto3
import json

NOME_DA_FILA = 'queue-trabgb' 

sqs = boto3.client('sqs')

try:
    # pega a url da fila com base no nome
    response = sqs.get_queue_url(QueueName=NOME_DA_FILA)
    queue_url = response['QueueUrl']

    print(f"URL da Fila: {queue_url}")

    # a mensagem em si
    mensagem_body = {
        'id_pedido': 123,
        'produto': 'Laptop',
        'quantidade': 1
    }

    # envia a mensagem
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(mensagem_body) # converte o dict para um JSON
    )

    print(f"Mensagem enviada! ID: {response['MessageId']}")

except sqs.exceptions.QueueDoesNotExist:
    print(f"Erro: A fila '{NOME_DA_FILA}' não foi encontrada.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")