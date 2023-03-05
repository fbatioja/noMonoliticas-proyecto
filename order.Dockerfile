FROM python:3.10

EXPOSE 5000/tcp

COPY order-requirements.txt ./
RUN pip install --upgrade --no-cache-dir pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r order-requirements.txt

COPY . .

CMD [ "flask", "--app", "./src/order/api", "run", "--host=0.0.0.0"]