FROM python:3.9.12-slim-buster

LABEL maintainer="data-engineering@energyaspects.com"

ARG SSH_PRIVATE_KEY

RUN pip3 install pip --upgrade

RUN apt-get update && apt-get install curl gnupg -y
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt-get update; apt-get install curl apt-transport-https ca-certificates -y

# Installing Git and other useful packages
RUN apt-get update && apt-get install git google-cloud-sdk git chromium wget unzip tesseract-ocr gcc python-dev libjpeg-dev zlib1g-dev -y

# PostgreSQL dependecies
RUN apt-get update && apt-get install libpq-dev -y && \
# Install Chrome WebDriver
wget "http://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip" && \
unzip chromedriver_linux64.zip && \
mv chromedriver /usr/lib/chromium/chromedriver && \
chown root:root /usr/lib/chromium/chromedriver && \
chmod +x /usr/lib/chromium/chromedriver



# Set the Chrome repo.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Install Chrome.
RUN apt-get update && apt-get -y install google-chrome-stable

# unpacking SSH key
RUN mkdir -p ~/.ssh && umask 0077 && echo "${SSH_PRIVATE_KEY}" > ~/.ssh/id_rsa \
&& git config --global url."git@github.com:".insteadOf https://github.com/ \
&& ssh-keyscan github.com >> ~/.ssh/known_hosts

RUN pip3 install git+ssh://git@github.com/energyaspects/helper_functions.git@latest

COPY . .

RUN pip install -r ./requirements/requirements.txt

RUN python setup.py install

CMD /bin/sh