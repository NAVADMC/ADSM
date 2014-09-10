
#ifndef _MEMOIZATION_H_
#define _MEMOIZATION_H_

#include "herd.h"

#define _IN_
#define _IN_OUT_
#define _OUT_


#ifndef TRUE
#define TRUE           (1)
#endif

#ifndef FALSE
#define FALSE          (0)
#endif


typedef unsigned int 	uint;
typedef unsigned short 	ushort;
typedef unsigned long 	ulong;
typedef uint 	boolean;


typedef struct HerdLocation HerdLocation;

/* location information of the a herd */

struct HerdLocation {
	uint uiID;    /* this is the id of this herd in the main herd list */
	float fLat;	/* can be latitude or longitude */
	float fLon;	/* can be longitude or latitude */
};

/************************** memoization functions ***********************************/


/*
   Description : This function initializes the memoization table and also 
                  creates sorted herd lists for circles and squares algorithm.
   Parameters  :  pointer to the herd list

   Usage :     : should be called before any calls are made to "searchWithMemoization" 
                  or "serchWithCirclesAndSquare, 
                  typically after herd list is created in main function "run_sim_main"  
*/
void initCirclesAndSquaresList(HRD_herd_list_t* herds);

/*
   Description  : search in circles and squares with memoization
   Parameters  : pointer to the herd for which "herds in proximity is calculated", 
                   "Radius" with which herds are to be found.
		   callback function to be called for a herd in given proximity (same as RTree argument)
		   arguments for callback function
 */
boolean searchWithMemoization (HRD_herd_t* pHerd, double dRadius,
			      SearchHitCallback pfCallback, void* pCallbackArgs);

/*
   Description  : search in circles and squares without memoization
   Parameters  : pointer to the herd for which "herds in proximity is calculated", 
                   "Radius" with which herds are to be found.
		   callback function to be called for a herd in given proximity (same as RTree argument)
		   arguments for callback function (same as RTree argument)
 */
/
boolean searchWithCirclesAndSquares (HRD_herd_t* pHerd, double dRadius,
				     SearchHitCallback pfCallback, void* pCallbackArgs);

#endif /* _MEMOIZATION_H_ */
