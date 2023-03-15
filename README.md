# Satellite Tracker with Python
This is a Python project that tracks satellites and sends their elevation and azimuth relative to the observer via serial communication to a microcontroller. The
microcontroller can then point a communications antenna at the chosen satellites. The project also manages a MySQL database that includes all active celestrak 
satellites so that any of those can be tracked. Additionally, the Python code allows users to update the database whenever they want.
## Getting Started
To use this project, you will need:
* Python 3
* MySQL
* A microcontroller with serial communication capability
To get started, follow these steps:
1. Clone this repository to your local machine.
2. Create a MySQL database and import the satellite.sql file included in the repository.
3. Modify the updatedb.py file to include your database credentials.
4. Install the required Python packages by running pip install -r requirements.txt.
5. Run the main.py file to start tracking satellites.
## Features
This project has the following features:
* Tracking of satellites with elevation and azimuth relative to the observer
* Serial communication with a microcontroller to point a communications antenna
* Management of a MySQL database with active celestrak satellites
* Ability to update the database whenever desired
## Contributing
Contributions are welcome! If you would like to contribute to this project, please follow these steps:
1. Fork this repository.
2. Create a new branch with your changes.
3. Submit a pull request.
## License
This project is licensed under the MIT License - see the LICENSE file for details.
## Acknowledgements
I would like to acknowledge andresv for his code. The Python class declaration that I used was based on his work, a link to his code is provided as a comment on 
main.py
This project uses data from celestrak.com.
