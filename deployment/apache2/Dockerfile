FROM ubuntu:16.04
ENV HOSTNAME aucr.io
RUN apt-get update && \
    apt-get install apache2 -y && \
    a2enmod rewrite && \
    a2dissite 000-default && \
    a2enmod proxy && \
    a2enmod proxy_http && \
    a2enmod proxy_html && \
    a2enmod xml2enc && \
    a2enmod ssl && \
    a2enmod authnz_ldap && \
    apt-get install ca-certificates && \
    setcap 'cap_net_bind_service=+ep' /usr/sbin/apache2 && \
    chown www-data:www-data -R /var/log/apache2

RUN apt-get upgrade -y
RUN apt-get install iptables -y
RUN apt-get install ufw -y


COPY aucr.conf /etc/apache2/sites-enabled/
COPY ./certs/ /etc/apache2/certs/
ENV APACHE_RUN_USER=www-data
ENV APACHE_RUN_GROUP=www-data
ENV APACHE_PID_FILE=/var/run/apache2/apache2.pid
RUN mkdir /var/run/apache2 && \
    mkdir /var/lock/apache2
ENV APACHE_RUN_DIR=/var/run/apache2
ENV APACHE_LOCK_DIR=/var/lock/apache2
ENV APACHE_LOG_DIR=/var/log/apache2

ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]