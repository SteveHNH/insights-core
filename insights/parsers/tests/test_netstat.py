from insights.parsers.netstat import Netstat, NetstatAGN, NetstatS, Netstat_I, SsTULPN
from insights.tests import context_wrap
from insights.parsers import netstat
from ...parsers import ParseException

import pytest

NETSTAT_S = '''
Ip:
    3405107 total packets received
    0 forwarded
    0 incoming packets discarded
    2900146 incoming packets delivered
    2886201 requests sent out
    456 outgoing packets dropped
    4 fragments received ok
    8 fragments created
Icmp:
    114 ICMP messages received
    0 input ICMP message failed.
    ICMP input histogram:
        destination unreachable: 107
        echo requests: 4
        echo replies: 3
    261 ICMP messages sent
    0 ICMP messages failed
    ICMP output histogram:
        destination unreachable: 254
        echo request: 3
        echo replies: 4
IcmpMsg:
        InType0: 3
        InType3: 107
        InType8: 4
        OutType0: 4
        OutType3: 254
        OutType8: 3
Tcp:
    1648 active connections openings
    1525 passive connection openings
    105 failed connection attempts
    69 connection resets received
    139 connections established
    2886370 segments received
    2890303 segments send out
    428 segments retransmited
    0 bad segments received.
    212 resets sent
Udp:
    4901 packets received
    107 packets to unknown port received.
    0 packet receive errors
    1793 packets sent
    0 receive buffer errors
    0 send buffer errors
UdpLite:
TcpExt:
    1239 TCP sockets finished time wait in fast timer
    295934 delayed acks sent
    6 delayed acks further delayed because of locked socket
    Quick ack mode was activated 9 times
    999263 packets directly queued to recvmsg prequeue.
    8266 bytes directly in process context from backlog
    104052505 bytes directly received in process context from prequeue
    122927 packet headers predicted
    339500 packets header predicted and directly queued to user
    253351 acknowledgments not containing data payload received
    711851 predicted acknowledgments
    1 times recovered from packet loss by selective acknowledgements
    1 congestion windows recovered without slow start after partial ack
    3 fast retransmits
    54 other TCP timeouts
    TCPLossProbes: 12
    TCPLossProbeRecovery: 12
    9 DSACKs sent for old packets
    13 DSACKs received
    72 connections reset due to unexpected data
    4 connections reset due to early user close
    53 connections aborted due to timeout
    TCPDSACKIgnoredNoUndo: 13
    TCPSpuriousRTOs: 1
    TCPSackShiftFallback: 6
    TCPDeferAcceptDrop: 537
    IPReversePathFilter: 1
    TCPRcvCoalesce: 2610
    TCPOFOQueue: 595
    TCPChallengeACK: 3
    TCPSpuriousRtxHostQueues: 3
IpExt:
    InNoRoutes: 9
    InMcastPkts: 406
    InBcastPkts: 517437
    InOctets: 865450302
    OutOctets: 812810111
    InMcastOctets: 12992
    InBcastOctets: 46402081
'''.strip()

NETSTAT_S_FAIL = "cannot open /proc/net/snmp: No such file or directory"

NETSTAT_S_W = '''
error parsing /proc/net/netstat: No such file or directory
Ip:
    6440 total packets received
    3 with invalid addresses
    0 forwarded
    0 incoming packets discarded
    6437 incoming packets delivered
    4777 requests sent out
    three hundred and eighty eight packets glanced at
'''


