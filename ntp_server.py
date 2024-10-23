# Server code (ntp_server.py)
from socketserver import ThreadingUDPServer, BaseRequestHandler
from datetime import datetime
import struct
import time

class NTPHandler(BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        
        try:
            # T2: Server receive time
            t2 = time.time() + 2208988800  # Convert to NTP era
            
            # Get T1 from client request if available
            t1 = 0
            if len(data) >= 48:
                t1_bytes = data[40:48]
                t1 = struct.unpack('!Q', t1_bytes)[0] / 2**32
            
            # T3: Server transmit time
            t3 = time.time() + 2208988800
            
            # Create response packet
            response = bytearray(48)
            
            # Set version number to 3 and mode to 4 (server)
            response[0] = 0x1C
            
            # Set stratum level
            response[1] = 1
            
            # Pack timestamps into response
            # Origin Timestamp (T1)
            struct.pack_into('!Q', response, 24, int(t1 * 2**32))
            # Receive Timestamp (T2)
            struct.pack_into('!Q', response, 32, int(t2 * 2**32))
            # Transmit Timestamp (T3)
            struct.pack_into('!Q', response, 40, int(t3 * 2**32))
            
            socket.sendto(response, self.client_address)
            print(f"\nTimestamps (NTP era):")
            print(f"T1 (Origin): {datetime.fromtimestamp(t1 - 2208988800)}")
            print(f"T2 (Receive): {datetime.fromtimestamp(t2 - 2208988800)}")
            print(f"T3 (Transmit): {datetime.fromtimestamp(t3 - 2208988800)}")
            
        except Exception as e:
            print(f"Error in handle: {e}")

if __name__ == "__main__":
    server_address = ("0.0.0.0", 8001)
    print(f"Starting NTP server on {server_address[0]}:{server_address[1]}")
    with ThreadingUDPServer(server_address, NTPHandler) as server:
        server.serve_forever()