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
         },
         'id': 5678},
        {"non-image_field": None,
         'pk': 1234},
]
media_resp_2 = [
        {'image_versions2': {
            'candidates': [
                {'height': 868, 'width': 750, 'url': 'image_url_1'},
                {'height': 278, 'width': 240, 'url': 'short_img_url_1'}
            ],
         'pk': 5678,
         'id': 4321
         }},
        {'image_versions2': {
            'candidates': [
                {'height': 868, 'width': 750, 'url': 'image_url_2'},
                {'height': 278, 'width': 240, 'url': 'short_img_url_2'}
            ],
         'pk': 5678,
         'id': 9876
         }}
]

storie_resp_1 = {
        'items': [
            {'image_versions2': {
                'candidates': [
                    {'height': 868, 'width': 750, 'url': 'image_url_1'},
                    {'height': 278, 'width': 240, 'url': 'short_img_url_1'}
                    ],
                },
             'media_type': 1,
             'id': 4321
             },
            {'image_versions2': {
                'candidates': [
                    {'height': 868, 'width': 750, 'url': 'image_url_2'},
                    {'height': 278, 'width': 240, 'url': 'short_img_url_2'}
                    ],
                },
             'media_type': 2
             }
            ]
        }

storie_resp_2 = {
        'items': [
            {'image_versions2': {
                'candidates': [
                    {'height': 868, 'width': 750, 'url': 'image_url_3'},
                    {'height': 278, 'width': 240, 'url': 'short_img_url_3'}
                    ],
                },
             'media_type': 1,
             'id': 9876
             },
            {'image_versions2': {
                'candidates': [
                    {'height': 868, 'width': 750, 'url': 'image_url_4'},
                    {'height': 278, 'width': 240, 'url': 'short_img_url_4'}
                    ],
                },
             'media_type': 1
             }
            ]
        }

vision_api_non_target = {'responses': [
    {"labelAnnotations": [
        {
            "mid": "/m/04_fs",
            "description": "muscle",
            "score": 0.7627564,
            "topicality": 0.7627564
            },
        {
            "mid": "/m/0dzf4",
            "description": "arm",
            "score": 0.75626075,
            "topicality": 0.75626075
            },
        {
            "mid": "/m/02p0tk3",
            "description": "human body",
            "score": 0.74117637,
            "topicality": 0.74117637
            },
        {
            "mid": "/m/035r7c",
            "description": "leg",
            "score": 0.7064597,
            "topicality": 0.7064597
            },
        {
            "mid": "/m/0k65p",
            "description": "hand",
            "score": 0.61223406,
            "topicality": 0.61223406
            },
        {
            "mid": "/m/05y5lj",
            "description": "sports equipment",
            "score": 0.565478,
            "topicality": 0.565478
            },
        {
            "mid": "/m/06bm2",
            "description": "recreation",
            "score": 0.56316197,
            "topicality": 0.56316197
            },
        {
            "mid": "/m/0dm6dl",
            "description": "barechestedness",
            "score": 0.5615934,
            "topicality": 0.5615934
            }
        ]
        }]}

vision_api_target = {'responses': [{
    "labelAnnotations": [
        {
            "mid": "/m/09j5n",
            "description": "Footwear",
            "score": 0.97527814,
            "topicality": 0.97527814
            },
        {
            "mid": "/m/06rrc",
            "description": "Shoe",
            "score": 0.90856355,
            "topicality": 0.90856355
            },
        {
            "mid": "/m/035r7c",
            "description": "Leg",
            "score": 0.8656675,
            "topicality": 0.8656675
            },
        {
            "mid": "/m/01dvt1",
            "description": "Joint",
            "score": 0.8487657,
            "topicality": 0.8487657
            },
        {
            "mid": "/m/09w5r",
            "description": "Human leg",
            "score": 0.82455796,
            "topicality": 0.82455796
            },
        {
            "mid": "/m/0715t2",
            "description": "Calf",
            "score": 0.7601689,
            "topicality": 0.7601689
            },
        {
            "mid": "/m/02p0tk3",
            "description": "Human body",
            "score": 0.74117637,
            "topicality": 0.74117637
            },
        {
            "mid": "/m/0dzf4",
            "description": "Arm",
            "score": 0.718239,
            "topicality": 0.718239
            },
        {
            "mid": "/m/019swr",
            "description": "Knee",
            "score": 0.69414085,
            "topicality": 0.69414085
            },
        {
                "mid": "/m/05y5lj",
                "description": "Sports equipment",
                "score": 0.6789266,
                "topicality": 0.6789266
                },
        {
                "mid": "/m/031n1",
                "description": "Foot",
                "score": 0.65484965,
                "topicality": 0.65484965
                },
        {
                "mid": "/m/06bm2",
                "description": "Recreation",
                "score": 0.64873284,
                "topicality": 0.64873284
                },
        {
                "mid": "/m/04_fs",
                "description": "Muscle",
                "score": 0.6399608,
                "topicality": 0.6399608
                },
        {
                "mid": "/m/0hgrj75",
                "description": "Outdoor shoe",
                "score": 0.6220674,
                "topicality": 0.6220674
                },
        {
                "mid": "/m/0hr8",
                "description": "Asphalt",
                "score": 0.53616446,
                "topicality": 0.53616446
                }
        ]}]}
