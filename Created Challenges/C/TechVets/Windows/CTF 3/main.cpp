//CTF Demo 3 - PRET(P1NK_L0V35_DES_REV3NG_F14G_P74Y) 
#include "extra.h"

int main() {
    hidepass();
	first_stage();
}

void Print() {
    Sleep(2000);
    printf("\nThe final flag then, is;\n");
    Sleep(2000);
    printf("PRET(P1NK_L0V35_\n");
    Sleep(2000);
    printf("\n What did you need to find out? (???_???_???)\n"); //DES_REV3NG
    Sleep(2000);
    printf("_F14G_P74Y\n");

    exit(0);
}

//Not my work. Source link >> https://yurisk.info/2017/06/25/binary-obfuscation-string-obfuscating-in-C/
//Live link last checked online, working, 23/11/2020 (The year that shall not be spoken about!)

void hidepass() {   // store the "secret password" as mangled byte array in binary
    char str1[] = { HIDE_LETTER('D') , HIDE_LETTER('E') , HIDE_LETTER('S') , HIDE_LETTER('R') , HIDE_LETTER('E')
    , HIDE_LETTER('V') , HIDE_LETTER('E') , HIDE_LETTER('N') , HIDE_LETTER('G'),'\0' };

    UNHIDE_STRING(str1);  // unmangle the string in-place
    printf("%s", str1);
    HIDE_STRING(str1);  //mangle back

    return;
}
