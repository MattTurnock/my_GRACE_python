#include "GRACEiolib.h"
#include "GRACEio_utils.h"
#include "GRACEio_prototypes.h"


#define NBITSMAX 16

static int8_t SccsId[] = "$Id: ReadGPS1AFRecord.c,v 1.6 2009/06/06 22:15:38 glk Exp $";


boolean ReadGPS1AFRecord(FILE *src, GPS1A_t *record)
/*----------------------------------------------------------------------------->
/ purpose: read GPS Flight Data Format record from file pointer src
/          using generic routine ReadGFD1XFRecord.c
/
/ input:  *src    pointer to GPS Flight Data Format File
/ output: *record Pointer to GPS Flight Data struct (GPS1A_t)
/
/ return:      1       normal return
/              0       End Of File reached
<-----------------------------------------------------------------------------*/
{

  if (ReadGFD1XFRecord(src, record))
  {
    return True;
  }
  else
  {
    return False;
  }
}