//main.cpp
#include <gtkmm.h>
#include <gdkmm.h>
#include <iostream>
#include "clipper.h"

int main(int argc, char *argv[])

{
    Gtk::Main kit(argc, argv);
    capture_screen();
    capture_window();
    capture_area();
    return 0;
}



