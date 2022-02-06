FROM python:3.9

# timezone
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV ACCESS UDgx294CT64wyrhkKJ4dbk8oKnCLaze5qtrM5e0M
ENV SECRET YHbgxjlTzF4KYpwG3Kjhi1M91YpZNSep6aPFWgHO

COPY . /app

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN rm -rf requirements.txt

ENTRYPOINT ["python", "src/main.py", "KRW-BTC"]