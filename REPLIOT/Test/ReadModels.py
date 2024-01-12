import pickle

path_Models="/home/deangelis/Desktop/ReplayAttack/ScreenShot/ac:bf:71:6b:e8:5b/Experiments/Experiment_1"
try:
    clf_svm = pickle.load(open(path_Models+ "/svm.sav", 'rb'))
    clf_if = pickle.load(open(path_Models + "/if.sav", 'rb'))
    clf_ee = pickle.load(open(path_Models + "/ee.sav", 'rb'))
    clf_lo = pickle.load(open(path_Models+ "/lo.sav", 'rb'))
    clf_cc = pickle.load(open(path_Models+"/cc.sav", 'rb'))
    f = open(path_Models + "/feature_num.txt", "r")
    max_num_features = int(f.read())
except:
    print("Models not found")

res='HTTP/1.1 200 OK\r\nDate: Tue, 12 Sep 2023 10:49:52 GMT\r\nContent-Type: text/xml; charset="utf-8"\r\nExt:\r\nServer: Linux/3.18.71+ UPnP/1.0 GUPnP/1.0.5\r\nContent-Length: 280\r\n<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetVolumeDBResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetVolumeDBResponse></s:Body></s:Envelope>'


i=0

print(clf_cc.thresholdsCluster[15])
for cluster in clf_cc.clusters:
    for c in cluster:
        if 'SetVolumeDBResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1' in c:
            print(cluster)
            print(i)
            break
    i+=1
