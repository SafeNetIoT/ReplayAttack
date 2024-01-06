import sys
import pyshark
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score
from sklearn.svm import OneClassSVM
import collections
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import HashingVectorizer, CountVectorizer, TfidfTransformer
from sklearn.neighbors import LocalOutlierFactor
import pickle

from CustomClassifier import CustomClassifier

capture_path = str(sys.argv[1])
model_path = str(sys.argv[2])
mac_app = str(sys.argv[3])
mac_device = str(sys.argv[4])

import nltk

nltk.download('punkt')

capture = pyshark.FileCapture(capture_path)


def tokenizeText(sample):
    return list(set(word_tokenize(sample)))


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

payload_set = []
max_features = 0

############################################################################################################################
def training():
    global max_features
    #aggrega risposte dei flussi tcp (if any)
    for f in list_flows:
        if f.transport_layer == 'TCP':
            aggregated_response=""
            for r in f.list_responses:
                aggregated_response=aggregated_response+r
            payload = bytes.fromhex(aggregated_response).decode('ISO-8859-1')
            payload = payload.replace("/", "").replace("+", "")
            payload_set.append(payload)
            l = len(tokenizeText(payload))
            if l > max_features:
                max_features = l
        else:
            for r in f.list_responses:
                payload = bytes.fromhex(r).decode('ISO-8859-1')
                payload = payload.replace("/", "").replace("+", "")
                payload_set.append(payload)
                l = len(tokenizeText(payload))
                if l > max_features:
                    max_features = l


    vectorizer = HashingVectorizer(n_features=max_features, tokenizer=tokenizeText)
    training_Set = vectorizer.fit_transform(payload_set).toarray()

    real_labels = [1 for _ in range(len(payload_set))]

    clf_svm = OneClassSVM(nu=0.001, kernel="rbf", gamma='auto')
    clf_svm.fit(training_Set)
    predicted_labels = clf_svm.predict(training_Set)
    print("Accuracy SVM:")
    print(accuracy_score(real_labels, predicted_labels))

    clf_if = IsolationForest(contamination=0.01)
    clf_if.fit(training_Set)
    predicted_labels = clf_if.predict(training_Set)
    print("Accuracy IF:")
    print(accuracy_score(real_labels, predicted_labels))

    clf_ee = EllipticEnvelope(contamination=0.01)
    clf_ee.fit(training_Set)
    predicted_labels = clf_ee.predict(training_Set)
    print("Accuracy EE:")
    print(accuracy_score(real_labels, predicted_labels))

    clf_lo = LocalOutlierFactor(contamination=0.01, novelty=True)
    clf_lo.fit(training_Set)
    predicted_labels = clf_lo.predict(training_Set)
    print("Accuracy LO:")
    print(accuracy_score(real_labels, predicted_labels))

    clf_cc = CustomClassifier()
    clf_cc.fit(payload_set)
    predicted_labels = clf_cc.predict(payload_set)
    print("Accuracy CC:")
    print(accuracy_score(real_labels, predicted_labels))

    print("ThresholdsClusters:" + str(clf_cc.thresholdsCluster))

    f = open(model_path + "/feature_num.txt", "w")
    f.write(str(max_features))
    f.close()

    pickle.dump(clf_svm, open(model_path + "/svm.sav", 'wb'))
    pickle.dump(clf_if, open(model_path + "/if.sav", 'wb'))
    pickle.dump(clf_ee, open(model_path + "/ee.sav", 'wb'))
    pickle.dump(clf_lo, open(model_path + "/lo.sav", 'wb'))
    pickle.dump(clf_cc, open(model_path + "/cc.sav", 'wb'))

    capture.close()



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

        #payload = bytes.fromhex(payload).decode('ISO-8859-1')
        #print(payload)
        #print(bytes.fromhex(payload).decode('ISO-8859-1'))

        if str(packet.eth._all_fields['eth.src']) == str(mac_app) and str(packet.eth._all_fields['eth.dst']) == str(mac_device):

            if not request:
                request = True
                flow = Flow(packet.transport_layer, packet.ip.dst, packet[packet.transport_layer].dstport, packet[packet.transport_layer].srcport, [], [])
                flow.list_requests.append(payload)
                list_flows.append(flow)
            else:
                current_flow = list_flows[len(list_flows) - 1]
                current_flow.list_requests.append(payload)
                list_flows[len(list_flows) - 1] = current_flow
            continue


        if str(packet.eth._all_fields['eth.src']) == str(mac_device) and str(packet.eth._all_fields['eth.dst']) == str(mac_app):

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

if(len(list_flows)<1):
    print("Error in length list flow")
else:
    print('END READING PCAP')
    training()