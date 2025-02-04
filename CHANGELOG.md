# Changelog

## Version 1.1.3 (Apr 26, 2024)

Changes:
*   Add built-in support for additional datasets ([#257](https://github.com/AI-SDC/AI-SDC/pull/257))
*   Remove references to final score in outputs ([#259](https://github.com/AI-SDC/AI-SDC/pull/259))
*   Update package dependencies: remove support for Python 3.8; add support for Python 3.11 ([#262](https://github.com/AI-SDC/AI-SDC/pull/262))
*   Fix code coverage reporting ([#265](https://github.com/AI-SDC/AI-SDC/pull/265))
*   Remove useless pylint suppression pragmas ([#269](https://github.com/AI-SDC/AI-SDC/pull/269))
*   Fix axis labels in report ROC curve plot ([#270](https://github.com/AI-SDC/AI-SDC/pull/270))

## Version 1.1.2 (Oct 30, 2023)

Changes:
*   Fix a bug related to the `rules.json` path when running from package ([#247](https://github.com/AI-SDC/AI-SDC/pull/247))
*   Update user stories ([#247](https://github.com/AI-SDC/AI-SDC/pull/247))

## Version 1.1.1 (Oct 19, 2023)

Changes:
*   Update notebook example paths ([#237](https://github.com/AI-SDC/AI-SDC/pull/237))
*   Fix AdaBoostClassifier structural attack ([#242](https://github.com/AI-SDC/AI-SDC/pull/242))
*   Move experiments module and configs to separate repository ([#229](https://github.com/AI-SDC/AI-SDC/pull/229))

## Version 1.1.0 (Oct 11, 2023)

Changes:
*    Add automatic formatting of docstrings ([#210](https://github.com/AI-SDC/AI-SDC/pull/210))
*    Update user stories ([#217](https://github.com/AI-SDC/AI-SDC/pull/217))
*    Add module to run experiments with attacks and gather data ([#224](https://github.com/AI-SDC/AI-SDC/pull/224))
*    Fix bug in report.py: error removing a file that does not exist ([#227](https://github.com/AI-SDC/AI-SDC/pull/227))
*    Add structural attack for traditional and other risk measures ([#232](https://github.com/AI-SDC/AI-SDC/pull/232))
*    Fix package installation for Python 3.8, 3.9, 3.10 ([#234](https://github.com/AI-SDC/AI-SDC/pull/234))

## Version 1.0.6 (Jul 21, 2023)

Changes:
*    Update package dependencies ([#187](https://github.com/AI-SDC/AI-SDC/pull/187))
*    Fix bug when `n_dummy_reps=0` in worst case attack ([#191](https://github.com/AI-SDC/AI-SDC/pull/191))
*    Add ability to save target model and data to `target.json` ([#171](https://github.com/AI-SDC/AI-SDC/pull/171), [#175](https://github.com/AI-SDC/AI-SDC/pull/175), [#176](https://github.com/AI-SDC/AI-SDC/pull/176), [#177](https://github.com/AI-SDC/AI-SDC/pull/177))
*    Add safemodel SDC results to `target.json` and `attack_results.json` ([#180](https://github.com/AI-SDC/AI-SDC/pull/180))
*    Add generalisation error to `target.json` ([#183](https://github.com/AI-SDC/AI-SDC/pull/183))
*    Refactor attack argument handling ([#174](https://github.com/AI-SDC/AI-SDC/pull/174))
*    Append attack outputs to a single results file ([#173](https://github.com/AI-SDC/AI-SDC/pull/173))
*    Attack outputs written to specified folder ([#208](https://github.com/AI-SDC/AI-SDC/pull/208))
*    Add ability to run membership inference attacks from the command line using config and target files ([#182](https://github.com/AI-SDC/AI-SDC/pull/182))
*    Add ability to run attribute inference attacks from the command line using config and target files ([#188](https://github.com/AI-SDC/AI-SDC/pull/188))
*    Add ability to run multiple attacks from a config file ([#200](https://github.com/AI-SDC/AI-SDC/pull/200))
*    Add user story examples ([#194](https://github.com/AI-SDC/AI-SDC/pull/194))
*    Improve attack formatter summary generation ([#179](https://github.com/AI-SDC/AI-SDC/pull/179))
*    Attack formatter moves files generated for release into subfolders ([#197](https://github.com/AI-SDC/AI-SDC/pull/197))
*    Fix a minor bug in the attack formatter ([#204](https://github.com/AI-SDC/AI-SDC/pull/204))
*    Improve tests ([#196](https://github.com/AI-SDC/AI-SDC/pull/196), [#199](https://github.com/AI-SDC/AI-SDC/pull/199))

## Version 1.0.5 (Jun 5, 2023)

Changes:
*    Fix a bug calculating the number of data samples in the `Data` class ([#105](https://github.com/AI-SDC/AI-SDC/pull/105))
*    Add a fail-fast mechanism for the worst case attack that enables the number of attack repetitions to terminate early based on a given metric and comparison operator ([#105](https://github.com/AI-SDC/AI-SDC/pull/105))
*    Change the logging message when attack repetitions are run to 1-10 instead of 0-9 ([#105](https://github.com/AI-SDC/AI-SDC/pull/105))
*    Add the ability to specify the number of worst case attack dummy repetitions on the command line ([#105](https://github.com/AI-SDC/AI-SDC/pull/105))
*    Add LIRA fail-fast mechanism ([#118](https://github.com/AI-SDC/AI-SDC/pull/118))
*    Add the ability to load LIRA attack parameters from a config file ([#118](https://github.com/AI-SDC/AI-SDC/pull/118))
*    Add the ability to load worst case attack parameters from a config file ([#119](https://github.com/AI-SDC/AI-SDC/pull/119))
*    Standardise the MIA attack output ([#120](https://github.com/AI-SDC/AI-SDC/pull/120))
*    Prohibit the use of white space in report file names ([#154](https://github.com/AI-SDC/AI-SDC/pull/154))
*    Improve the safemodel request release test ([#160](https://github.com/AI-SDC/AI-SDC/pull/160))
*    Refactor LIRA attack tests ([#151](https://github.com/AI-SDC/AI-SDC/pull/151))
*    Fix setting the number of LIRA shadow models from a config file ([#165](https://github.com/AI-SDC/AI-SDC/pull/165))
*    Fix OS system calls relying on calling "python" ([#162](https://github.com/AI-SDC/AI-SDC/pull/162))
*    Fix invalid command line argument in worst case attack example ([#164](https://github.com/AI-SDC/AI-SDC/pull/164))
*    Add current output JSON format documentation ([#168](https://github.com/AI-SDC/AI-SDC/pull/168))
*    Add current attack config format documentation ([#168](https://github.com/AI-SDC/AI-SDC/pull/168))

## Version 1.0.4 (May 5, 2023)

Changes:
*    Fixed SafeRandomForestClassifier "base estimator changed" error ([#143](https://github.com/AI-SDC/AI-SDC/pull/143))

## Version 1.0.3 (May 2, 2023)

Changes:
*    Refactored metrics ([#111](https://github.com/AI-SDC/AI-SDC/pull/111))
*    Fixed a bug making a report when dummy reps is 0 ([#113](https://github.com/AI-SDC/AI-SDC/pull/113))
*    Fixed safemodel JSON output ([#115](https://github.com/AI-SDC/AI-SDC/pull/115))
*    Added a module to produce recommendations from attack JSON output ([#116](https://github.com/AI-SDC/AI-SDC/pull/116))
*    Disabled non-default report logs ([#123](https://github.com/AI-SDC/AI-SDC/pull/123))
*    Fixed a minor bug in worst case example ([#124](https://github.com/AI-SDC/AI-SDC/pull/124))

## Version 1.0.2 (Feb 27, 2023)

Changes:
*    Added support for Python 3.8, 3.9 and 3.10 and update requirements.
*    Fixed documentation links to notebooks and added SafeSVC.
*    Added option to include target model error into attacks as a feature.

## Version 1.0.1 (Nov 16, 2022)

Changes:
*    Increased test coverage.
*    Packaged for PyPI.

## Version 1.0.0 (Sep 14, 2022)

First version.
