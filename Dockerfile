FROM python

WORKDIR /app
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
COPY app.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
