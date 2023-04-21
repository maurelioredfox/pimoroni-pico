import socket
import network
import WIFI_CONFIG
from network_manager import NetworkManager
from tinyweb.server import webserver
#TODO theres an AP in network_manager
ssid = "PicoW"
password = "123456789"

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password) 
ap.active(True)

while ap.active == False:
  pass

print("Access point active")
print(ap.ifconfig())

# Start up a tiny web server
app = webserver()

# Serve a simple Hello World! response when / is called
# and turn the LED on/off using toggle()
@app.route('/')
async def index(request, response):
    # Start HTTP response with content-type text/html
    await response.start_html()
    # Send actual HTML page
    await response.send('<html><body><h1>Hello, world!</h1></body></html>\n')

# Run the web server as the sole process
app.run(host="0.0.0.0", port=80)