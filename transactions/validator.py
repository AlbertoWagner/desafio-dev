from django.core.exceptions import ValidationError


def validaCpf(cpf):
    if cpf.isdigit() == False:
        raise ValidationError('Cpf deve conter apenas números: %s' % cpf)

    if len(cpf) != 11:
        raise ValidationError('Tamanho do cpf inválido: %s' % cpf)

    cpf_invalidos = [11 * str(i) for i in range(10)]
    if cpf in cpf_invalidos:
        raise ValidationError('Cpf inválido: %s' % cpf)

    selfcpf = [int(x) for x in cpf]
    cpfLista = selfcpf[:9]

    while len(cpfLista) < 11:
        r = sum([(len(cpfLista) + 1 - i) * v for i, v in [(x, cpfLista[x]) for x in range(len(cpfLista))]]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0

        cpfLista.append(f)

    if not (cpfLista == selfcpf):
        raise ValidationError('Cpf inválido: %s' % cpf)
    else:
        return True


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Arquivo não suportado.')
