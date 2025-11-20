import boto3
import json

sqs = boto3.client('sqs', region_name='us-east-2') 

MAIN_QUEUE_NAME = 'queue-trabgb'
DLQ_NAME = 'queue-trabgb-dlq' 

try:
    # cria a dlq
    dlq_response = sqs.create_queue(QueueName=DLQ_NAME)
    dlq_url = dlq_response['QueueUrl']
    
    # pegando o ARN (amazon resource name) da DLQ para configurar a principal
    dlq_attrs = sqs.get_queue_attributes(QueueUrl=dlq_url, AttributeNames=['QueueArn'])
    dlq_arn = dlq_attrs['Attributes']['QueueArn']

    # atualizando a fila principal com a redrive policy
    redrive_policy = {
        'deadLetterTargetArn': dlq_arn,
        'maxReceiveCount': '3' # SE falhar 3 vezes > vai para a DLQ
    }

    sqs.create_queue(
        QueueName=MAIN_QUEUE_NAME,
        Attributes={
            'RedrivePolicy': json.dumps(redrive_policy)
        }
    )

except Exception as e:
    print(f"Erro: {e}")