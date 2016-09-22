'''
Created on Dec 3, 2015

@author: Robyn
'''

import sys
import pymysql

numArgs = len(sys.argv)

if numArgs < 1:

    print ("Anda belum meng-input 4 digit kode uker")

if numArgs > 0:
    
    if sys.argv[1]:
        
        branch_code = sys.argv[1]
        
        strQuery = " select branch,ipaddress,name,address,pic,picnumber from m_master_uko_ip where branch like '%"+branch_code+"%'"
        
        con = pymysql.connect(host = "1.132.218.71", user = "sa", passwd = "P@ssw0rd", db = "kanwiljak3")
        
        select_stmt = con.cursor()
        
        select_stmt.execute(strQuery)
        
        data = select_stmt.fetchone()
        
        if data :
        
            kode_uker = data[0]
            
            ip_address = data[1]
            
            nama_uker = data[2]
            
            alamat = data[3]
            
            pic = data[4]
            
            picnumber = data[5]
            
            strMsg = "Kode Uker : " + kode_uker + "\n"
            strMsg = strMsg + "IP : " + ip_address + "\n"
            strMsg = strMsg + "Unit Kerja : " + nama_uker + "\n"
            strMsg = strMsg + "Alamat : " + alamat + "\n"
            strMsg = strMsg + "PIC : " + pic + "\n"
            strMsg = strMsg + "No Telp : " + picnumber + "\n"
            
            print(strMsg)
        else :
            strMsg = "Kode uker "+branch_code+" belum terdaftar di basis data kami."
            
            print(strMsg)
        