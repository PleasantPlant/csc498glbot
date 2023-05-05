import json
import http.client


class notifObj:
    def __init__(self):
        self.who = None
        self.what = None
        self.stream = None
        self.permalink = None

    def importData(self, exportJson):
        export = exportJson
        try:
            export = json.loads(exportJson)
        except AttributeError:
            export = exportJson
        finally:
            self.__dict__ = export
            return True


def lambda_handler(event, context):
    conn = http.client.HTTPSConnection("hooks.slack.com")
    for i in event["Records"]:
        lejson = i["body"]
        nobj = notifObj()
        nobj.importData(lejson)
        loadpay = f'"Alert!\nWhat: {nobj.what}\nWho: {nobj.who}\nStream: {nobj.stream}\nPermalink: {nobj.permalink}"'
        payload = '{"text":' + loadpay + "}"
        headers = {"Content-type": "application/json"}
        conn.request(
            "POST",
            "/services/T04SDDC220K/B051HRHKW81/6slicYEvNHdKWuiyUdmXgjKg",
            payload,
            headers,
        )
        res = conn.getresponse()
        data = res.read()

    return payload
