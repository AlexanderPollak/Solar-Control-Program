
/* Copyright (C) MOXA Inc. All rights reserved.

   This is free software distributed under the terms of the
   GNU Public License.  See the file COPYING-GPL for details.
*/

#include "nport.h"
#include <stdio.h>
#include <stdlib.h>
#include <linux/version.h>
#include <stdio.h>
#include <errno.h>
#include "misc.h"

#define VERSION_CODE(ver,rel,seq)	((ver << 16) | (rel << 8) | seq)

#define LOADMODULE      3
#define LOADNODE        2

#define TMP_STR_LEN		1024

int version_upgrade_check()
{
#define TOKEN_LEN 256
    char tmpstr[TMP_STR_LEN], tmpstr2[TMP_STR_LEN], token[TOKEN_LEN], *chk;
    char delim[] = " \t";
    FILE *f, *ft;
    int i;

    /* check if existing npreal2d.cf is empty or not (There is only config in DRIVERPATH when the 1st time installation) */
    memset(tmpstr, '\0', TMP_STR_LEN);
    sprintf(tmpstr, "grep -v \"#\" %s/npreal2d.cf |", DRIVERPATH);
    sprintf(tmpstr + strlen(tmpstr), " grep -v \"ttymajor\" |");
    sprintf(tmpstr + strlen(tmpstr), " grep -v \"calloutmajor\" > /usr/lib/npreal2/tmp/nprtmp_checkcf");
    system(tmpstr);

    f = fopen ("/usr/lib/npreal2/tmp/nprtmp_checkcf", "r");
    if (f == NULL)
    {
        printf("file open error\n");
        return(0);
    }

    if (filelength(fileno(f)))
    {
        memset(tmpstr, '\0', TMP_STR_LEN);
        sprintf(tmpstr, "cp -f %s/config %s/npreal2d.cf", DRIVERPATH, DRIVERPATH);
        system(tmpstr);

        memset(tmpstr, '\0', TMP_STR_LEN);
        sprintf(tmpstr, "%s/npreal2d.cf", DRIVERPATH);
        ft = fopen (tmpstr, "a+");
        if (ft == NULL)
        {
            printf("file open error_4\n");
            fclose(f);
            return -1;
        }
        for (;;)
        {
            memset(tmpstr, '\0', TMP_STR_LEN);
            memset(tmpstr2, '\0', TMP_STR_LEN);
            memset(token, '\0', TOKEN_LEN);
            if (fgets(tmpstr, TMP_STR_LEN, f) == NULL)
            {
                break;
            }
            strcpy(tmpstr2, tmpstr);
            for (i=0; i<7; i++)
            {
                if (i==0)
                {
                    strtok(tmpstr, delim);
                }
                else
                {
                    if (strtok(NULL, delim) == NULL)
                    {
                        break;
                    }
                }
            }
            // Check whether the count of parameters of configuration is more than 6.
            // That is the newer version of configuration is found. Just save them.
            if (i >= 7)
            {
                fputs (tmpstr2, ft);
            }
            // the old config format is detected. upgrading config.
            if (i == 6)
            {
                for (i=0; i<6; i++)
                {
                    if (i==0)
                    {
                        sprintf(token, "%s", strtok(tmpstr2, delim));
                        DBG_PRINT("(i=0)  token=[%s]\n", token);
                    }
                    else
                    {
                        DBG_PRINT("i=%d\n", i);
                        chk = strtok(NULL, delim);
                        if (i == 2 && chk != NULL)
                        {
                            DBG_PRINT("dataport = [%s]\n", chk);
                            sprintf(token + strlen(token), "\t%d", atoi(chk)+949);  // data port
                            sprintf(token + strlen(token), "\t%d", atoi(chk)+965);  // command port
                            continue;
                        }
                        if (chk != NULL)
                        {
                            sprintf(token + strlen(token), "\t%s", chk);  //  [Nport IP]
                            continue;
                        }
                    }
                }
                fputs (token, ft);
            }
            else
            {
                DBG_PRINT("invalid config format.");
            }
        }
        fclose(ft);
    }
    fclose(f);
    return 0;
}

