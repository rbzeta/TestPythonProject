#!/usr/bin/python
#=================================================================================#
# (c) Jansen A. Simanullang: fetchAllDataEDCUkerImplementor
# 19.05.2015 10:56:27 getTableHeader from thead, getNumRowsFoot and getNumRowsHead
# 01.06.2015 16:36:49 importing urllib2
# 06.11 2015 08:51:58 changing port to 888
#=================================================================================#
from __future__ import division
from urllib.request import urlparse,urlopen
from bs4 import BeautifulSoup

import os,  time
import urllib, pymysql

#=================================================================================#
# CONFIGURABLE PARAMETER
#=================================================================================#
RegionName = 'JAKARTA 3'
#=================================================================================#


firstURL = 'http://172.18.44.66/edcpro/index.php/main/home/index.php'
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"



def firstVisit(firstURL):

    strHTML = fetchHTML(firstURL)
    table = getLargestTable(getTableList(strHTML))
    strHTMLTableRows = getSpecificRow(table, getRowIndex(table, RegionName))
    
    soup = BeautifulSoup(strHTMLTableRows)
    rows = soup.findAll('a')
    alamatURL = str(rows[0].get('href'))

    return alamatURL



def welcomeScreen():

    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

    print ("NOTIFIKASI EDC UKER \n\n\n")


def fetchHTML(alamatURL):

    #print "fetching HTML from URL...\n", alamatURL
    #strHTML = urlopen(urllib.request(alamatURL, headers={ 'User-Agent': 'Mozilla/5.0' })).read()
    strHTML = urlopen(alamatURL).read().decode("ISO-8859-1")
    #strHTML = strHTML.decode("windows-1252")

    strHTML = strHTML.encode('ascii', 'ignore')
    #mysoup = BeautifulSoup(strHTML)
    
    #print ">> URL fetched."

    return strHTML



def getStyleList(strHTML):

    #print "\ngetting Style List...\n"

    mysoup = BeautifulSoup(strHTML)

    arrStyle = mysoup.findAll('link', rel = "stylesheet" )

    strStyle = ""

    for i in range (0, len(arrStyle)):

        strStyle = strStyle + str(arrStyle[i])
    
    return strStyle



def getTableList(strHTML):

    #print "\ngetting Table List...\n"

    mysoup = BeautifulSoup(strHTML)

    arrTable = mysoup.findAll('table')

    #print "there are:", len(arrTable), "tables."
    
    return arrTable



def getLargestTable(arrTable):

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

    if table:
        print (">> the largest from table list is chosen.")

    return table



def getNumCols(table):

    # bagaimana cara menentukan berapa jumlah kolomnya?

    soup = BeautifulSoup(str(table))

    numCols = len(soup.findAll('tbody')[0].findAll('tr')[0].findAll('td'))

    #print "number of columns is", numCols

    return numCols



def getNumRows(table):

    # bagaimana cara menentukan berapa jumlah kolomnya?

    numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
    
    return numRows



def getNumRowsHead(table):

    # bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai header?

    soup = BeautifulSoup(str(table))
    head = soup.findAll('thead')

    numRowsHead = 0

    for i in range (0, len(head)):

        numRowsHead += len(head[i].findAll('tr'))

    #print "there is", len(head), "header with", numRowsHead, "rows"
        
    return numRowsHead



def getNumRowsFoot(table):

    # bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai footer?

    soup = BeautifulSoup(str(table))
    foot = soup.findAll('tfoot')

    numRowsFoot = 0

    for i in range (0, len(foot)):

        numRowsFoot += len(foot[i].findAll('tr'))

    #print "there is", len(foot), "footer with", numRowsFoot, "rows"
        
    return numRowsFoot



def getTableDimension(table):
    
    numRows = getNumRows(table)
    numRowsHead = getNumRowsHead(table)
    numCols = getNumCols(table)
    
    return numRows, numRowsHead, numCols



def getSpecificRow(table, rowIndex):

    print ("Let's take a look at the specific rows of index", rowIndex)

    soup = BeautifulSoup(str(table))
    rows = soup.findAll('tr')
    strHTMLTableRows = ""

    for i in range (rowIndex, rowIndex+1):

        strHTMLTableRows = str(rows[i])
    
    return strHTMLTableRows



