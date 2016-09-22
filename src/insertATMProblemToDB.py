# -*- coding: utf-8 -*-
#!/usr/bin/python
### Jansen A. Simanullang 
### 22.04.2015 18:36:34 getEDCUKONOPKanwil.py
### 07.08.2015 12:32:17
### 13.08.2015 14:27:48 added percent availability and color indicator name
from __future__ import division
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os, time

import pymysql
import urllib

atmproIP = "172.18.65.42"
################################################################################################
firstURL='http://'+atmproIP+'/statusatm/dashboard_3.pl?ERROR=CLOSE_ST'
RegionName = "JAKARTA III"
periodeMonitoring=3600*4
################################################################################################

scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"

asciiArt="""
       ▄▄▄▄▄▄▄▄▄
        ▄█████████████▄ 
█████  █████████████████  █████
▐████▌ ▀███▄       ▄███▀ ▐████▌
 █████▄  ▀███▄   ▄███▀  ▄█████
 ▐██▀███▄  ▀███▄███▀  ▄███▀██▌    
  ███▄▀███▄  ▀███▀  ▄███▀▄███ 
  ▐█▄▀█▄▀███ ▄─▀─▄ ███▀▄█▀▄█▌
   ███▄▀█▄██ ██▄██ ██▄█▀▄███
    ▀███▄▀██ █████ ██▀▄███▀
   █▄ ▀█████ █████ █████▀ ▄█
   ███        ███     ███
   ███▄    ▄█ ███ █▄    ▄███
   █████ ▄███ ███ ███▄ █████
   █████ ████ ███ ████ █████
   █████ ████ ███ ████ █████
   █████ ████ ███ ████ █████
   █████ ████▄▄▄▄▄████ █████
    ▀███ █████████████ ███▀
      ▀█ ███ ▄▄▄▄▄ ███ █▀
         ▀█▌▐█████▌▐█▀
            ███████
"""

asciiArt="""
       ▄▄▄▄▄▄▄▄▄
        ▄█████████████▄ 
█████  █████████████████  █████
▐████▌ ▀███▄       ▄███▀ ▐████▌
 █████▄  ▀███▄   ▄███▀  ▄█████    NOTIFIKASI ATM via TELEGRAM
"""

asciiArt = asciiArt +" ▐██▀███▄  ▀███▄███▀  ▄███▀██▌    "+RegionName
asciiArt = asciiArt +"""
  ███▄▀███▄  ▀███▀  ▄███▀▄███     
  ▐█▄▀█▄▀███ ▄▀ ▀▄ ███▀▄█▀▄█▌     (c) JANSEN SIMANULLANG
   ███▄▀█▄██ ██ ██ ██▄█▀▄███      MEI 2015
    ▀███▄▀██ ██ ██ ██▀▄███▀
   █▄ ▀█████ █████ █████▀ ▄█        \__/  \__/  \__/  \__/  \__/  \__/
   ███        ███     ███      __/  \__/  \__/  \__/  \__/  \__/  \_
   ███▄    ▄█ ███ █▄    ▄███        \__/  \__/  \__/  \__/  \__/  \__/ 
   █████ ▄███ ███ ███▄ █████     \__/  \__/  \__/  \__/  \__/  \__/  \_
   █████ ████ ███ ████ █████        \__/  \__/  \__/  \__/  \__/  \__/ 
   █████ ████ ███ ████ █████     \__/  \__/  \__/  \__/  \__/  \__/  \_ 
   █████ ████ ███ ████ █████        \__/  \__/  \__/  \__/  \__/  \__/ 
   █████ ████▄▄▄▄▄████ █████     \__/  \__/  \__/  \__/  \__/  \__/   
    ▀███ █████████████ ███▀    __/  \__/  \__/  \__/  \__/  \__/  \__/
      ▀█ ███ ▄▄▄▄▄ ███ █▀     /  \__/  \__/  \__/  \__/  \__/  \__/  
         ▀█▌▐█████▌▐█▀        \__/  \__/  \__/  \__/  \__/  \__/  \__/
            ███████        \__/  \__/  \__/  \__/  \__/  \__/  \__/  
"""
"""
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_

"""
def clearScreen():

    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