// Create new [modifle] file, copy [tmpfile] to modifle, and insert [addstr] after the continuous '#'.
// Return: 1:success 0:NG
int modify_script(char *tmpfile, char *modfile, char *addstr)
{
    char *filestr;
    FILE *f, *tf;
    int len=1024;

    filestr = (char *)malloc(1024);

    f = fopen (tmpfile, "r");
    if (f == NULL)
    {
        printf("file open error\n");
        free(filestr);
        return(0);
    }
    tf = fopen (modfile, "w");
    if (tf == NULL)
    {
        printf("file open error\n");
        free(filestr);
        return(0);
    }

    for (;;)
    {
        if (getline (&filestr, (size_t*)&len, f) < 0)
            break;
        fputs(filestr, tf);
        if (strstr(filestr, "#") != NULL)
            continue;
        else
            break;
    }

    fputs(addstr, tf);

    for (;;)
    {
        if (getline (&filestr, (size_t*)&len, f) < 0)
            break;
        fputs(filestr, tf);
        if (feof(f) == 0)
            continue;
        else
            break;
    }

    fclose(tf);
    fclose(f);
    free(filestr);
    return 1;
}

int main(int arg, char *argv[])
{
    int len, makenode;
    int ttymajor, calloutmajor;
    int daemon_flag, cf_flag;
    char tmpstr[TMP_STR_LEN];
	char *tmpstrptr;
    char major[20];
    FILE *f, *fos;
    int is_ps_valid = 1;

    if (arg > 2)
    {
        printf("\nSyntax error!!\nusage: mxloadsvr [option]\n\n");
        return -1;
    }
    else if (arg == 2)
    {
        if (strcmp(argv[1], "module") && strcmp(argv[1], "install"))
        {
            printf("\nWarning: unrecognized option -> \"%s\"\n\n", argv[1]);
        }
    }

    MK_TEMP();	
    is_ps_valid = check_ps_param();   
 
    makenode = LOADNODE;
    if (arg == 2)
    {
        if (strcmp(argv[1], "module") == 0)
        {
            makenode = LOADMODULE;
        }
        else if (strcmp(argv[1], "install") == 0)
        {
            makenode = LOADMODULE;
            version_upgrade_check();
        }
    }

    memset(tmpstr, '\0', TMP_STR_LEN);
    daemon_flag = 0;
    cf_flag = 0;
    sprintf(tmpstr, "%s/npreal2d.cf", DRIVERPATH);

    f = fopen (tmpstr, "r");
    if (f == NULL)
    {
        printf("file open error\n");
        RM_TEMP();
        return(0);
    }

	tmpstrptr = tmpstr;
    /* get ttymajor & calloutmajor */
    for (;;)
    {
		len = TMP_STR_LEN;
        if (getline (&tmpstrptr, (size_t*)&len, f) < 0)
        {
            break;
        }
        if (strstr(tmpstrptr, "#") != NULL)
        {
            continue;
        }

        memset(major, '\0', 20);
        sscanf(tmpstrptr, "%s", major);

        if (strstr(major, "ttymajor") != NULL)
        {
            ttymajor = atoi(strstr(major, "=")+1);
            continue;
        }

        if (strstr(major, "calloutmajor") != NULL )
        {
            calloutmajor = atoi(strstr(major, "=")+1);
            continue;
        }
    }
    fclose(f);

    /* stop daemon (npreal2d) */
    memset(tmpstr, '\0', TMP_STR_LEN);
    if( is_ps_valid ){
        sprintf(tmpstr, "ps -ef | grep npreal2d |");
        sprintf(tmpstr + strlen(tmpstr), " awk '$0 !~ /grep/ {system(\"kill -15 \"$2)}'");
    } else {
        sprintf(tmpstr, "ps | grep npreal2d |");
        sprintf(tmpstr + strlen(tmpstr), " awk '$0 !~ /grep/ {system(\"kill -15 \"$1)}'");
    }
    system(tmpstr);

    DBG_PRINT("kill -15 npreal2d\n");

    if (makenode == LOADMODULE)
    {
        /* rm and mknod for all device node */
        memset(tmpstr, '\0', TMP_STR_LEN);
        if( is_ps_valid ){
            sprintf(tmpstr, "ps -ef | grep npreal2d |");
            sprintf(tmpstr + strlen(tmpstr), " awk '$0 !~ /grep/ {system(\"kill -9 \"$2)}'");
        } else {
            sprintf(tmpstr, "ps | grep npreal2d |");
            sprintf(tmpstr + strlen(tmpstr), " awk '$0 !~ /grep/ {system(\"kill -9 \"$1)}'");
        }
        system(tmpstr);
        DBG_PRINT("kill -9 npreal2d\n");

        printf("\nLoading TTY Driver...\n");
        system("rmmod npreal2 > /dev/null 2>&1");

        sprintf(tmpstr, "cd %s", DRIVERPATH);
        system(tmpstr);
        sprintf(tmpstr, "modprobe npreal2 ttymajor=%d calloutmajor=%d verbose=0", ttymajor, calloutmajor);
        system(tmpstr);
    }

    //  if (makenode >= LOADNODE) {
    /* delete all device file configured in npreal2d.cf */
    memset(tmpstr, '\0', TMP_STR_LEN);
    sprintf(tmpstr, "awk '$0 !~ /#/' %s/npreal2d.cf |", DRIVERPATH);
    sprintf(tmpstr + strlen(tmpstr), " awk '$6 != \"\" ' |");
    sprintf(tmpstr + strlen(tmpstr), " awk '$7 != \"\" ' |");
    sprintf(tmpstr + strlen(tmpstr), " awk '{system(\"%s/mxrmnod \"$6); system(\"%s/mxrmnod \"$7)}'", DRIVERPATH, DRIVERPATH);
    system(tmpstr);

    /* create all device file configured in npreal2d.cf */
    memset(tmpstr, '\0', TMP_STR_LEN);
    sprintf(tmpstr, "awk '$0 !~ /#/' %s/npreal2d.cf |", DRIVERPATH);
    sprintf(tmpstr + strlen(tmpstr), " awk '$7 != \"\" ' |");
    sprintf(tmpstr + strlen(tmpstr), " awk '$8 != \"\" ' |");
    sprintf(tmpstr + strlen(tmpstr), " awk '{system(\"%s/mxmknod \" $7 \" %d \" $1); system(\"%s/mxmknod \" $8 \" %d \" $1)}'", DRIVERPATH, ttymajor, DRIVERPATH, calloutmajor);
    system(tmpstr);

#ifndef NO_INIT

    // Use /usr/lib/npreal2/driver/state.start to control the deamon loding process in load_npreal2.sh script
	// If the state.start is exist, the mxloadsvr will be executed in systemd-start.
	// Original code removes the mxloadsvr loading here and adds it back in the end of this routine.

	system("rm -f /usr/lib/npreal2/driver/state.start > /dev/null 2>&1");
	system("systemctl daemon-reload > /dev/null 2>&1");
	system("systemctl enable npreal2 > /dev/null 2>&1");

#endif /* #ifndef NO_INIT */

    /* check if daemon is running or not */
    memset(tmpstr, '\0', TMP_STR_LEN);
    if( is_ps_valid )
        sprintf(tmpstr, "ps -ef | grep npreal2d | grep -v grep");
    else
        sprintf(tmpstr, "ps | grep npreal2d | grep -v grep");
    sprintf(tmpstr + strlen(tmpstr), " > /usr/lib/npreal2/tmp/nprtmp_checkdaemon");
    system(tmpstr);

    f = fopen ("/usr/lib/npreal2/tmp/nprtmp_checkdaemon", "r");
    if (f == NULL)
    {
        DBG_PRINT("file open error_checkdaemon\n");
        RM_TEMP();
        return(0);
    }
    if (filelength(fileno(f)) != 0)
    {
        daemon_flag = 1; /* Means any npreal2d is running now. */
    }
    else
    {
        daemon_flag = 0;
    }
    fclose(f);

    /* check if npreal2d.cf is empty or not */
    sprintf(tmpstr, "%s/mxcfmat", DRIVERPATH);
    system(tmpstr);

    memset(tmpstr, '\0', TMP_STR_LEN);
    sprintf(tmpstr, "grep -v \"#\" %s/npreal2d.cf |", DRIVERPATH);
    sprintf(tmpstr + strlen(tmpstr), " grep -v \"ttymajor\" |");
    sprintf(tmpstr + strlen(tmpstr), " grep -v \"calloutmajor\" > /usr/lib/npreal2/tmp/nprtmp_checkcf");
    system(tmpstr);

    memset(tmpstr, '\0', TMP_STR_LEN);
    sprintf(tmpstr, "/usr/lib/npreal2/tmp/nprtmp_checkcf");
    f = fopen (tmpstr, "r");
    if (f == NULL)
    {
        DBG_PRINT("file open error\n");
        RM_TEMP();
        return(0);
    }
    if (filelength(fileno(f)) != 0)
    {
        cf_flag = 1; /* Means configurations are exist */
    }
    else
    {
        cf_flag = 0;
    }
    fclose(f);

    memset(tmpstr, '\0', TMP_STR_LEN);
    if (daemon_flag == 1)
    {
    	// If there is npreal2d daemon running...

        if (cf_flag == 1)
        {
        	// If there is npreal2d.cf configurations...
            memset(tmpstr, '\0', TMP_STR_LEN);
            if( is_ps_valid ){
                sprintf(tmpstr, "ps -ef | grep npreal2d |");
                sprintf(tmpstr + strlen(tmpstr), " awk '$0 !~ /grep/ {system(\"kill -15 \"$2)}'");
            } else {
                sprintf(tmpstr, "ps | grep npreal2d |");
                sprintf(tmpstr + strlen(tmpstr), " awk '$0 !~ /grep/ {system(\"kill -15 \"$1)}'");
            }
            system(tmpstr);
            DBG_PRINT("daemon=1, cf=1, kill -15 npreal2d\n");

        }
        else
        {
            memset(tmpstr, '\0', TMP_STR_LEN);
            if( is_ps_valid ){
                sprintf(tmpstr, "ps -ef | grep npreal2d |");
                sprintf(tmpstr + strlen(tmpstr), " awk '$0 !~ /grep/ {system(\"kill -9 \"$2)}'");
            } else {
                sprintf(tmpstr, "ps | grep npreal2d |");
                sprintf(tmpstr + strlen(tmpstr), " awk '$0 !~ /grep/ {system(\"kill -9 \"$1)}'");
            }
            system(tmpstr);
            DBG_PRINT("daemon=1, cf=0, kill -9 npreal2d\n");
        }
    }
    else
    { /* daemon_flag = 0 */
        if (cf_flag == 1)
        {
            sprintf(tmpstr, "%s/npreal2d_redund -t 1", DRIVERPATH);
            system(tmpstr);
            sprintf(tmpstr, "%s/npreal2d -t 1", DRIVERPATH);
            system(tmpstr);
            DBG_PRINT("daemon=0, cf=1, [start daemon] %s\n", tmpstr);

        }
        else
        {
            DBG_PRINT("daemon=0, cf=0\n");
        }
    }

#ifndef NO_INIT

    memset(tmpstr, '\0', TMP_STR_LEN);
    if (cf_flag == 0)
    {
    	// If there is no configuration, remove mxloadsvr in rc.local
        system("rm -f /usr/lib/npreal2/driver/state.start > /dev/null 2>&1");
	 	//system("systemctl disable npreal2 > /dev/null 2>&1");
    }
    else if (cf_flag == 1)
    {
    	// If there is no mxloadsvr in rc.local, add it...
		system("touch /usr/lib/npreal2/driver/state.start > /dev/null 2>&1");
		system("systemctl daemon-reload > /dev/null 2>&1");
		system("systemctl enable npreal2 > /dev/null 2>&1");
    }
#endif /* #ifndef NO_INIT */

    RM_TEMP();

    printf("Complete.\n\n");

    return 0;
}
