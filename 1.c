#include <stdio.h>


Symtab * GlobalTable;            //global symble table for variables

 

/* the hash function */

static int hash(char * key)

{

  int temp = 0;

  int i;

  for (i = 0; key[i] != '\0'; i++)

         temp = ((temp << SHIFT) + key[i]) % SIZE;

  return temp;

}

static int error(char * key)

{

          char a='a;

          a='';

          a='\a';

          a='b';

          int b=1e;

          b=12ef;

          b=12.2.3;

         int B=@b;

         b=0xgh;

         b=089;

         b=12.;

         b=12;

         b=0.2;

         b=012ef;

         b=0x12effe;

         b=0076;

         b=12e12;

         b=12e-12;

         b=12e+12;

         b=12.90e-12;

         char b[]="kjk;

         b=" ' ";

         b="\ojk";

         b="\ajkl\" jshkh\"khk" ;      

}

 

static int success(char * key)

{

          char a='b';

          int b=12.90e-12;

          b=0x12fe;

          b=076601;

          b=76601e12;

          char b="\ajkl\" jshkh\"khk" ;

}

 

void printSymTab(TreeNode * tree)