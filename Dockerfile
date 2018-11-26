FROM tmacro/python:3

ADD ./requirements.txt /tmp
RUN python -m pip install -r /tmp/requirements.txt

ADD ./ /usr/local/src/

RUN cd /usr/local/src \
	&& python setup.py install

ENTRYPOINT [ "sq" ]
CMD ["help"]
