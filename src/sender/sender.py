###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) typedef int GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import asyncio

from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


class MyClientProtocol(WebSocketClientProtocol):
    def __init__(self, text):
        super().__init__()
        self.text_to_send = text  # Initialize as None initially

    def onConnect(self, response):
        #print("Server connected: {0}".format(response.peer))
        return

    def onConnecting(self, transport_details):
        #print("Connecting; transport details: {}".format(transport_details))
        return None  # ask for defaults

    def onOpen(self):
        #print("WebSocket connection open.")

        def send():
            self.sendMessage(self.text_to_send.encode('utf8'))
            self.sendClose()

        send()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        #print("WebSocket connection closed: {0}".format(reason))
        self.factory.loop.stop()

async def connect_to_server(text, loop):
    factory = WebSocketClientFactory("ws://127.0.0.1:9000")
    factory.protocol = lambda: MyClientProtocol(text)
    coro = loop.create_connection(factory, '127.0.0.1', 9000)
    await coro

def send_message(text):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(connect_to_server(text, loop))

    loop.run_forever()
    loop.close()

#if __name__ == '__main__':
    # First connection
    #send_message("This is the first message")
    #send_message("This is the second message")

    # Second connection
    #loop = asyncio.new_event_loop()
    #text = "My second text"
    #loop.run_until_complete(connect_to_server(text))

    #loop.run_forever()
    #loop.close()