class TestNetstats():
    def test_netstat_s(self):
        info = NetstatS(context_wrap(NETSTAT_S)).data

        assert info['ip'] == {'total_packets_received': '3405107',
                              'forwarded': '0',
                              'incoming_packets_discarded': '0',
                              'incoming_packets_delivered': '2900146',
                              'requests_sent_out': '2886201',
                              'outgoing_packets_dropped': '456',
                              'fragments_received_ok': '4',
                              'fragments_created': '8'}
        assert info['icmp'] == {'icmp_messages_received': '114',
                                'input_icmp_message_failed': '0',
                                'icmp_input_histogram': {
                                    'destination_unreachable': '107',
                                    'echo_requests': '4',
                                    'echo_replies': '3',
                                },
                                'icmp_messages_sent': '261',
                                'icmp_messages_failed': '0',
                                'icmp_output_histogram': {
                                    'destination_unreachable': '254',
                                    'echo_request': '3',
                                    'echo_replies': '4'
                                }
                                }
        assert info['icmpmsg'] == {'intype0': '3',
                                   'intype3': '107',
                                   'intype8': '4',
                                   'outtype0': '4',
                                   'outtype3': '254',
                                   'outtype8': '3'}
        assert info['tcp'] == {'active_connections_openings': '1648',
                               'passive_connection_openings': '1525',
                               'failed_connection_attempts': '105',
                               'connection_resets_received': '69',
                               'connections_established': '139',
                               'segments_received': '2886370',
                               'segments_send_out': '2890303',
                               'segments_retransmited': '428',
                               'bad_segments_received': '0',
                               'resets_sent': '212'}
        assert info['udp'] == {'packets_received': '4901',
                               'packets_to_unknown_port_received': '107',
                               'packet_receive_errors': '0',
                               'packets_sent': '1793',
                               'receive_buffer_errors': '0',
                               'send_buffer_errors': '0'}
        assert info['udplite'] == {}
        assert info['tcpext'] == {'tcp_sockets_finished_time_wait_in_fast_timer': '1239',
                                  'delayed_acks_sent': '295934',
                                  'delayed_acks_further_delayed_because_of_locked_socket': '6',
                                  'quick_ack_mode_was_activated_times': '9',
                                  'packets_directly_queued_to_recvmsg_prequeue': '999263',
                                  'bytes_directly_in_process_context_from_backlog': '8266',
                                  'bytes_directly_received_in_process_context_from_prequeue': '104052505',
                                  'packet_headers_predicted': '122927',
                                  'packets_header_predicted_and_directly_queued_to_user': '339500',
                                  'acknowledgments_not_containing_data_payload_received': '253351',
                                  'predicted_acknowledgments': '711851',
                                  'times_recovered_from_packet_loss_by_selective_acknowledgements': '1',
                                  'congestion_windows_recovered_without_slow_start_after_partial_ack': '1',
                                  'fast_retransmits': '3',
                                  'other_tcp_timeouts': '54',
                                  'tcplossprobes': '12',
                                  'tcplossproberecovery': '12',
                                  'dsacks_sent_for_old_packets': '9',
                                  'dsacks_received': '13',
                                  'connections_reset_due_to_unexpected_data': '72',
                                  'connections_reset_due_to_early_user_close': '4',
                                  'connections_aborted_due_to_timeout': '53',
                                  'tcpdsackignorednoundo': '13',
                                  'tcpspuriousrtos': '1',
                                  'tcpsackshiftfallback': '6',
                                  'tcpdeferacceptdrop': '537',
                                  'ipreversepathfilter': '1',
                                  'tcprcvcoalesce': '2610',
                                  'tcpofoqueue': '595',
                                  'tcpchallengeack': '3',
                                  'tcpspuriousrtxhostqueues': '3'}
        assert info['ipext'] == {'innoroutes': '9',
                                 'inmcastpkts': '406',
                                 'inbcastpkts': '517437',
                                 'inoctets': '865450302',
                                 'outoctets': '812810111',
                                 'inmcastoctets': '12992',
                                 'inbcastoctets': '46402081'}

    def test_netstat_s_fail(self):
        with pytest.raises(ParseException):
            NetstatS(context_wrap(NETSTAT_S_FAIL))

    def test_netstat_s_w(self):
        info = NetstatS(context_wrap(NETSTAT_S_W)).data

        assert len(info) == 1
        assert info['ip'] == {'total_packets_received': "6440",
                              "with_invalid_addresses": "3",
                              "forwarded": "0",
                              "incoming_packets_discarded": "0",
                              "incoming_packets_delivered": "6437",
                              "requests_sent_out": "4777"}


TEST_NETSTAT_AGN = """
IPv6/IPv4 Group Memberships
Interface       RefCnt Group
--------------- ------ ---------------------
lo              1      224.0.0.1
eth0            1      224.0.0.1
lo              3      ff02::1
eth0            4      ff02::1
eth0            1      ff01::1

"""


def test_get_netstat_agn():
    result = NetstatAGN(context_wrap(TEST_NETSTAT_AGN)).group_by_iface()
    assert len(result) == 2
    assert len(result["lo"]) == 2
    assert len(result["eth0"]) == 3
    assert result["lo"] == [
        {"refcnt": "1", "group": "224.0.0.1"},
        {"refcnt": "3", "group": "ff02::1"}]
    assert result["eth0"] == [
        {"refcnt": "1", "group": "224.0.0.1"},
        {"refcnt": "4", "group": "ff02::1"},
        {"refcnt": "1", "group": "ff01::1"}]


