import numpy as np
import cv2

# Βρείτε τα pixel που είναι πάνω από το κατώφλι
# Το κατώφλι για RGB > 160 είναι μια καλή εκτίμηση για να βρούμε τα pixels που θέλουμε, δηλαδή "φωτεινό" λευκό
def ground_thresh(img, rgb_thresh=(160, 160, 160)):
    
    ###############################################################################
    #########################ΣΥΜΠΛΗΡΩΣΤΕ ΕΔΩ#######################################
    
    # Δημιουργία ενός πίνακα με μηδενικά για να αποθηκεύσουμε την εικόνα που θα προκύψει, αλλά με ένα μόνο channel
    # αφού θα έχουμε τιμές 0 ή 1 (ασπρόμαυρο)
    ground_select = np.zeros_like(img[:,:,0])
    # Απαιτείται κάθε εικονοστοιχείο να είναι πάνω από τις τρεις τιμές κατωφλίου σε RGB
    # Το above_thresh θα περιέχει τώρα έναν δυαδικό πίνακα με "True"
    # όπου ικανοποιήθηκε το όριο
    
    above_thresh = 0 
    
    ground_select[above_thresh] = 1
    
    ###############################################################################
    ###############################################################################
    
    return ground_select

def rock_thresh(img, rgb_thresh=(0, 0, 0)):
    
    ###############################################################################
    #########################ΣΥΜΠΛΗΡΩΣΤΕ ΕΔΩ#######################################
    
    rock_select = np.zeros_like(img[:,:,0])
    
    above_thresh = 0
    
    rock_select[above_thresh] = 1
    
    ###############################################################################
    ###############################################################################
    
    return rock_select

def obstacle_thresh(img, rgb_thresh=(0, 0, 0)):
    
    ###############################################################################
    #########################ΣΥΜΠΛΗΡΩΣΤΕ ΕΔΩ#######################################
    
    obstacle_select = np.zeros_like(img[:,:,0])
    
    above_thresh = 0
    
    obstacle_select[above_thresh] = 1
    
    ###############################################################################
    ###############################################################################
    
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
    yaw_rad = 0
    
    # Εφαρμόστε περιστροφή
    xpix_rotated =0
                            
    ypix_rotated = 0
    
    ###############################################################################
    ###############################################################################
      
    return xpix_rotated, ypix_rotated

#Εφαρμογή μετaτόπισης και κλιμάκωσης
def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale): 
    
    ###############################################################################
    #########################ΣΥΜΠΛΗΡΩΣΤΕ ΕΔΩ#######################################
    
    # Εφαρμόστε κλιμάκωση και μετατόπιση
    xpix_translated = 0
    ypix_translated = 0
    
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

    # 2) Εφαρμόστε μετασχηματισμό προοπτικής
    dst_size = 5
    bottom_offset = 6

    source = np.float32([[],[],[],[]])
    destination = np.float32([[],[],[],[]])

    # 3) Εφαρμόστε κατώφλι χρώματος για εμπόδια, πλοηγήσιμο έδαφος και πετρώματα

    # 4) Ενημερώστε την εικόνα που εμφανίζεται κάτω αριστερά (Rover.vision_image)
    # την εικόνα που είναι σε bird's eye view
        # Παράδειγμα: Rover.vision_image[:,:,0] = obstacle color-thresholded binary image (στο κόκκινο κανάλι τα εμπόδια)
        #             Rover.vision_image[:,:,1] = rock_sample color-thresholded binary image (στο πράσινο κανάλι τα πετρώματα)
        #             Rover.vision_image[:,:,2] = navigable terrain color-thresholded binary image (στο μπλε κανάλι το λοηγίσιμο έδαφος)


    # 5) Μετατροπή των συντεταγμένων εικόνας σε rover-centric (ρομπο-κεντρικές)

    # 6) Μετατροπή των rover-centric συντεταγμένων σε συντεταγμένες περιβάλλλοντος (global coordinates)

    # 7) Ενημέρωση του χάρτη pixel pixel (κάτω δεξιά)
        # Παράδειγμα: Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1 (τα pixel που είναι εμπόδια, κόκκινο κανάλι)
        #             Rover.worldmap[rock_y_world, rock_x_world, 1] += 1 (τα pixel που είναι πετρώματα, πράσινο κανάλι)
        #             Rover.worldmap[navigable_y_world, navigable_x_world, 2] += 1 (τα pixel που είναι πλοηγήσιμο έδαφος, μπλε κανάλι)


    # 8) Μετατροπή των rover-centric pixels σε πολικές συντεταγμένες
    # και έπειτα ενημέρωση του rover
        # Παράδειγμα ενημέρωσης: Rover.nav_dists = rover_centric_pixel_distances
        #                        Rover.nav_angles = rover_centric_angles

      
    
    ###############################################################################
    ###############################################################################


    return Rover
