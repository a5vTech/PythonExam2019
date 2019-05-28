import sys, os, re
from urllib.request import urlopen
global baseUrl
baseUrl = 'https://clbokea.github.io/exam/'
global projectName
projectName = ''



def startProgram():
   gatherInfoFromUser()
# Create project folder
   createProjectFolder(projectName)

# Create files
   links = fetchAllLinksFromBasePage(projectName, baseUrl)
   downloadHtmlFiles(links)
   crawlTheLinks(links)
   fixNestedAtag(links)

# Fetch websites 

pass

def fixNestedAtag(links):
        for link in links:
                print('Current link  :   ' + link )
                mdFile = open(projectName+'\\'+link+'-converted.md','w')
                aTagRegex = "(<a )([a-z-=\" ]+ )(href=\")([a-z-.-_]+)(\">)([a-z-A-Z-0-9 ]+)(</a>)"
                #aTagFixRegex = '(<ahref=\")([a-z-.-_]+)(\">)([a-z-A-Z-0-9 ]+)(</a>)'
                aTagFixRegex = '(<a.*href=\")([a-z-.-_]+)(\">)([a-z-A-Z-0-9 ]+)(</a>)'
                linkRegex = '\[(.+)\]\(([a-z._0-9\/:]+)\)'
                file = open(projectName+'\\'+link+'.md')
                for line in file:
                        if(re.search(linkRegex, line)):
                                print('FOUND' + line)
                                if(re.search(linkRegex,line).group(2)[0:4] != 'http'):
                                        mdFile.write('['+re.search(linkRegex, line).group(1)+']('+ baseUrl+ re.search(linkRegex,line).group(2)+')\n')

                        if re.search(aTagRegex, line):
                                lineToWrite = '['+re.search(aTagRegex, line).group(6)+']('+ re.search(aTagRegex,line).group(4)+')\n'
                                
                                if(re.search(linkRegex, lineToWrite) and re.search(linkRegex,lineToWrite).group(2)[0:4] != 'http'):
                                        lineToWrite = '['+re.search(linkRegex, lineToWrite).group(1)+']('+ baseUrl+ re.search(linkRegex,lineToWrite).group(2)+')\n'

                                mdFile.write(lineToWrite)
                                 #mdFile.write('['+re.search(aTagRegex, line).group(6)+']('+ re.search(aTagRegex,line).group(4)+')\n')
                        elif re.search(aTagFixRegex, line):
                                mdFile.write('['+re.search(aTagFixRegex, line).group(4)+']('+ re.search(aTagFixRegex,line).group(2)+')\n')
                        else:
                                mdFile.write(line)
                        
                file.close()

                os.remove(projectName+'\\'+link+'.md')                     
        pass


def gatherInfoFromUser():
        print('+----------------------------------------------------------+')
        print('|          Welcome to Leaders WEB crawler                  |')
        print('|          I will convert html to Markdown                 |')
        print('+----------------------------------------------------------+')
        global projectName
        projectName = input('Please provide a name for  your project: ')
        print('You have chosen the name: \"'+ projectName + '\" for your project')
        print('Would you like to use the test url or provide your own?')
        answer = input('(y/n): ')
        if answer == 'n':
                global baseUrl
                baseUrl = input('Please input url of website: ')
        
    

def fetchAllLinksFromBasePage(project, baseUrl):
        listOfLinks = set()

        print('Fetching data')
        basePage = urlopen(baseUrl)
        html = basePage.read().decode('utf-8')
        createBasePageTxt(project, html)
        
        file = open(project+'\\basePage.txt','r')
        for line in file:
                if '<a ' in line:
                        hrefIndex = line.find('href')

                        if(hrefIndex >0):
                                tempLine = line[hrefIndex+6:]
                                quoteIndex = tempLine.find('"')
                                # Start index from address
                                link = tempLine[:quoteIndex]
                                if (link[0]  != '#'):
                                        listOfLinks.add(link)
        #print(listOfLinks)
        return listOfLinks



def createBasePageTxt(project, html):
        file = open(project+'\\basePage.txt', 'w')
        file.write(html)
        file.close

def createProjectFolder(projectDirectory):
    if not (os.path.exists(projectDirectory)):
        print('Making project folder for: ' + projectDirectory)
        os.makedirs(projectDirectory)


