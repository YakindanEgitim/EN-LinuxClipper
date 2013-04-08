CC = g++
SRC_DIR = src
FILES = testapp.cpp
OUTPUT = testapp
OUTPUT_DIR = build
LIBS = gtkmm-3.0

build:
	mkdir $(OUTPUT_DIR)
	$(CC) -Wall $(SRC_DIR)/$(FILES) -o $(OUTPUT_DIR)/$(OUTPUT) `pkg-config $(LIBS) --cflags --libs`

run:
	$(OUTPUT_DIR)/$(OUTPUT)

clean:
	rm -rf $(OUTPUT_DIR)