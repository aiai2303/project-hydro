FROM python

RUN useradd -m -u 1000 user

COPY . /home/user

RUN pip install -r requirements.txt

RUN chown -R user:user /home/user

RUN chmod +x start.sh

EXPOSE 8080

ENTRYPOINT ./start.sh