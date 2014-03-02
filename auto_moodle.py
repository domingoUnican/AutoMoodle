# coding: UTF-8
# -*- coding: utf-8 -*-
__author__="David Perera Barreda"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

import time, re, os, shutil
import argparse
import mechanize

import ply.yacc as yacc

from CLexer import Lexico

PAT=re.compile('mce_[0-9]+_ifr',re.DOTALL|re.M) #Search for the frame when writting a document
PAT_WEB=re.compile('http:[a-zA-Z0-9?=\/\.]+assignsubmission_file/submission_files[a-zA-Z0-9\/?=\.]+')

TEMPDIR = os.path.abspath('tmp')#Temp Dir

def axml(s):
    return s.decode('utf-8').encode('ascii','xmlcharrefreplace')
class Sintactico:

    tokens = Lexico.tokens
    start = 'file'
    br = mechanize.Browser()

    def p_file(self,p):
        """
        file : Options Units
        """
        print "ALL Units processed"
        self.driver.quit()

    def p_options(self, p): #If only username is provided, password must be taken from the initial params
                            #Allowing password without username, does not make any sense
        """
        Options : OptionUsername OptionPassword OptionCourse
                | OptionUsername OptionPassword
                | OptionUsername OptionCourse
                | OptionCourse
                |
        """
        print "ALL Options processed\n"
        self.selenium_initialization()

    def p_optionUsername(self, p):#TODO: If the username has not been provided in the text file, and in the command line, then a message has to appear without waiting 15secs
        """
        OptionUsername : USERNAME COLON STRING
        """
        optionUsername=p[3]
        if self.user=="": #command line input prevails
            self.user=optionUsername

        if self.user == "":
            print "You need to specify the Username\nfinishing..."
            self.driver.quit()
        print "OptionUsername with Username='"+self.user+"' processed\n"

    def p_optionPassword(self, p):#TODO: If the password has not been provided in the text file, and in the command line, then a message has to appear without waiting 15secs
        """
        OptionPassword : PASSWORD COLON STRING
        """
        if self.password=="":
            self.password=p[3]

        if self.password == "":
            print "You need to specify the Password\nfinishing..."
            self.driver.quit()

        print "OptionPassword processed\n"

    def p_optionCourse(self, p):#TODO: If the course has not been provided in the text file, and in the command line, then a message has to appear without waiting 15secs
        """
        OptionCourse : COURSE COLON STRING
        """
        optionCourse=p[3]
        if self.course=="":
            self.course=optionCourse
        if self.course == "":
            print "You need to specify the name of the Course\nfinishing..."
            varURL = args.url
            self.driver.quit()
        print "OptionCourse with Course='"+self.course+"' processed\n"

    def p_units(self,p):
        """
        Units : Unit
              | Unit Units
        """

    def p_unit(self,p):
        """
        Unit : EQUALS NUMBER DATESEPARATOR STRING EQUALS ManyLineString Components
             | EQUALS NUMBER DATESEPARATOR STRING EQUALS ManyLineString
        """
        unitNumber=p[2]# unit number BY POSITION in moodle
        unitName=p[4]
        unitDescription=axml(p[6])

        #TODO: If the unit is not new, then we can skip the Name and Description, if the user
        #adds the name and/or description, we update it, otherwise we maintain the previus name and/or description,
        #this is a quick way of adding more components to a course without repeating the name,
        #but also permits to update the name and description of the courses
        #If the unit is not new, of course it needs to have a name, the description could be blank

        newUnit = True#True if the unit is new, false if already exists (and thus, we are going to update it)
        if self.selenium_existsUnit(unitNumber):
            #The unit alredy exists, so we are updating the unit
            newUnit = False
            print "Unit with number = "+str(unitNumber)+" already exists, updating\n"

        self.selenium_addOrUpdateUnit(unitNumber,unitName,unitDescription,newUnit)

        if len(p)==8:
            p[7](unitNumber)#execute components

        print "Unit with Number="+str(unitNumber)+"\nName='"+unitName+"'\nDescription='"+unitDescription+"'\nprocessed\n"

    def p_Update(self, p):
        """
        update : UPDATE
        |
        """
        p[0] = True if len(p)==2 else False

    def p_Components(self,p):
        """
        Components : update Component
                   | update Component Components
        """
        if not p[1]:
            def h(unitNumber):
                pass
            p[0] = h if len(p)==3 else p[3]
        elif len(p)==3:
            p[0]=p[2]

        else:
            f=p[2]
            g=p[3]
            def h(unitNumber):
                f(unitNumber)
                g(unitNumber)
            p[0]=h


    def p_Component(self,p):
        """
        Component  : Label
                   | Link
                   | Assignment
        """
        p[0]=p[1]


    def p_Label(self,p):
        """
        Label : LABEL COLON STRING
        """
        labelDescription=axml(p[3])
        def f(unitNumber):
            self.selenium_addLabel(unitNumber,labelDescription)
            print "Label for Unit="+str(unitNumber)+"\nwith Text='"+labelDescription+"'\nprocessed\n"
        p[0]=f

    def p_Link(self,p):
        """
        Link : LINK COLON TAB NAME COLON STRING TAB DESCRIPTION COLON STRING TAB URL COLON STRING
        """
        linkName=axml(p[6])
        linkDescription=axml(p[10])
        linkURL=p[14]
        def f(unitNumber):
            self.selenium_addLink(unitNumber,linkName,linkDescription,linkURL)
            print "Link for Unit="+str(unitNumber)+"\nwith Name="+linkName+"\nDescription='"+linkDescription+"'\nURL="+linkURL+"\nprocessed\n"
        p[0]=f

    def p_Assignment(self,p):
        """
        Assignment : ASSIGNMENT COLON TAB ACTION COLON STRING TAB NAME COLON STRING TAB DESCRIPTION COLON STRING TAB STARTDATE COLON NUMBER\
        DATESEPARATOR NUMBER DATESEPARATOR NUMBER TAB STARTHOUR COLON NUMBER COLON NUMBER TAB ENDDATE COLON NUMBER DATESEPARATOR NUMBER\
        DATESEPARATOR NUMBER TAB ENDHOUR COLON NUMBER COLON NUMBER
                   | ASSIGNMENT COLON TAB ACTION COLON STRING TAB NAME COLON STRING TAB COMMENTSFILENAME COLON STRING TAB MARKFILENAME COLON STRING\
        TAB EXECUTABLEFILENAME COLON STRING
        """
        assignmentAction=p[6]
        assignmentName=p[10]
        #TODO importante: INTRODUCIR COMO PARAMETROS DE Grade: nombre del fichero de notas, nombre del fichero de comentarios, nombre del
        #ejecutable que va a corregir
        if assignmentAction=="Add":
            if len(p)==23:
                def f(unitNumber):
                    print "The fields specified are for 'Grading', but your action is 'Add' in Assignment for Unit="+str(unitNumber)+"\nwith Name="+assignmentName+"\nskipping\n"
            else:
                assignmentName=axml(p[10])
                assignmentDescription=axml(p[14])
                startDay=p[18]
                startMonth=p[20]
                startYear=p[22]
                startHour=p[26]
                startMinute=p[28]

                endDay=p[32]
                endMonth=p[34]
                endYear=p[36]
                endHour=p[40]
                endMinute=p[42]

                def f(unitNumber):
                    self.selenium_addAssignment(unitNumber,assignmentName,assignmentDescription,startDay,startMonth,startYear,startHour,startMinute,endDay,endMonth,endYear,endHour,endMinute)
                    print "Adding of Assignment for Unit="+str(unitNumber)+"\nwith Name="+assignmentName+"\nDescription='"+assignmentDescription+"\nprocessed\n"
        elif assignmentAction=="Grade":
            if len(p)==43:
                def f(unitNumber):
                    print "The fields specified are for 'Adding', but your action is 'Grade' in Assignment for Unit="+str(unitNumber)+"\nwith Name="+assignmentName+"\nskipping\n"
            else:
                commentsFileName=p[14]
                markFileName=p[18]
                executableFileName=p[22]#name of the executable who receives a .zip and generates the comments and mark files
                def f(unitNumber):
                    self.selenium_gradeAssignment(unitNumber,assignmentName,commentsFileName,markFileName,executableFileName)
                    print "Grading of Assignment for Unit="+str(unitNumber)+"\nwith Name="+assignmentName+"\nprocessed\n"
        else:
            def f(unitNumber):
                print "WRONG Action '"+assignmentAction+"' for Assignment for Unit="+str(unitNumber)+"\nwith Name="+assignmentName+"\nskipping\n"
        p[0]=f

    def p_manyLineString(self,p):
        """
        ManyLineString : STRING
                       | STRING ManyLineString
        """
        if len(p)==2:
            p[0]=p[1]
        else:
            p[0]=p[1]+"\n"+p[2]

    def p_error(self, p):
        print("Syntax error at '%s'" % p.value)

    def run(self, s, varUsername, varPassword, varCourse, varURL):
        self.user=varUsername
        self.password=varPassword
        self.course=varCourse
        self.url=varURL

        if self.url == "":
            print "You need to specify the base URL\nfinishing..."
        else:
            lexico = Lexico()
            lexico.build()
            global tokens
            self.parser = yacc.yacc(debug = True, module= self)
            result =self.parser.parse(s,lexico)
            return  result


    #Functions with Selenium Code
    def selenium_initialization(self):
        profile = webdriver.FirefoxProfile()#Profile for the downloads
        profile.set_preference('browser.download.folderList', 2) # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        #profile.set_preference('browser.download.dir', '/tmp')#TODO:Maybe could be done to choose the download directory (at the moment it could be done for all the downloads)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/x-compressed,application/x-zip-compressed,application/zip,multipart/x-zip')
        #profile.set_preference('text/csv,application/vnd.ms-excel', 'text/csv')

        self.driver = webdriver.Firefox(profile)
        #next line tells to wait if do not find an element till it finds for 15 seconds
        self.driver.implicitly_wait(15)#maybe this time could be passed by param if someone has slow internet connection

        self.base_url = self.url
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Entrar").click()
        current_url = str(driver.current_url)
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(self.user)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(self.password)
        driver.find_element_by_id("loginbtn").click()
        driver.find_element_by_link_text(self.course).click()
        self.br.open(current_url)
        self.br.select_form (nr = 1)
        self.br.form['username'] = self.user
        self.br.form['password'] = self.password
        self.br.submit()
        time.sleep(5)
        driver.find_element_by_link_text("Turn editing on").click()

    """
    Waits 5 seconds until it finds the unit. Returns true if the unit is found, false otherwise
    """
    def selenium_existsUnit(self,unitNumber):
        driver=self.driver
        try:
            #TODO: (not important) Maybe is possible to optimize the number of seconds that this has to wait
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//li["+str(unitNumber+1)+"]/div[3]/div/a/img")))
            return True
        except TimeoutException:
            return False

    def selenium_addOrUpdateUnit(self,unitNumber,unitName,unitDescription,newUnit):
        driver = self.driver
        if newUnit:#This if is unnecesary because of the while, but maybe newUnit could be used in the future for something more
            #TODO: (not important) Maybe this while could be done in some other way that does not need to wait so much
            while self.selenium_existsUnit(unitNumber) == False:#This while is here because maybe there are units not defined
                driver.find_element_by_xpath("//div/div/div/a/img").click()#increase the number of sections
        time.sleep(5)# we need to wait actively, otherwise sometimes maybe do not work
        driver.find_element_by_xpath("//li["+str(unitNumber+1)+"]/div[3]/div/a/img").click()
        if driver.find_element_by_id("id_usedefaultname").is_selected():#we only deselect the default name if is selected
            driver.find_element_by_id("id_usedefaultname").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys(unitName)

        self.selenium_insertTextInHtmlTextBox(unitDescription)#Insert text in description box

        driver.find_element_by_id("id_submitbutton").click()

    def selenium_insertTextInHtmlTextBox(self,textToInsert):
        driver=self.driver
        #driver.execute_script("document.body.contentEditable = true;"); TODO: This is necessary?? (I suppose NO, check with Domingo's moodle)
        driver.find_element_by_css_selector("span.mceIcon.mce_code").click()
        identifier = PAT.findall(driver.page_source)
        identifier = identifier[0]
        #with open('salida', 'w') as f:
        #    f.write(driver.page_source.encode('utf-8'))
        driver.switch_to_frame(identifier)
        e=driver.switch_to_active_element()
        e.clear()
        e.click()
        e.send_keys("<p>"+textToInsert+"</p>")
        driver.find_element_by_id("insert").click();
        driver.switch_to_active_element()

    def selenium_addLabel(self,unitNumber,labelDescription):
        driver = self.driver
        driver.find_element_by_xpath("//li["+str(unitNumber+1)+"]/div[3]/div[2]/div/div/span/a/span").click()
        driver.find_element_by_id("module_label").click()
        driver.find_element_by_name("submitbutton").click()

        self.selenium_insertTextInHtmlTextBox(labelDescription)#Insert text in description box

        driver.find_element_by_id("id_submitbutton2").click()

    def selenium_addLink(self,unitNumber,linkName,linkDescription,linkURL):
        driver = self.driver
        driver.find_element_by_xpath("//li["+str(unitNumber+1)+"]/div[3]/div[2]/div/div/span/a/span").click()
        driver.find_element_by_id("module_url").click()
        driver.find_element_by_name("submitbutton").click()

        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys(linkName)

        self.selenium_insertTextInHtmlTextBox(linkDescription)#Insert text in description box

        driver.find_element_by_id("id_externalurl").clear()
        driver.find_element_by_id("id_externalurl").send_keys(linkURL)

        driver.find_element_by_id("id_submitbutton2").click()

    def selenium_addAssignment(self,unitNumber,assignmentName,assignmentDescription,comboStartDay,comboStartMonth,comboStartYear,comboStartHour,
                               comboStartMinute,comboEndDay,comboEndMonth,comboEndYear,comboEndHour,comboEndMinute):
        driver = self.driver
        driver.find_element_by_xpath("//li["+str(unitNumber+1)+"]/div[3]/div[2]/div/div/span/a/span").click()
        driver.find_element_by_id("module_assign").click()
        driver.find_element_by_name("submitbutton").click()

        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys(assignmentName)

        self.selenium_insertTextInHtmlTextBox(assignmentDescription)#Insert text in description box


        #Here we parse the user input (because the combo box works with an autonumeric number which means the position of the option you specified)
        #We search the first year in the combo, because we need to substract it for knowing the relative position of the real year we need (see startYear variable)
        firstYearInCombo=int(driver.find_element_by_xpath("//select[@id='id_duedate_year']/option[1]").get_attribute('value'))

        startDay=comboStartDay
        startMonth=comboStartMonth
        startYear=comboStartYear-firstYearInCombo+1
        startHour=comboStartHour+1
        startMinute=comboStartMinute/5+1#moodle only allow us to put minutes multiples of 5, so if you specified another, it will truncated

        endDay=comboEndDay
        endMonth=comboEndMonth
        endYear=comboEndYear-firstYearInCombo+1
        endHour=comboEndHour+1
        endMinute=comboEndMinute/5+1

        driver.find_element_by_xpath("//select[@id='id_allowsubmissionsfromdate_day']/option["+str(startDay)+"]").click()
        driver.find_element_by_xpath("//select[@id='id_allowsubmissionsfromdate_month']/option["+str(startMonth)+"]").click()
        #important TODO: Problem with year, maybe we have to pass to the program a param who says in which year starts the ttbox (or
        #maybe we can know it for the year we are, but I dont know how moodles code handle this)
        #or maybe we can give to the user the option to select the year relative to the actual year (ex. this year, next year)
        driver.find_element_by_xpath("//select[@id='id_allowsubmissionsfromdate_year']/option["+str(startYear)+"]").click()
        driver.find_element_by_xpath("//select[@id='id_allowsubmissionsfromdate_hour']/option["+str(startHour)+"]").click()
        # TODO: we have to do a mapping between the real minutes selected by the user and an option in the checkbox for this hour
        #maybe with a division between 5 is enough (because the minutes are multiple of 5)
        driver.find_element_by_xpath("//select[@id='id_allowsubmissionsfromdate_minute']/option["+str(startMinute)+"]").click()

        driver.find_element_by_xpath("//select[@id='id_duedate_day']/option["+str(endDay)+"]").click()
        driver.find_element_by_xpath("//select[@id='id_duedate_month']/option["+str(endMonth)+"]").click()
        driver.find_element_by_xpath("//select[@id='id_duedate_year']/option["+str(endYear)+"]").click()
        driver.find_element_by_xpath("//select[@id='id_duedate_hour']/option["+str(endHour)+"]").click()
        driver.find_element_by_xpath("//select[@id='id_duedate_minute']/option["+str(endMinute)+"]").click()
        #TODO: Maybe is better (if needed by the user) to separate in two end dates, the due date and the cut off date.
        driver.find_element_by_xpath("//select[@id='id_cutoffdate_day']/option["+str(endDay)+"]").click()
        driver.find_element_by_xpath("//select[@id='id_cutoffdate_month']/option["+str(endMonth)+"]").click()
        driver.find_element_by_xpath("//select[@id='id_cutoffdate_year']/option["+str(endYear)+"]").click()
        driver.find_element_by_xpath("//select[@id='id_cutoffdate_hour']/option["+str(endHour)+"]").click()
        driver.find_element_by_xpath("//select[@id='id_cutoffdate_minute']/option["+str(endMinute)+"]").click()


        driver.find_element_by_id("id_submitbutton2").click()

    def selenium_gradeAssignment(self,unitNumber,assignmentName,commentsFileName,markFileName,executableFileName):
        driver = self.driver
        driver.find_element_by_link_text(assignmentName).click()
        time.sleep(5)# we need to wait actively, because there is a chance of getting the clicks on the previous page
        driver.find_element_by_link_text("View/grade all submissions").click()
        time.sleep(5)# we need to wait actively, because there is a chance of getting the clicks on the previous page
        driver.find_element_by_css_selector("img.smallicon").click()
        while self.selenium_existsMoreSubmissions():
            self.selenium_gradeOne(commentsFileName,markFileName,executableFileName)
            time.sleep(5)
            driver.find_element_by_id("id_saveandshownext").click()
        #if there are no more submissions do the last, save and return (this is done in this way, because there are no do while in python)
        self.selenium_gradeOne(commentsFileName,markFileName,executableFileName)
        driver.find_element_by_id("id_savegrade").click()

        driver.find_element_by_css_selector("a[title=\""+self.course+"\"]").click()

    def selenium_existsMoreSubmissions(self):
        driver=self.driver
        time.sleep(5)# we need to wait actively, because there is a chance of getting the button of the previous page
        try:
            #TODO: (not important) Maybe is possible to optimize the number of seconds that this has to wait
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "id_saveandshownext")))
            return True
        except TimeoutException:
            return False

    def selenium_gradeOne(self,commentsFileName,markFileName,executableFileName):
        driver=self.driver
        time.sleep(5)# we need to wait actively, because there is a chance of getting the regular expression on the previous page
        #driver.find_element_by_xpath("//td[2]/div/a").click() this clicks the link and do the same than the two lines below
        iden = PAT_WEB.findall(driver.page_source)
        if iden:
            iden = iden[0]
            print "link,", iden
            nombre_fichero = os.path.basename(iden)
            if '?' in nombre_fichero:
                nombre_fichero = nombre_fichero[:nombre_fichero.index('?')]
            f = self.br.retrieve(iden)
            nombre_fichero = os.path.join(TEMPDIR,nombre_fichero)
            os.system(executableFileName)
            shutil.move(f[0], nombre_fichero)
            with open(commentsFileName) as f:
                comments=f.read()
            with open(markFileName) as f:
                mark=float(f.readline())
        else:
            comments = ''
            mark = ''
        time.sleep(5)
        driver.find_element_by_id("id_grade").clear()
        driver.find_element_by_id("id_grade").send_keys(str(mark))
        self.selenium_insertTextInHtmlTextBox(comments)


