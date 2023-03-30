FROM python:alpine

WORKDIR /app
RUN wget -O - https://sh.rustup.rs -q | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY app.py /app

ENTRYPOINT ["python"]
CMD ["app.py"]
