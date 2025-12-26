
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

typedef struct _CONINFO
{
    int idx;
    char ipaddr[40];
    char data[10];
    char cmd[10];
    char fifo[10];
    int secure;
    char tty[10];
    char cout[10];
    int num;
    char scope_id[10];
    int	 mode;	/* mode : 0 RealCOM Mode, 1 Reduntant Mode*/
    char ipaddr2[40];
}
CONINFO;

char svrList[256][40];
int total[256];
int idx, change_flag;
CONINFO	info[256];

int SetSecure(int index);
int SelectNPort();

void GetIP(unsigned long ip, char *ret)
{
    struct in_addr ad;

    ad.s_addr = ip;
    sprintf(ret, "%s", inet_ntoa(ad));

}

int SetSecure(int index)
{
    int i, j, s, start, ret, page=0;
    struct in_addr ad;
    unsigned long ip;
    char	c[5];

    for (i = 0; i < 256; i++)
    {
        if (!strcmp(info[i].ipaddr, svrList[index]))
            break;
    }

    while (1)
    {
	int tot=0;
        system("clear");
        printf("Set Security Parameter ...\n");
        printf("<<Port Selection>>\n");
        printf("\n[ID]\t%-40s [Port]\t%-12s\t[Cert.]\n", "[Server IP]", "[Sec.]");
        s = 0;
        while (!strcmp(svrList[index], info[s+i].ipaddr))
        {
	    tot++;
            if (info[s+i].num > (page+1)*16 || info[s+i].num <= page*16)
	    {
		s++;
                continue;
	    }
#if 0
            if (info[s+i].secure)
                printf("  (%d)\t%-40s\t  %d\t  Yes", s+1, info[s+i].ipaddr, info[s+i].num);
            else
                printf("  (%d)\t%-40s\t  %d\t  No",  s+1, info[s+i].ipaddr, info[s+i].num);
#else
            printf("(%d)\t%-40s %d\t", s+1, info[s+i].ipaddr, info[s+i].num);
            switch(info[s+i].secure)
            {
                case SECURE_NONE:
                    printf("%-12s\t%s", "None", "None");
                    break;
                case SECURE_DATA:
                    printf("%-12s\t%s", "Data only", "None");
                    break;
                case SECURE_DATA_CMD:
                    printf("%-12s\t%s", "Data & command", "None");
                    break;
                case SECURE_DATA_CERT:
                    printf("%-12s\t%s", "Data only", "Enable");
                    break;
                case SECURE_DATA_CMD_CERT:
                    printf("%-12s\t%s", "Data & command", "Enable");
                    break;
            }
#endif
	    printf("\n");
            s++;
        }

        printf("(a)\tAll port Data only encrypted (For model name without '-G2')\n");
        printf("(b)\tAll port Data and Command encrypted (For model name with '-G2')\n");
        printf("(c)\tDisable all port encrypted\n");
        printf("(d)\tEnable all port Certificate Authentication (only active with secure enabled port)\n");
        printf("(e)\tDisable all port Certificate Authentication\n");

	if (tot > 16)
        {
            if (page == 0)
		printf("(n)\tnext page\n");
            if (page == 1)
                printf("(p)\tprevious page\n");
        }
        printf("(q)\tback to model selection\n");
        printf("\nPlease select a port you want to change security setting: ");

        scanf("%s", c);

        if ((c[0] == 'q') || (c[0] == 'Q'))
        {
            break;
        }
        if ((c[0] == 'n') || (c[0] == 'N'))
        {
            if (page == 0 && tot>16)
                page++; 
        }
        if ((c[0] == 'p') || (c[0] == 'P'))
        {
            if (page == 1 && tot>16)
                page--; 
        }
        else if ((c[0] == 'a') || (c[0] == 'A'))
        {
            int secure = SECURE_DATA;
            for(j=0; j<tot; j++)
            {
                info[i+j].secure = secure;
            }
            change_flag = 1;
        }
        else if ((c[0] == 'b') || (c[0] == 'B'))
        {
            int secure = SECURE_DATA_CMD;
            for(j=0; j<tot; j++)
            {
                info[i+j].secure = secure;
            }
            change_flag = 1;
        }
        else if ((c[0] == 'c') || (c[0] == 'C'))
        {
            int secure = SECURE_NONE;
            for(j=0; j<tot; j++)
            {
                info[i+j].secure = secure;
            }
            change_flag = 1;
        }
        else if ((c[0] == 'd') || (c[0] == 'D'))
        {
            for(j=0; j<tot; j++)
            {
                switch(info[i+j].secure)
                {
                    case SECURE_NONE:
                        info[i+j].secure = SECURE_NONE;
                        break;
                    case SECURE_DATA:
                        info[i+j].secure = SECURE_DATA_CERT;
                        break;
                    case SECURE_DATA_CERT:
                        info[i+j].secure = SECURE_DATA_CERT;
                        break;
                    case SECURE_DATA_CMD:
                        info[i+j].secure = SECURE_DATA_CMD_CERT;
                        break;
                    case SECURE_DATA_CMD_CERT:
                        info[i+j].secure = SECURE_DATA_CMD_CERT;
                        break;
                }
            }
            change_flag = 1;
        }
        else if ((c[0] == 'e') || (c[0] == 'E'))
        {
            for(j=0; j<tot; j++)
            {
                switch(info[i+j].secure)
                {
                    case SECURE_NONE:
                        info[i+j].secure = SECURE_NONE;
                        break;
                    case SECURE_DATA:
                        info[i+j].secure = SECURE_DATA;
                        break;
                    case SECURE_DATA_CERT:
                        info[i+j].secure = SECURE_DATA;
                        break;
                    case SECURE_DATA_CMD:
                        info[i+j].secure = SECURE_DATA_CMD;
                        break;
                    case SECURE_DATA_CMD_CERT:
                        info[i+j].secure = SECURE_DATA_CMD;
                        break;
                }
            }
            change_flag = 1;
        }
        else if ((atoi(c) > 0) && (atoi(c) <= s))
        {
            j = atoi(c) - 1;
            change_flag = 1;
            /*
            if (info[i+j].secure)
                info[i+j].secure = 0;
            else
                info[i+j].secure = 1;
            */
            switch(info[i+j].secure)
            {
                case SECURE_NONE:
                    info[i+j].secure = SECURE_DATA;
                    break;
                case SECURE_DATA:
                    info[i+j].secure = SECURE_DATA_CERT;
                    break;
                case SECURE_DATA_CERT:
                    info[i+j].secure = SECURE_DATA_CMD;
                    break;
                case SECURE_DATA_CMD:
                    info[i+j].secure = SECURE_DATA_CMD_CERT;
                    break;
                case SECURE_DATA_CMD_CERT:
                    info[i+j].secure = SECURE_NONE;
                    break;
            }
        }
    }

    return 1;
}

