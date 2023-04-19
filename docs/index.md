<p align="center">
    <img width="800" src=".github/logo.png" title="Logo do projeto"><br />
    <img src="https://img.shields.io/maintenance/yes/2023?style=for-the-badge" title="Status do projeto">
</p>

# Automação de envio de certificados para validação de ACCs

Este projeto tem como objetivo automatizar o envio de certificados para validação de ACCs utilizando RPA com Selenium e
Django.

## ✨ Funcionalidades

* ✔️ Coleta de informações dos certificados: nome do aluno, nome do curso, data de conclusão, etc.
* 🥢 Automação do preenchimento de formulário no forms do google;
* 🖖 Envio automático dos certificados

## Tecnologias

- 🐍 Python
- 🖥 Django
- 🤖 Selenium

## 🚀 Começando

### 1. Primeiro passo para começar

Geralmente o primeiro passo para começar é instalar dependências para rodar o projeto. Rode:

```
pip install -r requirements.txt
```

Execute o servidor Django:

```
python manage.py runserver
```

## Como utilizar

### Acesse a página inicial da aplicação

![Preenchendo campos](preenchendo_campos.gif)

### O sistema vai preencher com base preenchido no form incial e o que encontrou no arquivo PDF e ira automatizar a escrita no forms do google

![Usando RPA](usando_rpa.gif)

### Clique em enviar

## Aviso de responsabilidade

> **IMPORTANTE:** Este projeto é fornecido "como está" e eu não me responsabilizo por qualquer dano que possa ocorrer
> durante o uso do sistema. Certifique-se de testar o sistema completamente antes de utilizá-lo em um ambiente de
> produção.

## Considerações finais

Este projeto é uma solução eficiente para otimizar o processo de envio de certificados para o sistema da universidade.
Sua implementação possibilita uma economia significativa de tempo e recursos humanos, além de minimizar possíveis erros
de preenchimento manual.

## 🤝 Contribua

Sua ajuda é muito bem-vinda, independente da forma! Confira o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para conhecer
todas as formas de contribuir com o projeto. Por
exemplo, [sugerir uma nova funcionalidade](https://github.com/ccuffs/template/issues/new?assignees=&labels=&template=feature_request.md&title=), [reportar um problema/bug](https://github.com/ccuffs/template/issues/new?assignees=&labels=bug&template=bug_report.md&title=), [enviar um pull request](https://github.com/ccuffs/hacktoberfest/blob/master/docs/tutorial-pull-request.md),
ou simplemente utilizar o projeto e comentar sua experiência.

Veja o arquivo [ROADMAP.md](ROADMAP.md) para ter uma ideia de como o projeto deve evoluir.

## 🎫 Licença

Esse projeto é licenciado nos termos da licença open-source [MIT](https://choosealicense.com/licenses/mit) e está
disponível de graça.

## 🧬 Changelog

Veja todas as alterações desse projeto no arquivo [CHANGELOG.md](CHANGELOG.md).

## 🧪 Projetos semelhates

Abaixo está uma lista de links interessantes e projetos similares:

* [Outro projeto](https://github.com/projeto)
* [Projeto inspiração](https://github.com/projeto)
* [Ferramenta semelhante](https://github.com/projeto)
