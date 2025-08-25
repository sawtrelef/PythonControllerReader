Hey everybody!

This is a fun little project I put together just to kind of have something to do.

In its current state it is two separate programs that operate on all the same things, this will be changed in the future.

GamepadReader as it is will read the layout saved to layout.txt, it will not read or load from any other file name as it currently is.

BuildALayout will *ALWAYS* overwrite layout.txt when the SAVE button is clicked.

BuildaLayout will also *ALWAYS* load from layout.txt.

To save multiple layouts, it is recommended to keep dummy files in another folder with different names.  To preserve the dummy layout, simply make a copy of it and rename it to layout.txt and move the new layout.txt to the main folder overwriting the old one.

BuildALayout currently has no option to extract axis or buttons from sticks, so do be cautions when selecting which ones to add where, because they will be lost to the void otherwise.

To add addional stick and button layouts you must follow a certain file name protocal, I made it fairly simple.
Requirements:
  Buttons - Must have 2 files in the buttons folder, one with the word "unpressed", and the other with the word "pressed".  "pressed" and "unpressed" **MUST** be in the same location in a filename
      Example: starunpressed.png
               starpressed.png

  Sticks - Same deal sticks, but in the sticks folder
      Example: spiralpressed.png
               spiralunpressed.png
  Customization for Axis bars will currently require replacing of the paddle.png and bar.png files in the axis folder.

If you wish to customize the options buttons, all of those currently live in the assets folder with names you'd expect them to be - why you'd do this I do not know.

OH, and to move things around simply select the button/axis/stick by clicking on it, and then clicking the selected button/axis/stick a second time will allow you to drag it around!
