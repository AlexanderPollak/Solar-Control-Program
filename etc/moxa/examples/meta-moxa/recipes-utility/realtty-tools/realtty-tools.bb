DESCRIPTION = "Service utilities for NPort"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://moxa//COPYING-GPLV2.TXT;md5=5205bcd21ef6900c98e19cf948c26b41"

# OpenSSL is required for secured mode
DEPENDS = "openssl"

# Specify the compressed driver file for SRC_URI
SRC_URI = "file://npreal2_vM.N_BUILD-DATE.tgz"

S = "${WORKDIR}"

# Specify the destination of RealTTY driver
DEST_DIR = "${D}${libdir}/npreal2/driver"

FILES_${PN} += "${libdir}/npreal2/driver/*"

# If SSL secure mode is required to connect to the NPort, unremark the following line:
#SSL_MODE = "yes"

do_compile () {
	${CC} -o mxaddsvr ${S}/moxa/mxaddsvr.c ${S}/moxa/misc.c
	${CC} -o mxdelsvr ${S}/moxa/mxdelsvr.c ${S}/moxa/misc.c
	${CC} -o mxcfmat ${S}/moxa/mxcfmat.c
	${CC} -o mxloadsvr -DNO_INIT ${S}/moxa/mxloadsvr.c ${S}/moxa/misc.c
	${CC} -o mxsetsec -DNO_INIT ${S}/moxa/mxsetsec.c ${S}/moxa/misc.c

	if [ ${SSL_MODE} = "yes" ] 
	then
		${CC} -o npreal2d_redund -lssl -lpthread -DSSL_ON -DOPENSSL_NO_KRB5 ${S}/moxa/redund_main.c ${S}/moxa/redund.c
		${CC} -o npreal2d -lssl -DSSL_ON -DOPENSSL_NO_KRB5 ${S}/moxa/npreal2d.c
	else
		${CC} -o npreal2d_redund -lpthread ${S}/moxa/redund_main.c ${S}/moxa/redund.c
		${CC} -o npreal2d ${S}/moxa/npreal2d.c
	fi
}

do_install () {
	install -m 0755 -d ${DEST_DIR}
	install -m 0755 ${S}/mxaddsvr ${DEST_DIR}
	install -m 0755 ${S}/mxdelsvr ${DEST_DIR}
	install -m 0755 ${S}/mxcfmat ${DEST_DIR}
	install -m 0755 ${S}/mxloadsvr ${DEST_DIR}
	install -m 0755 ${S}/mxsetsec ${DEST_DIR}
        install -m 0755 ${S}/moxa/mxmknod ${DEST_DIR}
        install -m 0755 ${S}/moxa/mxrmnod ${DEST_DIR}
	install -m 0755 ${S}/npreal2d ${DEST_DIR}
        install -m 0755 ${S}/npreal2d_redund ${DEST_DIR}
        install -m 0755 ${S}/moxa/npreal2d.cf ${DEST_DIR}
}

# Ignore GNU_HASH (didn't pass LDFLAGS)
INSANE_SKIP_${PN} = "ldflags"

