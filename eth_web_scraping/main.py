#!/usr/bin/env python3
from eth_web_scraping.eth_room_search import ETHRoomSearch
from eth_web_scraping.email_notification import EmailNotification
import time
import os
import argparse
'''
You can run this file in your terminal:  ./main.py -e EMAIL -p PASSWORD. Note you need to give execution right 
to this file first: chmod +x main.py

'''

def main():
    """Entry point for the application script"""
    # formatter_class=argparse.ArgumentDefaultsHelpFormatter will display the default values of your arguments.
    my_parser = argparse.ArgumentParser(
        description="Do web scraping for available rooms from Student Village and Living Science",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    my_parser.add_argument('-n', '--name', help='The greeting name that will appear in your email', default="Sir/Madam")
    
    my_parser.add_argument('-e', '--email', help='The email address you would like to use for receiving data.'
                                                 '(Only Gmail is supported currently)', required=True)
    my_parser.add_argument('-p', '--password', help='The password of your provided email address', required=True)
    my_parser.add_argument('-f', '--frequency', help='The frequency of web scraping (Hz)', default="0.2", type=float)
    my_args = my_parser.parse_args()

    eth_room_search_obj = ETHRoomSearch()
    here = os.path.abspath(os.path.dirname(__file__))
    email_notification_obj = EmailNotification(contact_file=os.path.join(here, "files/contacts.txt"),
                                               template_message_file=os.path.join(here, "files/message_template.txt"))
    old_pandas_data_sv_to_string = ""
    old_pandas_data_ls_to_string = ""
    web_scrape_counter = 0
    while True:

        web_scrape_counter = web_scrape_counter + 1
        print("Web Scraping Counter: " + str(web_scrape_counter))
        sv_html_segments = eth_room_search_obj.filter_entries_from_sv_url()
        ls_html_segments = eth_room_search_obj.filter_entries_from_ls_url()

        pandas_data_sv_to_string = eth_room_search_obj.organize_sv_data(sv_html_segments).to_string()
        if pandas_data_sv_to_string != old_pandas_data_sv_to_string:
            old_pandas_data_sv_to_string = pandas_data_sv_to_string
            email_notification_obj.notify_by_email(email_address=my_args.email, email_password=my_args.password,
                                                   email_subject="SV at your request is available!",
                                                   message_to_send=old_pandas_data_sv_to_string, greeting_name=my_args.name)
            print(pandas_data_sv_to_string + '\n\n')

        pandas_data_ls_to_string = eth_room_search_obj.organize_ls_data(ls_html_segments).to_string()
        if pandas_data_ls_to_string != old_pandas_data_ls_to_string:
            old_pandas_data_ls_to_string = pandas_data_ls_to_string
            email_notification_obj.notify_by_email(email_address=my_args.email, email_password=my_args.password,
                                                   email_subject="LS at your request is available!",
                                                   message_to_send=old_pandas_data_ls_to_string, greeting_name=my_args.name)
            print(pandas_data_ls_to_string + '\n\n')

        # You need to configure your email setting inside this function.
        # email_notification_obj.notify_by_email(email_address="example@gmail.com", email_password="xxx")
        time.sleep(1.0 / my_args.frequency)


if __name__ == '__main__':
    # todo: add test code for checking this module here.
    main()
