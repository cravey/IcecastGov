# Playing with ChatGPT
#
# Certainly! Below is a Python script that accomplishes the task as you've described.
# This script expects four arguments: an instanceNum, a template_filename, a destination_filename, and a database_filename. 
# It will search the SQLite database for the row with the given instanceNum and replace any instances of %%columnname%% in the 
# template file with the corresponding values from that row. Finally, it will save the modified content to a new file 
# with instanceNum appended to the filename before the dot ahead of the three-letter filetype suffix.
#
#
# Usage: python generate_config.py 1 template.txt destination.txt client_config.db
#
#
import sqlite3
import sys

def generate_config(instanceNum, template_filename, destination_filename, database_filename):
    # Connect to SQLite database
    conn = sqlite3.connect(database_filename)
    cursor = conn.cursor()

    # Fetch the record for the given instanceNum
    cursor.execute("SELECT * FROM ClientInfo WHERE instanceNum = ?", (instanceNum,))
    row = cursor.fetchone()

    if row is None:
        print(f"No record found for instanceNum: {instanceNum}")
        return

    # Load the template file
    with open(template_filename, 'r') as f:
        template_content = f.read()

    # Replace placeholders in the template
    for idx, column in enumerate(cursor.description):
        column_name = column[0]
        column_value = row[idx]
        placeholder = f"%%{column_name}%%"
        template_content = template_content.replace(placeholder, str(column_value))

    # Create the destination filename with instanceNum
    name_parts = destination_filename.rsplit('.', 1)
    modified_dest_filename = f"{name_parts[0]}_{instanceNum}.{name_parts[1]}"

    # Save the modified content to the destination file
    with open(modified_dest_filename, 'w') as f:
        f.write(template_content)

    print(f"Config generated and saved to {modified_dest_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <instanceNum> <template_filename> <destination_filename> <database_filename>")
    else:
        instanceNum = int(sys.argv[1])
        template_filename = sys.argv[2]
        destination_filename = sys.argv[3]
        database_filename = sys.argv[4]
        
        generate_config(instanceNum, template_filename, destination_filename, database_filename)
