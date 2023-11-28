#questo codice lancia un attacco UDP generico contro il mio switch
import socket
import subprocess


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
def attack_udp(target_ip):
    if not is_host_reachable(target_ip):
        raise ValueError("L'host non è raggiungibile.")
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        sock.sendto(b"",(target_ip,80))

#if __name__=="__main__":
    #target_ip="127.0.0.1"
    #attack(target_ip)
