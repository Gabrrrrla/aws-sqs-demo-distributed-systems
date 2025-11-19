import boto3
import json
import time

NOME_DA_FILA = 'queue-trabgb' 

sqs = boto3.client('sqs')

try:
    # URL da fila
    response = sqs.get_queue_url(QueueName=NOME_DA_FILA)
    queue_url = response['QueueUrl']

    print(f"Iniciando consumidor para a fila: {queue_url}")
    print("Pressione CTRL+C para parar...")

    # polling
    while True:
        
        # recebe mensagens da fila. WaitTimeSeconds > 0 habilita o "Long Polling"
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages = 1, # qnts msgs pegar por vez
            WaitTimeSeconds = 10     # tempo que a chamada espera por mensagens
        )

        # vê se a chave 'Messages' existe na resposta
        if 'Messages' in response:
            for message in response['Messages']:
                body_str = message['Body']
                print(f"\n[MENSAGEM RECEBIDA]")
                
                # processa como JSON
                try:
                    data = json.loads(body_str)
                    print(f"Processando Pedido ID: {data.get('id_pedido')} para o produto: {data.get('produto')}")
                except json.JSONDecodeError:
                    print(f"Processando mensagem (texto): {body_str}")
                
                # simula um tempo de processamento de 2s
                time.sleep(2) 

                # exclui a mensagem da fila após o processamento
                
                receipt_handle = message['ReceiptHandle']
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )
                
                print("[MENSAGEM PROCESSADA E DELETADA]")

        else:
            print("Nenhuma mensagem na fila. Aguardando...")

except sqs.exceptions.QueueDoesNotExist:
    print(f"Erro: A fila '{NOME_DA_FILA}' não foi encontrada.")
except KeyboardInterrupt:
    print("\nConsumidor encerrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")