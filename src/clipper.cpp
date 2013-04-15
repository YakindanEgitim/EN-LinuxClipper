#include <gtkmm.h>
#include <gdkmm.h>
#include <iostream>
#include <clipper.h>

void capture_screen()
{
    Glib::RefPtr<Gdk::Window> root_win =  Gdk::Window::get_default_root_window();
    
    int width = root_win->get_width();
    int height = root_win->get_height();

    int x_orig, y_orig;
    root_win->get_origin(x_orig, y_orig);

    Glib::RefPtr<Gdk::Pixbuf> screenshot = Gdk::Pixbuf::create(root_win, x_orig, y_orig, width, height);
    screenshot->save("/tmp/testshot0.png", "png");
}

void capture_window()
{
    Glib::RefPtr<Gdk::Screen> screen = Gdk::Screen::get_default();
    Glib::RefPtr<Gdk::Window> active_win = screen->get_active_window();

    int width = active_win->get_width();
    int height = active_win->get_height();

    //int x_orig, y_orig;
    //active_win->get_origin(x_orig, y_orig);

    Glib::RefPtr<Gdk::Pixbuf> screenshot = Gdk::Pixbuf::create(active_win, 0, 0, width, height);
    screenshot->save("/tmp/testshot1.png", "png");

}

void capture_area()
{
    Glib::RefPtr<Gdk::Window> root_win =  Gdk::Window::get_default_root_window();
    
    int width = root_win->get_width();
    int height = root_win->get_height();

    int x_orig, y_orig;
    root_win->get_origin(x_orig, y_orig);

    Glib::RefPtr<Gdk::Pixbuf> screenshot = Gdk::Pixbuf::create(root_win, x_orig, y_orig, width, height);
    Gtk::Window selection_window;

    selection_window.move(0,0);
    selection_window.set_decorated(FALSE);
    selection_window.set_size_request(width, height);
    Gtk::Main::run(selection_window);

}
