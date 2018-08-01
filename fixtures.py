followers = [{'full_name': 'name1',
    'has_anonymous_profile_picture': False,
    'is_private': True,
    'is_verified': False,
    'pk': 1234,
    'profile_pic_id': '1234_5678',
    'profile_pic_url': 'url_1',
    'reel_auto_archive': 'on',
    'username': 'username1'},
    {'full_name': 'name2',
        'has_anonymous_profile_picture': False,
        'is_private': False,
        'is_verified': False,
        'latest_reel_media': 1532807182,
        'pk': 5678,
        'profile_pic_id': '5678_9123',
        'profile_pic_url': 'url_2',
        'reel_auto_archive': 'on',
        'username': 'username2'}]

media_resp_1 = [
        {'image_versions2': {
            'candidates': [
                {'height': 868, 'width': 750, 'url': 'image_url_0'},
                {'height': 278, 'width': 240, 'url': 'short_img_url_)'}
            ],
         'pk': 1234
         }},
        {"non-image_field": None,
         'pk': 1234},
]
media_resp_2 = [
        {'image_versions2': {
            'candidates': [
                {'height': 868, 'width': 750, 'url': 'image_url_1'},
                {'height': 278, 'width': 240, 'url': 'short_img_url_1'}
            ],
         'pk': 5678
         }},
        {'image_versions2': {
            'candidates': [
                {'height': 868, 'width': 750, 'url': 'image_url_2'},
                {'height': 278, 'width': 240, 'url': 'short_img_url_2'}
            ],
         'pk': 5678
         }}
]
