OS := $(shell uname)
ARCH := $(shell arch)

PYTHON ?= python3

all : libhts.a longphase libclair3.so
clean : clean_htslib clean_longphase clean_libclair3

SAMVER=1.10
LPVER=1.0

samtools-$(SAMVER)/Makefile:
		curl -L -o samtools-${SAMVER}.tar.bz2 https://github.com/samtools/samtools/releases/download/${SAMVER}/samtools-${SAMVER}.tar.bz2; \
		tar -xjf samtools-${SAMVER}.tar.bz2; \
		rm samtools-${SAMVER}.tar.bz2

libhts.a: samtools-$(SAMVER)/Makefile
	# this is required only to add in -fpic so we can build python module
	@echo "\x1b[1;33mMaking $(@F)\x1b[0m"
	cd samtools-${SAMVER}/htslib-${SAMVER}/ && CFLAGS="-fpic -std=c99 -O3" ./configure && make
	cp samtools-${SAMVER}/htslib-${SAMVER}/$@ $@


longphase-$(LPVER)/Makefile:
	curl -L -o longphase-${LPVER}.tar.gz https://github.com/twolinin/longphase/archive/refs/tags/v${LPVER}.tar.gz; \
	tar -zxvf longphase-${LPVER}.tar.gz; \
	rm longphase-${LPVER}.tar.gz

longphase: longphase-$(LPVER)/Makefile
	@echo "\x1b[1;33mMaking $(@F)\x1b[0m"
	cd longphase-${LPVER} && autoreconf -i && ./configure && make -j4
	cp longphase-${LPVER}/$@ $@


libclair3.so: samtools-${SAMVER}/htslib-${SAMVER}
	${PYTHON} build.py


.PHONY: clean_htslib
clean_htslib:
	cd samtools-${SAMVER} && make clean || exit 0
	cd samtools-${SAMVER}/htslib-${SAMVER} && make clean || exit 0

.PHONY: clean_longphase
clean_longphase:
	cd longphase-${LPVER} && make clean || exit 0

.PHONY: clean_libclair3
clean_libclair3:
	rm libclair3.*
