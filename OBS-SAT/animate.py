#!/usr/bin/env python 


import click
from manim  import *
from manim.opengl import *
from parsers.navigation import NAVIGATION
from georinex import rinexnav
from threaded.threads.Fthread import Fthread
import numpy as np

##########################################################DATA COLLECTION#################################


# prompt user 
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


# Get Nav data for all satellite 
def getData(path_to_nav: str , isAuto : bool = False, argsSV: tuple = ()) -> dict:

     # Read gps files 
    fullNav = rinexnav(path_to_nav, use="G") 
    
    # Length of time
    lenTime = len(fullNav.time)
    

    while True:    
        if not isAuto:
            # Prompt for a observational epoch
            choice = prompt([obj.values.__str__() for obj in fullNav.time], promptStr= "Select a Observational Epoch", retVal= True, addAll= False)
        else :
            choice = lenTime
            lenTime -= 1
        
        
        # User Prompted Epoch
        epoch = fullNav.time[choice -1 ]
        
        # Selected Time 
        epoch = epoch.values
        # Available SV data 
        nav = fullNav.sel(time=epoch)

        
        # List of all available SV as str 
        availableSV = [sv.item(0) for sv in nav.sv]
        

        # Navigation data 
        navData = [NAVIGATION(nav, sat, epoch, True) for sat in availableSV]

    
        # Check Data integrety
        if np.isnan(navData[0]['eccentricity']):
            print(f"No GPS data for {epoch.__str__()} epoch!\n")
            continue

        break   
    
    # Dict of Nav Data for all available sv
    navData = dict(zip(availableSV , navData))

    # Filtered SV
    for keys in availableSV:
        if np.isnan(navData[keys]["eccentricity"]):
            navData.pop(keys)

    
    # filter args SV
    if len(argsSV) != 0 :
        returndataSV = {}

        for passedSV in argsSV:
            if passedSV not in navData.keys():
                raise Exception(f"Cannot find full data for {passedSV} in {epoch.__str__()} epoch! \n Only following SV are avaialable {list(navData.keys())}")
            else:
                returndataSV[passedSV] = navData[passedSV]
        
        return returndataSV

    return navData
        

##########################################################################################################

##################################################### ANIMATION HELPER FUNC #############################
# Constants
R = 6.3781 * 10 ** 6  # Radius of Earth

scaling_factor = 1 / (12 * 10 ** 6)  # inverse of unit distance in the axis in meters

inverse_scaling = 1 / scaling_factor  # inverse of scaling factor

R = R * scaling_factor


# gets elliptical parameters - major and minor axis length with the scaling factor
def elliptial_parameter(a: float, e: float) -> dict:
    return {'width': a * 2 * scaling_factor, 'height': 2 * np.sqrt((1 - e ** 2) * a ** 2) * scaling_factor}





# gets the distance to focus of an ellipse from center
def get_focus(mob: Ellipse) -> float:
    a = mob.get_width() / 2
    b = mob.get_height() / 2

    return np.sqrt(a ** 2 - b ** 2)




# Recursive angular correction-> condenses any angle between 0 to 2pi
def angular_correction(ang) -> float:
    if 0 <= ang <= TAU:
        return ang
    elif ang > TAU:
        return angular_correction(ang - TAU)
    else:
        return angular_correction(ang + TAU)
        # SV animation snapshot




# angle between two vector
def angle(vct1: np.array, vct2: np.array) -> float:
    dot_product = np.dot(vct1, vct2)

    norm1 = np.linalg.norm(vct1)

    norm2 = np.linalg.norm(vct2)

    cos_correctiom = np.arccos(dot_product / (norm1 * norm2))
    return (180 / np.pi) * cos_correctiom


