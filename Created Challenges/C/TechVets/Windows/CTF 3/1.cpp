#include "extra.h"

char welcomemsg[] = "Welcome to Pinks laughable mess that will annoy you, but made me chuckle whilst making it\n";
char set1[] = "Enter the first password :\n";
char set2[] = "Ok, you got lucky. Move along\n";
char set3[] = "Not today, children!\n";
char set4[] = "Ok, last challenge. You can't jump this because its the final challenge,\nbut you need to look for pass that's playing hide and seek in your\ndebugger/disassembler of choice and maybe phone home?\n";
char set5[] = "Too many characters. Calm down, poorly coded and may break.\n";

void welcome() {
	printf(welcomemsg);

	return;
}

void first_stage() {
	char guess_1[20];
	Sleep(2000);
	// First stage
	printf(set1);
	fgets(guess_1, 10, stdin);
	size_t lenguess = strlen(guess_1);
	if (lenguess == 5) {
		printf(set2);
		Sleep(2000);
		second_Stage(); // Ensure to capitalise Stage on prod
		second_stage();
	}
	else if (lenguess > 7) {
		printf(set5);
		Sleep(2000);
		first_stage();
	}
	else {
		printf(set3);
		Sleep(2000);
		first_stage();
	}
}

void Third_stage() {
	printf("Impressive! Looks like we need to be evil to finish.\n\n");
	Sleep(2000);
	printf(set4);
	Sleep(2000);
	Print();
}
