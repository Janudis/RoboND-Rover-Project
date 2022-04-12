import numpy as np
import cv2


def ground_thresh(img, rgb_thresh=(160, 160, 160)):

    ground_select = np.zeros_like(img[:, :, 0])

    above_thresh = (img[:, :, 0] > rgb_thresh[0]) \
                & (img[:, :, 1] > rgb_thresh[1]) \
                & (img[:, :, 2] > rgb_thresh[2])

    ground_select[above_thresh] = 1

    ###############################################################################
    ###############################################################################

    return ground_select


def rock_thresh(img):

    ###############################################################################
    #########################ΣΥΜΠΛΗΡΩΣΤΕ ΕΔΩ#######################################
    hsv_img=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    rock_lower = np.array([0, 200, 100])     # HSV lower limit for golden rocks
    rock_upper = np.array([179, 255, 255])   # HSV upper limit for golden rocks

    rock_select = cv2.inRange(hsv_img, rock_lower, rock_upper)

    return rock_select*255


def obstacle_thresh(img, rgb_thresh=(160, 160, 160)):

    ###############################################################################
    #########################ΣΥΜΠΛΗΡΩΣΤΕ ΕΔΩ#######################################

    obstacle_select = np.zeros_like(img[:, :, 0])

    above_thresh = (img[:, :, 0] < rgb_thresh[0]) \
                & (img[:, :, 1] < rgb_thresh[1]) \
                & (img[:, :, 2] < rgb_thresh[2])

    obstacle_select[above_thresh] = 1

    return obstacle_select


# Μετατροπή από τις συντεταγμένες της εικόνας σε συντεταγμένες rover
def rover_coords(binary_img):
    # Βρείτε τα μη μηδενικά pixels
    ypos, xpos = binary_img.nonzero()
    # Υπολογίστε τις θέσεις pixel με τη θέση του rover να βρίσκεται στο
    # κεντρικό κάτω μέρος της εικόνας.

    x_pixel = -(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[1]/2 ).astype(np.float)

    return x_pixel, y_pixel

# Μετατροπή σε πολικές συντεταγμένες


def to_polar_coords(x_pixel, y_pixel):
    dist = np.sqrt(x_pixel**2 + y_pixel**2)

    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

# Εφαρμογή περιστροφής


def rotate_pix(xpix, ypix, yaw):

    ###############################################################################
    #########################ΣΥΜΠΛΗΡΩΣΤΕ ΕΔΩ#######################################
    # Μετατροπή μοιρών σε ακτίνια
    yaw_rad = (yaw * np.pi) / 180

    # Εφαρμόστε περιστροφή
    xpix_rotated =(xpix * np.cos(yaw_rad)) - (ypix * np.sin(yaw_rad))

    ypix_rotated = (xpix * np.sin(yaw_rad)) + (ypix * np.cos(yaw_rad))

    ###############################################################################
    ###############################################################################

    return xpix_rotated, ypix_rotated



#Εφαρμογή μετaτόπισης και κλιμάκωσης



def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale):

    ###############################################################################
    #########################ΣΥΜΠΛΗΡΩΣΤΕ ΕΔΩ#######################################

    # Εφαρμόστε κλιμάκωση και μετατόπιση
    xpix_translated = (xpix_rot / scale) + xpos
    ypix_translated = (ypix_rot / scale) + ypos

    ###############################################################################
    ###############################################################################

    return xpix_translated, ypix_translated


# Ορίστε μια συνάρτηση για εφαρμογή περιστροφής και μετάτόπισης (και αποκοπής).
def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
    # Περιστροφή
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    # Μετατόπιση
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    # Αποκοπή των pixels που πέφτουν έξω από τον κόσμο
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)

    # επιστροφή των συντεταγμένων κόσμου
    return x_pix_world, y_pix_world

# Define a function to perform a perspective transform


def perspect_transform(img, src, dst):

    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image

    return warped