# get dot and orbital path 
def getOrbitalMobjects( svName :str = None, svData: dict = None) -> tuple:

    # get elliptical parameter
    a = elliptial_parameter(svData['semimajor'], svData['eccentricity'])

    # Orbital path 
    orbital_path = Ellipse(**a)

    # Shift orbital path 
    orbital_path.shift(RIGHT * get_focus(orbital_path))

    # Orbit attached to vectors 
    path_group = VGroup(orbital_path, Vector(OUT))

    # Angle of inclination about y-axis
    path_group.rotate(angle=angular_correction(svData['inclination']), axis=np.array([1, 0, 0]), about_point=ORIGIN)  
    # RANN rotation-- ascending node rotations
    path_group.rotate(angle=angular_correction(svData['acending_node']), axis=np.array([0, 0, 1]),about_point=ORIGIN)
    # Angle of Perigee rotation
    path_group.rotate(angle=angular_correction(svData['periapsis']), axis=path_group[1].get_end(), about_point= ORIGIN)

    # Random color 
    randcol = random_color()

    # Satellite 
    sat = Dot3D(radius=0.06, point=scaling_factor * np.array(svData['position']), color=randcol)

    satLable = Text(svName, color =randcol, slant = ITALIC , weight = BOLD, font_size = 20).next_to(sat , direction= UP +RIGHT , buff= 0.1)

    satLable.add_updater(lambda mob : mob.next_to(sat , direction= UP +RIGHT , buff= 0.1))

    return sat , satLable, orbital_path

###################################################HELPER FUNC###########################################

@click.command(no_args_is_help=True)
@click.option("-n", "--nav", "path_to_nav" , required = True ,  type = click.Path(exists=True,  resolve_path=True, readable= True),help ="Path to RINEX navigation file" )
@click.option("-a", "--auto", "auto", is_flag=True, help = "Choose epoch automatically for Animation")
@click.option("-s", "--sv", "sv" ,  type = str, multiple = True ,  help = "Select specific SV's"  )
def main(path_to_nav: str = None, auto: bool  = False, sv : tuple = ()) -> None :
    
    
    # Get the nav data 
    navData = getData(path_to_nav, auto, sv)

   
    

    # Animation class
    class animateSV(ThreeDScene):
        def construct(self):     
            # SECTION: CAMERA SETTINGS 
            
            # Beginning Camara Orientation and Rotation
            self.camera.set_euler_angles(phi=PI / 2.4, theta=PI / 4)
            # Ambient Camera Rotation
            self.add(self.camera)
            self.add(self.camera.light_source)
            self.camera.add_updater(lambda mob, dt: mob.increment_theta(dt * 0.025))
            self.update_self(0.001)
            # END OF CAMERA SETTING 


            # SECTION: THREE D AXIS SETTINGS
            ax = ThreeDAxes(x_range=[-30, 30, 1], y_range=[-30, 30, 1], z_range=[-30, 30, 1], x_length=30, y_length=30,
                        z_length=30, tips=False,
                        stroke_width=1, axis_config={'include_ticks': False, 'stroke_width': 3}).set(
                        color=BLUE_C).set_opacity(0.67)
            # END OF THREED AXIS SETTING 

            # SECTION: EARTH MOBJECT 
            #earth = Sphere(radius=R, resolution=(50, 50), color=BLUE,)
            earth = OpenGLSurface(lambda u, v: (np.cos(u) *np.sin(v) , np.sin(u) * np.sin(v),np.cos(v)),u_range=(0, 2 * np.pi),v_range=(0, np.pi))
            earth = OpenGLTexturedSurface(earth, 'images/day.jpg', 'images/night.jpg')
            # END OF EARTH SETTINGS 

            self.play(Create(earth))

            # SECTION : MOBJECT CREATION 
            tupMobject = []
            for keys in navData.keys():
                tupMobject.append(getOrbitalMobjects(keys , navData[keys]))

            print(tupMobject)
    
    
    with tempconfig({"renderer": "opengl" , "preview" : True, "fps" : 75}) :
        scene = animateSV()
        scene.render()
    
    pass




if __name__ == "__main__":
    main()



