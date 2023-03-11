FROM python:3.10

EXPOSE 5001/tcp

COPY warehouse-requirements.txt ./
RUN pip install --upgrade --no-cache-dir pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r warehouse-requirements.txt

COPY . .

CMD [ "flask", "--app", "./src/warehouse_ms/modules/outbounds/api", "run", "--host=0.0.0.0"]