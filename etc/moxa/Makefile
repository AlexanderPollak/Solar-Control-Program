PATH1="."
PWD         := $(shell pwd)
MX_VER_H    := $(PWD)/np_ver.h
ifeq ($(KERNELRELEASE),)
MX_VER_TXT  := $(PWD)/VERSION.TXT
BUILD_VERSION   := $(shell awk '{if($$1=="Version:"){print $$2}}' $(MX_VER_TXT))
endif
BUILD_DATE:=$(shell date +%g%m%d%H)

##############################################################
# Linux Kernel 6.0
##############################################################

all: module npreal2d npreal2d_redund tools
SP1: module npreal2d npreal2d_redund tools
ssl: module SSLnpreal2d npreal2d_redund tools
SP1_ssl: module SSLnpreal2d npreal2d_redund tools
ssl64: module SSL64npreal2d npreal2d_redund tools
SP1_ssl64: module SSL64npreal2d npreal2d_redund tools
ppc64: module ppc64npreal2d npreal2d_redund tools

FLAGS += $(OS_TYPE)
FLAGS += $(POLLING)
FLAGS += -DTTYNAME='"$(TTY)"'
FLAGS += -DNP_TIMEOUT='$(NP_TIMEOUT)'
FLAGS += $(CFLAGS) $(LDFLAGS)

npreal2d: npreal2d.o
	$(CROSS_COMPILE)$(CC) $(FLAGS) npreal2d.o -o npreal2d
	$(CROSS_COMPILE)strip	npreal2d

npreal2d.o : npreal2d.c npreal2d.h
	$(CROSS_COMPILE)$(CC) $(FLAGS) -c npreal2d.c

npreal2d_redund: 	redund_main.o redund.o
	$(CROSS_COMPILE)$(CC) $(FLAGS) redund_main.o redund.o -lpthread -o npreal2d_redund
	$(CROSS_COMPILE)strip	npreal2d_redund

redund_main.o:	redund_main.c npreal2d.h redund.h
	$(CROSS_COMPILE)$(CC) $(FLAGS) -c redund_main.c

redund.o:	redund.c redund.h npreal2d.h
	$(CROSS_COMPILE)$(CC) $(FLAGS) -c redund.c

SSLnpreal2d: 	SSLnpreal2d.o
	$(CROSS_COMPILE)$(CC)	$(FLAGS) npreal2d.o -o npreal2d -lssl -lcrypto 
	$(CROSS_COMPILE)strip	npreal2d

SSLnpreal2d.o:	npreal2d.c
	$(CROSS_COMPILE)$(CC) $(FLAGS) -c -DSSL_ON -DOPENSSL_NO_KRB5 npreal2d.c -I$(PATH1)/include
	
SSL64npreal2d: 	SSL64npreal2d.o
	$(CROSS_COMPILE)$(CC)   -m64 npreal2d.o -o npreal2d -lssl
	$(CROSS_COMPILE)strip   npreal2d

SSL64npreal2d.o:	npreal2d.c
	$(CROSS_COMPILE)$(CC) $(FLAGS) -c -m64 -DSSL_ON -DOPENSSL_NO_KRB5 npreal2d.c -I$(PATH1)/include
	
ppc64npreal2d: 	ppc64npreal2d.o
	$(CROSS_COMPILE)$(CC)   -mpowerpc64 npreal2d.o -o npreal2d -lssl
	$(CROSS_COMPILE)strip   npreal2d

ppc64npreal2d.o:	npreal2d.c
	$(CROSS_COMPILE)$(CC) $(FLAGS) -c -mpowerpc64 -DSSL_ON -DOPENSSL_NO_KRB5 npreal2d.c -I$(PATH1)/include

#MY_FLAGS += -g -DDEBUG

ifneq ($(KERNELRELEASE),)
obj-m := npreal2.o
#ccflags-y += ${MY_FLAGS}
#CC += ${MY_FLAGS}
else
KDIR	:= /lib/modules/$(shell uname -r)/build
PWD	:= $(shell pwd)

