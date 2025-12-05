# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from app import Sesion as sesion
from app import Seccion as secciones

from lib import SQL as sql
from lib import HTML as html
from lib import Utils as utils


def agregarError(  ):
    secciones.Secciones().agregarError( "Hola" )