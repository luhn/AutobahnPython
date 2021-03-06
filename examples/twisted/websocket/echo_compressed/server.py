###############################################################################
##
##  Copyright (C) 2011-2013 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory, \
                                       listenWS

from autobahn.websocket.compress import PerMessageDeflateOffer, \
                                        PerMessageDeflateOfferAccept


class EchoServerProtocol(WebSocketServerProtocol):

   def onConnect(self, request):
      print("WebSocket connection request by {}".format(request.peer))

   def onOpen(self):
      print("WebSocket extensions in use: {}".format(self.websocket_extensions_in_use))

   def onMessage(self, payload, isBinary):
      self.sendMessage(payload, isBinary)


if __name__ == '__main__':

   if len(sys.argv) > 1 and sys.argv[1] == 'debug':
      log.startLogging(sys.stdout)
      debug = True
   else:
      debug = False

   factory = WebSocketServerFactory("ws://localhost:9000",
                                    debug = debug,
                                    debugCodePaths = debug)

   factory.protocol = EchoServerProtocol


   ## Enable WebSocket extension "permessage-deflate".
   ##

   ## Function to accept offers from the client ..
   def accept(offers):
      for offer in offers:
         if isinstance(offer, PerMessageDeflateOffer):
            return PerMessageDeflateOfferAccept(offer)

   factory.setProtocolOptions(perMessageCompressionAccept = accept)


   ## run server
   ##
   listenWS(factory)

   webdir = File(".")
   web = Site(webdir)
   reactor.listenTCP(8080, web)

   reactor.run()