NETSTAT = """
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      PID/Program name     Timer
tcp        0      0 192.168.0.1:53          192.168.0.53:53         ESTABLISHED 0          1817       12/dnsd              off (0.00/0/0)
tcp        0      0 0.0.0.0:5672            0.0.0.0:*               LISTEN      996        19422      1279/qpidd           off (0.00/0/0)
tcp        0      0 127.0.0.1:27017         0.0.0.0:*               LISTEN      184        20380      2007/mongod          off (0.00/0/0)
tcp        0      0 127.0.0.1:53644         0.0.0.0:*               LISTEN      995        1154674    12387/Passenger Rac  off (0.00/0/0)
tcp        0      0 0.0.0.0:5646            0.0.0.0:*               LISTEN      991        20182      1272/qdrouterd       off (0.00/0/0)
tcp        0      0 10.24.1.245:80          10.24.36.145:32790      SYN_RECV    0          0          -                    on (0.79/0/0)
Active UNIX domain sockets (servers and established)
Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path
unix  2      [ ]         DGRAM                    11776    1/systemd            /run/systemd/shutdownd
unix  2      [ ACC ]     STREAM     LISTENING     535      1/systemd            /run/lvm/lvmetad.socket
unix  2      [ ACC ]     STREAM     LISTENING     16411    738/NetworkManager   /var/run/NetworkManager/private
"""


def test_get_netstat():
    ns = Netstat(context_wrap(NETSTAT))
    assert len(ns.data) == 2
    assert netstat.ACTIVE_INTERNET_CONNECTIONS in ns.data
    assert 'PID/Program name' in ns.data[netstat.ACTIVE_INTERNET_CONNECTIONS]
    assert 'Local Address' in ns.data[netstat.ACTIVE_INTERNET_CONNECTIONS]
    assert netstat.ACTIVE_UNIX_DOMAIN_SOCKETS in ns.data

    assert "1279/qpidd" in ns.data[netstat.ACTIVE_INTERNET_CONNECTIONS]['PID/Program name']
    assert "738/NetworkManager" in ns.data[netstat.ACTIVE_UNIX_DOMAIN_SOCKETS]['PID/Program name']

    # Datalist access
    assert hasattr(ns, 'datalist')
    nsdl = ns.datalist[netstat.ACTIVE_INTERNET_CONNECTIONS]
    assert len(nsdl) == 6
    assert nsdl[0] == {
        'Proto': 'tcp', 'Recv-Q': '0', 'Send-Q': '0',
        'Local Address': '192.168.0.1:53', 'Local IP': '192.168.0.1',
        'Port': '53', 'Foreign Address': '192.168.0.53:53',
        'State': 'ESTABLISHED', 'User': '0', 'Inode': '1817',
        'PID/Program name': '12/dnsd', 'PID': '12', 'Program name': 'dnsd',
        'Timer': 'off (0.00/0/0)',
    }
    # tcp        0      0 10.24.1.245:80          10.24.36.145:32790      SYN_RECV    0          0          -                    on (0.79/0/0)
    assert nsdl[5] == {
        'Proto': 'tcp', 'Recv-Q': '0', 'Send-Q': '0',
        'Local Address': '10.24.1.245:80', 'Local IP': '10.24.1.245',
        'Port': '80', 'Foreign Address': '10.24.36.145:32790',
        'State': 'SYN_RECV', 'User': '0', 'Inode': '0',
        'PID/Program name': '-',
        'Timer': 'on (0.79/0/0)',
    }

    # Search for rows by:
    results = ns.rows_by(netstat.ACTIVE_INTERNET_CONNECTIONS, {'State': 'ESTABLISHED'})
    assert results == [{
        'Proto': 'tcp', 'Recv-Q': '0', 'Send-Q': '0',
        'Local Address': '192.168.0.1:53', 'Local IP': '192.168.0.1',
        'Port': '53', 'Foreign Address': '192.168.0.53:53',
        'State': 'ESTABLISHED', 'User': '0', 'Inode': '1817',
        'PID/Program name': '12/dnsd', 'PID': '12', 'Program name': 'dnsd',
        'Timer': 'off (0.00/0/0)',
        'raw line': 'tcp        0      0 192.168.0.1:53          192.168.0.53:53         ESTABLISHED 0          1817       12/dnsd              off (0.00/0/0)'
    }]


