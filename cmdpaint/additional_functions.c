#include "cmdpaint.h"

void change_palette_color(int pal){
	printf("Enter %d palette symbol: ", pal + 1);
	clear_console_input_buffer();
	char newchar = getchar();
	if (newchar != '\n') *(palette + pal) = newchar;
	fflush(stdin);
}

int open_art(char* filename){
	FILE* openart = fopen(filename, "rb");
	if (!openart){ return 1; }

	fread(&SIZEX, sizeof(int), 1, openart);
	fread(&SIZEY, sizeof(int), 1, openart);
	free(canvas);

	canvas = (char*)malloc((sizeof(char) * (SIZEX+1))*SIZEY);
	if (!canvas) {
		printf("Memory error!\n");
		system("PAUSE");
		return 2;
	}
	fread(canvas, (sizeof(char) * (SIZEX+1))*SIZEY, 1, openart);
	fclose(openart);

	return 0;
}

int save_art(char* filename){
	FILE* saveart = fopen(filename, "wb");
	if (!saveart) return 1;
	
	fwrite(&SIZEX, sizeof(int), 1, saveart);
	fwrite(&SIZEY, sizeof(int), 1, saveart);
	fwrite(canvas, sizeof(char) * (SIZEX+1) * SIZEY, 1, saveart);
	printf("Art saved in [%s]\n\nPress any key to continue...", filename);
	fclose(saveart);

	return 0;
}
