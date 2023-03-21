FROM python

WORKDIR /app
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY app.py /app

ENTRYPOINT ["python"]
CMD ["app.py"]
