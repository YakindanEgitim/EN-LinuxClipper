CC = g++
SRC_DIR = src
OUTPUT = main
OUTPUT_DIR = build
LIBS = gtkmm-3.0

all:
	rm -rf $(OUTPUT_DIR)
	mkdir $(OUTPUT_DIR)
	$(CC) -Wall -I $(SRC_DIR) $(SRC_DIR)/*.cpp -o $(OUTPUT_DIR)/$(OUTPUT) `pkg-config $(LIBS) --cflags --libs`
	$(OUTPUT_DIR)/$(OUTPUT)

	