def welcomeScreen():
    
    clearScreen()

    #print asciiArt


def countDomainLevel(alamatURL):

    intDomainDepth = alamatURL.count('/') - 2*alamatURL.count('//')

    return intDomainDepth



def getDomainParts(alamatURL):

    parts = alamatURL.split('//')

    protocol = parts [0]

    arrDomainParts = parts[1].split('/', countDomainLevel(alamatURL))

    return protocol, arrDomainParts
    


def nLevelDomain(alamatURL, n):

    protocol, arrDomainParts = getDomainParts(alamatURL)

    urlnLevelDomain = ""

    for i in range (0, n):

        urlnLevelDomain = urlnLevelDomain + arrDomainParts[i]+"/"

    urlnLevelDomain = protocol + "//" + urlnLevelDomain

    return urlnLevelDomain



def getQueryContent(alamatURL, strQuery):
    
    parsed = urlparse(alamatURL)
    QueryContent = str(urllib.parse.parse_qs(parsed.query)[strQuery][0])
    return QueryContent



def cleanUpHTML(strHTML):

    URLdomain = nLevelDomain(alamatURLNOPG, 1)
    URLdomain2 = nLevelDomain(alamatURLNOPG, 2)
    
    # fixing broken HTML
    strHTML = strHTML.replace('</tr><td>',"</tr><tr><td>")
    strHTML = strHTML.replace('</td></tr><td>','</td></tr><tr><td>')
    strHTML = strHTML.replace('<table class=fancy>','</td></tr></table><table class=fancy>')
    strHTML = strHTML.replace('</th>\n</tr>',"</th></tr><tr>")
    strHTML = strHTML.replace('</tr>\n\n<td>',"</tr><tr><td>")


    strHTML = strHTML.replace(' bgcolor>', '>')
    strHTML = strHTML.replace('<table class=fancy>','</td></tr></table><table class=fancy>')


    # translating relative to absolute reference
    strHTML = strHTML.replace('@import "/','@import "'+URLdomain)
    strHTML = strHTML.replace('href="/','href="'+URLdomain)
    strHTML = strHTML.replace("href='/","href='"+URLdomain)
    strHTML = strHTML.replace("href='./",'href="'+URLdomain)
    strHTML = strHTML.replace("href='../","href='"+URLdomain2)

    return strHTML
    


def fetchHTML(alamatURL):
    # fungsi ini hanya untuk mengambil stream string HTML dari alamat URL yang akan dimonitor
    # Content-Type utf-8 raises an error when meets strange character
    #print "fetching HTML from URL...\n", alamatURL
    strHTML = urlopen(alamatURL).read().decode("ISO-8859-1")

    #strHTML = strHTML.decode("windows-1252")

    #strHTML = strHTML.encode('ascii', 'ignore')

    strHTML = cleanUpHTML(strHTML)

    #mysoup = BeautifulSoup(strHTML, "html.parser")
    
    #print ">> URL fetched."

    return strHTML



def getTableList(strHTML):

    #print "\ngetting Table List...\n"

    mysoup = BeautifulSoup(strHTML, "html.parser")

    arrTable = mysoup.findAll('table')

    #print "there are:", len(arrTable), "tables."

    return arrTable



def getStyleList(strHTML):

    #print "\ngetting Style List...\n"

    mysoup = BeautifulSoup(strHTML, "html.parser")

    arrStyle = mysoup.findAll('link', rel = "stylesheet" )

    strStyle = ""

    for i in range (0, len(arrStyle)):

        strStyle = strStyle + str(arrStyle[i])
    
    return strStyle



def getHeading(strHTML):

    print ("\ngetting Heading...\n")

    strHTML = cleanUpHTML(strHTML)

    mysoup = BeautifulSoup(strHTML, "html.parser")

    heading1 = mysoup.findAll('h1')

    if heading1 != []:

        strHeading = heading1[0].getText().upper()
        strHeading = strHeading.replace("BY REGION", RegionName)


    heading3 = mysoup.findAll('h3')

    if heading3 != []:

        strHeading = heading3[0].getText().upper()
        strHeading = strHeading.replace("REGION: "+RegionName+" - ", "")
        strHeading = strHeading.replace("FOR REGION", "")



    else:
        strHeading = 'AVAILABILITY ATM BRI ' + RegionName
    

    #
    strHeading = strHeading.replace("LIST OF", "")

    # avoid semicolon, slash and double space by deleting them
    strHeading = strHeading.replace(":", "")
    strHeading = strHeading.replace("/", " ")
    strHeading = strHeading.replace("  ", " ")

    return strHeading.strip()