def getRowIndex(table, strSearchKey):

    # fungsi ini untuk mendapatkan nomor indeks baris yang mengandung satu kata kunci

    soup = BeautifulSoup(str(table))
    rows = soup.findAll('tr')
    
    numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))

    rowIndex = 0

    for i in range (0, numRows):

        trs = BeautifulSoup(str(rows[i]))
        tdcells = trs.findAll("td")
            
        for j in range (0, len(tdcells)):

            if tdcells[j].getText().upper() == strSearchKey.upper():
                
                rowIndex = i

                print ("we got the index = ", rowIndex, "from ", numRows, "for search key ='"+strSearchKey+"'")
    return rowIndex



def getSpecificRows(table, rowIndex):

    print ("Let's take a look at the specific rows of index", rowIndex)

    soup = BeautifulSoup(str(table))
    rows = soup.findAll('tr')
    strHTMLTableRows = ""

    for i in range (rowIndex, rowIndex+1):

        strHTMLTableRows = str(rows[i])
    
    return strHTMLTableRows



def prepareDirectory(strOutputDir):
    # siapkan struktur direktori untuk penyimpanan data
    # struktur direktori adalah ['OUTPUT', 'EDC', '2015', '04-APR', 'DAY-28'] makes './OUTPUT/EDC/2015/04-APR/DAY-28'

    arrDirectoryStructure = [strOutputDir, 'EDC', time.strftime("%Y"), time.strftime("%m-%b").upper() , "DAY-"+time.strftime("%d")]

    fullPath = scriptDirectory

    for i in range (0, len(arrDirectoryStructure)):
    
        fullPath = fullPath + arrDirectoryStructure[i] + "/"

        if not os.path.exists(fullPath):

            print ("creating directories:", arrDirectoryStructure[i])
            os.mkdir(fullPath)
            os.chdir(fullPath)

    print (fullPath)

    return fullPath



def fileCreate(strNamaFile, strData):
    f = open(strNamaFile, "w")
    f.writelines(str(strData))
    f.close()


    
def fileAppend(strNamaFile, strData):
    f = open(strNamaFile, "a")
    f.writelines(str(strData))
    f.close()


def makeFileName(alamatURL):
    # makes title of a section based on a URL

    strFileName = getQueryContent(alamatURL, "peruntukkan")

    statusAvail = getQueryContent(alamatURL, "status_available")

    if statusAvail == '5':

        strFileName = strFileName + " NOP LEBIH 30 HARI"

    if statusAvail == '4':

        strFileName = strFileName + " NOP 16-30 HARI"

    strFileName = "[" + strFileName + "]"
    # embraced by a parentheses

    return strFileName


def prepareHTMLFile(alamatURL):

    strNamaFile = makeFileName(alamatURL)

    strHTML = fetchHTML(alamatURL)

    arrTable = getTableList(fetchHTML(alamatURL))

    table = getLargestTable(arrTable)

    #NamaKanca = BeautifulSoup(getSpecificRows(table, 2)).findAll('td')[9]

    print ("preparing HTML file as canvas...", strNamaFile, "\n")

    strHTML = '<HTML><HEAD><TITLE>MONITORING EDC '+ RegionName +'</TITLE>' + getStyleList(strHTML) + '</HEAD><body>'

    strHTML += "<h5>" +strNamaFile + " - " + RegionName + "</h5>---fetched " + time.strftime("%d.%m.%Y - %H:%M:%S") + "---"

    strHTML += '<table class="tabledata">' + getTableHeader(table)

    strNamaFile = prepareDirectory('OUTPUT') + strNamaFile + ".html"
    #strNamaFile = "D:\RobynWorks\Google Drive\Projects\eclipse\TestPythonProject\src\OUTPUT\EDC\2016\06-JUN\DAY-28\[UKER NOP 16-30 HARI].html"
    fileCreate(strNamaFile, strHTML)

    return strNamaFile



