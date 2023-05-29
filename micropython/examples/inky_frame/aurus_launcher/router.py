from tinyweb.server import webserver

SKIP_DRAW = True

app = webserver()

@app.route('/')
async def index(request, response):
    # Start HTTP response with content-type text/html
    await response.start_html()
    # Send actual HTML page
    await response.send_file('inky.html')
    
@app.route('/savecamera', methods=['POST'], save_headers = ['Content-Length','Content-Type'])
async def savecamera(request, response):
    
    pass
   
@app.route('/save', methods=['POST'], save_headers = ['Content-Length','Content-Type'])
async def save(request, response):
    
    content = await request.read_parse_form_data()
    print(content)

# Run the web server as the sole process
def update():
    app.run(host="0.0.0.0", port=8080)

def draw():
    pass