def getLargestTable(arrTable):

    # pilihlah tabel yang terbesar yang memiliki jumlah baris terbanyak

    largest_table = None

    max_rows = 0

    for table in arrTable:

        # cek satu per satu jumlah baris yang ada pada masing-masing tabel dalam array kumpulan tabel
        # simpan dalam variabel bernama numRows

        numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
        
        # jika jumlah baris pada suatu tabel lebih besar daripada '0' maka jadikan sebagai max_rows sementara
        # proses ini diulangi terus menerus maka max_rows akan berisi jumlah baris terbanyak

        if numRows > max_rows:
            
            largest_table = table
            max_rows = numRows

    # ini hanya mengembalikan penyebutan 'tabel terbesar' hanya sebagai 'tabel'

    table = largest_table

    #if table:
        #print ">> the largest from table list is chosen."

    return table



def getWidestTable(arrTable):

    # pilihlah tabel yang terbesar yang memiliki jumlah baris terbanyak

    widest_table = None

    max_cols = 0

    for table in arrTable:

        # cek satu per satu jumlah baris yang ada pada masing-masing tabel dalam array kumpulan tabel
        # simpan dalam variabel bernama numRows

        numCols = len(table.contents[1])
        
        # jika jumlah baris pada suatu tabel lebih besar daripada '0' maka jadikan sebagai max_rows sementara
        # proses ini diulangi terus menerus maka max_rows akan berisi jumlah baris terbanyak

        if numCols > max_cols:
            
            widest_table = table
            max_cols = numCols

    # ini hanya mengembalikan penyebutan 'tabel terbesar' hanya sebagai 'tabel'

    table = widest_table

    #if table:
        #print ">> the widest from table list is chosen."

    return table



def getColsNumber(table):

    # bagaimana cara menentukan berapa jumlah kolomnya?

    numCols = len(table.contents[1])
    
    return numCols



def getRowsNumber(table):

    # bagaimana cara menentukan berapa jumlah kolomnya?

    numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
    
    return numRows

def getColsNumFromRows(row):

    # bagaimana cara menentukan berapa jumlah kolomnya?

    numCols = len(row.findAll(lambda tag: tag.name == 'td'))
    
    return numCols

def getRowsHeadNumber(table):

    # bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai header?

    soup = BeautifulSoup(str(table), "html.parser")
    rows = soup.findAll('tr')
    numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))

    # inisialisasi variabel numRowsHead sebagai jumlah baris yang mengandung header

    numRowsHead = 0    
    
    # periksa satu per satu setiap baris

    for i in range (0, numRows):
        
        # apabila dalam suatu baris tertentu terdapat tag <th>
        if rows[i].findAll('th'):
            
            # maka numRows bertambah 1
            numRowsHead = i + 1


    # hasil akhir fungsi getTableDimension ini menghasilkan jumlah baris, jumlah baris yang terpakai header, jumlah kolom dan isi tabel itu sendiri

    return numRowsHead



def getTableDimension(table):
    
    numRows = getRowsNumber(table)
    numRowsHead = getRowsHeadNumber(table)
    numCols = getColsNumber(table)
    
    return numRows, numRowsHead, numCols



def fileCreate(strNamaFile, strData):
    f = open(strNamaFile, "w")
    f.writelines(str(strData))
    f.close()


    
def fileAppend(strNamaFile, strData):
    f = open(strNamaFile, "a")
    f.writelines(str(strData))
    f.close()



def getTableHeader(table):

    numRowsHead = getRowsHeadNumber(table)

    soup = BeautifulSoup(str(table), "html.parser")
    rows = soup.findAll('tr', limit=numRowsHead)
    strHTMLTableHeader = ""
    
    for i in range (0, numRowsHead):

        strHTMLTableHeader = strHTMLTableHeader + str(rows[i])
    
    return strHTMLTableHeader



