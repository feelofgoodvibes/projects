#include "cmdpaint.h"

char* canvas_init(int x, int y, char fillchar){
	char* canvas = (char*)malloc((sizeof(char) * (x+1))*y);

	if (canvas == NULL){ return NULL; }

	for (int loop_y = 0; loop_y < y; loop_y++){
		for (int loop_x = 0; loop_x < x; loop_x++){
			*(canvas + (loop_y * (x + 1)) + loop_x) = fillchar;
		}
		*(canvas + (loop_y * (x + 1)) + x) = '\n';
	}

	return canvas;
}

void canvas_print(){
	static COORD start_of_cmd;
	start_of_cmd.X = 0;
	start_of_cmd.Y = 0;

	SetConsoleCursorPosition(con_handle, start_of_cmd);
	fwrite(canvas, (SIZEX+1)*SIZEY, 1, stdout);
	if (show_coords) printf("\nPalette:\n1: %c   2: %c   3: %c   4: %c   5: %c   6: %c           [%4ld ; %-4ld]   ",
		*palette, *(palette + 1), *(palette + 2), *(palette + 3), *(palette + 4), *(palette + 5),
		(mouse_pos.x / font_info.dwFontSize.X), (mouse_pos.y / font_info.dwFontSize.Y));
}

void pixel_set(char symbol){
	int targx, targy;

	targx = (mouse_pos.x / font_info.dwFontSize.X);
	targy = (mouse_pos.y / font_info.dwFontSize.Y);

	if (*(canvas + (targy * (SIZEX+1)) + targx) == '\n') return;
	*(canvas + (targy * (SIZEX+1)) + targx) = symbol;
}