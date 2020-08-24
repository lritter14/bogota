
# SOURCE: RAFAEL PRERIA, python_script
from org.opentripplanner.scripting.api import OtpsEntryPoint

# Instantiate an OtpsEntryPoint
# NOTE WOULD NEED TO CHANGE THIS IN ORDER TO 
otp = OtpsEntryPoint.fromArgs(['--graphs', '/Users/BrianHill/otp/graphs',
                               '--router', 'bogota_no_gondola'])

# Start timing the code
import time
start_time = time.time()

# Get the default router
router = otp.getRouter('bogota_no_gondola')


# Create a default request for a given departure time
req = otp.createRequest()
req.setDateTime(2019, 9, 15, 10, 00, 00)  # set departure time (April 4, 2019)

#req.setWaitReluctance(1) # Set walk reluctance to be 1 instead of the default 2, make walking time equally bad to other times
#req.setMaxTimeSec(7200)                   # set a limit to maximum travel time (seconds)
req.setModes('WALK,BUS,RAIL,TRANSIT')             # define transport mode
#req.setClampInitialWait(0)                # clamp the initial wait time to zero
# req.maxWalkDistance = 3000                 # set the maximum distance (in meters) the user is willing to walk
# req.walkSpeed = walkSpeed                 # set average walking speed ( meters ?)
# req.bikeSpeed = bikeSpeed                 # set average cycling speed (miles per hour ?)
# ?ERROR req.setSearchRadiusM(500)                 # set max snapping distance to connect trip origin to street network

# for more routing options, check: http://dev.opentripplanner.org/javadoc/0.19.0/org/opentripplanner/scripting/api/OtpsRoutingRequest.html


# Read Points of Destination - The file points.csv contains the columns GEOID, X and Y.
points = otp.loadCSVPopulation('bogota_otp_setup_example_run/example_points_origins.csv', 'Y', 'X')
dests = otp.loadCSVPopulation('bogota_otp_setup_example_run/example_points_destinations.csv', 'Y', 'X')


# Create a CSV output
matrixCsv = otp.createCSVOutput()
matrixCsv.setHeader([ 'origin', 'destination', 'walk_distance', 'travel_time', 'boardings' ])

# Start Loop
for origin in points:
  print "Processing origin: ", origin
  req.setOrigin(origin)
  spt = router.plan(req)
  if spt is None: continue

  # Evaluate the SPT for all points
  result = spt.eval(dests)

  # Add a new row of result in the CSV output
  for r in result:
    matrixCsv.addRow([ origin.getStringData('GEOID'), r.getIndividual().getStringData('GEOID'), r.getWalkDistance() , r.getTime(),  r.getBoardings() ])

# Save the result
matrixCsv.save('bogota_otp_setup_example_run/example_travel_time_no_gondola_python_script.csv')

# Stop timing the code
print("Elapsed time was %g seconds" % (time.time() - start_time))