module:
	$(MAKE) -C $(KDIR) M=$(PWD) EXTRA_CFLAGS="$(FLAGS)" modules
	cp -p npreal2.ko /lib/modules/$(shell uname -r)/kernel/drivers/char/
	depmod -a

module_debug:
	$(MAKE) -C $(KDIR) M=$(PWD) EXTRA_CFLAGS="$(FLAGS) $(MY_FLAGS)" modules
	cp -p npreal2.ko /lib/modules/$(shell uname -r)/kernel/drivers/char/
	depmod -a

endif

tools: mxaddsvr mxdelsvr mxcfmat mxloadsvr mxsetsec

mxaddsvr: mxaddsvr.c misc.c
	$(CROSS_COMPILE)$(CC) $(FLAGS) -o mxaddsvr mxaddsvr.c misc.c
	$(CROSS_COMPILE)strip mxaddsvr

mxdelsvr: mxdelsvr.c misc.c
	$(CROSS_COMPILE)$(CC) $(FLAGS) -o mxdelsvr mxdelsvr.c misc.c
	$(CROSS_COMPILE)strip mxdelsvr

mxcfmat: mxcfmat.c
	$(CROSS_COMPILE)$(CC) $(FLAGS) -o mxcfmat mxcfmat.c
	$(CROSS_COMPILE)strip mxcfmat

mxloadsvr: mxloadsvr.c misc.c
	$(CROSS_COMPILE)$(CC) $(FLAGS) -o mxloadsvr mxloadsvr.c misc.c
	$(CROSS_COMPILE)strip mxloadsvr
	
mxsetsec: mxsetsec.c misc.c
	$(CROSS_COMPILE)$(CC) $(FLAGS) -o mxsetsec mxsetsec.c misc.c
	$(CROSS_COMPILE)strip mxsetsec
	
clean:
	rm -f *.o
	rm -rf ./.tmp_versions
	rm -f npreal2.mod*
	rm -f .npreal2*
	rm -f npreal2.ko
	rm -f *.order
	rm -f npreal2d
	rm -f npreal2d_redund
	rm -f /lib/modules/$(shell uname -r)/kernel/drivers/char/npreal2.ko
	rm -f /lib/modules/$(shell uname -r)/misc/npreal2.ko
	rm -f mxaddsvr
	rm -f mxdelsvr
	rm -f mxcfmat
	rm -f mxloadsvr
	rm -f mxsetsec
	rm -f Module.symvers
	rm -f .cache.mk
	rm -f ./output/*
	rm -f build.log
	rm -f .*.cmd
	
disk:
	@sudo $(MAKE) clean
	@rm -f $(MX_VER_H)
	@echo "#ifndef _NP_VER_H_" >> $(MX_VER_H)
	@echo "#define _NP_VER_H_" >> $(MX_VER_H)
	@echo -n "#define NPREAL_VERSION \"Ver" >> $(MX_VER_H)
	@echo -n "$(BUILD_VERSION)" >> $(MX_VER_H)
	@echo "\"" >> $(MX_VER_H)
	@echo -n "#define NPREAL_BUILD \"Build " >> $(MX_VER_H)
	@echo -n "$(BUILD_DATE)" >> $(MX_VER_H)
	@echo "\"" >> $(MX_VER_H)
	@echo "#endif" >> $(MX_VER_H)
	@echo "New $(MX_VER_H) is created."
	-rm -fri ../disk/*
	rm -rf ../disk/moxa
	mkdir ../disk/moxa
	cp -R * ../disk/moxa
	tar -C ../disk -zcvf ../disk/npreal2_v${BUILD_VERSION}_build_${BUILD_DATE}.tgz moxa
	rm -rf ../disk/moxa
	cp -f VERSION.TXT ../disk
	cp -f README.TXT ../disk
	@echo "Done"


