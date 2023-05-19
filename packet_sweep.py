from scapy.all import *
from scapy.utils import PcapWriter
from collections import defaultdict
import atexit

# Define pcap writers for each protocol
pcap_writers = defaultdict(lambda: PcapWriter("other.pcap", append=True))

# List of protocols to capture
protocols = [TCP, UDP, ICMP, ARP, IP, Ether]

def manage_packet(packet):
    # Check scapy protocols
    for protocol in protocols:
        if packet.haslayer(protocol):
            pcap_writers[protocol.__name__].write(packet)
            return

    # Check for specific conditions for high-level protocols
    if TCP in packet:
        if packet[TCP].dport == 80 or packet[TCP].sport == 80:
            pcap_writers['HTTP'].write(packet)
            return
        elif packet[TCP].dport == 443 or packet[TCP].sport == 443:
            pcap_writers['HTTPS'].write(packet)
            return
        elif packet[TCP].dport == 22 or packet[TCP].sport == 22:
            pcap_writers['SSH'].write(packet)
            return

    if UDP in packet:
        if packet[UDP].dport == 53 or packet[UDP].sport == 53:
            pcap_writers['DNS'].write(packet)
            return

    # If packet does not match any defined protocol, write to 'other.pcap'
    pcap_writers['other'].write(packet)

def cleanup():
    global pcap_writers
    for writer in pcap_writers.values():
        writer.close()

def main():
    global pcap_writers
    # Creating pcap writers for specific protocols
    for protocol in protocols:
        pcap_writers[protocol.__name__] = PcapWriter(f"{protocol.__name__}.pcap", append=True)

    # Create pcap writers for high-level protocols
    for protocol in ['HTTP', 'HTTPS', 'SSH', 'DNS']:
        pcap_writers[protocol] = PcapWriter(f"{protocol}.pcap", append=True)

    atexit.register(cleanup)
    
    print("Started packet capture - Ctrl+C to stop")
    # Start sniffing and call manage_packet for each packet
    try:
        sniff(prn=manage_packet)
    except KeyboardInterrupt:
        cleanup()

if __name__ == '__main__':
    main()
