@echo off
echo Iniciando a aplicacao NAU Industrial...

IF NOT EXIST venv (
    echo Criando ambiente virtual...
    py -m venv venv
)

echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo Iniciando aplicacao...
py run.py

pause 