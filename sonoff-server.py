import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import json
import datetime

# Fill the following parameters
deviceid = "10001d6a25"         # Your sonoff device id
server_ip = "192.168.0.101"     # IP of your RPi
port = 8888                     # An available port

sessions = []

class CommandOnHandler(tornado.web.RequestHandler):
    def get(self):
        for c in sessions:
            c.write_message("""{ "action": "update", "deviceid": "%s", "apikey": "111111111-1111-1111-1111-111111111111", "userAgent": "app", "ts": 0, "params": { "switch": "on" }, "from": "ddmbr" }""" % deviceid)

class CommandOffHandler(tornado.web.RequestHandler):
    def get(self):
        for c in sessions:
            c.write_message("""{ "action": "update", "deviceid": "%s", "apikey": "111111111-1111-1111-1111-111111111111", "userAgent": "app", "ts": 0, "params": { "switch": "off" }, "from": "ddmbr" }""" % deviceid)

class dispatchDeviceHandler(tornado.web.RequestHandler):
    def post(self):
        print "/dispatch/device"
        data = tornado.escape.json_decode(self.request.body)
        print data
        self.write("""{ "error": 0, "reason": "ok", "IP": "%s", "port": %s }""" % (server_ip, port))

class SocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in sessions:
            sessions.append(self)

    def on_message(self, message):
        message = json.loads(message)
        if 'action' in message:
            if message['action'] == 'register':
                self.write_message("""{ "error" : 0, "deviceid" : "%s", "apikey" : "111111111-1111-1111-1111-111111111111" }""" % deviceid)
            elif message['action'] == 'date':
                self.write_message("""{ "error" : 0, "date"  : %s, "deviceid" : "%s", "apikey" : "111111111-1111-1111-1111-111111111111" }""" % (datetime.date.today().isoformat, deviceid))

    def on_close(self):
        if self in sessions:
            sessions.remove(self)

application = tornado.web.Application([
    (r'/', getToken),
    (r'/dispatch/device', dispatchDeviceHandler),
    (r'/api/ws', SocketHandler),
    (r'/command_on', CommandOnHandler),
    (r'/command_off', CommandOffHandler),
])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": "sonoff-server.crt",
        "keyfile": "sonoff-server.key",
    })
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