int SelectNPort()
{

    int i, ret;
    struct in_addr ad;
    char c[5];

    system("clear");
    printf("Set Security Parameter ...\n");
    printf("<<Model Selection>>\n");

    printf("\n[ID]\t%-40s\t[Port(s)]\n", "[Server IP]");
    for (i=0; i<idx; i++)
    {
        printf("(%d)\t%-40s\t  %d\n", i+1, svrList[i], total[i]);
    }

	printf("(q)\tExit \n");
    printf("\nPlease select a model you want to set up: ");
    scanf("%s", c);

    if ((c[0] == 'q') || (c[0] == 'Q'))
        return -1;
    if (atoi(c)<=0 || atoi(c)>idx)
        return 0;
    else
    {
        ret = SetSecure(atoi(c)-1);
    //    SelectNPort();
    }
    return 0;
}

int main(int arg, char *argv[])
{
    int i, j;
    int len, daemon, num, ret;
    char *tmpstr, *tmp;
    char token[40], tty[10], cout[10], major[20], del[16], sec[10], index[10];
    char data[10], cmd[10], fifo[10], scope[10];
    char token2[40]={0};
    char mode[10];
    FILE *f, *ft;

    idx = 0;
    daemon = 0;
    change_flag = 0;
    tmpstr = (char *)malloc(1024);
    len = 1024;
    tmp = (char *)malloc(20);
  
    MK_TEMP();

    memset(scope, 0x0, sizeof(scope));
    memset(svrList, 0x0, 256*40);
    memset(total, 0x0, 256*sizeof(int));
    memset(info, 0x0, 256*sizeof(CONINFO));
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
		len = 1024;
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

        sscanf(tmpstr, "%s%s%s%s%s%s%s%s%s%s%s", index, token, data, cmd, fifo, sec, tty, cout, scope, mode, token2);
        num = atoi(index);
        for (i=0; i<idx; i++)
        {
            if (!strcmp(svrList[i],token))
            {
                total[i]++;
                info[num].idx = num;
                strcpy(info[num].ipaddr, token);
                strcpy(info[num].data, data);
                strcpy(info[num].cmd, cmd);
                strcpy(info[num].fifo, fifo);
                info[num].secure = atoi(sec);
                strcpy(info[num].tty, tty);
                strcpy(info[num].cout, cout);
                info[num].num = total[i];
                strcpy(info[num].scope_id, scope);
		info[num].mode = atoi(mode);
                strcpy(info[num].ipaddr2, token2);
                break;
            }
        }
        if (i == idx)
        {
            strcpy(svrList[idx], token);
            total[idx]++;
            info[num].idx = num;
            strcpy(info[num].ipaddr, token);
            strcpy(info[num].data, data);
            strcpy(info[num].cmd, cmd);
            strcpy(info[num].fifo, fifo);
            info[num].secure = atoi(sec);
            strcpy(info[num].tty, tty);
            strcpy(info[num].cout, cout);
            info[num].num = total[i];
            strcpy(info[num].scope_id, scope);
	    info[num].mode = atoi(mode);
            strcpy(info[num].ipaddr2, token2);
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

    while(SelectNPort() == 0)
    {}

    printf("Exit!!\n\n");

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

    for (;;)
    {
		len = 1024;
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
        for (i=0; i<256; i++)
        {
            if (strlen(info[i].ipaddr) > 0)
	    {
#if 1
                sprintf (tmpstr, "%d\t%s\t%s\t%s\t%s\t%d %s\t%s\t%s\t%d\t%s\n", info[i].idx, info[i].ipaddr,
                info[i].data, info[i].cmd, info[i].fifo, info[i].secure, info[i].tty, info[i].cout, info[i].scope_id,
		info[i].mode, info[i].ipaddr2);
#else
                sprintf (tmpstr, "%d\t%s\t%s\t%s\t%s\t%d %s\t%s\t%s\n", info[i].idx, info[i].ipaddr,
                info[i].data, info[i].cmd, info[i].fifo, info[i].secure, info[i].tty, info[i].cout, info[i].scope_id);
#endif
                fputs (tmpstr, ft);
                /* daemon is a flag which is used to delete the */
                /* daemon start string in /etc/rc.d/rc.local */
                if (change_flag)
                    daemon = 1;
            }
        }
        break;
    }

    fclose(ft);
    fclose (f);

#ifndef NO_INIT
#if 0  /* Comment it because I don't know why does original code remove mxloadsvr if config not changed? */
    if (!daemon)
    {
		system("rm -f /usr/lib/npreal2/driver/state.start > /dev/null 2>&1");
		//system("systemctl disable npreal2 > /dev/null 2>&1");
    }
#endif
#endif /* ifndef NO_INIT */

    sprintf(tmpstr, "cp -f /usr/lib/npreal2/tmp/nprtmp_cf %s/npreal2d.cf", DRIVERPATH);
    system(tmpstr);
    system("rm -f /usr/lib/npreal2/tmp/nprtmp_cf");

    sprintf(tmpstr, "%s/mxloadsvr", DRIVERPATH);
    system(tmpstr);

    free(tmpstr);
    free(tmp);

    RM_TEMP();
    return 0;
}


