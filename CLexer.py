__author__="David Perera Barreda"

import ply.lex as lexer

class Lexico:
    tokens = ('USERNAME','PASSWORD','COURSE','LABEL','LINK','NAME','DESCRIPTION','URL','ASSIGNMENT','STARTDATE','ENDDATE','STARTHOUR','ENDHOUR','ACTION',
              'COMMENTSFILENAME','MARKFILENAME','EXECUTABLEFILENAME','DATESEPARATOR','EQUALS','COLON','STRING','NUMBER','TAB','UPDATE')


    def t_USERNAME(self, t):
        r'Username'
        t.type = 'USERNAME'
        return t

    def t_PASSWORD(self, t):
        r'Password'
        t.type = 'PASSWORD'
        return t

    def t_COURSE(self, t):
        r'Course'
        t.type = 'COURSE'
        return t

    def t_LABEL(self, t):
        r'Label'
        t.type = 'LABEL'
        return t

    def t_LINK(self, t):
        r'Link'
        t.type = 'LINK'
        return t

    def t_NAME(self, t):
        r'Name'
        t.type = 'NAME'
        return t
    def t_UPDATE(self, t):
        r'UPDATE'
        t.type = 'UPDATE'
        return t
    def t_DESCRIPTION(self, t):
        r'Description'
        t.type = 'DESCRIPTION'
        return t

    def t_URL(self, t):
        r'URL'
        t.type = 'URL'
        return t

    def t_ASSIGNMENT(self, t):
        r'Assignment'
        t.type = 'ASSIGNMENT'
        return t

    def t_STARTDATE(self, t):
        r'StartDate'
        t.type = 'STARTDATE'
        return t

    def t_ENDDATE(self, t):
        r'EndDate'
        t.type = 'ENDDATE'
        return t

    def t_STARTHOUR(self, t):
        r'StartHour'
        t.type = 'STARTHOUR'
        return t

    def t_ENDHOUR(self, t):
        r'EndHour'
        t.type = 'ENDHOUR'
        return t

    def t_ACTION(self, t):
        r'Action'
        t.type = 'ACTION'
        return t

    def t_COMMENTSFILENAME(self, t):
        r'CommentsFile'
        t.type = 'COMMENTSFILENAME'
        return t

    def t_MARKFILENAME(self, t):
        r'MarkFile'
        t.type = 'MARKFILENAME'
        return t

    def t_EXECUTABLEFILENAME(self, t):
        r'ExecutableFile'
        t.type = 'EXECUTABLEFILENAME'
        return t

    def t_DATESEPARATOR(self, t):#/ or -
        r'(\/|-)'
        t.type = 'DATESEPARATOR'
        return t

    def t_EQUALS(self, t):
        r'=+'
        t.type = 'EQUALS'
        return t

    #def t_MINUS(self, t): #Commented because of DATESEPARATOR
    #    r'\-'
    #    t.type = 'MINUS'
    #    return t

    def t_COLON(self, t):
        r'(\ )*:(\ )*'
        t.type = 'COLON'
        return t

    def t_TAB(self, t):
        r'\t'
        t.type = 'TAB'
        return t

    def t_NUMBER(self, t):
        r'[0-9]+'
        t.type = 'NUMBER'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'.+'
        t.type='STRING'
        return t

    def t_ANY_newline(self,t):
        r'[\n\r]+'
        t.lexer.lineno += len(t.value)

    def t_ANY_newspace(self,t):
        r'[ \t]+'
        pass

    def t_ANY_error(self,t):
        print "No se reconoce '%s' en la linea '%s' y\
         el caracter %s" % (t.value[0], t.lexer.lineno, t.lexer.lexpos)
        t.lexer.skip(1)



    def build(self, **kwargs):
        self.lexer = lexer.lex(module = self, **kwargs)
        self.lexer.posicion = 1

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()

    def test(self,data):
        self.lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok: break
            print tok

if __name__ == '__main__':
    m = Lexico()
    m.build()
    with open("prueba.txt",'r') as f:
        m.test(f.read())
