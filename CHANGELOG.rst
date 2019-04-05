Changelog
=========

v1.7.0 (April 4, 2019)
----------------------
- Added custom sampler feature.  Interface requires creation of a class, but allows for inclusion of things like Gibbs samplers.  User can explicitly pass in features to the sum-of-squares function.
- Added check routines for reading in parallel MCMC results to ensure only directories with name 'chain_' are queried.
- All files were updated to comply with formatting standards using *flake8*.
- Added coverage report check to ensure minimal testing requirements are met.
- Added original covariance matrix to results structure for reference.

v1.6.0 (August 31, 2018)
----------------------
- Added optimal handling of prior function used numpy array multiplication.
- Fixed bug with saving results to json file - output directory now automatically made.
- Updated PI plotting to allow any valid matplotlib input.
- Added Gelman-Rubin diagnostics to ChainStatistics module, with display feature.
- Added numpy error settings option to MCMC initialization.
- Setup no adaptation feature.  Can sample parameters without adapting them.
- Added restart routine to ParallelMCMC.  Can restart from json files.
- Added parallel chain organization routines to the chain subpackage.

v1.5.0 (July 27, 2018)
----------------------
- Final release of 1.5.0.
- First release with complete test coverage.
- Updated analysis options and diagnostics.
- Improved workflow on remote OS.
- Added link to Zenodo DOI.

v1.4.0 (July 11, 2018)
----------------------
- Added extensive unit tests.

v1.3.1 (April 20, 2018)
-----------------------
- Fixed sample feature (allows for fixed variables).
- automatic naming (and expansion) for plot labels.
- added covariance matrix to log file output.

v1.3.0 (April 3, 2018)
----------------------
- All features updated to work with Python 3.6
- This was the last version developed using Python 2.7.  It may still work on Python 2.7, but it will not be included as a part of testing.

v1.2.0 (April 3, 2018)
----------------------
- Added ellipse contour routine for pairwise plots.
- Added progress bar to prediction interval generation (as it can be time consuming).
- Added log file saving so you can periodically dump the latest set of samples to file.

v1.1.1 (February 26, 2018)
--------------------------
- Fixed bug associated with plotting credible intervals without prediction intervals.

v1.1.0 (February 19, 2018)
--------------------------
- Added feature for generating and plotting prediction/credible intervals.

v1.0.0 (February 15, 2018)
--------------------------
- First official release.
- Incorporated class structures into entire architecture.