def test_listening_pid():
    ns = Netstat(context_wrap(NETSTAT))
    assert len(ns.data) == 2
    assert ns.listening_pid['12387'] == {'addr': '127.0.0.1', 'name': 'Passenger Rac', 'port': '53644'}
    assert ns.listening_pid['1272'] == {'addr': '0.0.0.0', 'name': 'qdrouterd', 'port': '5646'}


def test_get_original_line():
    ns = Netstat(context_wrap(NETSTAT))
    assert len(ns.data) == 2
    assert NETSTAT.splitlines()[4].strip() == ns.get_original_line(netstat.ACTIVE_INTERNET_CONNECTIONS, 1)
    assert NETSTAT.splitlines()[5].strip() == ns.get_original_line(netstat.ACTIVE_INTERNET_CONNECTIONS, 2)
    assert ns.get_original_line("Fabulous Green", 1) is None
    assert NETSTAT.splitlines()[11].strip() == ns.get_original_line(netstat.ACTIVE_UNIX_DOMAIN_SOCKETS, 0)


NETSTAT_NOMATCH1 = """
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      PID/Program name     Timer
tcp        0      0 ::ffff:127.0.0.1:7403   :::*                    LISTEN      500        19075      2647/java            off (0.00/0/0)
tcp        0      0 :::5227                 :::*                    LISTEN      0          15758      2416/perfd           off (0.00/0/0)
tcp        0      0 :::7788                 :::*                    LISTEN      500        97305      7661/httpd.worker    off (0.00/0/0)
"""

NETSTAT_NOMATCH2 = """
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      PID/Program name     Timer
tcp        0      0 ::1:5432                :::*                    LISTEN      26         14071      1474/postmaster      off (0.00/0/0)
tcp        0      0 ::1:25                  :::*                    LISTEN      0          12554      1569/master          off (0.00/0/0)
tcp        0      0 :::8443                 :::*                    LISTEN      91         14065      1641/java            off (0.00/0/0)
"""

NETSTAT_MATCH1 = """
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      PID/Program name     Timer
tcp        0      0 0.0.0.0:7788            0.0.0.0:*               LISTEN      0          97305      7661/httpd.worker    off (0.00/0/0)
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      0          9154       3544/portmap         off (0.00/0/0)
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      0          11821      4009/httpd           off (0.00/0/0)
"""


def test_is_httpd_running():
    assert "httpd" in Netstat(context_wrap(NETSTAT_MATCH1)).running_processes
    assert "httpd" not in Netstat(context_wrap(NETSTAT_NOMATCH1)).running_processes
    assert "httpd" not in Netstat(context_wrap(NETSTAT_NOMATCH2)).running_processes


NETSTAT_BLANK = ''

NETSTAT_TRUNCATED = """
error parsing /proc/net/netstat: No such file or directory
"""

NETSTAT_CONTENT_BUT_NO_PARSED_LINES = """
tcp        0      0 0.0.0.0:7788            0.0.0.0:*               LISTEN      0          97305      7661/httpd.worker    off (0.00/0/0)
tcp        0      0 ::1:5432                :::*                    LISTEN      26         14071      1474/postmaster      off (0.00/0/0)
tcp        0      0 ::1:25                  :::*                    LISTEN      0          12554      1569/master          off (0.00/0/0)
tcp        0      0 :::8443                 :::*                    LISTEN      91         14065      1641/java            off (0.00/0/0)
"""

NETSTAT_CONTENT_BUT_NO_PID_PROGRAM = """
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      Timer
tcp        0      0 0.0.0.0:7788            0.0.0.0:*               LISTEN      0          97305      off (0.00/0/0)
tcp        0      0 ::1:5432                :::*                    LISTEN      26         14071      off (0.00/0/0)
tcp        0      0 ::1:25                  :::*                    LISTEN      0          12554      off (0.00/0/0)
tcp        0      0 :::8443                 :::*                    LISTEN      91         14065      off (0.00/0/0)
"""

NETSTAT_CONTENT_BUT_NO_LOCAL_ADDR_COLON = """
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address     Port  Foreign Address   Port  State       User       Inode      PID/Program name     Timer
tcp        0      0 0.0.0.0           7788  0.0.0.0           *     LISTEN      0          97305      7661/httpd.worker    off (0.00/0/0)
tcp        0      0 ::1               5432  ::                *     LISTEN      26         14071      1474/postmaster      off (0.00/0/0)
"""

