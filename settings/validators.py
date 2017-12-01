# -*- coding: utf-8 
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
import time
import datetime
from datetime import timedelta

def limit_date(value):
	register_date = value.strftime("%Y-%m-%d")
	now = datetime.datetime.now()
	hoy = now.strftime("%Y-%m-%d")
	today = time.strptime(hoy, "%Y-%m-%d")
	end_date = now - timedelta(days=5)
	limit = end_date.strftime("%Y-%m-%d")
	date_1 = time.strptime(limit, "%Y-%m-%d")
	date_2 = time.strptime(register_date, "%Y-%m-%d")
	if date_2 < date_1:
		raise ValidationError(_('No es permitido crear un registro antes de %(limit)s'), params={'limit': limit}, )
	if date_2 > today:
		raise ValidationError(_('No es permitido crear registros futuros'))
	return

def lenght_min(value):
	minimum = 4
	if len(value) < minimum:
		raise ValidationError(_('%(value)s es demasiado corto'), params={'value': value}, )
	return

def lenght_max(value):
	maximum = 50
	if len(value) > maximum:

		raise ValidationError(_('%(value)s es muy largo'), params={'value': value},)
	return

def rfc(value):
	minimum = 12
	maximum = 13
	if len(value) < minimum:
		raise ValidationError(_('%(value)s no es un RFC aceptado'), params={'value': value}, )
	if len(value) > maximum:
		raise ValidationError(_('%(value)s no es un RFC aceptado'), params={'value': value}, )
	return

#Número del seguro social

social_number = RegexValidator(regex=r'^[0-9]{11}$', message="Este campo debe ser númerico y contar con 11 digitos")

year = RegexValidator(regex=r'^[0-9]{4}$', message="No es un formato de año Valido")
month = RegexValidator(regex=r'^[0-9]{1,2}$', message="No es un formato de año Valido")
# Validación para nombre de usuario
user_name = RegexValidator(regex='^.{4,15}$', message='Este campo debe tener 4 a 15 carácteres', code='nomatch')

phone = RegexValidator(regex=r'^[0-9]{10}$', message="Este campo debe ser númerico y contar con 10 digitos")
	
zip_code = RegexValidator(regex=r'^[0-9]{5}$', message="Este campo debe ser númerico y contar con 5 digitos")

ext = RegexValidator(regex=r'^[0-9]{0,5}$', message="Este campo debe ser númerico y contar con 5 digitos")


