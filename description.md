Overview
This assignment was designed in the aim to test the technical ability and skill level of a full stack
developer, using any programming language and technologies he or she feels most comfortable with.
Goals
1. Test client side / front-end development.
2. Test back-end / server-side development.
3. Test basic database design and knowledge.
4. Test integration development using RESTful services.
5. Test logic and problem-solving abilities.
Prerequisites
- Internet connection.
- Local database of your choice. e.g. MySQL, SQL Server, Postgres etc.
- IDE to write and compile your preferred programming language.
- An internet browser to test your solution.
- A free GitHub account to house the assessment source code and project files.
Requirements
User Story 1
As an end user, I want to able to access a web page to input my South Africa ID Number to check if there
are any important public holidays on my date of birth.
Acceptance Criteria
 A web page with an input field to input an ID Number.
 An info / description section on the web page to provide information as to what the page does.
 A search button that will be used to execute a “Search” action.
Additional Information
 The design, look and feel are entirely in your hands.
User Story 2
As an end user, I must enter a valid South Africa ID Number before I can submit a search action so that
value can decoded into its relevant parts / information.
Acceptance Criteria
 The search button should be disable until a valid ID number is input.
 The validity of the ID number must be determined based on the below publication describing how
to validate an ID number.
 A message or prompt should be displayed when an invalid ID number is input.
Additional Information
 South Africa ID Number Decoding - https://www.westerncape.gov.za/generalpublication/decoding-your-south-african-id-number-0
User Story 3
As a developer, I want to ensure we store information extracted about the ID number and a count of
searches for a given ID number so that we can track how often the specific ID number is querie
Acceptance Criteria
 Only valid ID number searches should be stored in the database in a table.
 The ID number itself should be a unique key / reference for future updates.
 Decoded information about the ID number must be stored against the record in the database.
 A counter on the record must be incremented each time a visitor searches using the same SA ID
number.
Additional Information
 Decoded information – Date of Birth, Gender, SA Citizen
User Story 4
As an end user, I want to know if there are any public holidays that fall on the Date of Birth for a given ID
number so that I can display the results back to the visitor.
Acceptance Criteria
 After saving an ID record, the Calendarific REST API endpoint should be called to determine if
there are any public holidays for the date of birth.
 A separate table should be used to store public holidays returned from the API relating to a
specific ID number.
 Each holiday needs to be stored as a separate row.
 You need to store basic information for each holiday i.e., name, description, date, and type.
Additional Information
 You need to use the year obtained from the SA ID number and South Africa (ZA) as the
parameters to the Calendarific REST API endpoint.
 https://calendarific.com/api-documentation
o Access above URL
o Select the Sign-up option and chose the $0 plan.
o Login to get your API key that you would need for the callouts.
Read through the API documentation.
User Story 5
As an end user, I want to see all information gathered about the ID number displayed in a results section
so that I can clearly see the information returned.
Acceptance Criteria
 Display all the data stored in your local database for the specific SA ID number.
 Data should be neat and easy to read and follow.
Additional Information
 The design, look and feel are entirely in your hands.
Document Tracking
Description Author Date Version
Wording update Peter Guest 13/05/2021 1.2
User stories Peter Guest 30/04/2021 1.1
Initial version Rudolf Niehaus 26/11/2020 1.0