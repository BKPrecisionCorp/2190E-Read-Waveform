import pyvisa
import pylab as pl

#####_____ initialization ______#####
rm = pyvisa.ResourceManager()
li = rm.list_resources()
choice = ''
while(choice == ''):
    for index in range(len(li)):
        print(str(index)+" - "+li[index])
    choice = input("Select DUT: ")
    try: 
        if(int(choice) > len(li) - 1 or int(choice) < 0):
            choice = ''
            print("Invalid Input\n")
    except:
        print("Invalid Input\n")
        choice = ''
inst = rm.open_resource(li[int(choice)])

def main():
    ###___Get channel parameters_____###
    inst.write("chdr off")
    vdiv = inst.query("c2:vdiv?")
    ofst = inst.query("c2:ofst?")
    tdiv = inst.query("tdiv?")
    sara = inst.query("sara?")
    sara_unit = {'G':1E9,'M':1E6,'k':1E3} #change scientific notation
    for unit in sara_unit.keys():
        if sara.find(unit)!=-1:
            sara = sara.split(unit)
            sara = float(sara[0])*sara_unit[unit]
            break
    sara = float(sara)#convert values to float
    inst.timeout = 30000 #default value is 2000(2s)
    inst.chunk_size = 20*1024*1024 #specifiy space needed to store the data collected from channel 2 default value is 20*1024(20k bytes)
    inst.write("c2:wf? dat2")
    recv = list(inst.read_raw())[15:]
    print(len(recv))
    recv.pop()
    recv.pop()
    volt_value = []
    for data in recv:
        if data > 127:
            data = data - 256
        else:
            pass
        volt_value.append(data)
    time_value = []
    for idx in range(0,len(volt_value)):
        volt_value[idx] = volt_value[idx]/25*float(vdiv)-float(ofst)
        time_data = -(float(tdiv)*14/2)+idx*(1/sara)
        time_value.append(time_data)
    print("Data covert finish,start to draw")
    pl.figure(figsize=(7,5))
    pl.plot(time_value,volt_value,markersize=2,label=u"Y-T")
    pl.legend()
    pl.grid()
    pl.show()
if __name__=='__main__':
    main()








