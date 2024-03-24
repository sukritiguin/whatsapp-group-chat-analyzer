# Whatsapp Group Chat Analyzer
This project involves analyzing WhatsApp group chat data to gain insights into the communication patterns and behaviors of participants. It begins with collecting the chat data, preprocessing it to extract relevant information, and then analyzing it to calculate various statistics and metrics such as message frequency, media usage, and emoji usage. The analysis results are then visualized using charts and graphs to make them easy to understand. Finally, an interactive web application is developed to facilitate the upload of chat data files and provide users with access to the analysis results. The application allows users to explore the data visually and gain valuable insights into the dynamics of the WhatsApp group chat.

# Motivation behind the project
The motivation behind this project stems from the desire to understand and explore the dynamics of communication within WhatsApp group chats. WhatsApp has become a ubiquitous platform for social interaction, collaboration, and information sharing among groups of various sizes and interests. However, analyzing the vast amount of data generated within these group chats manually can be time-consuming and inefficient.

By developing an automated pipeline for analyzing WhatsApp group chat data, we aim to provide users with valuable insights into their communication patterns, behaviors, and preferences. This analysis can help users better understand the dynamics of their groups, identify key contributors, track trends over time, and enhance their overall communication experience.

Furthermore, by visualizing the analysis results in an intuitive and interactive manner, we aim to make the insights accessible and actionable for users, enabling them to make informed decisions and optimize their group communication strategies.

Overall, the motivation behind this project is to empower users with the tools and knowledge to unlock the full potential of their WhatsApp group chats and foster more meaningful and productive interactions within their communities.

## Project Pipeline
Detailed outline of the pipeline for this WhatsApp group chat analysis project:

1. **Data Collection:**
   - Users export their WhatsApp group chat data as a text file from the WhatsApp application.
   - The text file contains the entire conversation history of the group chat, including messages, timestamps, and other metadata.

2. **Data Preprocessing:**
   - Read the text file containing the chat data into memory.
   - Extract relevant information from the text file, such as:
     - Usernames or phone numbers of participants.
     - Message content.
     - Timestamps.
     - Deleted messages.
     - Media files (images, videos, etc.).
   - Clean the data by removing irrelevant information, formatting inconsistencies, and special characters.
   - Convert timestamps to a standardized format.

3. **Data Analysis:**
   - Calculate various statistics and metrics based on the preprocessed data, such as:
     - Total number of messages.
     - Number of messages sent by each user.
     - Number of deleted messages by each user.
     - Distribution of messages over time (by year, month, day, hour).
     - Most frequently used emojis.
     - Word frequency in messages.
     - Distribution of media types (images, videos, etc.) sent by each user.
   - Visualize the calculated statistics using charts and graphs for easy interpretation and analysis.

4. **Application Development:**
   - Choose a web development framework for building the analytical application (e.g., Dash, Flask, Django).
   - Implement the user interface for uploading chat data files.
   - Develop interactive components for selecting date and time formats and configuring visualization options.
   - Integrate the data preprocessing and analysis functionalities into the application backend.
   - Design and implement the different charts and graphs to display the analysis results.
   - Ensure responsiveness and user-friendly interactions in the application interface.

