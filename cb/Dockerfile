FROM crossbario/crossbar

# copy over our own node directory from the host into the image
# set user "root" before copy and change owner afterwards
USER root
COPY .crossbar /cb/.crossbar
RUN chown -R crossbar:crossbar /cb

ENTRYPOINT ["crossbar", "start", "--cbdir", "/cb/.crossbar"]