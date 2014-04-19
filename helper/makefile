CC = gcc -g -Wall 
GLIB =  `pkg-config --cflags --libs glib-2.0`
PCAPLIB     = -lpcap
LNETLIB     = -lnet

LIBS_SRC    = /opt/local/lib/libnids.a
LIBS        = $(PCAPLIB) $(LNETLIB) -lgthread-2.0 

capture: hcapture.c
	$(CC) -c $(CFLAGS) hcapture.c -o capture.o $(GLIB) $(LIBS)
	$(CC) capture.o -o capture $(LIBS_SRC) $(GLIB) $(LIBS)
