
/* Copyright (C) MOXA Inc. All rights reserved.

   This is free software distributed under the terms of the
   GNU Public License.  See the file COPYING-GPL for details.
*/

#include    <stdio.h>
#include    <string.h>
#include    <fcntl.h>
#include	<time.h>
#include	<unistd.h>
#include	<sys/timeb.h>
#include	<sys/time.h>
#include	<sys/types.h>


#define     TRUE    1
#define     FALSE   0
#define     SEARCH_TIMEOUT                  100
#define     SEARCH_RETRY_CNT                30
#define     MAX_DEVICE_NUM        10

#define     TEMPDIR     "/usr/lib/npreal2/tmp"
#define     NPPATH      "/usr/lib/npreal2"
#define     DRIVERPATH  "/usr/lib/npreal2/driver"

#define		MK_TEMP()		system("mkdir /usr/lib/npreal2/tmp > /dev/null 2>&1");
#define		RM_TEMP()		{system("rm -rf /usr/lib/npreal2/tmp/* > /dev/null 2>&1"); system("rmdir /usr/lib/npreal2/tmp > /dev/null 2>&1");}

#define		NP5210          0x0322
#define		NP5230          0x0312
#define		NP5410          0x0504
#define		NP5430          0x0534
#define		NP5610_8        0x5618
#define		NP5610_16       0x5613

#define     SECURE_NONE          0
#define     SECURE_DATA          1
#define     SECURE_DATA_CERT     2
#define     SECURE_DATA_CMD      3
#define     SECURE_DATA_CMD_CERT 4

//#define _DEBUG_PRINT 1
#ifdef _DEBUG_PRINT
#define DBG_PRINT       printf
#else
#define DBG_PRINT       if (0) printf
#endif

