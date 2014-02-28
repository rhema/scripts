from settings import *
from amazon_sender import AmazonSender
from csv import DictReader

#conn.verify_email_address('some@address.com') add new address
# tested with boto version '2.5.2'
# https://docs.google.com/spreadsheet/ccc?key=0Al2ia8wE351odF9UcVhFaFRtdmVTTzhwbmQzdllIWlE

sender = None

#print conn.list_verified_email_addresses()

def test_send_to_self():
    print "sending to self"
    sender.send_email(sender='Rhema Linder HCC TA<rhemalinder@gmail.com>',
                         to_addresses=['rhemalinder@gmail.com'],
                         subject='This is a test from myself',
                         text='A test to myself where http://google.com/')#,
                         #html='<b>A test to myself</b>')

def send_feedback_csv_as_emails(csv_file,from_email,email_subject,email_column,prepend_message,show_each_value_columns=None,test=True):
    #read from csv
    reader = DictReader(open(csv_file))
    for row in reader:
        message = prepend_message
        to_email = row[email_column]
        
        for col in show_each_value_columns:
            message += col+": "+row[col]+"\n"
        
        #check using test, i guess
        print "    begin","--"*100
        print "FROM:",from_email
        print "SUBJECT:",email_subject
        print "TO:",to_email
        print "BODY:",message
        print "   end","--"*100
        if not test:
#            to_email = "rhemalinder@gmail.com"
            sender.send_email(sender=from_email,
                             to_addresses=[to_email],
                             subject=email_subject,
                             text=message)
            

    
#AmazonSender

#AWS_KEY, AWS_SECRET_KEY

prepend_email_v1 ="""This email contains feedback for your presentation of Assignment 1: interaction breakdown.
Overall score shows your grade out of 100. Rubric scores are on a 0 to 5 scale.

We also include your 'alias'. Look up your alias to see your grades on this spreadsheet:
   https://docs.google.com/spreadsheet/ccc?key=0Al2ia8wE351odF9UcVhFaFRtdmVTTzhwbmQzdllIWlE .
"""

prepend_email_v2 ="""This email contains feedback for your Assignment 2 deliverable 1: needs and requirements.
Overall score shows your grade out of 100. Each grading rubric criteria is presented along with your score and some additional comments.


"""

if __name__ == "__main__":
    sender = AmazonSender(AWS_KEY, AWS_SECRET_KEY)
    #(csv_file,from_email,email_subject,email_column,prepend_message,show_each_value_columns=None,test=True):
#    send_feedback_csv_as_emails("hccGradesSpring2014BreakdownA1.csv",
#                                "Rhema Linder HCC TA<rhemalinder@gmail.com>",
#                                "CPCE655 / HCC Assignment 1 Feedback + Alias For Grades",
#                                "email",
#                                prepend_email_v1,
#                                ["Alias",
#                                     "Feedback",
#                                     "Overall Score",
#                                     "Is Breakdown / Engagement-factor",
#                                     "Clear Description of Breakdown",
#                                     "Use of Principles in Articulation",
#                                     "Alternative Design Ideas",
#                                     "Visual Presentation of Slides",
#                                     "Oral Presentation"]
#                                ,True)
    send_feedback_csv_as_emails("a21.csv",
                                "Rhema Linder HCC TA<rhemalinder@gmail.com>",
                                "CPCE655 / HCC Assignment 2 Deliverable 1 Feedback",
                                "email",
                                prepend_email_v2,
                                ["Overall Score",
                                "Overall Comments",
                                "Are a set of needs clearly presented? (20)",
                                "Additional Comments 1",
                                "Do you thoroughly and incisively investigate activities and tasks that the users perform in comparative technology shopping? (10)",
                                "Additional Comments 2",
                                "How you define sensemaking tasks for comparative technology shopping? (10)",
                                "Additional Comments 3",
                                "How do you examine existing shopping assistants? (10)",
                                "Additional Comments 4",
                                "Do you collect data? Is it presented clearly? (15)",
                                "Additional Comments 5",
                                "How you explain data collection methods and reasons for use? (7.5)",
                                "Additional Comments 6",
                                "How do you analyze collected data? (10)",
                                "Additional Comments 7",
                                "How do you incorporate the concepts and vocabulary from the readings? (7.5)",
                                "Additional Comments 8",
                                "Presentation (structure, organization, grammar) (10)",
                                "Additional Comments 9"]
                                ,False)
    #test_send_to_self()