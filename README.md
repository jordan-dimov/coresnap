# coresnap

This repo contains a Python script which visualises tree structures based on indented text. It can, among other things, be used to visualise simple "mind-maps" of notes and outlines. Using GPT and this script you can summarise entire articles, papers or books into a single image. 

This project uses Poetry as the Python dependency manager. It uses GraphViz for rendering the images. You will need both of these tools installed as pre-requisites. 


## Step 0: Install dependencies

    poetry install


## Step 1: Use GPT to summarise the body of text

Here is the prompt I use:

    Generate a mindmap with the core ideas from the book "The Inner Game of Tennis" and output it as an indented list of bullet points. 

This is the typical output:

    - The Inner Game of Tennis
        - Two Selves
            - Self 1: Conscious thinking, analytical mind
            - Self 2: Subconscious, intuitive, bodily action
        - Focusing on the Process
            - Concentration on the present moment
            - Ignoring past mistakes or future concerns
        - Trusting the Body
            - Allowing Self 2 to guide movement
            - Avoid overthinking actions

## Step 2: Use the script to produce a DOT file

Once you have the hierarchical list of bullet points saved in a text file, you can use the script to produce a DOT file:

    poetry run python src/coresnap.py samples/inner_game_of_tennis.txt

This will output a DOT file with a description of the mind-map tree. The DOT file (which is a text file) can be visualised with GraphViz. 

## Step 4: Render the DOT file into a PNG

    poetry run python src/coresnap.py render output.dot samples/inner_game_of_tennis.png --output-format=png

Supported file formats are: PNG, JPG, GIF, SVG, PDF, PS