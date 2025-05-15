import http.server 
import ssl

# Define the handler to use for the server (SimpleHTTPRequestHandler serves files from the current directory)
handler = http.server.SimpleHTTPRequestHandler

# Set up the server
server_address = ('0.0.0.0', 8002)  # Use port 8002 (or any other available port)
httpd = http.server.HTTPServer(server_address, handler)

# Create SSL Context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# Wrap the socket with SSL
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Serving on https://0.0.0.0:8002")
httpd.serve_forever()
