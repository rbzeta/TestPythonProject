# -*- coding: utf-8 -*-
#!/usr/bin/python
### to be used with telegram-bot plugin updateinfo.lua
### !updateinfo (atm) [TID] [Description]

import os, sys, time


numArgs = len(sys.argv)

if numArgs == 1:

    print ("Format pesan anda tidak lengkap")

if numArgs > 1:


    if sys.argv[4]:
    # msg.from
        report_creausr = sys.argv[1]
        # terminal ID
        branch_code = sys.argv[2]
        
        #appname
        app_name = sys.argv[3]
        
        #appstatus
        app_status = sys.argv[4]
        
        
        
        # create date
        atmproblem_creadt = time.strftime("%Y-%m-%d %H:%M:%S")
        # description
        atmproblem_keterangan = " ".join(sys.argv[5:numArgs])


        strQuery = "INSERT INTO m_report_aplikasi(rptapl_brcode,rptapl_name,rptapl_status,rptapl_date,rptapl_rspntime,rptapl_desc,rptapl_creadt,rptapl_creausr,rptapl_upddt,rptapl_updusr)VALUES ('"+branch_code+"','"+app_name+"', '"+app_status+"', '"+atmproblem_creadt+"', '""', '"+atmproblem_keterangan+"', '"+atmproblem_creadt+"', '"+report_creausr+"', '"+atmproblem_creadt+"', '"+report_creausr+"');"
        
        strCmd = 'mysql -h 1.132.218.71 --user sa --password=P@ssw0rd -D kanwiljak3 -e "' + strQuery + '"'

        #print strCmd

        os.system(strCmd)

        print ("Terima kasih telah atas laporan anda.")
    else:
        print ("Format pesan anda tidak lengkap")



