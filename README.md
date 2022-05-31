# Link-the-Twin
Beat the twin link!

This project is the program that help you match the cartoon character for the sake of matching game playing. As the name says, this project is designed for the game names 'Twin Link' (IOS) or 'Twin Fun' (Android). The brief explanations of how this project work are 1. It find all possible pattern, 2. It find matched pattern, 3. It show matched pattern to you.

# Interfaces
<p align="center">
  <img src="documents/init_interfaces.png" alt="Interfaces of program"/>
</p>

If you want to use the program, you must mirror you game screen to the screen of your computer.
When the program start (by exercuting `main.py`), you will see 3 buttons namely `Set panel`, `Read template`, and `Match template`.

- `Set panel`: You must set the panel to the area where all pattern are. Click on the button so the button go blue (indicate that now you can set the panel). Then, move your mouse cursor to the top right corner of the most top right cell on the panel and press `t` on your keyboard. The bottom right corner is set using key `b`, settting procedure is the same. Don't forget that the program must be focused while you press the key or the panel is not set.
- `Read template`: After the panel is set, hit this button. It will take a while (up to 10 seconds) for reading and extracting all distinct pattern on the panel. The default number of cell on the panel is 14x8 which is the panel size of IOS version. It should be 14x7 for Android version. This size is set via the attribute `self.__cell_count` in `game_panel` module.
- `Match template`: When an aforemention procedures is done, the final step is perform matching. The matching is started when this button is hit. The matching process are perform automatically and endlessly until you close the program.

# Working Methods
The necessary working methods can be descripted briefly in 3 steps: finding all distinct pattern, finding matching pattern, and visualizing matched pattern.
## Finding all distinct pattern
After the panel is set and the read template is hit, the program start this procedure. The cell is extracted cell by cell, compared to previous extracted cells and added to the templates if it's not the same. The templates is the record of all distinct pattern found on the panel. The extraction method is `pyautogui.screenshot()` which return the image object. And the comparing method is `pyautogui.locate()` which likely is the pixel by pixel operation.
## Finding matching pattern
This procedure consists of 2 sub procedures: finding adjacents and finding the path. The program will match all the patterns found on screen, label it with different number, and store it as a matrix. The finding is first to look for adjacent cells in four vicinities by matching the label number. If no adjacents found, the program will find the path which connect the distant cells. This step is simple implementation of traditional AI which is just a tree breadth first searching. The path is the collection of sequential connected cells. It is generated on the empty space (label `0`) and increase the lenght by one on each iteration until it connect two same label or be terminated. The path will be terminated if the line using in the path is more than 3 lines, as it's the rule of the game.
## Visualizing matched pattern
The matched pattern is visualized using the simple solid color square. The detected pattern is colored as white, the matched cell is colored as red, and if it's the path, color it with yellow. The actual detected pattern image is shown below the panel.

When the matched adjacents is found:
<p align="center">
  <img src="documents/match_adjacents.png" alt="Visualizaion of matched adjacents"/>
</p>

When the matched path is found:
<p align="center">
  <img src="documents/match_path.png" alt="Visualizaion of matched via path"/>
</p>


The finding matching and visualizing procedures take time about 1.4-1.5 seconds each round.

# Notes
Since this program using a lot of image processing and processing so much pixels, the run time is very long (The first version take time about almost 5 seconds each round). There is some optimization that speed up the program.

- Using comparing method with `grayscale=True` specification. Reducing color channel to compare, the run time is reduced roughly 40%.
- Using screen capture and then perform `pyautogui.locate()` instead of using `pyautogui.locateOnScreen()`. Reducing the run time by 20%.
- Adapting the idea of `image pyramid` which is the idea of reducing size of image. In the step of finding all distinct pattern, the new extracted pattern has 1 of 3 size of the existing templates (1 of 9 in pixels number). And if it's not the same as any existing templates, the pattern is then captured again in a full size and be stored with the half size of it' appearance on screen. The captured screen using in finding matching procedure also be resized down to half. Reducing size of image, the run time is reduced roughly 20%.
- Store the distinct templates in the memory using `dict` type variable instead of reading the image from the file every time it's needed. Reducing accessing time, the result is ambiguous as it can speed up only 1%.
- 99% of the run time is used in the comparing image procedure, so make the program perform the comparing only when it's needed is the idea. Just like `onchange` in web application, the finding matching procedure is performed only when the game panel is changed.