FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "src/tests/ui_tests", "--html=ui_test_report.html", "--self-contained-html"]
