# Base image
FROM python:3.12-slim

# Atualiza os pacotes e instala dependências do LaTeX, incluindo o pacote de idioma português
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-xetex \
    texlive-lang-portuguese \   
    && rm -rf /var/lib/apt/lists/*

## Copie o requirements.txt
COPY requirements.txt /app/requirements.txt

WORKDIR /app

# Instale as dependências usando o pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Copie o restante do seu código para o contêiner
COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "FormataiBackEnd.wsgi:application"]
