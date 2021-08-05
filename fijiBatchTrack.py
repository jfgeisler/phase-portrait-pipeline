#@ string inDir 
#@ string outDir
#@ double radius
#@ double threshold
#@ int frameGap
#@ double linkingMax
#@ double closingMax

# This Python/ImageJ2 script shows how to use TrackMate for multi-channel
# analysis. It is derived from a Groovy script by Jan Eglinger, and uses
# the ImageJ2 scripting framework to offer a basic UI / LCI interface 
# for the user.
#
# You absolutely need the `TrackMate_extras-x.y.z.jar` to be in Fiji plugins
# or jars folder for this to work. Check here to download it: 
# https://imagej.net/TrackMate#Downloadable_jars
#inpath="/Users/jangeisler/Documents/Grill/Pipeline/Jython/Composite.tif"
#outpath = "/Users/jangeisler/Documents/Grill/Pipeline/Jython/resultsbyline.txt"


from fiji.plugin.trackmate import Logger
import fiji.plugin.trackmate.Spot as Spot
import fiji.plugin.trackmate.Model as Model
import fiji.plugin.trackmate.Settings as Settings
import fiji.plugin.trackmate.TrackMate as TrackMate
 
import fiji.plugin.trackmate.detection.LogDetectorFactory as LogDetectorFactory
 
import fiji.plugin.trackmate.tracking.LAPUtils as LAPUtils
import fiji.plugin.trackmate.tracking.sparselap.SparseLAPTrackerFactory as SparseLAPTrackerFactory

 
import ij. IJ as IJ
import java.io.File as File
import java.util.ArrayList as ArrayList

##### Python modules
import os
print("Analysing .tifs in "+inDir)
import os
ext=".tif"
for root, directories, filenames in os.walk(inDir):
	for filename in filenames:
		print(filename)
  	# Check for file extension
  		if not filename.endswith(ext):
  			continue
  		imgPath = inDir+"/"+filename	
  		print( imgPath )
 		imp=IJ.openImage(imgPath)	
		# Swap Z and T dimensions if T=1
		dims = imp.getDimensions()# default order: XYCZT
		IJ.log(str([dims[2],dims[4],dims[3]]))
		#IJ.log(str(dims[int(2),int(4),int(3)]))
		
		if (dims[4] == 1):
			imp.setDimensions( dims[2],dims[4],dims[3] )

		# Setup settings for TrackMate
		settings = Settings()
		settings.setFrom( imp )
		settings.dt = 0.05
		from fiji.plugin.trackmate.providers import SpotAnalyzerProvider
		#from fiji.plugin.trackmate.providers import EdgeAnalyzerProvider
		#from fiji.plugin.trackmate.providers import TrackAnalyzerProvider
		
		spotAnalyzerProvider = SpotAnalyzerProvider()
		for key in spotAnalyzerProvider.getKeys():
		    #print( key )
		    settings.addSpotAnalyzerFactory( spotAnalyzerProvider.getFactory( key ) )
		     
		# Spot analyzer: we want the multi-C intensity analyzer.
		#settings.addSpotAnalyzerFactory( SpotMultiChannelIntensityAnalyzerFactory() )
		 
		# Spot detector.
		settings.detectorFactory = LogDetectorFactory()
		settings.detectorSettings = settings.detectorFactory.getDefaultSettings()
		settings.detectorSettings['RADIUS'] = radius
		settings.detectorSettings['THRESHOLD'] = threshold
		 
		# Spot tracker.
		settings.trackerFactory = SparseLAPTrackerFactory()
		settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap()
		settings.trackerSettings['MAX_FRAME_GAP']  = frameGap
		settings.trackerSettings['LINKING_MAX_DISTANCE']  = linkingMax
		settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE']  = closingMax
		 
		# Run TrackMate and store data into Model.
		model = Model()
		#model.setLogger( Logger.IJ_LOGGER )
		trackmate = TrackMate(model, settings)
		#trackmate.getModel().getLogger().log( settings.toStringFeatureAnalyzersInfo() )
		#trackmate.computeSpotFeatures( True )
		#results = ResultsTable()
		
		if not trackmate.checkInput() or not trackmate.process():
		    #print('Could not execute TrackMate: ' + str( trackmate.getErrorMessage() ) )
		    IJ.log('Could not execute TrackMate: ' + str( trackmate.getErrorMessage() ) )
		else:
		    #print('TrackMate completed successfully.' )
		    #print( 'Found %d spots in %d tracks.' % ( model.getSpots().getNSpots( True ) , model.getTrackModel().nTracks( True ) ) )
		    IJ.log('TrackMate completed successfully.' )
		    IJ.log( 'Found %d spots in %d tracks.' % ( model.getSpots().getNSpots( True ) , model.getTrackModel().nTracks( True ) ) )
		 
		    # Print results in the console.
		    headerStr = '%10s %10s %10s %10s %10s %10s %10.1s' % ( 'Spot_ID', 'Track_ID', 'Frame', 'X', 'Y', 'Z','Total_Intensity')
		    rowStr = '%10d %10d %10d %10.1f %10.1f %10.1f %10.1f'
		     
		    IJ.log('\n')
		    IJ.log( headerStr)
		    tm = model.getTrackModel()
		    #tm.results    results.saveAs(rtsavelocation)
		    #log.info('Save Results to : ' + rtsavelocation)
		    with open(outDir+"/"+filename[:-8]+"RES.txt", "w") as myfile:
					myfile.write("")
		    trackIDs = tm.trackIDs( True )
		    counter=max(trackIDs)
		    for trackID in trackIDs:
		        spots = tm.trackSpots( trackID )
		        # Let's sort them by frame.
		        ls = ArrayList( spots );
		        #ls.sort( Spot.frameComparator )
				
		        for spot in ls:
		        	#if spot.getFeature('TOTAL_INTENSITY') !=0:
		        	#print(float(spot.getFeature('TOTAL_INTENSITY')))
		        	values= [  spot.ID(), trackID, spot.getFeature('FRAME'), \
		            	spot.getFeature('POSITION_X'), spot.getFeature('POSITION_Y'), spot.getFeature('RADIUS'), spot.getFeature('SNR'), spot.getFeature('ESTIMATED_DIAMETER')]#,spot.getFeature('SPOT_ID')
		            	#print(str(values)+"\n")
				#trackmate.getLogger().log(str(  spot.ID(), trackID, spot.getFeature('FRAME'), \
		        #    	spot.getFeature('POSITION_X'), spot.getFeature('POSITION_Y'), spot.getFeature('POSITION_Z'),spot.getFeature('AREA'), spot.getFeature('TOTAL_INTENSITY')))
				#results[trackID]=str(values)
				with open(outDir+"/"+filename[:-8]+"RES.txt", "a") as myfile:
					myfile.write(str(values)[1:-1]+"\n")
		print("output format: spotID, trackID, frame, x, y, radius, SNR, est.Diameter ")
