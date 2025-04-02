# Bibliotecas, ambientes e instalações

## Bibliotecas Python (requirements.txt)

dash
dash-bootstrap-components
waitress
pandas
numpy
plotly
dash-mantine-components==0.12.1
dash-iconify==0.1.2
dash-bootstrap-templates

## Atualizar o pip install

    python -m pip install --upgrade pip

## Listar modulos e bibliotecas instalados

    pip list

## Requirements

    pip freeze > requirements.txt

## Ambiente Virtual

    Virtualenv:
        pip install virtualenv
        virtualenv env_proj_name
    venv:
        python -m venv env_proj_name
        python -m venv .venv

## Ativar o ambiente virtual no Windows

    meu_ambiente\Scripts\activate
    .venv\Scripts\activate
    cd .venv/Script
    activate.bat (cmd)
    Activate.ps1 (pwsh)

## Desativar ambiente virtual

    deactivate

## Apagar um ambiente virtual

    rmdir /s /q venv

## Instalar pacotes

    pip install -r requirements.txt

## Configurando user.name e user.email no Git Bash

    git config --global user.name "Seu Nome"
    git config --global user.email "seu@email.com"

## Executar projeto

    python main.py
