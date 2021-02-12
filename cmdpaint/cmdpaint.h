#ifndef CMDP_H

#define CMDP_H

#include <windows.h>
#include <stdio.h>

#define MAX_FILENAME 100
#define INPUT_BUFFER_SIZE 5

#define K_ERASE	0x45
#define K_CLEAR	0x43
#define K_FILL	0x46
#define K_T 	0x54
#define K_SAVE 	0x53
#define K_OPEN 	0x4F

short PAL_KEYS[6];

CONSOLE_FONT_INFO font_info;
HWND win_handle;
HANDLE con_handle;
HANDLE inp_handle;
POINT mouse_pos;
RECT con_size;
int show_coords;

int SIZEX;
int SIZEY;
char* canvas;
char palette[7];

char* canvas_init(int x, int y, char fillchar);
void canvas_print();
void pixel_set(char symbol);

void get_mouse_pos();
int is_mouse_on_con();
int is_mouse_on_canvas();
int is_key_down(int keycode);

void clear_console_input_buffer();
void clear_last_lines(int after, int amount);

void change_palette_color(int pal);

int open_art(char* filename);
int save_art(char* filename);

#endif