DESCRIPTION = "Linux kernel module for NPort"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING-GPLV2.TXT;md5=5205bcd21ef6900c98e19cf948c26b41"

inherit module

SRC_URI = " \
	file://Makefile \
	file://npreal2.h \
	file://np_ver.h \
	file://npreal2.c \
	file://COPYING-GPLV2.TXT \
"

S = "${WORKDIR}"

# The inherit of module.bbclass will automatically name module packages with
# "kernel-module-" prefix as required by the oe-core build environment.

RPROVIDES_${PN} += "kernel-module-npreal2"



