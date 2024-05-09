#Librerias que no necesitan descargarse#
import re
import time

# Estados: sin-moneda, con-moneda, a1-servida, a2-servida, a3-servida.
# Acciones: pedir-moneda, pedir-codigo, esperar.
# Percepciones: moneda, a1, a2, a3, servida.

""" Conjunto de condiciones
    Necesarias para las acciones que necesita tomar el agente
"""
REGLAS = {  'sin-moneda' : 'pedir-moneda',
            'con-moneda' : 'pedir-codigo',
            'a1-servida' : 'esperar',
            'a2-servida'  : 'esperar',
            'a3-servida'  : 'esperar'}

""" Conjunto de operadores
    Acciones que realizará el agente de acuerdo a los dos primeros factores
"""
MODELO = {  ('sin-moneda','pedir-moneda','moneda')   : 'con-moneda',
            ( 'con-moneda' ,'pedir-codigo', 'a1')    : 'a1-servida',
            ( 'con-moneda' , 'pedir-codigo', 'a2')   : 'a2-servida',
            ( 'con-moneda', 'pedir-codigo', 'a3')    : 'a3-servida', 
            ( 'a1-servida','esperar','servida')      : 'sin-moneda',
            ( 'a2-servida','esperar ','servida')     : 'sin-noneda',
            ( 'a3-servida','esperar','servida')      : 'sin-moneda'}


class Agente:
    """Agente de tipo reactivo y de memoria
    Para la funcion del agente requiere de las condiciones y reglas
    así como un estado inicial y accion incial"""
    def __init__ (self, modelo, reglas, estado_inicial='',accion_inicial=''): #Constructor para el modelo de agente
        self.modelo = modelo
        self.reglas = reglas
        self.estado_inicial = estado_inicial
        self.accion_inicial = accion_inicial
        self.accion = None
        self.estado = self.estado_inicial
        self. ult_accion = self.accion_inicial
    
    def actuar(self, percepcion) :
        """Actua según la percepción, devolviendo una acción"""
        if not percepcion :
            return self.accion_inicial
        clave = (self.estado, self.ult_accion, percepcion)
        if clave not in self.modelo.keys(): #Si no encuentra una clave valida regresa al estado inicial
            self.accion = None
            self.estado = self.estado_inicial
            self.ult_accion =self.accion_inicial
            return self.accion_inicial
        self.estado = self.modelo[clave]
        if self.estado not in self.reglas.keys(): #Si no encuentra un estado valido regresa al estado inicial
            self.accion = None
            self.estado = self.estado_inicial
            self.ult_accion = self.accion_inicial
            return self.accion_inicial
        #Se hace el retorno de la accion tomada
        accion = self.reglas[self.estado]
        self.ult_accion = accion
        return accion
    
"""Validar una cadena de acuerdo con un patron"""
def regex(cadena, patron):
    #Hacer match con el valor que se pasa de la cadena
    resultado = re.match(patron, cadena)
    #Retorna True si coincide, de lo contrario retorna false
    return resultado is not None
#Regex para las variables a* = a[1-3]$

print("-- Máquina Expendedora --")
#Inicialización del agente
expendedora = Agente(MODELO, REGLAS, 'sin-moneda','pedir-moneda')
percepcion = input( "Inserte moneda:\n|:")

#Flujo del Agente
while percepcion:
    accion = expendedora.actuar(percepcion)
    if(accion == 'pedir-moneda'): #En caso de que solicite no haya insertado la 'moneda' lo solicita
        percepcion = input( "Favor de insertar la moneda\n|:")
    elif(accion == 'pedir-codigo'): #Cuando solicite pedir codigo imprimira las opciones disponibles
        print("Ingrese el código del producto deseado")
        print("Gansito => a1")
        print("Coca-Cola => a2")
        print("Pingüinos => a3")
        decision = input("|: ")
        print(decision)
        retorno = regex(decision, "a[1-3]$")
        if(retorno):
            percepcion = decision
        else:#Regresar moneda en caso de error
            print("Codigo insertado no válido")
            time.sleep(1)
            print("Regresando moneda.")
            time.sleep(1)
            print("Regresando moneda..")
            time.sleep(1)
            print("Regresando moneda...")
    elif(accion == 'esperar'): #Tiempo de espera de la maquina en la entrega del producto
        print("Entregando.")
        time.sleep(2)
        print("Entregando..")
        time.sleep(2)
        print("Entregando...")
        time.sleep(2)
        print("Producto entregado")
        percepcion = 'servida'
