FROM python:3.11
COPY . .
RUN pip3 install -r requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS=token.json
CMD [ "uvicorn","main:app","--port","8000","--host","0.0.0.0" ]