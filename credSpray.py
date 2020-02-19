import random
import math
from time import sleep
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import Select

##############################################################################################################
###---------------------------------------------- CONFIG --------------------------------------------------###
##############################################################################################################
WEBSITE = " " #add url or file path 
EMAILID = "email" #id of the html field where the user inputs email
PASSWORDID = "password" #id of the password field where the user inputs password
SENDID = "submit" #id of the submit button id in html
##############################################################################################################
##############################################################################################################
##############################################################################################################

passwordFile = "fakePasswords.txt"          #random passwords from pastebin
randPasswordFile = "randomPasswords.txt"    #from rockyou.txt
#lastNameFile = "lastNames.txt"             #based on top 1000 last names in the US
#emailFile = "email.txt"                    #@domain.extension, ex '@gmail.com' '@protonmail.com' '@outlook.com'
emailFile = "emailsFiltered.txt"            #using email list
obfuscateEmails = True                      #if using a list of real emails, modify them a bit
testing = False

def main():
    accounts = 50000
    #emails = generateEmailList(accounts) #create random list of emails
    emails = getEmailList(accounts) #use existing list of emails
    passwords = generatePasswordList(accounts)
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\Driver\chromedriver") #Downloaded chromedriver and put it into my chrome installation folder
    driver.get(WEBSITE)
    """ 
    #disable chrome's warning for deceptive content
    safety = driver.find_element_by_id("details-button")
    safety.click()
    safety = driver.find_element_by_id("proceed-link")
    safety.click()
    """
    try:
        for usr,pswrd in zip(emails,passwords):
            #go through form
            emailField = driver.find_element_by_id(EMAILID)
            emailField.send_keys(usr)
            passwordField = driver.find_element_by_id(PASSWORDID)
            passwordField.send_keys(pswrd)
            sendButton = driver.find_element_by_id(SENDID)
            sendButton.click()
            sleepTime = random.uniform(1.0,8.0)
            print("Submitted fake creds:",usr+":"+pswrd," - Waiting",sleepTime,"seconds until next submit")
            ##For 404 error landing page
            driver.back()
            ##For alert redirect
            #todo
            emailField = driver.find_element_by_id(EMAILID)
            emailField.clear()
            passwordField = driver.find_element_by_id(PASSWORDID)
            passwordField.clear()
            sleep(sleepTime)
    except:
        print("Error, restarting")
        driver.close()
        sleep(5)
        main()

#generates emails on a basis of first initial, last name, [number] @ domain.TLD
def genRandomEmailList(num): 
    emails = []
    #last names lines
    ln = open(lastNameFile,'r')
    lnLines = ln.readlines()

    #random emails
    eml = open(emailFile,'r')
    emlLines = eml.readlines()

    for x in range(num):
        #create random email
        #create random first name off weighted dictionary, based on actual first name statistics
        firstName = ''.join(random.choices(
            population = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], #[['a'],['b'],['c'],['d'],['e'],['f'],['g'],['h'],['i'],['j'],['k'],['l'],['m'],['n'],['o'],['p'],['q'],['r'],['s'],['t'],['u'],['v'],['w'],['x'],['y'],['z']],
            weights=[0.06428,0.06796,0.07596,0.08596,0.02976,0.00888,0.02776,0.01354,0.00333,0.12861,0.06530,0.05331,0.08951,0.01377,0.00244,0.03687,0.00044,0.05864,0.08662,0.05108,0.00111,0.00933,0.01666,0.00155,0.00511,0.00222],
            k=1
        ))
        #pick random last name
        lastName = lnLines[random.randint(1,len(lnLines))-1][:-1] #[:-1] to get rid of the \n character
        #generate email domain
        try:
            domain = emlLines[random.randint(1,len(emlLines))-1]
        except (ValueError): #if only one domain needed/present
            domain = emlLines[0]
        #generate random number
        num = random.randint(2,300)
        #generate final email
        if(num<240):
            fakeEmail = firstName + lastName + str(num) + domain
        else:
            fakeEmail = firstName + lastName + domain
        emails.append(fakeEmail)
    eml.close()
    ln.close()
    """
    var setupScript=`var prefs = Components.classes["@mozilla.org/preferences-service;1"]
    .getService(Components.interfaces.nsIPrefBranch);

    prefs.setIntPref("network.proxy.type", 1);
    prefs.setCharPref("network.proxy.http", "${proxyUsed.host}");
    prefs.setIntPref("network.proxy.http_port", "${proxyUsed.port}");
    prefs.setCharPref("network.proxy.ssl", "${proxyUsed.host}");
    prefs.setIntPref("network.proxy.ssl_port", "${proxyUsed.port}");
    prefs.setCharPref("network.proxy.ftp", "${proxyUsed.host}");
    prefs.setIntPref("network.proxy.ftp_port", "${proxyUsed.port}");
                      `;    

    //running script below  
    driver.executeScript(setupScript);

    //sleep for 1 sec
    driver.sleep(1000);
    """
    return(emails)

def getEmailList(num):
    emails = []
    with open(emailFile,'r') as eml:
        emlLines = eml.readlines()
        for x in range(num):
            randNum = random.randint(1,len(emlLines))-1
            email = emlLines[randNum][:-1]
            if(not obfuscateEmails):
                emails.append(email)
            else:
                #print(email,end=" -> ")
                #find @ index and index of first numbers given, as well as length
                atIndex = email.find("@")
                numLength = 0; #length of the numbers in the emails
                if(atIndex<0):
                    #print("Found email with no @:",email,"at line",randNum);
                    continue
                for x in range(1,4): #go backwards from the @ symbol, maximum of 4 numbers
                    try:
                        int(email[atIndex-x])
                        numLength+=1
                    except:
                        break;
                #remove the numbers and replace them with a number within an exponetial range
                if(numLength>0): #if numbers exist
                    num = int(email[atIndex-numLength:atIndex])
                    email = email[:atIndex-numLength] + str(random.randint(1,math.ceil(int(1.5*num)))) + email[atIndex:]
                #replace the first letter of the email
                firstName = ''.join(random.choices(
                    population = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], #[['a'],['b'],['c'],['d'],['e'],['f'],['g'],['h'],['i'],['j'],['k'],['l'],['m'],['n'],['o'],['p'],['q'],['r'],['s'],['t'],['u'],['v'],['w'],['x'],['y'],['z']],
                    weights=[0.06428,0.06796,0.07596,0.08596,0.02976,0.00888,0.02776,0.01354,0.00333,0.12861,0.06530,0.05331,0.08951,0.01377,0.00244,0.03687,0.00044,0.05864,0.08662,0.05108,0.00111,0.00933,0.01666,0.00155,0.00511,0.00222],
                    k=1
                ))
                email = firstName + email[1:]
                #add email to list
                emails.append(email)
    return(emails)


def generatePasswordList(num,weightRandom=0.4):
    passwords=[]
    #password lines
    ps = open(passwordFile,'r')
    psLines = ps.readlines()

    #random password lines
    psr = open(randPasswordFile,'r',encoding='cp850') #rockyou.txt is in cp850, not utf-8
    psrLines = psr.readlines()

    for x in range(num):
        choice = random.randint(1,100)-1
        if(choice < weightRandom*100):
            pswd = psLines[random.randint(1,len(psLines))-1]
        else:
            pswd = psrLines[random.randint(1,len(psrLines))-1]
        passwords.append(pswd[:-1]) #[:-1] removes the newline character
    ps.close()
    psr.close()
    return(passwords)


if(not testing):
    main()    
