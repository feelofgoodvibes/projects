#include <stdio.h>
#include <windows.h>
#include <time.h>
#include <conio.h>

#define TEXT_LEN 10000
#define PRINT_ONLY 50

char good_symbols[] = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz";
HANDLE hStdOut;
CONSOLE_SCREEN_BUFFER_INFO standart_buffer;

void set_output_color(){
	SetConsoleTextAttribute(hStdOut, 0 | BACKGROUND_BLUE | BACKGROUND_GREEN | BACKGROUND_RED | BACKGROUND_INTENSITY);
}

void reset_output_color(){
	SetConsoleTextAttribute(hStdOut, standart_buffer.wAttributes);
}

void setup_output_color(){
	hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);
	GetConsoleScreenBufferInfo(hStdOut, &standart_buffer);
}

void print_progress(char* text, int text_len, char* current_letter){
	if ((current_letter - text) < PRINT_ONLY/2) fwrite(text, current_letter - text, 1, stdout);
	else fwrite(current_letter - (PRINT_ONLY / 2), (PRINT_ONLY / 2), 1, stdout);
	set_output_color();
	printf("%c", *current_letter);
	reset_output_color();
	fwrite(current_letter + 1, (PRINT_ONLY / 2), 1, stdout);
}

void main(){
	setup_output_color();
	printf("\n\n\n");

	char text[TEXT_LEN];
	char* current_letter = text;				// current letter user must press
	FILE* textfile = fopen("text.txt", "r");
	fread(text, TEXT_LEN, 1, textfile);
	int text_len = 0;
	int mistakes = 0;							// wrong keyboard strokes

	// fixing text, accepting only "good_symbols"
	for (char* c = text; *c; c++){
		char* gc;
		for (gc = good_symbols; *gc; gc++)
			if (*c == *gc) break;

		if (!(*gc)) *c = ' ';
		text_len += 1;
	}

	clock_t start = NULL;
	double current_time = 0;

	while (*current_letter){
		if (start) current_time = (double)(clock() - start) / CLOCKS_PER_SEC;
		else start = clock();

		printf("  [%5.2f] [%3.0f symb/min] ", current_time, ((current_letter - text) * 60) / current_time);
		print_progress(text, text_len, current_letter);
		
		if (getch() == *current_letter) current_letter++;
		else mistakes += 1;

		printf("\r");
	}

	printf("Text len: %d, done in %.2f seconds. %.0f symb/min, %d mistakes (%.2f%%)                                      \n", text_len, current_time, (text_len * 60) / current_time, mistakes, ((double)mistakes * 100) / text_len);
	printf("Press [Q] to Quit\n");
	while (getch() != 'q') continue;
}