# Usa uma imagem oficial do Python baseada em Debian (slim)
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Evita que o Python escreva arquivos .pyc e ativa o buffer de saída
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema: compiladores, ferramentas de PDF e o ambiente LaTeX completo com ABNT
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    # Dependências comuns para geração de PDFs (como wkhtmltopdf/pango se seu pacote precisar)
    wkhtmltopdf \
    xvfb \
    # Instalação do LaTeX e pacotes de suporte (inclui o abnt2 e textlive)
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-lang-portuguese \
    texlive-fonts-recommended \
    # Limpeza para reduzir o tamanho da imagem Docker
    && rm -rf /var/lib/apt/lists/*

# Instala o pipenv
RUN pip install --no-cache-dir pipenv

# Copia os arquivos de dependências do Python
COPY Pipfile Pipfile.lock /app/

# Instala as dependências do Pipenv no escopo do sistema do container
RUN pipenv install --system --deploy

# Copia o restante do código do projeto
COPY . /app/

# Executa migrações, coleta estáticos e inicia o servidor
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn nome_do_seu_projeto.wsgi:application --bind 0.0.0.0:$PORT