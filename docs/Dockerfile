FROM python:slim

WORKDIR /docs
RUN apt-get update \
 && apt-get install --no-install-recommends -y \
      graphviz \
      imagemagick \
      make \
      pandoc \
 && apt-get autoremove \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir -U pip
RUN python3 -m pip install --no-cache-dir \
Sphinx==4.5.0  \
Pillow  \
recommonmark \
nbsphinx \
pydata-sphinx-theme

CMD ["make", "html"]