from eth_web_scraping.eth_room_search import ETHRoomSearch


def main():
    """Entry point for the application script"""
    eth_room_search_obj = ETHRoomSearch()
    sv_html_segments = eth_room_search_obj.filter_entries_from_sv_url()
    pandas_data_sv = eth_room_search_obj.organize_sv_data(sv_html_segments)

    ls_html_segments = eth_room_search_obj.filter_entries_from_ls_url()
    pandas_data_ls = eth_room_search_obj.organize_ls_data(ls_html_segments)
    print(pandas_data_sv.to_string() + '\n\n' + pandas_data_ls.to_string())