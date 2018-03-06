# -*- coding: utf-8 -*-


from DriverInterface import DriverInterface
import logging
from FiscalPrinterDriver import PrinterException


import requests
import json


class JsonDriver(DriverInterface):

	__name__ = "JsonDriver"


	fiscalStatusErrors = []

	printerStatusErrors = []


	def __init__(self, host, user = None, password = None, port=80):
		logging.getLogger().info("conexion con JSON Driver en host: %s puerto: %s" % (host, port))
		self.host = host
		self.user = user
		self.password = password
		self.port = port

	def start(self):
		"""Inicia recurso de conexion con impresora"""
		pass

	def close(self):
		"""Cierra recurso de conexion con impresora"""
		pass

	def sendCommand(self, jsonData, parameters = None, skipStatusErrors = None):
		"""Envia comando a impresora"""
		url = "http://%s:%s/fiscal.json" % (self.host, self.port)

		logging.getLogger().info("conectando a la URL %s"%url)
		print(jsonData)
		headers = {'Content-type': 'application/json'}


		try: 
			if self.password:
				reply = requests.post(url, data=json.dumps(jsonData), headers=headers, auth=(self.user, self.password))
			else:
				reply = requests.post(url, data=json.dumps(jsonData), headers=headers)
			print("INICIANDO::::")
			print(reply)
			print(reply.json())
			print(reply.content)
			print("salio la respuesta")
			
			#
			#
			#PARSEAR RESPUESTA
			#VER QUE SI HAY UN ERROR DEVUELVE
			#{"error": { "Identificador": "X", "Descripcion": "..", "Contecto": "..." } }  ESTE SERIA UN ERROR FATAL
			#Podemos analizar los estados de "Impresora" y "Fiscal" hacerlo error parcial y ver que hacer
			#

			return reply.content
			
		except requests.exceptions.Timeout:			
		    # Maybe set up for a retry, or continue in a retry loop
		    logging.getLogger().error("timeout de conexion con la impresora fiscal")
		except requests.exceptions.RequestException as e:
		    # catastrophic error. bail.
		    logging.getLogger().error(str(e))
		
		

   
