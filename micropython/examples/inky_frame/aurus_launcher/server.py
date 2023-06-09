import inky_helper_custom as helper
from tinyweb.server import webserver
from machine import reset
import gc
import os
import ubinascii

SKIP_DRAW = True

app = webserver()

@app.route('/')
async def index(request, response):
    # Start HTTP response with content-type text/html
    await response.start_html()
    # Send actual HTML page
    await response.send_file('inky.html')
    
@app.route('/reset')
async def boot(request, response):
    # Start HTTP response with content-type text/html
    await response.start_html()
    # Send actual HTML page
    await response.send('<html><body><h1>Rebooting into menu!</h1></body></html>\n')
    helper.update_state("menu")
    reset()
    
@app.route('/savecamera', methods=['POST'], save_headers = ['Content-Length','Content-Type'], max_body_size = 160000)
async def savecamera(request, response):
    print('/savecamera called')
    gc.collect()
    
    if helper.file_exists("img/camera.jpg"):
        os.remove("img/camera.jpg")
        
    content = await request.read_parse_form_data()
    with open("img/camera.jpg", "wb") as f:
        f.write(ubinascii.a2b_base64(content['image']))
        
    await response.start_html()
    await response.send('<html><body>ok</body></html>\n')
    
    print('/savecamera finished')
    
@app.route('/savecamerabadge', methods=['POST'], save_headers = ['Content-Length','Content-Type'], max_body_size = 160000)
async def savecamerabadge(request, response):
    print('/savecamera called')
    gc.collect()
    
    if helper.file_exists("img/camerabadge.jpg"):
        os.remove("img/camerabadge.jpg")
        
    content = await request.read_parse_form_data()
    with open("img/camerabadge.jpg", "wb") as f:
        f.write(ubinascii.a2b_base64(content['image']))
        
    await response.start_html()
    await response.send('<html><body>ok</body></html>\n')
    
    print('/savecamera finished')
    
   
@app.route('/save', methods=['POST'], save_headers = ['Content-Length','Content-Type'])
async def save(request, response):
    print('/save called')
    
    content = await request.read_parse_form_data()
    helper.update_state(content["state"])
    if(content["state"] == 'badge'):
        helper.save_json('/badge_state.json', content["config"])
    
    elif(content["state"] == 'image_gallery'):
        helper.save_json('/image_gallery_state.json', content["config"])
    
    elif(content["state"] == 'passport'):
        pass
    
    await response.start_html()
    await response.send('<html><body>ok</body></html>\n')
    
    reset()
    
    

# Run the web server as the sole process
def update():
    helper.access_point_start()
    app.run(host="0.0.0.0", port=80)

def draw():
    pass