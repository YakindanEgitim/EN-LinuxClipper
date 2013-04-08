#include <gtkmm.h>

int main(int argc, char *argv[])
{
  Glib::RefPtr<Gtk::Application> app = Gtk::Application::create(argc, argv, "org.gtkmm.examples.base");
  Gtk::Window window;
  Gtk::Button button1;

  window.set_title("deneme");
  window.add(button1);
  window.show_all();
  
  return app->run(window);
}
