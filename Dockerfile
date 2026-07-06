# Usa uma imagem oficial do Python baseada em Debian (slim)
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Evita que o Python escreva arquivos .pyc e ativa o buffer de saída
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema: compiladores, ferramentas de PDF e o ambiente LaTeX completo com ABNT
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    fontconfig \
    xvfb \
    # Instalação do LaTeX e pacotes de suporte (inclui o abnt2 e textlive)
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-lang-portuguese \
    texlive-fonts-recommended \
    # wkhtmltopdf saiu dos repositorios do Debian (projeto arquivado);
    # instala o .deb estatico oficial direto do GitHub
    && wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb -O /tmp/wkhtmltox.deb \
    && apt-get install -y --no-install-recommends /tmp/wkhtmltox.deb \
    && rm /tmp/wkhtmltox.deb \
    # Limpeza para reduzir o tamanho da imagem Docker
    && rm -rf /var/lib/apt/lists/*

# Instala o pipenv
RUN pip install --no-cache-dir pipenv

# Copia os arquivos de dependencias do Python
COPY Pipfile Pipfile.lock /app/

# Instala as dependencias do Pipenv no escopo do sistema do container
RUN pipenv install --system --deploy

# Copia o restante do codigo do projeto
COPY . /app/

# Torna o entrypoint executavel
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# Executa migracoes, coleta estaticos e inicia o servidor
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn plataformaResumosAPI.wsgi:application --bind 0.0.0.0:$PORT