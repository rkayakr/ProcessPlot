# subroutine to read header and return node and beacon info
# basically code moved from main program to call once for each file to allow label of node and beacon
# Bob Benedict 8/12/2021
import sys
def readheader(Header):
    #print('in readheader')
    NewHdr = 'Unknown'
    if (Header[0] == "#"):
        print('New Header String Detected')
    # Have new header format - pull the data fields out
    NewHdr = 'New'
    UTCDTZ = Header[1]
    #print('\nUTCDTZ Original Header from file read = ' + UTCDTZ)
    UTC_DT = UTCDTZ[:10] # Strip off time and ONLY keep UTC Date
    #print('\nExtracted UTC_DT only = ' + UTC_DT)
    UTCDTZ=UTCDTZ.replace(':','') # remove the semicolons
    print('\ncorrected UTCDTZ =', UTCDTZ)
    #        node= Header[0] = Header[2]
    nodenum= Header[2]
    #        print('Node =', node)
    GridSqr = Header[3]
    #        print('GridSqr =', GridSqr)
    Lat = Header[4]
    #print('Lat =', Lat)
    Long = Header[5]
    #print('Long =', Long)
    Elev = Header[6]
    #        print('Elev =', Elev)
    citystate = Header[7]
    #        print('City State =', citystate)
    RadioID = Header[8]
    #        print('Radio ID =', RadioID)
    beacon = Header[9]
    #        print('Beacon =', beacon)


    if (NewHdr == 'Unknown'):
        print('Unknown File header Structure - Aborting!')
        sys.exit(0)
    #2.5MHz WWv
    if (beacon == 'WWV2p5'):
        print('Plot for Decoded 2.5MHz WWV Beacon\n')
        beaconlabel = 'WWV 2.5 MHz'
        beaconf=2500000.0

    #5MHz WWV
    elif (beacon == 'WWV5'):
        print('Plot for Decoded 5MHz WWV Beacon\n')
        beaconlabel = 'WWV 5 MHz'
        beaconf=5000000.0
        
    #10MHz WWV
    elif (beacon == 'WWV10'):
        print('Plot for Decoded 10MHz WWV Beacon\n')
        beaconlabel = 'WWV 10 MHz'
        beaconf=10000000.0
        
    #15MHz WWV
    elif (beacon == 'WWV15'):
        print('Plot for Decoded 15MHz WWV Beacon\n')
        beaconlabel = 'WWV 15 MHz'
        beaconf=15000000.0
        
    #20MHz WWV
    if (beacon == 'WWV20'):
        print('Plot for Decoded 20MHz WWV Beacon\n')
        beaconlabel = 'WWV 20 MHz'
        beaconf=20000000.0    

    #25MHz WWV
    elif (beacon == 'WWV25'):
        print('Plot for Decoded 25MHz WWV Beacon\n')
        beaconlabel = 'WWV 25 MHz'
        beaconf=25000000.0    

    #3.33MHz CHU
    if (beacon == 'CHU3'):
        print('Plot for Decoded 3.33MHz CHU Beacon\n')
        beaconlabel = 'CHU 3.330 MHz'
        beaconf=3330000.0    

    #7.85MHz CHU
    elif (beacon == 'CHU7'):
        print('Plot for Decoded 7.85MHz CHU Beacon\n')
        beaconlabel = 'CHU 7.850'
        beaconf=7850000.0
        
    #14.67MHz CHU
    elif (beacon == 'CHU14'):
        print('Plot for Decoded 14.67MHz CHU Beacon\n')
        beaconlabel = 'CHU 14.670 MHz'
        beaconf=14670000.0
        
    elif (beacon == 'Unknown'):
        print('Plot for Decoded Unknown Beacon\n')
        print('Unknown Beacon - Aborting!')
        sys.exit(0)
    return nodenum, beaconlabel, beaconf, Lat, Long