def updateHTMLFile(alamatURL):

    strNamaFile = makeFileName(alamatURL)

    #strHTML = fetchHTML(alamatURL)

    arrTable = getTableList(fetchHTML(alamatURL))

    table = getLargestTable(arrTable)

    strHTMLTableContents =  getTableContents(table)
        
    strHTML = strHTMLTableContents

    strNamaFile = prepareDirectory('OUTPUT') + strNamaFile + ".html"

    fileAppend(strNamaFile, strHTML)

    return strNamaFile



def finaleHTMLFile(alamatURL):

    strNamaFile = makeFileName(alamatURL)

    #strHTML = fetchHTML(alamatURL)

    arrTable = getTableList(fetchHTML(alamatURL))

    table = getLargestTable(arrTable)
    numRowsHead = getNumRowsHead(table)
    numRows =getNumRows(table)
    if ((numRows-numRowsHead) > 1):
        numCols = getNumCols(table)
    else :
        numCols = 0
    strHTML = '<tfoot><th colspan="'+str(numCols)+'">***</th></tfoot></table>'

    strNamaFile = prepareDirectory('OUTPUT') + strNamaFile + ".html"

    fileAppend(strNamaFile, strHTML)

    return strNamaFile



def getTableHeader(table):

    #numRowsHead = getNumRowsHead(table)

    soup = BeautifulSoup(str(table))
    head = soup.findAll('thead')
    strHTMLTableHeader = ""
    
    for i in range (0, len(head)):

        strHTMLTableHeader = strHTMLTableHeader + str(head[i])
    
    return strHTMLTableHeader



def getTableContents(table):

    numRows = getNumRows(table)
    numRowsHead = getNumRowsHead(table)
    numRowsFoot = getNumRowsFoot(table)

    soup = BeautifulSoup(str(table))
    rows = soup.findAll('tr')
    strHTMLTableContents = ""

    for i in range (numRowsHead, numRows-numRowsFoot):

        strHTMLTableContents = strHTMLTableContents + str(rows[i])

    return strHTMLTableContents



def getColIndex(table, strSearchKey1, strSearchKey2):

    # fungsi ini untuk mendapatkan nomor indeks kolom yang mengandung satu kata kunci

    numCols = getNumCols(table)
    #numRowsHead = getNumRowsHead(table)

    soup = BeautifulSoup(str(table))
    rows = soup.findAll('tr')

    colIndex1 = -1

    for i in range (0, 1):

        trs = BeautifulSoup(str(rows[i]))
        thcells = trs.findAll("th")
            
        for i in range (0, len(thcells)):

            if ("colspan" in str(thcells[i]) and thcells[i].findAll('a')[0].getText().upper() == strSearchKey1.upper()):

                intColSpan = int(thcells[i]['colspan'])

                print (i, intColSpan)

                colIndex1 = (i-1) * intColSpan + 1

                
            elif ("rowspan" in str(thcells[i]) and thcells[i].getText().upper() == strSearchKey1.upper()):

                intColSpan = 1

                colIndex1 = (i-1) * intColSpan + 1 

                print (i, "rowspan")
    #colIndex2 = 0
    for i in range (1, 2):
                    
        soup = BeautifulSoup(str(rows[i]))
        thcells2 = soup.findAll("th")

        # the length must be limited to the colindex of the above search
        maxIndex = len(thcells2)
        maxIndex = colIndex1 - 1

        for i in range (0, maxIndex):
        
            if thcells2[i].getText().upper() == strSearchKey2.upper():
                colIndex2 = i+3 # the factor +3 is due to the two columns with the rowspan before
                


                
    print ("we got the col index = (", colIndex1, ") from ", numCols-1, "index for search key ='"+strSearchKey1+"'")
    print ("we got the col index = (", colIndex2, ") from ", numCols-1, "index for search key ='"+strSearchKey2+"'")
    return colIndex2



def getQueryContent(alamatURL, strQuery):
    
    parsed = urlparse(alamatURL)
    QueryContent = str(urllib.parse.parse_qs(parsed.query)[strQuery][0])
    return QueryContent





