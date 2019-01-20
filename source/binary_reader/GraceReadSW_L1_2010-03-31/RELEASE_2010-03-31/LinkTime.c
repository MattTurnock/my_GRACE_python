# include <stdio.h>
# include <string.h>
# include <inttypes.h>
 
void LinkTime(char *label)
{
 int8_t  tag[] = "@(#) 2019-01-20 11:35:17 matt  matt-amd-desktop";
 strcpy(label,tag);
}