def getSpecificRows(table, rowIndex):

    #print "Let's take a look at the specific rows of index", rowIndex

    soup = BeautifulSoup(str(table), "html.parser")
    rows = soup.findAll('tr')
    strHTMLTableRows = ""

    for i in range (rowIndex, rowIndex+1):

        strHTMLTableRows = str(rows[i])
    
    return strHTMLTableRows



def getTableContents(table):

    numRows = getRowsNumber(table)
    numRowsHead = getRowsHeadNumber(table)

    soup = BeautifulSoup(str(table), "html.parser")
    rows = soup.findAll('tr')
    strHTMLTableContents = ""

    for i in range (numRowsHead, numRows):

        strHTMLTableContents = strHTMLTableContents + str(rows[i])
    
    return strHTMLTableContents



def getRowIndex(table, strSearchKey):

    # fungsi ini untuk mendapatkan nomor indeks baris yang mengandung satu kata kunci

    soup = BeautifulSoup(str(table), "html.parser")
    rows = soup.findAll('tr')
    
    numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))

    rowIndex = 0

    for i in range (0, numRows):

        trs = BeautifulSoup(str(rows[i]), "html.parser")
        tdcells = trs.findAll("td")
            
        for j in range (0, len(tdcells)):

            if tdcells[j].getText().upper() == strSearchKey.upper():
                
                rowIndex = i

                #print "we got the index = ", rowIndex, "from ", numRows, "for search key ='"+strSearchKey+"'"
    return rowIndex



def getATMProbUKOCRO(table):

    try:

        #print "getting List of ATMs requires attention..."
    
        soup = BeautifulSoup(str(table), "html.parser")
    
        rows = soup.findAll('tr')

        numRows = getRowsNumber(table)

        numRowsHead = getRowsHeadNumber(table)

        numProbUKO = 0
        numProbCRO = 0

        for i in range (numRowsHead, numRows):

            trs = BeautifulSoup(str(rows[i]), "html.parser")
            tdcells = trs.findAll("td")

            if "ATM CENTER" in tdcells[6].getText():

                numProbCRO = numProbCRO + 1

        numProbUKO = numRows - numProbCRO -numRowsHead

        #print "number of CRO problem(s)", numProbCRO, "number of UKO problem(s):", numProbUKO

    except IndexError:

        numProbUKO, numProbCRO = getATMProbUKOCRO(table)

    except RuntimeError:

        numProbUKO, numProbCRO = "0","0"


    return int(numProbUKO), int(numProbCRO)



def getATMProbUKOCRO2(table):

    try:

        #print "getting List of ATMs requires attention..."
    
        soup = BeautifulSoup(str(table), "html.parser")
    
        rows = soup.findAll('tr')

        numRows = getRowsNumber(table)

        numRowsHead = getRowsHeadNumber(table)

        numProbUKO = 0
        numProbCRO = 0

        for i in range (numRowsHead, numRows):

            trs = BeautifulSoup(str(rows[i]), "html.parser")
            tdcells = trs.findAll("td")

            if "ATM CENTER" in tdcells[8].getText():

                numProbCRO = numProbCRO + 1

        numProbUKO = numRows - numProbCRO -numRowsHead

        #print "number of CRO problem(s)", numProbCRO, "number of UKO problem(s):", numProbUKO

    except IndexError:

        numProbUKO, numProbCRO = getATMProbUKOCRO(table)

    except RuntimeError:

        numProbUKO, numProbCRO = "0","0"


    return int(numProbUKO), int(numProbCRO)



def getAvailability(table):

    try:

        #print "getting List of ATMs requires attention..."
    
        soup = BeautifulSoup(str(table), "html.parser")
    
        rows = soup.findAll('tr')

        numRows = getRowsNumber(table)

        numRowsHead = getRowsHeadNumber(table)

        #numProbUKO = 0
        #numProbCRO = 0

        for i in range (numRowsHead, numRows):

            trs = BeautifulSoup(str(rows[i]), "html.parser")
            tdcells = trs.findAll("td")

            percentAvail = tdcells[24].getText()
            #colorCode = tdcells[8].getText()

    

    except IndexError:

        percentAvail = getAvailability(table)

    return percentAvail

