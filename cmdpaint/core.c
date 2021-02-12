#include "cmdpaint.h"

short PAL_KEYS[6] = {0x31, 0x32, 0x33, 0x34, 0x35, 0x36};
short PAL_NUMKEYS[6] = {VK_NUMPAD1, VK_NUMPAD2, VK_NUMPAD3, VK_NUMPAD4, VK_NUMPAD5, VK_NUMPAD6};
int show_coords = 1;

int main(){
	system("CLS");
	// Console setting-up
	win_handle = GetConsoleWindow();
	con_handle = GetStdHandle(STD_OUTPUT_HANDLE);
	inp_handle = GetStdHandle(STD_INPUT_HANDLE);
	SetConsoleTitle("CMDPaint");
	GetCurrentConsoleFont(con_handle, 0, &font_info);

	// Canvas setting-up

	printf("\t\t    ____ __  __ ____  ____       _       _   \n");
	printf("\t\t   / ___|  \\/  |  _ \\|  _ \\ __ _(_)_ __ | |_ \n");
	printf("\t\t  | |   | |\\/| | | | | |_) / _` | | '_ \\| __|\n");
	printf("\t\t  | |___| |  | | |_| |  __/ (_| | | | | | |_ \n");
	printf("\t\t   \\____|_|  |_|____/|_|   \\__,_|_|_| |_|\\__|\n");
	printf("\n\t===============================================================\n\n\t\t\t\tHow to use:\n\n");
	printf("\t>> Navigate with mouse cursor\n");
	printf("\t>> Press 1/2/3/4/5/6 to draw 1/2/3/4/5/6 symbol from palette\n");
	printf("\t>> Press [Shift] + 1/2/3/4/5/6 to change this symbol in palette\n");
	printf("\t>> E - Erase pixel\n");
	printf("\t>> C - Clear canvas\n");
	printf("\t>> F - Fill canvas with 1st color in palette\n");
	printf("\t>> T - Show/Hide GUI\n");
	printf("\t>> S - Save art in file\n");
	printf("\t>> O - Open art from file\n\n\t===============================================================\n");

	COORD screen_size;
	screen_size.X = GetSystemMetrics(SM_CXFULLSCREEN);
	screen_size.Y = GetSystemMetrics(SM_CYFULLSCREEN);

	printf("\n\n\t\t\t\tCanvas settings\n\t\t\tEnter X (fullscreen: near %d): ", ((screen_size.X - 20) / font_info.dwFontSize.X));
	if (scanf("%d", &SIZEX) == 0) { printf("Wrong entry!\n"); system("PAUSE"); return 1; };
	fflush(stdin);

	printf("\t\t\tEnter Y (fullscreen: near %d): ", ((screen_size.Y - (int)((double)screen_size.Y*0.05)) / font_info.dwFontSize.Y) - 1);
	if (scanf("%d", &SIZEY) == 0) { printf("Wrong entry!\n"); system("PAUSE"); return 1; };
	fflush(stdin);

	if ((font_info.dwFontSize.X * SIZEX) > (screen_size.X - 20))
		printf("X is probably too big and will not fit your screen.\nTry lower X value.\n\n");
	if ((font_info.dwFontSize.X * SIZEY) > ((screen_size.Y - (int)((double)screen_size.Y*0.05))-1))
		printf("Y is probably too big and will not fit your screen.\nTry lower Y value.\n\n");

	strcpy(palette, "OOOOOO");

	system("CLS");
	canvas = canvas_init(SIZEX, SIZEY, *palette);
	canvas_print();

	while (1){
		get_mouse_pos(win_handle, con_handle, &mouse_pos, &con_size);


		for (int i = 0; i < 6; i++){
			if ((is_key_down(PAL_KEYS[i]) || is_key_down(PAL_NUMKEYS[i])) && is_mouse_on_canvas()) {
				pixel_set(palette[i]);
				canvas_print();
				break;
			}
		}

		if (is_key_down(K_ERASE)  && is_mouse_on_canvas()) {
			pixel_set(' ');
			canvas_print();
			continue;
		}

		if (is_key_down(K_FILL)){
			free(canvas);
			canvas = canvas_init(SIZEX, SIZEY, *palette);
			canvas_print();
			continue;
		}

		if (is_key_down(K_CLEAR)){
			free(canvas);
			canvas = canvas_init(SIZEX, SIZEY, ' ');
			canvas_print();
			continue;
		}

		if (is_key_down(VK_SHIFT)){
			canvas_print();
			for (int i = 0; i < 6; i++){
				if (is_key_down(PAL_KEYS[i]) || is_key_down(PAL_NUMKEYS[i])) {
					change_palette_color(i);
					clear_last_lines(SIZEY, 5);
					canvas_print();
					break;
				}
			}
		}

		if (is_key_down(K_T)){
			if (show_coords) show_coords = 0;
			else show_coords = 1;

			clear_last_lines(SIZEY, 2);
			canvas_print();
			system("timeout /t 1 /nobreak > nul");
			continue;
		}

		if (is_key_down(K_SAVE)){
			canvas_print();
			char filename[MAX_FILENAME];
			printf("\n\nSaving art. Enter filename (leave blank to break): ");
			clear_console_input_buffer();
			gets(filename);
			fflush(stdin);
			if (!*filename){
				clear_last_lines(SIZEY, 5);
				canvas_print();
				continue;
			}
			strcat(filename, ".cmdart");
			save_art(filename);
			system("PAUSE>nul");
			system("CLS");
			canvas_print();
			continue;
		}

		if (is_key_down(K_OPEN)){
			canvas_print();
			char filename[MAX_FILENAME];

			printf("\n\nEnter filename to open an art (leave blank to break): ");
			clear_console_input_buffer();
			gets(filename);
			fflush(stdin);

			if (!*filename){
				clear_last_lines(SIZEY, 5);
				canvas_print();
				continue;
			}

			int op = open_art(filename);
			if (op == 1){
				printf("Cant find file [%s]\nPress any key to continue...", filename);
				system("PAUSE>nul");
				system("CLS");
				canvas_print();
			}

			if (op == 2){ return 1; }

			system("CLS");
			canvas_print();
			continue;
		}
	}

	system("PAUSE>nul");
	return 0;
}