def clearDirectory(strOutputDir):

    # clear directory from previous call within the same date

    arrDirectoryStructure = [strOutputDir, 'EDC', time.strftime("%Y"), time.strftime("%m-%b").upper() , "DAY-"+time.strftime("%d")]

    fullPath = scriptDirectory

    for i in range (0, len(arrDirectoryStructure)):
    
        fullPath = fullPath + arrDirectoryStructure[i] + "/"

    if os.path.exists(fullPath):

        print ("clearing today's data directory:...\n", fullPath)
        os.system('rm -rf '+ fullPath)


#def fileCreate(strNamaFile, strData):
#    f = open(strNamaFile, "w")
#    f.writelines(str(strData))
#    f.close()


    
#def fileAppend(strNamaFile, strData):
#    f = open(strNamaFile, "a")
#    f.writelines(str(strData))
#    f.close()

def createTextFile(namaFile):
    # create a text file
    print ("preparing text file...", namaFile.split("/")[-1])
    
    strTitle = "NOTIFIKASI EDC " + namaFile.split("/")[-1].replace("_"," ").replace("[","").replace("]","") +"\n"+time.strftime("%d.%m.%Y-%H:%M") + "\n"
    # make a title for this purpose

    fileCreate(namaFile, strTitle)


def updateTextFile(namaFile, strData):
    # update a text file of namaUker with a strData

    strNamaFile = prepareDirectory('OUTPUT') + namaFile
    # make a full file name

    if not os.path.exists(strNamaFile):
    # if the full file name does not exist then create it

        createTextFile(strNamaFile) # try changing this from namaFile to strNamaFile

    print ("updating text file...", namaFile)

    fileAppend(strNamaFile, strData)


def getSectionTitle(alamatURL):
    # makes title of a section based on a URL

    strTitle = getQueryContent(alamatURL, "peruntukkan")

    statusAvail = getQueryContent(alamatURL, "status_available")

    if statusAvail == '5':

        strTitle = strTitle + " NOP > 30 HARI"

    if statusAvail == '4':

        strTitle = strTitle + " NOP 16-30 HARI"

    strTitle = "[" + strTitle + "]\n\n"
    # embraced by a parentheses

    return strTitle



def getLastPageNum(alamatURL):


    strHTML = fetchHTML(alamatURL)

    mysoup = BeautifulSoup(strHTML)

    arrURL = mysoup.findAll('tfoot')[0].findAll('tr')[0].findAll('a')
    
    maxPage = 0

    if arrURL:
        
        for i in range (0, len(arrURL)):

            lastPageNum = int(arrURL[i].get('href').split('/')[7].split('?')[0])

            if lastPageNum > maxPage:

                maxPage = lastPageNum

        lastPageNum = maxPage
        
    else:
        lastPageNum = 0
    print ("last page number is:", lastPageNum)
    return int(lastPageNum)







def getArrURLPages(alamatURL):
    # this function makes an array of URLs
    # based on the last page number

    intLastPage = getLastPageNum(alamatURL)
    arrURL = []

    for i in range (0, int(intLastPage/50+1)):

        arrURL.append(alamatURL.replace("merchant?","merchant/"+str(i*50)+"?"))

    return arrURL



def getURLfromFoot(columnIndex, table):
    # this function gets url form footer in a column 
    # the column position is in index columnIndex

    soup = BeautifulSoup(str(table))
    rows = soup.findAll('tr')

    #numRowsHead =getNumRowsHead(table)
    numRows =getNumRows(table)
    #numRowsFoot =getNumRowsFoot(table)
    
    for i in range(numRows-1, numRows):

        ths = rows[i].findAll('th')[columnIndex]
        # collect all the <th>s that is at the columnIndex

        if ths.findAll('a'):
        # check only <th>s containing <a>
            
            alamatURL = ths.findAll('a')[0].get('href')
            # save the 'href' content as alamatURL

    return alamatURL


