# PREFIXES:
#   G   =   Global value
#   M   =   Map Value
#   P   =   Physics
#	U	=	UI/Graphics
#	F	=	Fighter Value
#   C   =   Controls

# Game Graphics
GU_DISPWIDTH = 1280
GU_DISPHEIGHT = 720
GU_GRID = 32
UU_DEBUGWIDTH = 1280
UU_DEBUGHEIGHT = 128
MU_DISPWIDTH = 1280
MU_DISPHEIGHT = 720
MU_X = 0
MU_Y = 0
UU_DEBUGX = 0
UU_DEBUGY = MU_DISPHEIGHT - UU_DEBUGHEIGHT
DEF_WIDGET_W: int = 128 #128
DEF_WIDGET_H: int = 128 #128

# Player physics
GP_xACCEL = 2  # Horizontal Acceleration
GP_yACCEL = 2  # Vertical Acceleration
GP_xDECEL = 1  # Horizontal Deceleration
GP_yDECEL = 1  # Vertical Deceleration

FP_BUMPSPEED = 5  # Speed required to bounce an object

# Fighter Animation
FU_FRAMESPEED = 30  # Animation frame speed
BPM = 15 # beatlocked frame speed
