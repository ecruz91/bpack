# -*- coding: utf-8 
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


def lenght_min(value):
	minimum = 4
	if len(value) < minimum:
		raise ValidationError(_('%(value)s es demasiado corto'), params={'value': value}, )
	return

def lenght_max(value):
	maximum = 25
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


phone = RegexValidator(regex=r'^[0-9]{10}$', message=" Este campo debe ser númerico y contar con 10 digitos")
	
zip_code = RegexValidator(regex=r'^[0-9]{5}$', message="Este campo debe ser númerico y contar con 5 digitos")

ext = RegexValidator(regex=r'^[0-9]{0,5}$', message="Este campo debe ser númerico y contar con 5 digitos")


