FROM python:2.7.10

COPY start.sh /
COPY requirements.txt /

ENV TERM xterm

RUN pip install -r requirements.txt && \
    git clone https://github.com/aheeki/dadjoke.git

ENTRYPOINT ./start.sh