def getUkerImplementor(alamatURL):

    strHTML = fetchHTML(alamatURL)
    arrTable = getTableList(strHTML)
    # get all the table and display in a list

    for i in range (0, len(arrTable)):

        if "Implementor" in str(arrTable[i]):
        # if a keyword 'Implementor' is in the table

            indexTable = i
            # then index table that contains the keyword is 'i'

    table = arrTable[indexTable]
    # we choose only the table that matches our criteria at the index
        
    strHTMLTableRows = getSpecificRow(table, getRowIndex(table, "Sub Channel"))
    # we choose the specific row contains the keyword 'Sub Channel'

    mysoup = BeautifulSoup(strHTMLTableRows)
    # make a soup from the table row

    arrTDs = mysoup.findAll('td')
    # collect all the <td>s in an array

    strSubChannel = arrTDs[1].getText().strip()
    # save the text of the data

    strHTMLTableRows = getSpecificRow(table, getRowIndex(table, "Implementor"))
    # we choose the specific row contains the keyword 'Implementor'

    mysoup = BeautifulSoup(strHTMLTableRows)
    # make a soup from the table row

    arrTDs = mysoup.findAll('td')
    # collect all the <td>s in an array

    strImplementor = arrTDs[1].getText().upper().strip()
    # save the text of the data

    if not strImplementor:
    # if strImplementor is empty, which is almost all in the BRILINK NOP data

        strHTMLTableRows = getSpecificRow(table, getRowIndex(table, "Kanwil Implementor"))
        # we choose the specific row contains the keyword 'Implementor'

        mysoup = BeautifulSoup(strHTMLTableRows)
        # make a soup from the table row

        arrTDs = mysoup.findAll('td')
        # collect all the <td>s in an array

        strImplementor = arrTDs[1].getText().upper().strip()

    return strSubChannel, strImplementor



def getArrNamaUker():

    fName = scriptDirectory +"conf/branchCode.888"
        
    f = open(fName)

    branchLine = f.readlines()


    arrNamaUker = ['']*(len(branchLine)-1)

    for i in range(0, len(arrNamaUker)-1):

        arrNamaUker[i] = branchLine[i].replace("\n","").split("|")[1]
        
    return arrNamaUker



def getArrKodeUker():

    fName = scriptDirectory +"conf/branchCode.888"
        
    f = open(fName)

    branchLine = f.readlines()


    arrKodeUker = ['']*(len(branchLine)-1)

    for i in range(0, len(arrKodeUker)-1):

        arrKodeUker[i] = branchLine[i].replace("\n","").split("|")[0]
        
    return arrKodeUker




def createNSendTelegramTextFiles(strNamaFile):

    EDCTitle = strNamaFile.split("/")[-1].split(".")[0].replace(" ","_")

    arrNamaUker = getArrNamaUker()

    arrNumEDC = [0]*(len(arrNamaUker)+4)
    
    strHTML = fetchHTML("file://"+strNamaFile)
    table = getLargestTable(getTableList(strHTML))

    soup = BeautifulSoup(str(table))
    rows = soup.findAll('tr')

    numRows = len(rows)
    numRowsHead = getNumRowsHead(table)
    numRowsFoot = getNumRowsFoot(table)

    print ("numRowsHead=", numRowsHead)
    print ("numRows=",numRows)

    #============================================================================================
    # this process data of EDC in this topic

    if numRowsHead == numRows-numRowsFoot:

        textEDC = ">>NO EDC NOP IN THIS CATEGORY<<"

    else:
        textEDC = ""
        strSubChannel = ""


        for j in range (numRowsHead, numRows-numRowsFoot):

            print ("loop ke-", j)

            tds = rows[j].findAll('td')

            linkTID = tds[2].findAll('a')[0].get('href')
            
            try:
                strSubChannel, strImplementor = getUkerImplementor(linkTID)

            except UnboundLocalError:
                
                strImplementor = tds[9].getText().upper().strip()


            namaUker = tds[9].getText().upper()
            namaUker = cleanupNamaUker(namaUker)

            if namaUker == "":

                namaUker = tds[7].getText().upper()
                namaUker = cleanupNamaUker(namaUker)

            if (("UNIT " in namaUker) or ("KCP " in namaUker) or ("KK " in namaUker)):

                namaUker = cleanupNamaUker(strImplementor)

            if namaUker not in arrNamaUker:

                arrNamaUker.append(namaUker)
                indexUker = arrNamaUker.index(namaUker)

            else:

                indexUker = arrNamaUker.index(namaUker)
            # find the index

                arrNumEDC[indexUker] = arrNumEDC[indexUker] + 1
                # increment the array
                
                if arrNumEDC[indexUker] == 1:

                    strTitle = "\n" + getNamaFileOnly(strNamaFile) + "\n"
                    updateTextFile(EDCTitle+"-"+namaUker.replace(" ","_"), strTitle)

            


            print ("\n\nindexUker = ", indexUker)
            print ("len(arrNumEDC) = ", len(arrNumEDC), "\n\n")
        

            textEDC = str(arrNumEDC[indexUker-1]) + ") " + tds[2].getText()+" "+tds[3].getText()
            
            strImplementor = cleanupNamaUker(strImplementor).replace("JAKARTA 3", "")

            if (namaUker in strImplementor.upper()):

                strImplementor = ""

            if ((strImplementor) and ("KANWIL" not in strImplementor)):

                textEDC += ", "+strImplementor

            strSubChannel = cleanupNamaUker(strSubChannel).replace("JAKARTA 3", "")

            if (namaUker in strSubChannel.upper()):

                strSubChannel = ""

            if ((strSubChannel) and ("KANWIL" not in strSubChannel)):

                textEDC += " ("+strSubChannel+")"

            if tds[10].getText().split(" ")[0]:

                textTrx = " (Trx="+tds[10].getText().split(" ")[0]+")"
            else:
                textTrx = ""

            textEDC += textTrx + "\n"
            print ("\n\nnama uker = ", namaUker)
            updateTextFile(EDCTitle+"-"+namaUker.replace(" ","_"), textEDC)

    #============================================================================================
    NotifikasiEDC(EDCTitle)
    #============================================================================================

