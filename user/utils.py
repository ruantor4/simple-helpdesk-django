from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def createUserValidation(request, username: str, email: str, password: str):
    if not username or not email or not password:
        messages.error(request, "Todos os campos são obrigatórios.")
        return False

    if User.objects.filter(username=username).exists():
        messages.error(request, "Já existe um usuário com esse nome")
        return False

    if User.objects.filter(email=email).exists():
        messages.error(request, "Já existe um usuário com esse email.")
        return False

    try:
        validate_email(email)
    except ValidationError as e:
        messages.error(request, "Endereço de email inválido, tente novamente.")
        return False

    return True

def updateUserValidation(request, user: User, username: str, email: str):
    if not username or not email:
        messages.error(request, "Os campos 'Usuário' e 'E-mail' são obrigatórios.")
        return False

        # Verifica duplicidade de username (ignorando o próprio)
    if User.objects.filter(username=username).exclude(id=user.id).exists():
        messages.error(request, "Já existe outro usuário com este nome.")
        return False

        # Verifica duplicidade de e-mail (ignorando o próprio)
    if User.objects.filter(email=email).exclude(id=user.id).exists():
        messages.error(request, "Já existe outro usuário com este e-mail.")
        return False

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Endereço de e-mail inválido.")
        return False

    return True

def passwordValidation(request, senha: str) -> bool:

    if not senha:
        return True  # Se o campo estiver vazio, não obriga trocar a senha

    if len(senha) < 6:
        messages.warning(request, " A senha deve ter pelo menos 6 caracteres.")
        return False

    return True