NETSTAT_SOCKETS_ONLY = """
Active UNIX domain sockets (servers and established)
Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path
unix  2      [ ]         DGRAM                    11776    1/systemd            /run/systemd/shutdownd
unix  2      [ ACC ]     STREAM     LISTENING     535      1/systemd            /run/lvm/lvmetad.socket
unix  2      [ ACC ]     STREAM     LISTENING     16411    738/NetworkManager   /var/run/NetworkManager/private
"""


def test_short_outputs():
    with pytest.raises(ParseException) as exc:
        Netstat(context_wrap(NETSTAT_BLANK))
    assert 'Input content is empty' in str(exc)

    with pytest.raises(ParseException) as exc:
        Netstat(context_wrap(NETSTAT_TRUNCATED))
    assert 'Input content is not empty but there is no useful parsed data' in str(exc)

    with pytest.raises(ParseException) as exc:
        Netstat(context_wrap(NETSTAT_CONTENT_BUT_NO_PARSED_LINES))
    assert 'Found no section headers in content' in str(exc)

    with pytest.raises(ParseException) as exc:
        Netstat(context_wrap(NETSTAT_CONTENT_BUT_NO_PID_PROGRAM))
    assert "Did not find 'PID/Program name' heading in header" in str(exc)

    with pytest.raises(ParseException) as exc:
        Netstat(context_wrap(NETSTAT_CONTENT_BUT_NO_LOCAL_ADDR_COLON))
    assert "Local Address is expected to have a colon separating address and port" in str(exc)

    ns = Netstat(context_wrap(NETSTAT_SOCKETS_ONLY))
    assert ns.running_processes == set()
    assert ns.listening_pid == {}


NETSTAT_TEST_RUNNING_PROCESSES = """
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      PID/Program name     Timer
tcp        0      0 192.168.0.1:53          192.168.0.53:53         ESTABLISHED 0          1817       12/dnsd              off (0.00/0/0)
tcp        0      0 ::1:5432                :::*                    LISTEN      26         14071                           off (0.00/0/0)
tcp        0      0 0.0.0.0:5672            0.0.0.0:*               LISTEN      996        19422      1279                 off (0.00/0/0)
tcp        0      0 127.0.0.1:27017         0.0.0.0:*               LISTEN      184        20380      mongod               off (0.00/0/0)
tcp        0      0 127.0.0.1:53644         0.0.0.0:*               LISTEN      995        1154674    12387/Passenger Rac  off (0.00/0/0)
tcp        0      0 0.0.0.0:5646            0.0.0.0:*               LISTEN      991        20182      1272/qdrouterd       off (0.00/0/0)
"""


def test_running_processes():
    ns = Netstat(context_wrap(NETSTAT_TEST_RUNNING_PROCESSES))
    assert len(ns.data) == 1
    assert netstat.ACTIVE_INTERNET_CONNECTIONS in ns.data
    assert 'PID/Program name' in ns.data[netstat.ACTIVE_INTERNET_CONNECTIONS]
    assert 'Local Address' in ns.data[netstat.ACTIVE_INTERNET_CONNECTIONS]
    assert len(ns.data[netstat.ACTIVE_INTERNET_CONNECTIONS]['Local Address']) == 6
    assert 'dnsd' in ns.running_processes  # ESTABLISHED processes are OK
    assert '1279' not in ns.running_processes
    assert 'mongod' not in ns.running_processes
    assert 'Passenger Rac' in ns.running_processes
    assert 'qdrouterd' in ns.running_processes

    pids = ns.listening_pid
    assert sorted(pids.keys()) == sorted(['12387', '1272'])


NETSTAT_I = """
Kernel Interface table
Iface       MTU Met    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
bond0      1500   0   845265      0      0      0     1753      0      0      0 BMmRU
bond1      1500   0   842447      0      0      0     4233      0      0      0 BMmRU
eth0       1500   0   422518      0      0      0     1703      0      0      0 BMsRU
eth1       1500   0   422747      0      0      0       50      0      0      0 BMsRU
eth2       1500   0   421192      0      0      0     3674      0      0      0 BMsRU
eth3       1500   0   421255      0      0      0      559      0      0      0 BMsRU
lo        65536   0        0      0      0      0        0      0      0      0 LRU
"""