if __name__ == '__main__':
    #this params should put in the variables the proper value, this is the value itself or the empy string "" when nothing is specified

    #varUsername = "profesorprueba"
    #varPassword = "ProfesorPrueba1,"
    #varCourse = "G1234 Curso de Prueba"
    #varURL= "http://localhost/"
    print "tempdir", TEMPDIR
    desc_program = "Program to organize moodle from the terminal"
    desc_file = "File where the description is read"
    desc_user = "Name of the user"
    desc_pass = "Password of the user"
    desc_course = "Name of the course"
    desc_url = "URL of the moodle server"
    parser = argparse.ArgumentParser(description = desc_program )
    parser.add_argument('file', help= desc_file)
    parser.add_argument('-u','--user', help= desc_user)
    parser.add_argument('-p','--password', help= desc_pass)
    parser.add_argument('-c','--course', help= desc_course)
    parser.add_argument('-w','--url', help= desc_url)
    args = parser.parse_args()
    fichero = args.file
    if args.user:
        varUsername = args.user
    else:
        varUsername = ""
    if args.password:
        varPassword = args.password
    else:
        varPassword = ""
    if args.course:
        varCourse = args.course
    else:
        varCourse = ""
    if args.url:
        varURL = args.url
    else:
        varURL = ""
        print "You need to specify an URL in the arguments"
        print "(unless you have specified it in the file)"

    #TODO: Maybe repeat all the Sintactico parser, but without code, only for checking sintax errores
    #before starting the real parser. Or maybe there is some way of doing it without repeating the code (ask Domingo)
    with open(fichero) as f:
        texto=f.read()
    parser = Sintactico()
    parser.run(texto,varUsername,varPassword,varCourse,varURL)
