import sys

exp_folder = str(sys.argv[1])
n_tests = int(str(sys.argv[2]))

ref = exp_folder + "Experiment_1/attackResult.txt"
file1 = open(ref, 'r')
Lines = [line.rstrip() for line in file1]
attack_working = False

if (Lines[0] == 'Replay Attack working'):
    attack_working = True
elif (Lines[0] == 'Replay Attack NOT working'):
    attack_working = False
else:
    print("Error in reading attackResult.txt")
    sys.exit(0)

correct_detection_svm = 0
correct_detection_if = 0
correct_detection_ee = 0
correct_detection_lo = 0
correct_detection_cc = 0

for i in range(1, n_tests+1):
    ref = exp_folder + "Experiment_" + str(i) + "/attackResult.txt"
    file1 = open(ref, 'r')
    Lines = [line.rstrip() for line in file1]


    if (Lines[0] == 'Replay Attack working' and not attack_working):
        print("Experiment " + str(i) + " Failed:repeat. Replay Attack not working")
        sys.exit(0)
    elif (Lines[0] == 'Replay Attack NOT working' and attack_working):
        print("Experiment " + str(i) + " Failed:repeat. Replay Attack working")
        sys.exit(0)

    path = exp_folder + "Experiment_" + str(i) + "/res.txt"
    file1 = open(path, 'r')
    Lines = [line.rstrip() for line in file1]

    if (Lines[-2] == 'NO RESPONSE AVAILABLE: REPLAY ATTACK NOT SUCCESSFUL' and attack_working):
        print("AUTOMATIC DETECTION FAILED")
        continue
    if (Lines[-2] == 'NO RESPONSE AVAILABLE: REPLAY ATTACK NOT SUCCESSFUL' and not attack_working):
        print("AUTOMATIC DETECTION SUCCESS")
        continue

    svm_res = Lines[-6]
    if_res = Lines[-5]
    ee_res = Lines[-4]
    lo_res = Lines[-3]
    cc_res = Lines[-2]

    if ("REPLAY ATTACK SUCCESSFUL WITH CLF=OneClassSVM" in svm_res and attack_working):
        correct_detection_svm=correct_detection_svm+1
    if ("REPLAY ATTACK NOT SUCCESSFUL WITH CLF=OneClassSVM" in svm_res and not attack_working):
        correct_detection_svm=correct_detection_svm+1

    if ("REPLAY ATTACK SUCCESSFUL WITH CLF=IsolationForest" in if_res and attack_working):
        correct_detection_if = correct_detection_if + 1
    if ("REPLAY ATTACK NOT SUCCESSFUL WITH CLF=IsolationForest" in if_res and not attack_working):
        correct_detection_if = correct_detection_if + 1

    if ("REPLAY ATTACK SUCCESSFUL WITH CLF=EllipticEnvelope" in ee_res and attack_working):
        correct_detection_ee = correct_detection_ee + 1
    if ("REPLAY ATTACK NOT SUCCESSFUL WITH CLF=EllipticEnvelope" in ee_res and not attack_working):
        correct_detection_ee = correct_detection_ee + 1

    if ("REPLAY ATTACK SUCCESSFUL WITH CLF=LocalOutlierFactor" in lo_res and attack_working):
        correct_detection_lo = correct_detection_lo + 1
    if ("REPLAY ATTACK NOT SUCCESSFUL WITH CLF=LocalOutlierFactor" in lo_res and not attack_working):
        correct_detection_lo = correct_detection_lo + 1

    if ("REPLAY ATTACK SUCCESSFUL WITH CLF=CustomClassifier" in cc_res and attack_working):
        correct_detection_cc = correct_detection_cc + 1
    if ("REPLAY ATTACK NOT SUCCESSFUL WITH CLF=CustomClassifier" in cc_res and not attack_working):
        correct_detection_cc = correct_detection_cc + 1

print("Correct Detections SVM="+str(correct_detection_svm))
print("Correct Detections IF="+str(correct_detection_if))
print("Correct Detections EE="+str(correct_detection_ee))
print("Correct Detections LO="+str(correct_detection_lo))
print("Correct Detections CC="+str(correct_detection_cc))


print("Accuracy SVM="+str(correct_detection_svm/n_tests))
print("AccuracyIF="+str(correct_detection_if/n_tests))
print("Accuracy EE="+str(correct_detection_ee/n_tests))
print("Accuracy LO="+str(correct_detection_lo/n_tests))
print("Accuracy CC="+str(correct_detection_cc/n_tests))
