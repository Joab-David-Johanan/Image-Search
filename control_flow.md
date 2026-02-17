## Control flow of the program:

1. Started with streamlit ***`app.py`*** file where we created all the streamlit widgets like ***`radio buttons`***, ***`expanders`***, ***`buttons`***.
2. Then created `src` folder where we created `inference.py` where we create a class called ***`YOLO_V11_Inference`*** and initialize it ***`model_name`***, ***`device`***. The class also handles behaviors in separate methods like ***`process_images`***, ***`process_directory`***.
3. We create a ***`configs`*** folder where we created ***`default.yaml`*** config file that is used in ***`inference.py`***
4. We call the ***`YOLO_V11_Inference`*** in ***`app.py`*** in when the user clicks on ***`Start Inference`***.
5. Once the inference class processes the images using the ***`process_images`*** method it returns the metadata which has to loaded and handled.
6. To handle the metadata we create a ***`utils.py`*** where we create directories to store the metadata.
7. Back in the ***`app.py`*** we save the metadata in session state and also we create ***`load_metadata`*** function in ***`utils.py`*** to load the metadata.
8. Once the metadata is saved it can be used to power the search functionality of the application.
9. We create a ***`search_params`*** variable in the session state to store ***`search_mode`***, ***`selected_classes`*** and ***`threshold`*** where in we allow the user to select the search mode, what classes they want to see and how many classes they want to see in their image.
10. The display functionality uses the search params values to control the images displayed as image-cards in columns that are controlled by a ***`grid_columns`*** variable in session state.