def test_get_netstat_i():
    result = Netstat_I(context_wrap(NETSTAT_I)).group_by_iface
    assert len(result) == 7
    assert result["bond0"] == {
            "MTU": "1500", "Met": "0", "RX-OK": "845265", "RX-ERR": "0",
            "RX-DRP": "0", "RX-OVR": "0", "TX-OK": "1753", "TX-ERR": "0",
            "TX-DRP": "0", "TX-OVR": "0", "Flg": "BMmRU"
                }
    assert result["eth0"] == {
            "MTU": "1500", "Met": "0", "RX-OK": "422518", "RX-ERR": "0",
            "RX-DRP": "0", "RX-OVR": "0", "TX-OK": "1703", "TX-ERR": "0",
            "TX-DRP": "0", "TX-OVR": "0", "Flg": "BMsRU"
                }


Ss_TULPN = """
Netid  State      Recv-Q Send-Q Local Address:Port               Peer Address:Port
udp    UNCONN     0      0         *:55898                 *:*
udp    UNCONN     0      0      127.0.0.1:904                   *:*                   users:(("rpc.statd",pid=29559,fd=7))
udp    UNCONN     0      0         *:111                   *:*                   users:(("rpcbind",pid=953,fd=9))
udp    UNCONN     0      0        :::37968                :::12345                    users:(("rpc.statd",pid=29559,fd=10))
udp    UNCONN     0      0        :::57315                :::*
udp    UNCONN     0      0        :::111                  :::*                   users:(("rpcbind",pid=953,fd=11))
tcp    LISTEN     0      1      10.72.32.206:5900                  *:*                   users:(("qemu-kvm",pid=9787,fd=20))
tcp    LISTEN     0      5         *:54322                 *:*                   users:(("ovirt-imageio-d",pid=929,fd=3))
tcp    LISTEN     0      100    127.0.0.1:25                    *:*                   users:(("master",pid=2612,fd=13))
tcp    LISTEN     0      64        *:34850                 *:*
tcp    LISTEN     0      64        *:35752                 *:*
tcp    LISTEN     0      128      :::2223                 :::*                   users:(("sshd",pid=1416,fd=4))
"""


def test_ss_tulpn_data():
    ss = SsTULPN(context_wrap(Ss_TULPN)).data
    assert len(ss) == 12
    assert ss[0] == {'Netid': 'udp', 'Peer-Address-Port': '*:*', 'Send-Q': '0', 'Local-Address-Port': '*:55898', 'State': 'UNCONN', 'Recv-Q': '0'}
    assert ss[1].get("Netid") == "udp"
    assert ss[9].get("Process") is None
    assert "sshd" in ss[-1].get("Process")
    assert "904" in ss[1].get("Local-Address-Port")


def test_ss_tulpn_get_service():
    ss = SsTULPN(context_wrap(Ss_TULPN))
    exp = [{'Netid': 'udp', 'Process': 'users:(("rpcbind",pid=953,fd=9))', 'Peer-Address-Port': '*:*', 'Send-Q': '0', 'Local-Address-Port': '*:111', 'State': 'UNCONN', 'Recv-Q': '0'},
           {'Netid': 'udp', 'Process': 'users:(("rpcbind",pid=953,fd=11))', 'Peer-Address-Port': ':::*', 'Send-Q': '0', 'Local-Address-Port': ':::111', 'State': 'UNCONN', 'Recv-Q': '0'}]
    assert ss.get_service("rpcbind") == exp


def test_ss_tulpn_get_port():
    ss = SsTULPN(context_wrap(Ss_TULPN))
    exp01 = [{'Netid': 'tcp', 'Process': 'users:(("sshd",pid=1416,fd=4))', 'Peer-Address-Port': ':::*', 'Send-Q': '128', 'Local-Address-Port': ':::2223', 'State': 'LISTEN', 'Recv-Q': '0'}]
    assert ss.get_localport("2223") == exp01
    exp02 = [{'Netid': 'udp', 'Process': 'users:(("rpc.statd",pid=29559,fd=10))', 'Peer-Address-Port': ':::12345', 'Send-Q': '0', 'Local-Address-Port': ':::37968', 'State': 'UNCONN', 'Recv-Q': '0'}]
    assert ss.get_peerport("12345") == exp02
    assert ss.get_port("12345") == exp02