def colorPercent(percentAvail):

    strColor = str(percentAvail)

    if percentAvail >= 0.00:
        strColor = "Merah"
    if percentAvail >= 87.00:
        strColor = "Kuning"
    if percentAvail >= 93.00:
        strColor = "Hijau Muda"
    if percentAvail >= 97.00:
        strColor = "Hijau Tua"


    return strColor

def getATMProblem(table,GNG,status,rowNum):

    try:
        listTable = []
        listRows = []
        numCols = 0
        #print "getting List of ATMs requires attention..."
    
        soup = BeautifulSoup(str(table), "html.parser")
    
        rows = soup.findAll('tr')
        
        numRows = getRowsNumber(table)
        
        if (numRows > 1):
        
            if (status in ("DF")):
                    numCols = 11
            else:
                numCols = getColsNumFromRows(BeautifulSoup(str(rows[1]), "html.parser"))
        
        
        

        numRowsHead = getRowsHeadNumber(table)

        for i in range (numRowsHead, numRows):
            rowNum += 1
            trs = BeautifulSoup(str(rows[i]), "html.parser")
            tdcells = trs.findAll("td")
            
            
            
            for j in range (0,numCols):
                tds = BeautifulSoup(str(tdcells[j]), "html.parser")
                if (status in ("DF")):
                    if (j == 8) :
                        listRows.insert(9, tds.text)
                    elif (j == 9):
                        listRows.insert(8, tds.text)
                    else :
                        listRows.append(tds.text)
                elif(status in ("OFF")):
                    if (j == 3):
                        listRows.append("")
                    if (j == 4):
                        continue
                    elif (j == 9):
                        continue
                    elif (j == 7):
                        listRows.insert(6,tds.text)
                    else:
                        listRows.append(tds.text)
                elif(status in ("CO")):
                    if (j == 9) :
                        listRows.insert(8, tds.text)
                    elif (j == 10):
                        continue
                    else:
                        listRows.append(tds.text)
                else :
                    listRows.append(tds.text)
                
                #print(tds.text)

             
            if (listRows.__len__() > 0 ) :
                if (status in ("OPS")):
                    listRows.append("")
                  
                if (status in ("OFF")):
                    listRows.append("")
                  
                if (status in ("DF")):
                    listRows.insert(10,"")
                    
                if (status not in ("OOS","CR","EPP","DF","CL","CO") ):
                    listRows.append("")
                listRows.append(time.strftime("%Y-%m-%d %H:%M:%S"))
                listRows.append(time.strftime("%Y-%m-%d %H:%M:%S"))
                listRows.append("OS Scheduler")
                listRows.append("OS Scheduler")
                listRows.append(GNG)
                listRows.append(status)
                listRows.append("1")
                listRows.append("")
                #remove rownumber and replace row number from custom rownum
                listRows.pop(0)
                listRows.insert(0, rowNum)
                listTable.append(listRows.copy())
            
            listRows.clear()
            
    except RuntimeError:

        print ("gagal mendapatkan tabel atm problem")


    return list(listTable),rowNum

def setATMProblemDataInactive(query) :
    try :
        conn = pymysql.connect(host='1.132.218.71', user='sa', passwd='P@ssw0rd', db='kanwiljak3')
        cur = conn.cursor()
        cur.execute(query)
        cur.close()
        conn.commit();
        conn.close()
    
    except RuntimeError :
        print ('gagal saat set inactive atm problem data tabel')
    
    

    return True

def moveDatatoHistoryTable(query):
    try :
        conn = pymysql.connect(host='1.132.218.71', user='sa', passwd='P@ssw0rd', db='kanwiljak3')
        cur = conn.cursor()
        cur.execute(query)
        cur.close()
        conn.commit();
        conn.close()
    
    except RuntimeError :
        print ('gagal saat set inactive atm problem data tabel')
    return True

def truncateDataTable(query):
    try :
        conn = pymysql.connect(host='1.132.218.71', user='sa', passwd='P@ssw0rd', db='kanwiljak3')
        cur = conn.cursor()
        cur.execute(query)
        cur.close()
        conn.commit();
        conn.close()
    
    except RuntimeError :
        print ('gagal saat set inactive atm problem data tabel')
    return True