def getNamaFileOnly(strNamaFile):
        
    strNamaFileOnly = strNamaFile.split("/")[-1].split(".")[0]
    return     strNamaFileOnly

def cleanupNamaUker(namaUker):


    namaUker = namaUker.replace("JAKARTA","")
    namaUker = namaUker.replace("Jakarta ","")
    namaUker = namaUker.replace("JKT","")
    namaUker = namaUker.replace("KANCA ","")
    namaUker = namaUker.replace("KC ","")

    if ("KANWIL" in namaUker or "3" in namaUker):

        namaUker = RegionName

    return namaUker.strip()



def mergePages(alamatURL):
    # merge pages into one file

    strNamaFile = prepareHTMLFile(alamatURL)
    
    arrURL = getArrURLPages(alamatURL)

    print ("updating HTML file: ", strNamaFile)

    for i in range(0, len(arrURL)):

        updateHTMLFile(arrURL[i])

    finaleHTMLFile(alamatURL)

    return strNamaFile

    
def sendTextTelegram(telegramName, strNamaFile):

    telegramCommand = 'echo "send_text '+telegramName+' '+strNamaFile+'" | nc 127.0.0.1 8885'
    print (telegramCommand)
    os.system(telegramCommand)
    
    #telegramName = 'Jansen_Simanullang'
    #os.system('echo "send_text Jansen_Simanullang '+strNamaFile+'" | nc 127.0.0.1 888')
    #sendTextTelegram(telegramName, strNamaFile)

def TelegramCLISender(telegramName, strNamaFile):

    #telegramCommand = 'echo "send_text '+telegramName+' '+strNamaFile+'" | nc 127.0.0.1 8885'
    telegramCommand = 'proxychains telegram-cli -W -e "send_text '+telegramName+' '+strNamaFile+'"'
    print (telegramCommand + "\n")
    os.system(telegramCommand)
    
    #telegramName = 'Jansen_Simanullang'
    #os.system('echo "send_text Jansen_Simanullang '+strNamaFile+'" | nc 127.0.0.1 888')
    #TelegramCLISender(telegramName, strNamaFile)



def TelegramBotSender(chat_id, strText):

    secretKey = "115651882:AAGDNzHXwLKNqOWmHWC8vMXg-Vy_fZD0350"

    #encText=urllib.parse.quote_plus(strText)

    strURL = "https://api.telegram.org/bot"+secretKey+"/sendMessage?chat_id="+chat_id+"&text="+urllib.parse.quote_plus(strText)

    os.system('proxychains w3m -dump "'+ strURL+'"')





