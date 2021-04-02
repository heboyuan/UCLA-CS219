
__all__ = ["mi_enb_decoder"]

import binascii
# from .dm_collector.dm_endec.ws_dissector import WSDissector

PACKET_TYPE = {
  "0xB0A3": "LTE_PDCP_DL_Cipher_Data_PDU",
  "0xB0B3": "LTE_PDCP_UL_Cipher_Data_PDU",
  "0xB173": "LTE_PHY_PDSCH_Stat_Indication",
  "0xB063": "LTE_MAC_DL_Transport_Block",
  "0xB064": "LTE_MAC_UL_Transport_Block",
  "0xB092": "LTE_RLC_UL_AM_All_PDU",
  "0xB082": "LTE_RLC_DL_AM_All_PDU",
  "0xB13C": "LTE_PHY_PUCCH_SR",
  "0xB0C0": "LTE_RRC_MESSAGE",
}

FUNCTION_NAME = {
  "0xB0A3": "handle_pdcp_dl",
  "0xB0B3": "handle_pdcp_ul",
  "0xB173": "handle_pdsch_stat", 
  "0xB063": "handle_mac_dl",
  "0xB064": "handle_mac_ul",
  "0xB092": "handle_rlc_ul",
  "0xB082": "handle_rlc_dl",
  "0xB13C": "handle_pucch_sr",
  "0xB0C0": "handle_rrc_message",
}


class mi_enb_decoder:
  def __init__(self, packet):
    self.packet = packet 
    self.p_type_name = None
    self.p_type = None
    self.content = None


  def get_type_id(self):
    # print (type(self.packet))
    try:
      l = self.packet.split(" ")
      # print (l)
      if (l[1] in PACKET_TYPE):
        self.p_type = l[1]
        self.p_type_name = PACKET_TYPE[l[1]]
      return self.p_type_name
    except:
      return None

  def get_content(self):
    if self.p_type is None:
      return -1
    else:
      method_to_call = getattr(self, FUNCTION_NAME[self.p_type])
      return method_to_call()
  
  def get_counter(self):
    return self.counter

  def handle_pdsch_stat(self):
    # PDSCH format: [MI] ID FN SFN nRB
    try:
      if self.content is None:
        d = {}
        packet = self.packet
        if packet[-1] == '\n':
            packet = packet[0:-1]
        l = packet.split(" ")

        d['Records'] = []
        dict_tmp = {}
        dict_tmp['Frame Num'] = int(l[2])
        dict_tmp['Subframe Num'] =  int(l[3])
        dict_tmp['Num RBs'] =  int(l[4])
        d['Records'].append(dict_tmp)
        self.content = d
    finally:
      return self.content

  def handle_pdcp_dl(self):
    # PDCP DL format: [MI] 0xB0A3 FN SFN SN Size
    try:
      if self.content is None:
        d = {}
        packet = self.packet
        if packet[-1] == '\n':
            packet = packet[0:-1]
        l = packet.split(" ")

        d['Subpackets'] = []
        dict_tmp = {}
        dict_tmp['Sys FN'] = int(l[2])
        dict_tmp['Sub FN'] = int(l[3])
        dict_tmp['SN'] = int(l[4])
        dict_tmp['PDU Size'] =  int(l[5])
        d['Subpackets'].append(dict_tmp)
        self.content = d  
    finally:
      return self.content


  def handle_pdcp_ul(self):
    # PDCP UL format: [MI] 0xB0B3 FN SFN SN Size RLC_Mode
    try:
      if self.content is None:
        d = {}
        packet = self.packet
        if packet[-1] == '\n':
            packet = packet[0:-1]
        l = packet.split(" ")

        d['Subpackets'] = []
        dict_tmp = {}
        dict_tmp['Sys FN'] = int(l[2])
        dict_tmp['Sub FN'] = int(l[3])
        dict_tmp['SN'] = int(l[4])
        dict_tmp['PDU Size'] =  int(l[5])
        d['Subpackets'].append(dict_tmp)
        self.content = d  
    finally:
      return self.content

  def handle_mac_ul(self):
    # MAC UL format: [MI] ID FN SFN Grant
    try: 
      if self.content is None:
        d = {}
        packet = self.packet
        if packet[-1] == '\n':
            packet = packet[0:-1]
        l = packet.split(" ")

        d['Subpackets'] = []
        dict_tmp = {}
        dict_tmp['Samples'] = []
        dict_tmp2 = {}
        dict_tmp2['SFN'] = int(l[2])
        dict_tmp2['Sub FN'] = int(l[3])
        dict_tmp2['Grant (bytes)'] =  int(l[4])
        dict_tmp['Samples'].append(dict_tmp2)
        d['Subpackets'].append(dict_tmp)
        self.content = d
    finally:  
      return self.content

  def handle_rlc_ul(self):
    # Format: [MI] 0xB092 SFN [MI] 0xB092 TYPE(1=data) FN SFN BEARER SIZE HDR_SIZE DATA_SIZE
    try:
      if self.content is None:
        packet = self.packet
        if packet[-1] == '\n':
            packet = packet[0:-1]
        l = packet.split(" ")

        if l[5] == "0":
          return None

        d = {}
        d['Subpackets'] = []
        sub_dict = {}
        record_dict = {}
        record_dict['sys_fn'] = int(l[6])
        record_dict['sub_fn'] = int(l[2])
        record_dict['pdu_bytes'] = int(l[9])
        sub_dict['RLCUL PDUs'] = [record_dict]

        d['Subpackets'].append(sub_dict)
        self.content = d
    finally:
      return self.content

  def handle_rlc_dl(self):
    pass

  def handle_pucch_sr(self):
    try:
      if self.content is None:
        d = {}
        packet = self.packet
        if packet[-1] == '\n':
            packet = packet[0:-1]
        l = packet.split(" ")

        d['Records'] = []
        record_dict = {}
        record_dict['Frame Num'] = int(l[3])
        record_dict['Subframe Num'] = int(l[5])
        d['Records'].append(record_dict)
        self.content = d
    finally:
      return self.content

  def handle_rrc_message(self):
    # RRC Message format: [MI] 0xB0C0 Message_Type Message_Content (... TODO)
    try:
      if self.content is None:
        d = {}
        packet = self.packet
        if packet[-1] == '\n':
            packet = packet[0:-1]
        l = packet.split(" ")
        d['Records'] = []
        record_dict = {}
        record_dict['Message Type'] = l[3]
        record_dict['Message Content'] = self.__decode_rrc_message(l[3], l[5])
        # TODO: can add more attributes for the packet

        d['Records'].append(record_dict)
        self.content = d
    finally:
      return self.content

  # def __decode_rrc_message(self, msg_type, msg_byte):
  #   """
  #   Decode rrc message byte as readable string
  #   :param msg_type: rrc message type
  #   :param msg_byte: rrc message byte in hex format
  #   :return: decoded message string
  #   """
  #   executable_path = None
  #   WSDissector.init_proc(executable_path, "/usr/local/lib")

  #   msg_byte = msg_byte.replace(".", "")
  #   decoded_msg = WSDissector.decode_msg(msg_type, binascii.a2b_hex(msg_byte))


  #   return decoded_msg