def insertTableIntoDB(listTable,query):
    
    try :
        conn = pymysql.connect(host='1.132.218.71', user='sa', passwd='P@ssw0rd', db='kanwiljak3')
        cur = conn.cursor()
        
        for i in range(len(listTable)):
            rowdata = listTable[i]
                 
            cur.execute(query,rowdata)
            
        
        cur.close()
        conn.commit();
        conn.close()
        #print('ok')
    
    except RuntimeError :
        return False
    
    

    return True


add_nopg_qry2 = (" INSERT INTO m_atm_nop_sum(atmnop_rowno,atmnop_tid,atmnop_brand,atmnop_vendor,atmnop_ip,atmnop_lokasi,atmnop_area,atmnop_pengelola,atmnop_downtime,atmnop_keterangan,atmnop_petugas) "
                " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ")

add_nopg_qry = (" INSERT INTO m_atm_nop_sum(atmnop_rowno,atmnop_tid,atmnop_brand,atmnop_vendor,atmnop_ip,atmnop_lokasi,atmnop_area,atmnop_pengelola,atmnop_downtime,atmnop_keterangan,atmnop_petugas,atmnop_lasttrx,atmnop_creadt,atmnop_upddt,atmnop_creausr,atmnop_updusr,atmnop_garansi,atmnop_status,atmnop_isactive,atmnop_garansidt) "
                " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ")

setinactive_qry_bak = "UPDATE m_atm_nop_sum SET atmnop_isactive = 0 WHERE atmnop_creadt <> (SELECT datevalue FROM (SELECT MAX(DISTINCT atmnop_creadt) AS datevalue FROM m_atm_nop_sum) AS m_atm_nop_sum_temp)"

setinactive_qry = "UPDATE m_atm_nop_sum SET atmnop_isactive = 0 "

movedata_qry = "INSERT INTO m_atm_nop_sum_hist(atmnop_tid,atmnop_brand,atmnop_vendor,atmnop_ip,atmnop_lokasi,atmnop_area,atmnop_pengelola,atmnop_downtime,atmnop_keterangan,atmnop_petugas,atmnop_lasttrx,atmnop_creadt,atmnop_upddt,atmnop_creausr,atmnop_updusr,atmnop_garansi,atmnop_status,atmnop_isactive,atmnop_garansidt,atmnop_rowno)  SELECT atmnop_tid,atmnop_brand,atmnop_vendor,atmnop_ip,atmnop_lokasi,atmnop_area,atmnop_pengelola,atmnop_downtime,atmnop_keterangan,atmnop_petugas,atmnop_lasttrx,atmnop_creadt,atmnop_upddt,atmnop_creausr,atmnop_updusr,atmnop_garansi,atmnop_status,atmnop_isactive,atmnop_garansidt,atmnop_rowno FROM m_atm_nop_sum "

truncate_qry = "TRUNCATE TABLE m_atm_nop_sum "


rowNumNOP = 0
rowNumRSK = 0
rowNumOPS = 0
rowNumOOS = 0
rowNumCR = 0
rowNumEPP = 0
rowNumDF = 0
rowNumOFF = 0
rowNumCL = 0
rowNumCO = 0
berhasil = True
# Get ATM NOP
alamatURLNOPG = 'http://atmpro.bri.co.id/statusatm/viewbynop.pl?REGID=15&gr=Y'
alamatURLNOPNG = 'http://atmpro.bri.co.id/statusatm/viewbynop.pl?REGID=15&gr=N'
tableNOPG = getLargestTable(getTableList(fetchHTML(alamatURLNOPG)))
tableNOPNG = getLargestTable(getTableList(fetchHTML(alamatURLNOPNG)))

listTableNOPG,rowNumNOP = getATMProblem(tableNOPG,"G","NOP",rowNumNOP)
listTableNOPNG,rowNumNOP = getATMProblem(tableNOPNG,"NG","NOP",rowNumNOP)

#Get RSK table (RSK)
alamatURLRSKG = 'http://atmpro.bri.co.id/statusatm/viewbyrsk.pl?REGID=15&gr=Y'
alamatURLRSKNG = 'http://atmpro.bri.co.id/statusatm/viewbyrsk.pl?REGID=15&gr=N'
tableRSKG = getLargestTable(getTableList(fetchHTML(alamatURLRSKG)))
tableRSKNG = getLargestTable(getTableList(fetchHTML(alamatURLRSKNG)))

