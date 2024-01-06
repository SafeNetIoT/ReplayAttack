import sys

mac_device=sys.argv[1]
name=sys.argv[2]
path_file="Result/"+mac_device+"/raw_"+name+"_coordinates.txt"

file = open(path_file, 'r')
Lines = file.readlines()
list_coordinates=[]
x_coordinate=""
y_coordinate=""
touch=False
# Strips the newline character
for line in Lines:
    if "BTN_TOUCH" in line:
        touch=True
    if touch:
        if "ABS_MT_POSITION_X" in line:
             x_coordinate=int(line.strip().split(" ")[-1],16)
        if "ABS_MT_POSITION_Y" in line:
             y_coordinate = int(line.strip().split(" ")[-1],16)
             list_coordinates.append((str(x_coordinate),str(y_coordinate)))
             touch=False

output_file="Result/"+mac_device+"/"+name+"_coordinates.txt"
f = open(output_file, "w")

for pair in list_coordinates:
    f.write("tap "+pair[0]+" "+pair[1]+"\n")

f.close()