def crawlTheLinks(links):
        for link in links:
                print('Current link  :   ' + link )
                mdFile = open(projectName+'\\'+link+'.md','w')
                aTagRegex = "(<a )([a-z-=\" ]+ )(href=\")([a-z-.-_]+)(\">)([a-z-A-Z-0-9 ]+)(</a>)"
                #h1TagRegexClass = "(?s)(<h1.+>)(.+?)(</h1>)"
                h1TagRegex = "(?s)(<h1.*?>)(.+?)(</h1>)"
                h2TagRegex = "(?s)(<h2.*?>)(.+?)(</h2>)"
                h3TagRegex = "(?s)(<h3.*?>)(.+?)(</h3>)"
                pTagRegex = "(?s)(<p.*?>)(.+?)(</p>)"
                liTagRegex = "(<li[a-z> =\"]+)([a-z-A-Z ]+)(</li>)"   
                aTagFixRegex = '(<a.*href=\")([a-z-.-_]+)(\">)([a-z-A-Z-0-9 ]+)(</a>)'
    
                file = open(projectName+'\\'+link+'.txt')
                for line in file:
                        strippedLine = line.strip() # Removes whitespace
                        if('<p' in strippedLine and '<pre' not in strippedLine):
                                templine = ''        
                                if '<p' in strippedLine and '</p>' in strippedLine:
                                        endofStartTagIndex = strippedLine.find('>')
                                        mdFile.write(strippedLine[endofStartTagIndex+1:-4]+"\n")
                                else:
                                        endofStartTagIndex = strippedLine.find('>')

                                        templine += strippedLine[endofStartTagIndex+1:]
                                        for line2 in file:
                                                if '</p>' in line2.strip():
                                                        templine+= line2.strip()[:-4]
                                                        break
                                                else:
                                                        templine+= line2.strip()
                                        if(re.search(aTagRegex, templine)):
                                                tempLine = '['+re.search(aTagRegex, tempLine).group(6)+']('+ re.search(aTagRegex, tempLine).group(4)+')'
                                        mdFile.write(templine+"\n")

                                        pass
                        if('<li' in strippedLine and '<link' not in strippedLine):
                                templine = ''
                                if('<li' in strippedLine and '</li>' in strippedLine):
                                        endofStartTagIndex = strippedLine.find('>')
                                        mdFile.write('- '+strippedLine[endofStartTagIndex+1:-5]+"\n")
                                       # print(strippedLine)
                                else:
                                        endofStartTagIndex = strippedLine.find('>')
                                        templine += '- '+strippedLine[endofStartTagIndex+1:]
                                        for line2 in file:
                                                if '</li>' in line2.strip():
                                                        templine+= line2.strip()[:-5]
                                                        break
                                                else:
                                                        templine+= line2.strip()
                                        mdFile.write(templine+"\n")

                        
                        if(re.search(h1TagRegex, strippedLine)):
                                mdFile.write("# "+re.search(h1TagRegex,strippedLine).group(2)+"\n")
                        if(re.search(h2TagRegex, strippedLine)):
                                mdFile.write('## '+ re.search(h2TagRegex, strippedLine).group(2)+"\n")
                        if(re.search(h3TagRegex, strippedLine)):
                                mdFile.write('### '+ re.search(h3TagRegex, strippedLine).group(2)+"\n")



                
                                
                                


                                
               # break                      
                        
                
                #print('\n\n\n')


               # print('REGES TESTING: ')
               # file.close()
               # file = open(projectName+'\\'+link+'.txt')
               # aTagRegex = "(<a )([a-z-=\"]+ )(href=\")([a-z-.-_]+)(\">)"
               # aTagRegex = "(<a )([a-z-=\"]+ )(href=\")([a-z-.-_]+)(\">)([a-z-A-Z-0-9 ]+)(</a>)"
               # for l in file: 
               #         if (re.search(aTagRegex, l)):
               #                 print(re.search(aTagRegex, l).group(4))
        pass


def downloadHtmlFiles(links):
        for link in links:
                page = open(projectName + '\\'+link+'.txt' ,'w')
                page.write(urlopen(baseUrl+link).read().decode('utf-8'))
                page.close   

if __name__ == "__main__":
    startProgram()