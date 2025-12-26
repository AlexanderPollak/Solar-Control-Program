
/* Copyright (C) MOXA Inc. All rights reserved.

   This is free software distributed under the terms of the
   GNU Public License.  See the file COPYING-GPL for details.
*/

#include "nport.h"
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <stdio.h>
#include "misc.h"

#define     ER_ARG  -10

#define VERSION_CODE(ver,rel,seq)	((ver << 16) | (rel << 8) | seq)

#define TMP_STR_LEN 1024

char svrList[256][50];
int total[256];
int idx;


int check_usage(int arg, char *argv[])
{
    if (arg > 2)
    {
        printf("mxdelsvr [ip]\n\n");
        return ER_ARG;
    }
    return 0;
}

void GetIP(unsigned long ip, char *ret)
{
    struct in_addr ad;

    ad.s_addr = ip;
    sprintf(ret, "%s", inet_ntoa(ad));

}

int main(int arg, char *argv[])
{
    int i, j;
    int len, daemon;
    struct in_addr ad;
    char *tmpstr, *tmp, c[5];
    char token[50], tty[20], cout[20], major[20], del[50];
    FILE *f, *ft;
	int is_ps_valid = 1;

    if (check_usage(arg, argv) != 0)
    {
        return 0;
    }

    system("clear");
    printf("\nDelete Server ...\n");

    idx = 0;
    daemon = 0;
    tmpstr = (char *)malloc(TMP_STR_LEN);
    len = 1024;
    tmp = (char *)malloc(20);

	MK_TEMP();
	
	is_ps_valid = check_ps_param();

    if (arg == 2)
    {

        sprintf(del, "%s", argv[1]);
        sprintf(tmpstr, "%s/npreal2d.cf", DRIVERPATH);
        f = fopen (tmpstr, "r");
        if (f == NULL)
        {
            printf("file open error\n");
            free(tmpstr);
            free(tmp);
			RM_TEMP();
            return(0);
        }

        /* search the del server */
        for (;;)
        {
            if (getline (&tmpstr, (size_t*)&len, f) < 0)
            {
                break;
            }
            if (strstr(tmpstr, "#") != NULL)
            {
                continue;
            }
            memset(major, '\0', 20);
            sscanf(tmpstr, "%s", major);
            if (strstr(major, "ttymajor") != NULL ||
                    strstr(major, "calloutmajor") != NULL )
            {
                continue;
            }

            // scan only 2 parameters...
            sscanf(tmpstr, "%s%s", token, token);

            if (strcmp(token, del) == 0)
            {
            	// If the ip token is same as argv[1] (=del[])...
                idx = 1;
                break;
            }
        }
        fclose (f);

        if (idx == 0)
        {
            printf("The speicified ip is not installed.\n\n");
            free(tmpstr);
            free(tmp);
			RM_TEMP();
            return 0;
        }

    }
    else
    {

        memset(svrList, 0x0, 256*50);
        memset(total, 0x0, 256*sizeof(int));
        sprintf(tmpstr, "%s/mxcfmat", DRIVERPATH);
        system(tmpstr);

        sprintf(tmpstr, "%s/npreal2d.cf", DRIVERPATH);
        f = fopen (tmpstr, "r");
        if (f == NULL)
        {
            printf("file open error\n");
            free(tmpstr);
            free(tmp);
			RM_TEMP();
            return(0);
        }

        /* print the list of installed server */
        for (;;)
        {
            if (getline (&tmpstr, (size_t*)&len, f) < 0)
            {
                break;
            }
            if (strstr(tmpstr, "#") != NULL)
            {
                continue;
            }
            memset(major, '\0', 20);
            sscanf(tmpstr, "%s", major);
            if (strstr(major, "ttymajor") != NULL ||
                    strstr(major, "calloutmajor") != NULL )
            {
                continue;
            }

            sscanf(tmpstr, "%s%s", token, token);
            for (i=0; i<idx; i++)
            {
                if (!strcmp(svrList[i],token))
                {
                    total[i]++;
                    break;
                }
            }
            if (i == idx)
            {
                strcpy(svrList[idx], token);
                total[idx]++;
                idx++;
            }
        }

        fclose (f);

        if (idx == 0)
        {
            printf("No NPort server is installed.\n\n");
            free(tmpstr);
            free(tmp);
			RM_TEMP();
            return 0;
        }

        printf("\n[Index]\t%-40s\t[Port(s)]\n", "[Server IP]");
        for (i=0; i<idx; i++)
        {
//    	    ad.s_addr = svrList[i];
            printf("  (%d)\t%-40s\t  %d\n", i+1, svrList[i], total[i]);
        }
		printf("  (q)\tExit\n");
        printf("\nSelect: ");
        scanf("%s", c);

        if (atoi(c)<=0 || atoi(c)>idx)
        {
            printf("Please run mxdelsvr again!!\n\n");
            free(tmpstr);
            free(tmp);
			RM_TEMP();
            return 0;
        }

        memset(tmp, '\0', 20);
//       GetIP(svrList[atoi(c)-1], tmp);
        strcpy(del, svrList[atoi(c)-1]);
    }

    sprintf(tmpstr, "%s/npreal2d.cf", DRIVERPATH);
    f = fopen (tmpstr, "r");
    if (f == NULL)
    {
        printf("file open error\n");
        free(tmpstr);
        free(tmp);
		RM_TEMP();
        return(0);
    }
    ft = fopen ("/usr/lib/npreal2/tmp/nprtmp_cf", "w");
    if (ft == NULL)
    {
        printf("file open error\n");
        free(tmpstr);
        free(tmp);
		RM_TEMP();
        return(0);
    }

    /* delete specified device file configured in npreal2d.cf */
    memset(tmpstr, '\0', 1024);
    sprintf(tmpstr, "awk '$0 !~ /#/' %s/npreal2d.cf |", DRIVERPATH);
    sprintf(tmpstr + strlen(tmpstr), " awk '$7 != \"\" ' |");
    sprintf(tmpstr + strlen(tmpstr), " awk '$8 != \"\" ' |");
    sprintf(tmpstr + strlen(tmpstr), " awk '$2 == \"%s\" ' |", del);
    sprintf(tmpstr + strlen(tmpstr), " awk '{system(\"%s/mxrmnod \"$7); system(\"%s/mxrmnod \"$8)}'", DRIVERPATH, DRIVERPATH);
    system(tmpstr);

    /* Delete the server selected by user,  */
    /* and remove the relevant device files */
    for (;;)
    {
        if (getline (&tmpstr, (size_t*)&len, f) < 0)
        {
            break;
        }
        if (strstr(tmpstr, "#") != NULL)
        {
            fputs (tmpstr, ft);
            continue;
        }
        memset(major, '\0', 20);
        sscanf(tmpstr, "%s", major);
        if (strstr(major, "ttymajor") != NULL ||
                strstr(major, "calloutmajor") != NULL )
        {
            fputs (tmpstr, ft);
            continue;
        }

        sscanf(tmpstr, "%s%s", token, token);
        if (strcmp(token, del) != 0)
        {
            fputs (tmpstr, ft);

            /* daemon is a flag which is used to delete the */
            /* daemon start string in /etc/rc.d/rc.local */
            daemon = 1;

        }
    }

    fclose(ft);
    fclose (f);

#ifndef NO_INIT
    if (!daemon )
    {
        system("rm -f /usr/lib/npreal2/driver/state.start > /dev/null 2>&1");
	    //system("systemctl disable npreal2 > /dev/null 2>&1");
    }
#endif /* #ifndef NO_INIT */

    sprintf(tmpstr, "cp -f /usr/lib/npreal2/tmp/nprtmp_cf %s/npreal2d.cf", DRIVERPATH);
    system(tmpstr);
    system("rm -f /usr/lib/npreal2/tmp/nprtmp_cf");

    printf("Deleting server: %s\n\n", del);
	{
		int daemon_flag=0;

		// If npreal2d is exist then trigger the -USR1 instead of running mxloadsvr
		do{
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
				printf("Failed to open nprtmp_checkdaemon.\n");
				system("rm -f /usr/lib/npreal2/tmp/nprtmp_checkdaemon ");
				break;
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

			system("rm -f /usr/lib/npreal2/tmp/nprtmp_checkdaemon ");
		} while (FALSE);

		if( daemon_flag ){
		    memset(tmpstr, '\0', TMP_STR_LEN);
			if( is_ps_valid )
				sprintf(tmpstr, "ps -ef | grep npreal2d | grep -v npreal2d_redund | awk '$0 !~ /grep/ {system(\"kill -USR1 \"$2)}'");
			else
				sprintf(tmpstr, "ps | grep npreal2d | grep -v npreal2d_redund | awk '$0 !~ /grep/ {system(\"kill -USR1 \"$1)}'");
		    system(tmpstr);
		} else {
			sprintf(tmpstr, "%s/mxloadsvr", DRIVERPATH);
			system(tmpstr);
		}

		// If npreal2d.cf is empty, then kill all npreal2d processes
		do {

		    /* check if npreal2d.cf is empty or not */
			system("rm -f /usr/lib/npreal2/tmp/nprtmp_checkcf");

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
		    	printf("Failed to open nprtmp_checkcf.\n");
		    	system("rm -f /usr/lib/npreal2/tmp/nprtmp_checkcf");
		        break;
		    }
		    if (filelength(fileno(f)) == 0)
		    {
		        /* Means configurations are not exist */
			    memset(tmpstr, '\0', TMP_STR_LEN);
				if( is_ps_valid )
					sprintf(tmpstr, "ps -ef | grep npreal2d | awk '$0 !~ /grep/ {system(\"kill -9 \"$2)}'");
				else
					sprintf(tmpstr, "ps | grep npreal2d | awk '$0 !~ /grep/ {system(\"kill -9 \"$1)}'");

			    system(tmpstr);

		    }
		    fclose(f);

		} while (FALSE);
	}

    free(tmpstr);
    free(tmp);
	RM_TEMP();
    return 0;
}