listTableRSKG,rowNumRSK = getATMProblem(tableRSKG,"G","RSK",rowNumRSK)
listTableRSKNG,rowNumRSK = getATMProblem(tableRSKNG,"NG","RSK",rowNumRSK)

#Get Operational Problem table (OPS)
alamatURLOPS = 'http://atmpro.bri.co.id/statusatm/viewbyoldstagging.pl?REGID=15&gr=H'
tableOPS = getLargestTable(getTableList(fetchHTML(alamatURLOPS)))
listTableOPS,rowNumOPS = getATMProblem(tableOPS,"-","OPS",rowNumOPS)

#Get Out Off Service table (OOS)
alamatURLOOSG = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobooscr.pl?REGID=15&ERROR=CLOSE_ST&gr=Y'
alamatURLOOSNG = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobooscr.pl?REGID=15&ERROR=CLOSE_ST&gr=N'
tableOOSG = getLargestTable(getTableList(fetchHTML(alamatURLOOSG)))
tableOOSNG = getLargestTable(getTableList(fetchHTML(alamatURLOOSNG)))

listTableOOSG,rowNumOOS = getATMProblem(tableOOSG,"G","OOS",rowNumOOS)
listTableOOSNG,rowNumOOS = getATMProblem(tableOOSNG,"NG","OOS",rowNumOOS)

#Get Card Reader Problem table (CR)
alamatURLCRG = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobooscr.pl?REGID=15&ERROR=CCR_ST&gr=Y'
alamatURLCRNG = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobooscr.pl?REGID=15&ERROR=CCR_ST&gr=N'
tableCRG = getLargestTable(getTableList(fetchHTML(alamatURLCRG)))
tableCRNG = getLargestTable(getTableList(fetchHTML(alamatURLCRNG)))

listTableCRG,rowNumCR = getATMProblem(tableCRG,"G","CR",rowNumCR)
listTableCRNG,rowNumCR = getATMProblem(tableCRNG,"NG","CR",rowNumCR)

#Get EPP Problem table (EPP)
alamatURLEPPG = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobooscr.pl?REGID=15&ERROR=EPP_ST&gr=Y'
alamatURLEPPNG = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobooscr.pl?REGID=15&ERROR=EPP_ST&gr=N'
tableEPPG = getLargestTable(getTableList(fetchHTML(alamatURLEPPG)))
tableEPPNG = getLargestTable(getTableList(fetchHTML(alamatURLEPPNG)))

listTableEPPG,rowNumEPP = getATMProblem(tableEPPG,"G","EPP",rowNumEPP)
listTableEPPNG,rowNumEPP = getATMProblem(tableEPPNG,"NG","EPP",rowNumEPP)

#Get Dispenser Failure table (DF)
alamatURLDF5 = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobdf1.pl?REGID=15&ERROR=DISP_ST'
alamatURLDF16 = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobdf3.pl?REGID=15&ERROR=DISP_ST'
alamatURLDF615 = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobdf2.pl?REGID=15&ERROR=DISP_ST'

tableDF5 = getLargestTable(getTableList(fetchHTML(alamatURLDF5)))
tableDF615 = getLargestTable(getTableList(fetchHTML(alamatURLDF615)))
tableDF16 = getLargestTable(getTableList(fetchHTML(alamatURLDF16)))

listTableDF16,rowNumDF = getATMProblem(tableDF16,">=16","DF",rowNumDF)
listTableDF615,rowNumDF = getATMProblem(tableDF615,"6-15","DF",rowNumDF)
listTableDF5,rowNumDF = getATMProblem(tableDF5,"<=5","DF",rowNumDF)

#Get Offline table (OFF)
alamatURLOFF = 'http://atmpro.bri.co.id/statusatm/viewbyoffline.pl?REGID=15&ERROR=DOWN_ST'
tableOFF = getLargestTable(getTableList(fetchHTML(alamatURLOFF)))
listTableOFF,rowNumOFF = getATMProblem(tableOFF,"-","OFF",rowNumOFF)