# Apply the above functions in succession and update the Rover state accordingly
def perception_step(Rover):

    # παράδειγμα χρήσης του databucket
    # print(data.xpos[data.count], data.ypos[data.count], data.yaw[data.count])

    ###############################################################################
    #########################ΣΥΜΠΛΗΡΩΣΤΕ ΕΔΩ#######################################

    # Εφαρμόστε τα βήματα της αντίληψης
    # Η εικόνα έρχεται στο Rover.img

    # 1) Ορίστε σημεία προορισμού και προέλευσης
    dst_size = 5
    bottom_offset = 6
    scale = 10
    rvr_xpos = Rover.pos[0]
    rvr_ypos = Rover.pos[1]
    rvr_yaw = Rover.yaw
    wrl_shp0 = Rover.worldmap.shape[0]

    source = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])
    #155,154, 165,154, 165,144  ,155, 144
    destination = np.float32([[Rover.img.shape[1] / 2 - dst_size, Rover.img.shape[0] - bottom_offset],
                              [Rover.img.shape[1] / 2 + dst_size, Rover.img.shape[0] - bottom_offset],
                              [Rover.img.shape[1] / 2 + dst_size, Rover.img.shape[0] - 2 * dst_size - bottom_offset],
                              [Rover.img.shape[1] / 2 - dst_size, Rover.img.shape[0] - 2 * dst_size - bottom_offset],
                              ])


    # 2) Εφαρμόστε μετασχηματισμό προοπτικής
    warped = perspect_transform(Rover.img, source, destination)
    rock_warped = perspect_transform(Rover.img, source, destination)



    # 3) Εφαρμόστε κατώφλι χρώματος για εμπόδια, πλοηγήσιμο έδαφος και πετρώματα
    ground = ground_thresh(warped)
    obstacle = obstacle_thresh(warped)
    rock = rock_thresh(rock_warped)

    # 4) Ενημερώστε την εικόνα που εμφανίζεται κάτω αριστερά (Rover.vision_image)
    # την εικόνα που είναι σε bird's eye view
    Rover.vision_image[:, :, 0] = obstacle*255 #obstacle color-thresholded binary image (στο κόκκινο κανάλι τα εμπόδια)
    Rover.vision_image[:, :, 1] = rock*255 #rock_sample color-thresholded binary image (στο πράσινο κανάλι τα πετρώματα)
    Rover.vision_image[:, :, 2] = ground*255 #navigable terrain color-thresholded binary image (στο μπλε κανάλι το λοηγίσιμο έδαφος)


    # 5) Μετατροπή των συντεταγμένων εικόνας σε rover-centric (ρομπο-κεντρικές)
    grdx_pix, grdy_pix = rover_coords(ground)  # convert navigable area thresholded to rover coords.
    obstx_pix, obsty_pix = rover_coords(obstacle)  # convert obstacle area thresholded to rover coords.
    rockx_pix, rocky_pix = rover_coords(rock)  # convert rock thresholded to rover coords.

    # 6) Μετατροπή των rover-centric συντεταγμένων σε συντεταγμένες περιβάλλλοντος (global coordinates)
    grdx_wld, grdy_wld = pix_to_world(grdx_pix, grdy_pix, rvr_xpos, rvr_ypos, rvr_yaw, wrl_shp0, scale)
    obstx_wld, obsty_wld = pix_to_world(obstx_pix, obsty_pix, rvr_xpos, rvr_ypos, rvr_yaw, wrl_shp0, scale)
    rockx_wld, rocky_wld = pix_to_world(rockx_pix, rocky_pix, rvr_xpos, rvr_ypos, rvr_yaw, wrl_shp0, scale)

    # 7)

    Rover.worldmap[obsty_wld, obstx_wld, 0] += 1
    Rover.worldmap[rocky_wld, rockx_wld, 1] += 1
    Rover.worldmap[grdy_wld, grdx_wld, 2] += 1

    # 8) Μετατροπή των rover-centric pixels σε πολικές συντεταγμένες
    # και έπειτα ενημέρωση του rover
    Rover.nav_dists, Rover.nav_angles = to_polar_coords(grdx_pix, grdy_pix)
    Rover.rock_dists, Rover.rock_angles = to_polar_coords(rockx_pix, rocky_pix)








    return Rover
