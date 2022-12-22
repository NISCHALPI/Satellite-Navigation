#!/usr/bin/env python 


import click
from manim  import *
from parsers.navigation import NAVIGATION
from georinex import rinexnav
import datetime 




def prompt( selection : iter, promptStr = "Select one option" , retVal : bool = True  , addAll : bool = False) -> any: 
    """RetVal = True  = Index
        RetVal = False = Value"""

    # prompt dict
    promptDict =  dict(zip( [ str(i) for i in range(1, len(selection) +1)], selection))

    # Add all options
    if addAll:
        promptDict[ str(len(selection) + 1) ] = "All"


    while True:
        for keys in promptDict.keys():
            click.echo( f"{keys} : {promptDict.get(keys)}")
        

        choice  = click.prompt(promptStr, type = str)
        
        if choice in promptDict.keys():
            if retVal:
                return int(choice)
            else:
                return promptDict[choice]

        else:
            click.echo("Invalid option! Select a valid one!\n")




@click.command(no_args_is_help=True)
@click.option("-n", "--nav", "path_to_nav" , required = True ,  type = click.Path(exists=True,  resolve_path=True, readable= True),help ="Path to RINEX navigation file" )
def main(path_to_nav: str = None, ) -> None :
    
    # Read gps files 
    nav = rinexnav(path_to_nav, use="G")

    
    
    # Prompt for a observational epoch
    choice = prompt([obj.values.__str__() for obj in nav.time], promptStr= "Select a Observational Epoch", retVal= True, addAll= False)

    # User Prompted Epoch
    epoch = nav.time[choice -1 ]
    
   

    
    pass




if __name__ == "__main__":
    main()



