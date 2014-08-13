# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 18:31:25 2014

@author: Javier
"""

import mechanize
from HTMLParser import HTMLParser

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Clase que permite interactuar con los formularios de la web y descargarlos
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class URL_BG():
    
    URL = 'https://moodle.unican.es/moodle2/login/index.php'
    USER = 'jgv03'
    PASS = '425358'
    br = 0
    
    # -------------------------------------------------------------------------
    # Metodo de inicio de creacion de la clase
    # -------------------------------------------------------------------------
    def __init__(self):
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
    
    # -------------------------------------------------------------------------
    # Metodo que descarga el fichero html de la pagina principal tras logearse
    # -------------------------------------------------------------------------
    def download_main_web(self,url,user,passwd,filename):

        self.br.open(url)
        formcount = 0
        for frm in self.br.forms():
            if str(frm.attrs["id"])=="login":
                break
            formcount = formcount+1
        self.br.select_form(nr=formcount)
        self.br["username"] = user
        self.br["password"] = passwd
        res = self.br.submit()
        content = res.read()
        f = open(filename,'w')
        f.write(content)
        f.close()
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que retorna los nombre y los links de las asignaturas
    # -------------------------------------------------------------------------
    def main_subjects(self):

        name_link = {}

        for lk in self.br.links():
            if str(lk).count("/course/") > 0:
                vals = str(lk).split(",")
                link = self.replace_all(vals[-1],{"]":"",")":"","\'":""," ":""})
                name = self.replace_all(vals[-3],{")":"","'":""})
                name_link[name] = link
        
        return name_link
        
    # -------------------------------------------------------------------------
    # Metodo que permite descargar una web concreta una vez logueados
    # -------------------------------------------------------------------------
    def web_download(self,url,filename):
        
        res = self.br.open(url)
        content = res.read()
        f = open(filename,'w')
        f.write(content)
        f.close()
        
        return 1   
       
    # -------------------------------------------------------------------------
    # Metodo que retorna todos los formularios existentes con sus atributos
    # -------------------------------------------------------------------------       
    def show_forms(self,url):
        
        res = self.br.open(url)
        content = res.read()        
        
        lines = content.splitlines()
        
        frm_names_attrs = {}
        frm_attrs = []
        
        for frm in self.br.forms():

            proc_attrs = 0
            
            for l in lines:
                
                if proc_attrs == 0:
                    if l.count(frm.attrs["id"])>0:
                        if l.count("<form")>0:
                            proc_attrs = 1
                            
                if proc_attrs == 1:
                    if l.count("</form"):
                        proc_attrs = 0

                if proc_attrs == 1: 
                    if l.count("<input")>0:                    
                        cont = 1
                        while (cont):
                            pos = l.find("name=")
                            if pos < 0:
                                cont = 0
                            else:
                                l = l[pos+6:len(l)]
                                l2 = l.split("\"")
                                frm_attrs.append(l2[0])
            
            frm_attrs.extend(frm.attrs)
            frm_names_attrs[frm.attrs["id"]] = frm_attrs
            frm_attrs = []
            
        return frm_names_attrs
       
    # -------------------------------------------------------------------------
    # Metodo que rellena un formulario web dado mediante un diccionario
    # -------------------------------------------------------------------------
    def refill_form(self,url,dicc_attrs,filename,form_id):
        
        self.br.open(url)
        
        formcount = 0
        for frm in self.br.forms():
            if str(frm.attrs["id"])==form_id:
                break
            formcount = formcount+1
        self.br.select_form(nr=formcount)

        for attr,val in dicc_attrs.iteritems():   
            self.br[attr] = val
        
        res = self.br.submit()
        content = res.read()
        f = open(filename,'w')
        f.write(content)
        f.close()
        
        return 1
        
    # -------------------------------------------------------------------------
    # Metodo que permite reemplazar multiples caracteres de un string por otros
    # -------------------------------------------------------------------------
    def replace_all(self,text,dic):
        for k, v in dic.iteritems():
            text = text.replace(k,v)
        return text
        
    # -------------------------------------------------------------------------
    # Metodo que descarga los html de las asignaturas en ficheros
    # -------------------------------------------------------------------------
    def download_courses(self):
        self.download_main_web(self.URL,self.USER,self.PASS,'Principal.txt')
        i = 0
        for k,v in u.main_subjects().iteritems():
            name = str(i)+".txt"
            self.web_download(v,name)
            i = i + 1
            
        return 1
    
    # -------------------------------------------------------------------------
    # Metodo que descarga un fichero concreto de una url, se le pasa el formato
    # -------------------------------------------------------------------------
    def download_file(self,url,filename):
        
        res = self.br.open(url)
        content = res.read()
        f = open(filename,'wb')
        f.write(content)
        f.close()   
        
        return 1
    
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Clase que permite parsear los ficheros html de las asignaturas
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class CoursesHTMLParser(HTMLParser): 
    
    found_section = 0
    found_instance = 0 
    found_secname = 0
    found_sectext = 0
    
    USER = 'jgv03'
    PASS = '425358'
    URL = 'https://moodle.unican.es/moodle2/login/index.php'
    
    first_time = 1
    
    link = ''
    link_type = 0
    
    f = 0
    
    # -------------------------------------------------------------------------
    # Manejador que se lanza cuando se encuentra una etiqueta html de comienzo
    # -------------------------------------------------------------------------
    def handle_starttag(self, tag, attrs):

        found_link = 0

        if tag == 'html':
            self.f = open("Procesado.xml",'w')
            self.f.write("<autodoc>\n")

        for a in attrs:
            if a[1].count('section-')>0:
                self.found_section = 1
                
            if a[1] == 'instancename':
                self.found_instance = 1
                
            if a[1] == 'sectionname':
                self.found_secname = 1                
                
            if a[1] == 'no-overflow':
                self.found_sectext = 1
                
            if (a[0] == 'class') & (a[1] == ''):
                found_link = 1
                
            if (found_link == 1) & (a[0] == 'href'):
                self.link = a[1]
                found_link = 0
                
            if (a[0] == 'alt') & (a[1] == 'Tarea'):
                self.link_type = 1
                        
            if (a[0] == 'alt') & (a[1] == 'URL'):
                self.link_type = 2
       
    # -------------------------------------------------------------------------
    # Manejador que se lanza cuando se encuentra una etiqueta html de final
    # -------------------------------------------------------------------------
    def handle_endtag(self, tag):
        
        if tag == 'html':
            self.f.write("</section>\n")
            self.f.write("</autodoc>\n")
            self.f.close()
            
        return 1
        
    # -------------------------------------------------------------------------
    # Manejador que se lanza cuando se encuentra datos sin etiquetas
    # -------------------------------------------------------------------------
    def handle_data(self, data):
        
        if self.found_section == 1:
            if self.first_time == 0:
                self.f.write("</section>\n")
            self.first_time = 0
            self.f.write("<section>\n")
            
            self.found_section = 0
            
        if self.found_instance == 1:
            
            self.f.write("<instance>\n")
            self.f.write("<instname>")
            self.f.write(data)
            self.f.write("</instname>\n")
            self.f.write("<instlink>")
            self.f.write(self.link)            
            self.f.write("</instlink>\n")
            
            u = URL_BG()
            u.download_main_web(self.URL,self.USER,self.PASS,'Principal.txt')
            u.web_download(self.link,"temp.txt")

            f = open("temp.txt","r")
            cont = f.read()
            sc = SubCourseHTMLParser()
            sc.feed(cont)
            f.close()
            
            state, data = sc.return_data()
            print state
            print data
            if state == 1:
                print "ENTRO ASSIG"
                tags_o = ["<subjname>","<subjdesc>","<subjdate>"] 
                tags_c = ["</subjname>\n","</subjdesc>\n","</subjdate>\n"]
                
                i = 0
                for d in data:
                    self.f.write(tags_o[i])
                    self.f.write(d)
                    self.f.write(tags_c[i])
                    i = i + 1
                
            elif state == 2:
                print "ENTRO LINK"
                tags_o = ["<linkname>","<linkdesc>","<linkurl>"] 
                tags_c = ["</linkname>\n","</linkdesc>\n","</linkurl>\n"]
                
                i = 0
                for d in data:
                    self.f.write(tags_o[i])
                    self.f.write(d)
                    self.f.write(tags_c[i])
                    i = i + 1
                
            self.f.write("</instance>\n")
            
            self.found_instance = 0
    
        if self.found_secname == 1:
            self.f.write("<secname>")
            self.f.write(data)
            self.f.write("</secname>\n")
            
            self.found_secname = 0
            
        if self.found_sectext == 1:
            self.f.write("<text>")
            self.f.write(data)
            self.f.write("</text>\n")            
            
            self.found_sectext = 0
        
        return 1
        
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Clase que permite parsear cada asignatura o link de manera independiente
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::       
class SubCourseHTMLParser(HTMLParser):
    
    Is_Subject = 0
    Is_Link = 0
    
    Subject_Name = ''
    Subject_Desc = ''
    Subject_Date = ''
    
    Link_Name = ''
    Link_Desc = ''
    Link_URL = ''
    
    Find_Data = 0
    
    # -------------------------------------------------------------------------
    # Manejador que se lanza cuando se encuentra una etiqueta html de comienzo
    # -------------------------------------------------------------------------
    def handle_starttag(self, tag, attrs):

        for a in attrs:
            
            if (a[0] == 'id') & (a[1] == 'urlheading'):
                self.Is_Subject = 0
                self.Is_Link = 1
                self.Find_Data = 1
                
            if (a[0] == 'id') & (a[1] == 'urlintro'): 
                self.Is_Subject = 0
                self.Is_Link = 1
                self.Find_Data = 2            
                
            if (a[0] == 'class') & (a[1] == 'urlworkarround'):
                self.Is_Subject = 0
                self.Is_Link = 1
                self.Find_Data = 3
                
            if (a[0] == 'id') & (a[1] == 'maincontent'):
                self.Is_Subject = 1
                self.Is_Link = 0
                self.Find_Data = 4                
                
            if (a[0] == 'id') & (a[1] == 'intro'):
                self.Is_Subject = 1
                self.Is_Link = 0
                self.Find_Data = 5

        return 1
        
    # -------------------------------------------------------------------------
    # Manejador que se lanza cuando se encuentra una etiqueta html de final
    # -------------------------------------------------------------------------
    def handle_endtag(self, tag):
        
        return 1
        
    # -------------------------------------------------------------------------
    # Manejador que se lanza cuando se encuentra datos sin etiquetas
    # -------------------------------------------------------------------------
    def handle_data(self, data):
        
        next_data = 0        
        
        if self.Find_Data == 1:
            self.Link_Name = data  
            self.Find_Data = 0
            
        if self.Find_Data == 2:
            self.Link_Desc = data
            self.Find_Data = 0
            
        if self.Find_Data == 3:
            self.Link_URL = data
            self.Find_Data = 0
            
        if self.Find_Data == 4:
            self.Subject_Name = data            
            self.Find_Data = 0            
            
        if self.Find_Data == 5:
            self.Subject_Desc = data
            self.Find_Data = 0 
            
        if next_data == 1:
            self.Subject_Date = data
            next_data = 0
            
        if data == 'Fecha de entrega':
            next_data = 1
            
            
        return 1
            
    # -------------------------------------------------------------------------
    # Metodo que retorna los datos concretos de la subpagina dada
    # -------------------------------------------------------------------------
    def return_data(self):
        
        temp = []
        state = 0
        
        if self.Is_Subject == 1:
            
            temp.append(self.Subject_Name)
            temp.append(self.Subject_Desc)
            temp.append(self.Subject_Date)
            
        elif self.Is_Link == 1:

            temp.append(self.Link_Name)
            temp.append(self.Link_Desc)
            temp.append(self.Link_URL)            
            
        else:
            
            temp = []
            
        if self.Is_Subject == 1:
            state = 1
        elif self.Is_Link == 1:
            state = 2
        
        return state, temp
    
    
u = URL_BG()
#u.download_main_web('http://moodle.unican.es/moodle2/','jgv03','425358','Principal.txt')
u.download_courses()
#i = 0
#for k,v in u.main_subjects().iteritems():
#    name = str(i)+".txt"
#    u.course_web_download(v,name)
#    i = i + 1

#u.file_course_to_xml("1.txt","fin.xml")
#u.download_file('http://www.marmolesrobles.com.mx/images/piedra/shows/cara-piedra-oro.jpg','cara.jpg')
parser = CoursesHTMLParser()
f = open("1.txt","r")
cont = f.read()
parser.feed(cont)