#Get Cash Low table (CL)
alamatURLCL = 'http://atmpro.bri.co.id/statusatm/viewbyregionprob.pl?REGID=15&ERROR=CSHLOW_ST'
tableCL = getLargestTable(getTableList(fetchHTML(alamatURLCL)))
listTableCL,rowNumCL = getATMProblem(tableCL,"-","CL",rowNumCL)


#Get Cash Out table (CO)
alamatURLCO5 = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobco1.pl?REGID=15&ERROR=CSHOUT_ST_1'
alamatURLCO615 = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobco2.pl?REGID=15&ERROR=CSHOUT_ST_2'
alamatURLCO16 = 'http://atmpro.bri.co.id/statusatm/viewbyregionprobco3.pl?REGID=15&ERROR=CSHOUT_ST_3'

tableCO16 = getLargestTable(getTableList(fetchHTML(alamatURLCO16)))
tableCO615 = getLargestTable(getTableList(fetchHTML(alamatURLCO615)))
tableCO5 = getLargestTable(getTableList(fetchHTML(alamatURLCO5)))

listTableCO16,rowNumCO = getATMProblem(tableCO16,">=16","CO",rowNumCO)
listTableCO615,rowNumCO = getATMProblem(tableCO615,"6-15","CO",rowNumCO)
listTableCO5,rowNumCO = getATMProblem(tableCO5,"<=5","CO",rowNumCO)

#set existing data into inactive
#setATMProblemDataInactive(setinactive_qry)

#move data table into history table
moveDatatoHistoryTable(movedata_qry)
#delete all data in master table
truncateDataTable(truncate_qry)

if (insertTableIntoDB(listTableNOPG,add_nopg_qry) and insertTableIntoDB(listTableNOPNG,add_nopg_qry)):
    print("tabel NOP berhasil disimpan")
else :
    berhasil = False
    print('tabel NOP gagal disimpan')
        
if (insertTableIntoDB(listTableRSKG,add_nopg_qry) and insertTableIntoDB(listTableRSKNG,add_nopg_qry)):
    print("tabel RSK berhasil disimpan")
else :
    berhasil = False
    print('tabel RSK gagal disimpan')
        
if (insertTableIntoDB(listTableOPS,add_nopg_qry)):
    print("tabel OPS berhasil disimpan")
else :
    berhasil = False
    print('tabel OPS gagal disimpan')
        
if (insertTableIntoDB(listTableOOSG,add_nopg_qry) and insertTableIntoDB(listTableOOSNG,add_nopg_qry)):
    print("tabel OOS berhasil disimpan")
else :
    berhasil = False
    print('tabel OOS gagal disimpan')
        
if (insertTableIntoDB(listTableCRG,add_nopg_qry) and insertTableIntoDB(listTableCRNG,add_nopg_qry)):
    print("tabel CR berhasil disimpan")
else :
    berhasil = False
    print('tabel CR gagal disimpan')
    
if (insertTableIntoDB(listTableEPPG,add_nopg_qry) and insertTableIntoDB(listTableEPPNG,add_nopg_qry)):
    print("tabel EPP berhasil disimpan")
else :
    berhasil = False
    print('tabel EPP gagal disimpan')
    
if (insertTableIntoDB(insertTableIntoDB(listTableDF16,add_nopg_qry) and listTableDF615,add_nopg_qry) and insertTableIntoDB(listTableDF5,add_nopg_qry)):
    print("tabel DF berhasil disimpan")
else :
    berhasil = False
    print('tabel DF gagal disimpan')
        
if (insertTableIntoDB(listTableOFF,add_nopg_qry)):
    print("tabel OFF berhasil disimpan")
else :
    berhasil = False
    print('tabel OFF gagal disimpan')
    
if (insertTableIntoDB(listTableCL,add_nopg_qry)):
    print("tabel CL berhasil disimpan")
else :
    berhasil = False
    print('tabel CL gagal disimpan')
    
if (insertTableIntoDB(listTableCO16,add_nopg_qry) and insertTableIntoDB(listTableCO615,add_nopg_qry) and insertTableIntoDB(listTableCO5,add_nopg_qry)):
    print("tabel CO berhasil disimpan")
else :
    berhasil = False
    print('tabel CO gagal disimpan')
