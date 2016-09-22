# -*- coding: utf-8 -*-
#!/usr/bin/python
### to be used with telegram-bot plugin updateinfo.lua
### !updateinfo (atm) [TID] [Description]

import os, sys, time


numArgs = len(sys.argv)

if numArgs == 1:

	print ("Anda belum meng-input keterangan")

if numArgs > 1:


	if sys.argv[3]:
	# msg.from
		atmproblem_creausr = sys.argv[1]
		# terminal ID
		atmproblem_tid = sys.argv[2]
		# create date
		atmproblem_creadt = time.strftime("%Y-%m-%d %H:%M:%S")
		# description
		atmproblem_keterangan = " ".join(sys.argv[3:numArgs])


		strQuery = "INSERT INTO m_atm_problem_keterangan (atmproblem_tid, atmproblem_keterangan, atmproblem_creadt, atmproblem_creausr) VALUES ('"+atmproblem_tid+"','"+atmproblem_keterangan+"', '"+atmproblem_creadt+"', '"+atmproblem_creausr+"');"
		
		strCmd = 'mysql -h 1.132.218.71 --user sa --password=P@ssw0rd -D kanwiljak3 -e "' + strQuery + '"'

		#print strCmd

		os.system(strCmd)

		print ("Terima kasih telah meng-update data problem ATM.")
	else:
		print ("Anda belum menginput keterangan")



