# holo-schedule-CLI
Hololive schedule scraping tool

# Requirement
- Python 3.x
- requests

- Japanese font (In order to display hololive member's name)

# Usage
By executing main\.py You can get information like these:
- The time hololive member's streaming will start in JST
- Who is streaming
- The streaming URL

# Notes
This program is a scraping tool. [The source page](https://schedule.hololive.tv/simple) 
says the schedule is updated every 15 minutes so this program might not deal with the latest changes. 
If you never want to miss any stream, it is recommended to follow the hololive member's Twitter account or subscribe their Youtube channel.  

Now this program is available to use options. For example, you can change hololive member's name English. Plese check text/help or execute with --help option.  

A moive will be on schedule after it is posted. The displayed time is its published time except premire moive. 

This program does not show bilibili streams. Check the official schedule if you want to check them.

# Screenshot
![sc](https://user-images.githubusercontent.com/42367122/79976625-e26f4700-84d7-11ea-9e36-e5262e317fbd.png)  
