import boto3
import json
import time

NOME_DA_FILA = 'queue-trabgb' 
sqs = boto3.client('sqs', region_name='us-east-1')

try:
    # URL da fila
    response = sqs.get_queue_url(QueueName=NOME_DA_FILA)
    queue_url = response['QueueUrl']

    print(f"Iniciando consumidor na fila: {queue_url}")
    print("Pressione CTRL+C para parar...")

    # polling
    while True:
        # recebe mensagens da fila
        response = sqs.receive_message(
            QueueUrl = queue_url,
            MaxNumberOfMessages = 1,
            WaitTimeSeconds = 10,
            AttributeNames=['ApproximateReceiveCount'] # pega a contagem de tentativas
        )

        if 'Messages' in response:
            for message in response['Messages']:
                body_str = message['Body']
                receipt_handle = message['ReceiptHandle']
                
                # pega quantas vezes essa mensagem já foi entregue
                try:
                    tentativas = int(message['Attributes']['ApproximateReceiveCount'])
                except KeyError:
                    tentativas = 1

                print(f"\n[MENSAGEM RECEBIDA - Tentativa #{tentativas}]")

                try:
                    # converte em JSON
                    data = json.loads(body_str)
                    produto = data.get('produto', 'Desconhecido')
                    
                    print(f"Conteúdo: {data}")

                    # se o produto for 'Bomba', um erro fatal eh gerado
                    if produto == 'Bomba':
                        raise ValueError("ERRO FATAL: Produto bomba detectado")

                    # aqui segue o processamento normal
                    print(f"Processando pedido ID: {data.get('id_pedido')}...")
                    time.sleep(2) # simula trabalho

                    # só deleta se chegar aqui sem erro
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=receipt_handle
                    )
                    print("[SUCESSO] Mensagem processada e deletada.")

                except json.JSONDecodeError:
                    print(f"[ERRO] JSON inválido: {body_str}")
                    # se o JSON é inválido deixamos estourar pra DLQ para analisar dps
                    print("Mensagem mantida na fila (vai para DLQ se persistir).")

                except Exception as e:
                    # pega o erro da 'Bomba' ou qualquer outro
                    print(f"[FALHA] Ocorreu um erro no processamento: {e}")
                    print("NÃO deletando a mensagem. Ela retornará para a fila após o Visibility Timeout.")
        else:
            print("Nenhuma mensagem na fila. Aguardando...")

except sqs.exceptions.QueueDoesNotExist:
    print(f"Erro: A fila '{NOME_DA_FILA}' não foi encontrada.")
except KeyboardInterrupt:
    print("\nConsumidor encerrado.")
except Exception as e:
    print(f"Ocorreu um erro geral: {e}")