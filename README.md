# JIRA-TO-WIKIJS-RELEASE-NOTE

Create a release note based on your Jira tickets !

## Requirements

This repo assume you have :
* A WikiJS setup and access to its API
* A Jira Cloud project setup and access to its API

## How it works

The script will first list all unreleased Jira versions.
You choose one.
It will search for all issues in this version.
From each issue it takes the key, title, and a description field (this can be set in .env file).
Behind the scene it converts the Jira Markdown to the standard one (Thank you https://github.com/catcombo/jira2markdown)
Then it concatenates evrything to create and upload a page in WikiJS.

## Setting up the Environment

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/PydImmodvisor/Jira2WikijsReleaseNote.git
   cd your-repo
   ```

2. **Install dependencies**
    ```
    pip install dotenv
    pip install jira2markdown
    ```

2. **Create the `.env` file:**
   - Copy the `.env.example` file and create a new file named `.env`:
     ```bash
     cp .env.example .env
     ```

3. **Fill in the Details:**
   - Open the `.env` file in a text editor of your choice and fill in the necessary details.

4. **Save and Close the File.**

## Execute

    ```
    python3 run.py
    ```
    
## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.