#/* Copyright (C) MOXA Inc. All rights reserved.

   This is free software distributed under the terms of the
   GNU Public License.  See the file COPYING-GPL for details.
*/

#ifndef _MISC_H_
#define _MISC_H_

extern void _log_event_backup(char *log_pathname, char *msg);
extern int ipv4_str_to_ip(char *str, ulong *ip);
extern int ipv6_str_to_ip(char *str, unsigned char *ip);
extern unsigned long filelength(int f);
extern int check_ps_param();

#endif /* _MISC_H_ */
