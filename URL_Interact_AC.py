# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 17:21:02 2014

@author: Javier
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import URL_Interact_BG
import glob
from Interfaz import Ui_MainWindow
from PyQt4 import QtCore, QtGui
import os
import sys

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Clase que permite manejar todo lo relacionado con las calificaciones
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class TrivialTasks():

    # -------------------------------------------------------------------------
    # Metodo de inicio de creacion de la clase
    # -------------------------------------------------------------------------
    def __init__(self,download_dir):
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference('browser.download.folderList',2)
        self.profile.set_preference('browser.download.manager.showWhenStarting', False)
        self.profile.set_preference('browser.download.dir',download_dir)
        self.profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/zip')        
        
        self.driver = webdriver.Firefox(self.profile)
        #self.driver.set_window_position(-2000,0)
        self.driver.implicitly_wait(3)
        self.base_url = "http://moodle.unican.es/"
        self.verificationErrors = []
        self.accept_next_alert = True
        
    # -------------------------------------------------------------------------
    # Metodo que permite acceder al usuario
    # -------------------------------------------------------------------------
    def login_account(self,user,passwd):
        
        driver = self.driver
        driver.get(self.base_url + "/moodle2/")
        driver.find_element_by_id("login_username").click()
        driver.find_element_by_id("login_username").clear()
        driver.find_element_by_id("login_username").send_keys(str(user))
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys(str(passwd))
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que cambia el estado del moodle a edicion para un curso
    # -------------------------------------------------------------------------
    def enable_disable_edit_mode(self,course_link):
        
        driver = self.driver
        driver.get(course_link)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        
        return 1
        
        
    def find_add_activity_buttons(self,course_link):
    
        driver = self.driver
        self.enable_disable_edit_mode(course_link)
        elements = driver.find_elements_by_class_name("section-modchooser-text")
        
        for e in elements:
            print e.get_attribute("text")
                
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que extrae los enlaces de todos los cursos disponibles
    # -------------------------------------------------------------------------
    def get_courses(self):
        
        driver = self.driver
        
        elements = driver.find_elements_by_partial_link_text("")
        titles = []
        links = []
        
        for element in elements:
            
            try:
                href = element.get_attribute("href")
                if href.count("http://moodle.unican.es/moodle2/course") > 0:
                    links.append(href)
                    titles.append(element.get_attribute("title"))
            except:
                print "El elemento no tienen atributo href"
                
        links_proc = []                   
                   
        for href in links: 
            if links_proc.count(href) == 0:
                links_proc.append(href)
                
        titles_proc = []                
                
        for name in titles:
            if titles_proc.count(name) == 0:
                titles_proc.append(name)
                    
        return links_proc ,titles_proc
    
    

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Clase que permite manejar todo lo relacionado con las calificaciones
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class Ratings():
    
    # -------------------------------------------------------------------------
    # Metodo de inicio de creacion de la clase
    # -------------------------------------------------------------------------
    def __init__(self,download_dir):
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference('browser.download.folderList',2)
        self.profile.set_preference('browser.download.manager.showWhenStarting', False)
        self.profile.set_preference('browser.download.dir',download_dir)
        self.profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/zip')        
        
        self.driver = webdriver.Firefox(self.profile)
        self.driver.set_window_position(-2000,0)
        self.driver.implicitly_wait(3)
        self.base_url = "http://moodle.unican.es/"
        self.verificationErrors = []
        self.accept_next_alert = True
        
    # -------------------------------------------------------------------------
    # Metodo que permite acceder al usuario
    # -------------------------------------------------------------------------
    def login_account(self,user,passwd):
        
        driver = self.driver
        driver.get(self.base_url + "/moodle2/")
        driver.find_element_by_id("login_username").click()
        driver.find_element_by_id("login_username").clear()
        driver.find_element_by_id("login_username").send_keys(str(user))
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys(str(passwd))
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que permite descargar los ficheros de una tarea concreta
    # -------------------------------------------------------------------------
    def download_assignments(self,course_link):
        
        hrefs_proc, names_proc = self.get_assigments(course_link)
        
        driver = self.driver
                                         
        try:        
            for href in hrefs_proc:
                
                driver.get(href+"&action=downloadall")
                
        except:
            print "Elemento no valido"
            
        driver.get(course_link)
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que permite descargar los ficheros de una tarea concreta
    # -------------------------------------------------------------------------
    def download_assignment(self,course_link,assig_link):
        
        hrefs_proc, names_proc = self.get_assigments(course_link)
        
        driver = self.driver
                                         
        try:        
            for href in hrefs_proc:
                if href.count(assig_link)>0:
                    driver.get(str(href)+"&action=downloadall")
                
        except:
            print "Elemento no valido"
            
        driver.get(course_link)
        
        return 1
            
    # -------------------------------------------------------------------------
    # Metodo que extrae los enlaces de todos los cursos disponibles
    # -------------------------------------------------------------------------
    def get_courses(self):
        
        driver = self.driver
        
        elements = driver.find_elements_by_partial_link_text("")
        titles = []
        links = []
        
        for element in elements:
            
            try:
                href = element.get_attribute("href")
                if href.count("http://moodle.unican.es/moodle2/course") > 0:
                    links.append(href)
                    titles.append(element.get_attribute("title"))
            except:
                print "El elemento no tienen atributo href"
                
        links_proc = []                   
                   
        for href in links: 
            if links_proc.count(href) == 0:
                links_proc.append(href)
                
        titles_proc = []                
                
        for name in titles:
            if titles_proc.count(name) == 0:
                titles_proc.append(name)
                    
        return links_proc ,titles_proc
        
    # -------------------------------------------------------------------------
    # Metodo que extrae los enlaces de todas las tareas de un curso
    # -------------------------------------------------------------------------
    def get_assigments(self,course_link):
        
        driver = self.driver
        
        driver.get(course_link)
        
        links = driver.find_elements_by_partial_link_text("")
        hrefs = []
        names = []
    
        for link in links:

            try:
                href = link.get_attribute("href")
                if href.count("http://moodle.unican.es/moodle2/mod/assign/") > 0:
                    hrefs.append(href)
                    names.append(link.get_attribute("text"))
            except:
                print "El elemento no tienen atributo href"
                
        hrefs_proc = []                   
                   
        for href in hrefs: 
            if hrefs_proc.count(href) == 0:
                hrefs_proc.append(href)
                
        names_proc = []                
                
        for name in names:
            if names_proc.count(name) == 0:
                names_proc.append(name)
                
        return hrefs_proc, names_proc
        
    # -------------------------------------------------------------------------
    # Metodo que asigna una nota a una tarea de un alumno cuyo numero es la columna
    # -------------------------------------------------------------------------
    def eval_assigment_student(self,assigment_link,alumno,note,remark):
        
        driver = self.driver
        driver.get(assigment_link+"&rownum="+str(alumno)+"&action=grade")
        handle_before = driver.current_window_handle
        driver.find_element_by_id("id_grade").click()
        driver.find_element_by_id("id_grade").clear()
        driver.find_element_by_id("id_grade").send_keys(note)
        self.insert_textbox_data(remark)
        driver.switch_to_window(handle_before)
        driver.find_element_by_id("id_savegrade").click()
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que permite introducir datos en una textbox
    # -------------------------------------------------------------------------
    def insert_textbox_data(self,text):
        
        driver=self.driver
        driver.find_element_by_css_selector("span.mceIcon.mce_code").click()
        PAT=re.compile('mce_[0-9]+_ifr',re.DOTALL|re.M)
        identifier = PAT.findall(driver.page_source)
        identifier = identifier[0]
        driver.switch_to_frame(identifier)
        e = driver.switch_to_active_element()
        e.click()
        e.clear()
        e.send_keys("<p>"+text+"<p>")
        driver.find_element_by_id("insert").click()
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo evalua a todos los alumnos de una asignatura dado el directorio
    # con las notas y el nombre del mismo sobre el actual
    # -------------------------------------------------------------------------
    def eval_assigment_all(self,course_name,assigment_name,dir_name):
        
        print course_name
        print assigment_name
        print dir_name        
        
        driver = self.driver
        search = str(dir_name)+'/*.txt'
        files = glob.glob(search)
        
        print files
        
        notes_files = []
        remark_files = []
        for f in files:
            if f.count("note")>0:
                notes_files.append(f)
            elif f.count("remark")>0:
                remark_files.append(f)
        
        links,names = self.get_courses()
        matches = []
        words_course = course_name.split(" ")

        temp = 0
        for n in names:
            for w in words_course:
                if w in n:
                    temp = temp + 1
            matches.append(temp)
            temp = 0

        max_val = max(matches)
        course_link = links.pop(matches.index(max_val))

        hrefs,names = self.get_assigments(course_link)
        
        words_assig = assigment_name.split(" ")        
        
        temp = 0
        matches = []
        for n in names:
            for w in words_assig:
                if w in n:
                    temp = temp + 1
            matches.append(temp)
            temp = 0
            
        max_val = max(matches)
        assigment_link = hrefs.pop(matches.index(max_val))
        
        cont = 1
        student_index = 0
        
        student_data = ""
        
        while (cont):
            
            driver.get(assigment_link+"&rownum="+str(student_index)+"&action=grade")
            links = driver.find_elements_by_partial_link_text("")
            error = driver.find_elements_by_class_name("errormessage")
            
            if len(error) > 0:
                print "Final de ejecucion por no mas alumnos"
                cont = 0
                
            else:
            
                student_data = []
                for link in links:
    
                    try:
                        href = link.get_attribute("href")
                        if href.count("http://moodle.unican.es/moodle2/user/view.php") > 0:
                            student_data.append(link.get_attribute("text"))
                    except:
                        print "El elemento no tienen atributo href"
                   
                data = []
                data = student_data[3].split(" ")
                matches_notes = []
                matches_remarks = []
    
                temp = 0            
                for nf in notes_files:
                    for d in data:
                        
                        if nf.count(d)>0:
                            temp = temp + 1
                    matches_notes.append(temp)
                    temp = 0
                    
                temp = 0
                for rf in remark_files:
                    for d in data:
                        if rf.count(d)>0:
                            temp = temp + 1
                    matches_remarks.append(temp)
                    temp = 0
                
                try:
                    print matches_notes
                    if max(matches_notes) > 0:
                        print "ENTRO"
                        f_n = open(notes_files.pop(matches_notes.index(max(matches_notes))),"r")
                        f_r = open(remark_files.pop(matches_remarks.index(max(matches_remarks))),"r")
                        note = f_n.read()
                        remark = f_r.read()
                        print assigment_link
                        print student_index
                        print note
                        print remark
                        self.eval_assigment_student(assigment_link,student_index,note,remark)
                except:
                    print "Todos han sido evaluados."
                    cont = 0
                    
            student_index = student_index + 1
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que cierra el navegador actual
    # -------------------------------------------------------------------------
    def close_webdriver(self):
        
        driver = self.driver
        driver.close()
        
        return 1
        
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Clase que genera la interfaz principal de evaluacion de tareas
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class Ratings_Interface(QtGui.QMainWindow):
    
    # -------------------------------------------------------------------------
    # Definicion del constructor de la clase
    # -------------------------------------------------------------------------
    def __init__(self):
  
        actdir = os.getcwd()
        self.R = Ratings(str(actdir))
        
        self.link_courses = []
        self.name_courses = []
        self.loged = 0
        
        # Inicializar el lanzamiento de ventanas
        self.app = QtGui.QApplication(sys.argv)        
        
        QtGui.QMainWindow.__init__(self)

        # Crear ventana de Registro
        self.ventana = Ui_MainWindow()
        self.ventana.setupUi(self)
        
        # Activar conectores y señales de los botones
        self.connect(self.ventana.BCancelar, QtCore.SIGNAL('clicked()'), self.close_window)
        self.connect(self.ventana.BDescargar, QtCore.SIGNAL('clicked()'), self.download)
        self.connect(self.ventana.BEntregas, QtCore.SIGNAL('clicked()'), self.evaluate)        
        self.connect(self.ventana.BAcceder, QtCore.SIGNAL('clicked()'), self.login)
        self.connect(self.ventana.CBAsignaturas, QtCore.SIGNAL('currentIndexChanged(QString)'), self.update_assigments)  
        
        self.ventana.progressBar.setValue(0)
            
        # Mostrar y ejecutar la ventana        
        self.show()
        self.app.exec_()
        
    # -------------------------------------------------------------------------
    # Metodo que actualiza los items de la interfaz
    # -------------------------------------------------------------------------
    def update_items(self):

        self.ventana.CBAsignaturas.clear()

        self.link_courses,self.name_courses = self.R.get_courses()
    
        for name in self.name_courses:

            value =  self.ventana.progressBar.value()
            if 100 >= value+(60/len(self.name_courses)):
                self.ventana.progressBar.setValue(value+(60/len(self.name_courses)))
            self.ventana.CBAsignaturas.addItem(name)
            
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que actualiza las tareas para una asignatura seleccionada
    # -------------------------------------------------------------------------
    def update_assigments(self):
        
        if self.loged == 1:
            
            self.ventana.CBTareas.clear()        
            
            index = self.ventana.CBAsignaturas.currentIndex()
            
            self.link_assigments, self.name_assigments = self.R.get_assigments(self.link_courses[index])
            
            for name in self.name_assigments:
                
                self.ventana.CBTareas.addItem(name)
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que logea al usuario para conocer sus datos
    # -------------------------------------------------------------------------  
    def login(self):
        
        if self.loged == 0:
            user = self.ventana.LUsuario.text()
            passwd = self.ventana.LPass.text()
            self.ventana.progressBar.setValue(10)
            self.R.login_account(user,passwd)
            self.loged = 1
            self.ventana.progressBar.setValue(40)
            self.update_items()
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que cierra la interfaz
    # -------------------------------------------------------------------------  
    def close_window(self):
        
        self.app.quit()
        self.R.close_webdriver()
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que descarga las tareas en la subcarpeta descargas
    # -------------------------------------------------------------------------
    def download(self):

        if self.loged == 1:
            course_index = self.ventana.CBAsignaturas.currentIndex()
            assig_index = self.ventana.CBTareas.currentIndex()
            self.R.download_assignment(self.link_courses[course_index],self.link_assigments[assig_index])
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que evalua las las entregas de una tarea
    # -------------------------------------------------------------------------
    def evaluate(self):
        
        if self.loged == 1:
            dir_name = self.ventana.LDir.text()
            course_name = self.ventana.CBAsignaturas.currentText()
            assig_name = self.ventana.CBTareas.currentText()

            self.R.driver.get("http://moodle.unican.es/moodle2/my/")
            self.R.eval_assigment_all(course_name,assig_name,dir_name)
            
        return 1
        
        
#R = Ratings("C:\\Prueba")
#R.login_account("jgv03","425358")
#R.eval_assigment_all("Curso de pruebas para","esto es el","prueba")
#R.eval_assigment_all(l[0],"prueba")
#R.download_assignment(l[0])
#R.eval_assigment("http://moodle.unican.es/moodle2/mod/assign/view.php?id=47830",0,90,"GENIAL")
#R.close_webdriver()
Ratings_Interface()
#T = TrivialTasks("C:\\Prueba")
#T.login_account("jgv03","425358")
#c,l=T.get_courses()
#T.find_add_activity_buttons(c[0])