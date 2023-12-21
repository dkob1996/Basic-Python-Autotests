## Импорт subprocess
import subprocess

## homebrew информация о 7z архиваторе
brew info sevenzip

## Путь к 7z
/opt/homebrew/Cellar/sevenzip/23.01

## Апдейт pip'а
pip3 install --upgrade pip

## Установка pytest фреймворка
python3 -m pip install pytest 

## Узнать полный путь до текущей директории
pwd

## Установка yaml пакета
python3 -m pip install pyyaml
brew install libyaml

## Модули отчетности командами
python3 -m pip install pytest-html
python3 -m pip install pytest-html-reporter

## Отчет в pytest
pytest -v

## Отчет в html pytest
pytest --html=report.html