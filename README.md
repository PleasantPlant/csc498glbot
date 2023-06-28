# csc498glbot
This is all that remains of my senior project, since hosting everything in AWS was costing me ~$20 a month.
Here's how it worked:

1. Whenever a logfile containing specific data is sent to Graylog (hosted on AWS EC2 t2.medium), 
    Graylog generates a notification json and sends it to Lambda

2. Lambda (GL_to_SQS) takes that notification file (that Graylog has pre-formatted, to some extent) and strips out the user,
    the basic event, which datastream the event belongs to, and the ID of the ticket for the permalink, creating a custom notification object.

3. Lambda (GL_to_SQS) then packages that notification object as json and sends it to SQS.
    It sends to SQS because if you send directly to lambda, you don't have a queing system to deal with high-volumes of traffic.
    This was never an issue for me, since I was the only one generating logfiles for Graylog, but I wanted to pretend I needed to think about scalability.

4. SQS then sends the notification object (as json) to Lambda (GL_Bot_MessageHandler)

5. Lambda (GL_Bot_MessageHandler) takes the message and reconstitutes the notification object (like packaged soup, just add hot water!)

6. Lambda then pings the specified user in Slack, using the notification object to form the message body.

5.5. The reason GL_Bot_MessageHandler is separate, is because the original design intended for users to be able to add/remove themselves 
from notification streams by messaging the bot in Slack. 
This was cut from the final product due to time constraints, and I never implimented it later as there is no current practical use for this app.
