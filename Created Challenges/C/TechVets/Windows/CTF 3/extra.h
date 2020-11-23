#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <windows.h>

#define HIDE_LETTER(a)   (a) + 0x50
#define UNHIDE_STRING(str)  do { char * ptr = str ; while (*ptr) *ptr++ -= 0x50; } while(0)
#define HIDE_STRING(str)  do {char * ptr = str ; while (*ptr) *ptr++ += 0x50;} while(0)

void first_stage();
void second_stage();
void second_Stage();
void third_stage();
void Third_stage();
void Print();
void hidepass();
void welcome();
