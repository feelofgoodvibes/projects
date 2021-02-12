#include "cmdpaint.h"

void clear_last_lines(int after, int amount){
	static COORD clear_info;
	clear_info.X = 0;

	for (int i = after; i < after + amount; i++){
		clear_info.Y = i;
		SetConsoleCursorPosition(con_handle, clear_info);
		printf("                                                                                                      ");
		printf("                                                                                                      ");
		printf("                                                                                                      ");
	}
}

void get_mouse_pos(){
	GetWindowRect(win_handle, &con_size);
	GetCursorPos(&mouse_pos);

	con_size.left += 9;
	con_size.top += 31;
	con_size.bottom -= 29;
	con_size.right -= 29;

	mouse_pos.x = mouse_pos.x - con_size.left;
	mouse_pos.y = mouse_pos.y - con_size.top;
}

int is_mouse_on_con(){
	if (mouse_pos.x < 0 || mouse_pos.y < 0) return 0;
	if (((con_size.right - con_size.left) < mouse_pos.x) || ((con_size.bottom - con_size.top) < mouse_pos.y)) return 0;
	return 1;
}

int is_mouse_on_canvas(){
	if (mouse_pos.x < 0 || mouse_pos.y < 0) return 0;
	if (mouse_pos.x > font_info.dwFontSize.X * SIZEX || mouse_pos.y > font_info.dwFontSize.Y * SIZEY)  return 0;
	return 1;
}

int is_key_down(int keycode){ return (GetKeyState(keycode) & 128) >> 7; }


void clear_console_input_buffer(){
	INPUT_RECORD input_rec[INPUT_BUFFER_SIZE];
	DWORD readed = INPUT_BUFFER_SIZE;

	while (readed == INPUT_BUFFER_SIZE)
		ReadConsoleInput(inp_handle, input_rec, INPUT_BUFFER_SIZE, &readed);
}
