# -*- coding: utf-8 -*-


from DriverInterface import DriverInterface
import logging
from FiscalPrinterDriver import PrinterException
from FiscalPrinterDriver import FiscalStatusError, FiscalPrinterDriver


import requests
import json


class JsonDriver(DriverInterface):

	__name__ = "JsonDriver"

	fiscalStatusErrors = [
                          ("ErrorMemoriaFiscal", "Error en memoria fiscal"),
                          ('MemoriaFiscalLlena', "Memoria Fiscal llena"),
                          ('MemoriaFiscalCasiLlena', "Memoria Fiscal casi llena"),
                          ('ErrorMemoriaTrabajo', 'Error en Memoria de trabajo'),
                          ('ErrorMemoriaAuditoria', 'Error en Memoria de auditoria'),
                          ('ErrorGeneral', 'Error General'),
                          ('ErrorParametro', 'Error Parametro'),
                          ('ErrorEstado', 'Error Estado'),
                          ('ErrorAritmetico', 'Error Aritmetico'),
                          ('ErrorEjecucion', 'Error de Ejecucion'),
                          ]

   	printerStatusErrors = [
    						('ImpresoraOcupada', 'La Impresora esta ocupada'),
    						('ErrorImpresora', 'Error y/o falla de la impresora'),
    						('ImpresoraOffLine', "Impresora fuera de linea"),
    						#('FaltaPapelJournal', "Poco papel para la cinta de auditoría"),
                            #(FaltaPapelReceipt', "Poco papel para comprobantes o tickets"),
    						('TapaAbierta', "Tapa de impresora abierta"),
    						('CajonAbierto', "Cajon Abierto"),
    						#('OrLogico', 'Or Logico'),
                           ]


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

		replyJson= {}
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
			
			replyJson= reply.json()
			
		except requests.exceptions.Timeout:			
		    # Maybe set up for a retry, or continue in a retry loop
		    logging.getLogger().error("timeout de conexion con la impresora fiscal")
		except requests.exceptions.RequestException as e:
		    # catastrophic error. bail.
		    logging.getLogger().error(str(e))

		key= list(replyJson.keys())[0]
		replyJson= replyJson[key]
		return self._parseReply(replyJson, skipStatusErrors)

	def _parseReply(self, reply, skipStatusErrors):
		# Saco la Clave Estados
		if not skipStatusErrors:
			self._parsePrinterStatus(reply['Estado']['Impresora'])
			self._parseFiscalStatus(reply['Estado']['Fiscal'])
                reply.pop('Estado')
                return reply

	def _parsePrinterStatus(self, printerStatus):
		for value, message in self.printerStatusErrors:
			if value in printerStatus:
				raise PrinterStatusError, message

	def _parseFiscalStatus(self, fiscalStatus):
		for value, message in self.fiscalStatusErrors:
			if value in fiscalStatus:
				raise FiscalStatusError, message
