import re
from itertools import cycle

from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

error_messages = {
    'invalid_CNPJ': _("CNPJ inválido."),    
    'invalid_CPF': _("CPF inválido."),  
    'max_digits': _("Este campo requer 14 dígitos."),
    'max_digits_cpf': _("Este campo requer 11 dígitos."),

    'tel_max_digits': _("O telefone deve conter 10 ou 11 números."),
    'tel_celular_invalido': _("O número de celular é invalido."),
    'tel_telefone_invalido': _("O número de telefone é invalido."),
}
def validate_TELEFONE(value):
    telefone = [int(char) for char in value if char.isdigit()]
    # print(telefone)
    if len(telefone)>11 or len(telefone)<10:
        if len(telefone)!=0:            
            raise ValidationError(error_messages['tel_max_digits'])
    telefone=''.join([str(_) for _ in telefone])
    if telefone in (c * 11 for c in "1234567890"):
        raise ValidationError(error_messages['tel_celular_invalido'])
    if telefone in (c * 10 for c in "1234567890"):
        raise ValidationError(error_messages['tel_telefone_invalido'])
    # print(telefone)
    return telefone

def validate_CNPJ(value):
#    print(value)
    cnpj = [int(char) for char in value if char.isdigit()]
#    print(cnpj)
    if len(cnpj) != 14:
        raise ValidationError(error_messages['max_digits'])
    if cnpj in (c * 14 for c in "1234567890"):
        raise ValidationError(error_messages['invalid_CNPJ'])
    orig_value = ''.join([str(_) for _ in cnpj])
    
    cnpj_r = orig_value[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1:i] != str(dv % 10):
            raise ValidationError(error_messages['invalid_CNPJ'])
#    print(orig_value)
    return orig_value


def validate_CPF(value):
#    print(value)
    cpf = [int(char) for char in value if char.isdigit()]
#    print(cnpj)
    # print(cpf)
    if len(cpf) != 11:
        raise ValidationError(error_messages['max_digits_cpf'])
    if cpf in (c * 11 for c in "1234567890"):
        raise ValidationError(error_messages['invalid_CPF'])
    orig_value = ''.join([str(_) for _ in cpf])    
    # print(orig_value)
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            raise ValidationError(error_messages['invalid_CPF'])
    return orig_value