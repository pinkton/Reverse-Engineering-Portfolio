#include "extra.h"

char sent1[] = "Ahh you found the correct path, move along\n\n";
char sent2[] = "Enter the amount of characters required previously:\n";
char sent3[] = "Level up!!\n";
char sent4[] = "Nope, through the trap door you go!\n";
char sent5[] = "On second thoughts. Nope\n";
char sent6[] = "Gutted mate. Try again\n";


void second_stage() {
	char ss_answer[2];
	printf(sent1);
	printf(sent2);
	fgets(ss_answer, 2, stdin);
	if (ss_answer[0] == '4') {
		printf(sent3);
		Sleep(2000);
		third_stage(); //Fake third stage
	}
	else if (ss_answer[0] == 'F') {
		printf(sent3);
		Sleep(2000);
		Third_stage(); //Real third stage
	} else {
		printf(sent4);
		Sleep(2000);
		first_stage();
	}
}

void second_Stage() {
	printf(sent5);
	Sleep(2000);
	first_stage();
}

void third_stage() {
	printf(sent6);
	Sleep(2000);
	first_stage();
}

