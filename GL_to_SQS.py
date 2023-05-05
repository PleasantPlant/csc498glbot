import json
import boto3

sqs = boto3.resource("sqs", region_name="us-east-2")
queue = sqs.get_queue_by_name(QueueName="GL-Tezt-Que")


class notifObj:
    def __init__(self):
        self.who = None
        self.what = None
        self.stream = None
        self.permalink = None

    def exportData(self):
        export = self.__dict__
        exportJson = json.dumps(export)
        return exportJson


def to_sqs(event, context):
    response = queue.send_message(MessageBody=event)
    print("Message published")
    print(event)
    return response


def lambda_handler(event, context):
    print(f"Received event:\n{event}\nWith context:\n{context}")
    eventbody = json.loads(event["body"])
    eventBacklog = eventbody["backlog"]
    nobj = notifObj()
    nobj.what = eventbody["event"]["fields"]["what"]
    nobj.who = eventbody["event"]["fields"]["who"]
    nobj.permalink = (
        "http://3.20.194.240/messages/"
        + eventBacklog[0]["index"]
        + "/"
        + eventBacklog[0]["id"]
    )
    nobj.stream = eventbody["event"]["fields"]["stream"]
    export = nobj.exportData()
    to_sqs(export, context)

    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
