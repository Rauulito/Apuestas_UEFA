# import sys
# sys.path.insert(0,"C:/Users/Lorenzo/Documents/programacion/2.Desarrollo_OO/Apuestas_UEFA/Api_Casas_Apuestas_main")
# import bookmaker as db
# from sqlalchemy.ext.hybrid import hybrid_property
# from flask import Flask, render_template, request  
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
"""
DOCSTRING
Importante--> el uso del ..
el .. hace referencia a la carpeta anterior y el . a la carpeta actual a esto se le conoce como import relativo
He puesto un docstring explicando esto ya que este concepto es clave a lo largo del desarrollo del proyecto
En la documentación(https://docs.python.org/es/3/reference/import.html) se puede ver con ejemplos(Apartado 5.7)
"""
from .. import db
from sqlalchemy.ext.hybrid import hybrid_property

class Equipo(db.Model):
    __tablename__ = 'equipos'
    __id = db.Column('id', db.Integer, primary_key=True)
    __nombre = db.Column('nombre', db.String(50), nullable=False)
    __escudo = db.Column('escudo', db.String(120), nullable=False)
    __pais = db.Column('pais', db.String(120), nullable=False)
    __puntaje = db.Column('puntaje', db.Float, nullable=False)
    __activado = db.Column('activado', db.Boolean, nullable=False, default=True)
    apuestas = db.relationship('Apuesta', back_populates="equipo_ganador", cascade="all, delete-orphan")

    @hybrid_property
    def id(self):
        return self.__id
    @id.setter
    def id(self, id):
        self.__id = id
    @id.deleter
    def id(self):
        del self.__id

    @hybrid_property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre
    @nombre.deleter
    def nombre(self):
        del self.__nombre

    @hybrid_property
    def escudo(self):
        return self.__escudo
    @escudo.setter
    def escudo(self, escudo):
        self.__escudo = escudo
    @escudo.deleter
    def escudo(self):
        del self.__escudo
    
    @hybrid_property
    def pais(self):
        return self.__pais
    @pais.setter
    def pais(self, pais):
        self.__pais = pais
    @pais.deleter
    def pais(self):
        del self.__pais

    @hybrid_property
    def puntaje(self):
        return self.__puntaje
    @puntaje.setter
    def puntaje(self, puntaje):
        self.__puntaje = puntaje
    @puntaje.deleter
    def puntaje(self):
        del self.__puntaje

    @hybrid_property
    def activado(self):
        return self.__activado
    @activado.setter
    def activado(self, activado):
        self.__activado = activado
    @activado.deleter
    def activado(self):
        del self.__activado