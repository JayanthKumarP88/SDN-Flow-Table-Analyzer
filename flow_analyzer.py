from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.recoco import Timer

log = core.getLogger()

class FlowAnalyzer (object):
    def __init__ (self, connection):
        self.connection = connection
        connection.addListeners(self)
        self.mac_to_port = {}
        # Project 8: Poll switch for stats every 10s
        Timer(10, self._request_stats, recurring=True)

    def _request_stats (self):
        # Send OpenFlow stats request to switch
        stats_req = of.ofp_stats_request(body=of.ofp_flow_stats_request())
        self.connection.send(stats_req)

    def _handle_FlowStatsReceived (self, event):
        # Process received stats; distinguish ACTIVE vs UNUSED via packet_count
        stats = event.stats
        print("\n--- [Analyzer] Flow Table for Switch s{} ---".format(event.connection.dpid))
        
        if not stats:
            print("Status: EMPTY | No flows installed.")
            return

        for f in stats:
            status = "ACTIVE" if f.packet_count > 0 else "UNUSED"
            print("Status: {} | Priority: {} | Packets: {} | Bytes: {}".format(
                status, f.priority, f.packet_count, f.byte_count))

    def _handle_PacketIn (self, event):
        # Learning switch logic with 30s idle_timeout for dynamic cleanup
        packet = event.parsed
        if not packet.parsed or packet.type in [packet.LLDP_TYPE, packet.IPV6_TYPE]:
            return

        self.mac_to_port[packet.src] = event.port

        if packet.dst in self.mac_to_port:
            out_port = self.mac_to_port[packet.dst]
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet, event.port)
            msg.idle_timeout = 30 # Rules expire after 30s of inactivity
            msg.actions.append(of.ofp_action_output(port = out_port))
            msg.data = event.ofp
            self.connection.send(msg)
        else:
            # Flood if destination is unknown
            msg = of.ofp_packet_out()
            msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            msg.data = event.ofp
            msg.in_port = event.port
            self.connection.send(msg)

def launch ():
    def start_switch (event):
        log.info("Analyzer attached to Switch s%s" % (event.connection.dpid,))
        FlowAnalyzer(event.connection)
    
    core.openflow.addListenerByName("ConnectionUp", start_switch)
    log.info("Flow Analyzer running. Waiting for switches...")
