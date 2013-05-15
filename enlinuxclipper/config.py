from base64 import b64encode, b64decode
import ConfigParser
import os


class ConfigManager():
    """
    This class reponsible for keeping and saving configuration variables
    """

    # set default values
    config = ConfigParser.SafeConfigParser({'access_token': '',
                                           'play-sound': 'True',
                                           'copy-to-clipboard': 'True',
                                           'googl-shortlink': 'True'})

    # config path
    cfg_dir = os.environ['HOME'] + '/.config/en-linuxclipper/'
    cfg_file = 'main.cfg'
    cfg_full_path = cfg_dir + cfg_file

    namespace = 'DEFAULT'
    config.read(cfg_full_path)

    @staticmethod
    def get_conf(key):
        """ Return configuration value for key """
        try:
            value = ConfigManager.config.get(ConfigManager.namespace, key)
        except ConfigParser.Error:
            print ("[DEBUG] No option '%s' found in namespace '%s'." %
                   (key, ConfigManager.namespace))
            return None

        # config parser storing all values as string
        # we need to convert them to python types
        try:
            return int(value)
        except ValueError:
            if value == 'True':
                return True
            elif value == 'False':
                return False
            else:
                if key == 'access_token':
                    # base64 required for parsing file properly
                    # because access_token have many special charachters.
                    value = b64decode(value)
                return value

    @staticmethod
    def set_conf(key, value):
        """ Keep new value for key """
        if key == 'access_token':
            value = b64encode(value)
        try:
            ConfigManager.config.set(ConfigManager.namespace, key, str(value))
        except ConfigParser.Error:
            print ("[DEBUG] No option '%s' found in namespace '%s'." %
                   (key, ConfigManager.namespace))
            return

    @staticmethod
    def save_config():
        """ Save configuration variables to file. """
        if not os.path.exists(ConfigManager.cfg_dir):
            os.mkdir(ConfigManager.cfg_dir)

        with open(ConfigManager.cfg_full_path, 'wb') as configfile:
            ConfigManager.config.write(configfile)

