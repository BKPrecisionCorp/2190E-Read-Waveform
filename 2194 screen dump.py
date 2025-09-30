import pyvisa
def main():
    rm = pyvisa.ResourceManager()
    sds = rm.open_resource("USB0::0x3121::0x2100::SDSAHBAD4R0328::INSTR")
    sds.chunk_size = 20*1024*1024 #default value is 20*1024(20k bytes)
    sds.timeout = 30000 #default value is 2000(2s)
    file_name = "C:\\Users\ARamirez.BK1\Desktop"
    sds.write("SCDP")
    sds.query("SCDP")
    data = sds.read_raw()
    f = open(file_name,"wb")
    f.write(result_str)
    f.flush()
    f.close()
if __name__=='__main__':
 main()