def readTextFile(strNamaFile):

    fText = open(strNamaFile)

    strText = ""
                    
    for baris in fText.readlines():

        strText += baris

    fText.close()

    return strText


def readBranchCode():

    arrBranchCode = []
    arrBranchName = []

    fName = scriptDirectory +"conf/branchCode.888"
        
    f = open(fName)

    for baris in f.readlines():

        col = baris.strip().split("|")
        arrBranchCode.append(col[0])
        arrBranchName.append(col[1])


    f.close()

    return arrBranchCode, arrBranchName


def NotifikasiEDC(EDCTitle):

    arrNamaUker = getArrNamaUker()

    arrKodeUker = getArrKodeUker()


    for i in range(0, len(arrNamaUker)):
        
        if ("PT." not in arrNamaUker[i]) and ("JAKARTA 3" not in arrNamaUker[i]): 
        # and ("JAKARTA 3" not in arrNamaUker[i])
        # and ("JAKARTA 3" in arrNamaUker[i])

        
            strNamaFile = prepareDirectory('OUTPUT') + EDCTitle + "-" + arrNamaUker[i].replace(" ", "_")
            
            if os.path.exists(strNamaFile):

                print ("SENDING TO UKER = ", arrNamaUker[i])
                #distList = scriptDirectory +"conf/EDCRecipients.888"

                #f = open(distList)

    
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='br1j4k4rt43', db='mantel')

                cur = conn.cursor()

                if "MERCHANT" in EDCTitle:

                    cur.execute('select telegram_id from notif2 where branchcode like "'+arrKodeUker[i]+'" and active="1"')

                if "BRILINK" in EDCTitle:

                    cur.execute('select telegram_id from notif3 where branchcode like "'+arrKodeUker[i]+'" and active="1"')

                if "UKER" in EDCTitle:

                    cur.execute('select telegram_id from notif4 where branchcode like "'+arrKodeUker[i]+'" and active="1"')

                

                strText = readTextFile(strNamaFile)

                print ("\n--------------------------------------------------\n")

                for row in cur:

                    telegram_id =(row[0])
                    #------------------------------------
                    # only for verbose debugging purpose
                    kur = conn.cursor()
                    kur.execute('select telegram_name from mantab where telegram_id="'+telegram_id+'"')

                    for baris in kur:

                        telegram_name = baris[0]

                    kur.close()
                    #print "chat_id", chat_id
                    #------------------------------------

                    print (arrNamaUker[i]+"--->: "+ telegram_name + "            \r")
                    #print readTextFile(strNamaFile)

                    TelegramBotSender(telegram_id, strText)

                    #print "CHAT ID = "+chat_id+ " TELEGRAM NAME = "+telegramName

                cur.close()
                conn.close()





                #f.close()

def main():

    clearDirectory('OUTPUT')

    #alamatURL = firstVisit(firstURL)
    #strHTML = fetchHTML(alamatURL)
    #table = getLargestTable(getTableList(strHTML))

    # [EDC_NOP_UKO]
    alamatURL = 'http://172.18.44.66/edcpro/index.php/detail/merchant?kanwil_implementor=Q&peruntukkan=UKER&status_available=5'
    strNamaFile = mergePages(alamatURL)
    createNSendTelegramTextFiles(strNamaFile)

    # [EDC_NOP_BRILINK]
    alamatURL = 'http://172.18.44.66/edcpro/index.php/detail/merchant?kanwil_implementor=Q&peruntukkan=BRILINKS&status_available=5'
    strNamaFile = mergePages(alamatURL)
    createNSendTelegramTextFiles(strNamaFile)

    # [EDC_NOP_MERCHANT]
    alamatURL = 'http://172.18.44.66/edcpro/index.php/detail/merchant?kanwil_implementor=Q&peruntukkan=MERCHANT&status_available=5'
    strNamaFile = mergePages(alamatURL)
    createNSendTelegramTextFiles(strNamaFile)


main()

