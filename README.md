# OCP-Workflow
## Requirements
- Node.js 22.0.0+
- npm
- Live Server Extension for Visual Studio Code
- Python 3.8+

## Installation
1. Clone the repository using `git clone https://github.com/OCP-Interns/OCP-Workflow.git`
2. Change directory to the repository using `cd OCP-Workflow`
3. Install the dependencies using `npm install`
4. Change directory to the API using `cd src/api`
5. Create a new Python virtual environment using `python -m venv venv`
6. Install the dependencies using `
`
7. Activate the virtual environment using `source venv/bin/activate` (Linux) or `.\venv\Scripts\activate` (Windows)
8. Change directory back to the root of the repository using `cd ../..`
9. Use the live server extension in Visual Studio Code to run the project
10. Change the port number in the `package.json` file and in the `index.js` file in the `src` folder to the port number used by the live server extension
11. Run the project using `npm run dev`