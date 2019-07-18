import pandas as pd
from io import StringIO
import json


def cleanse_date(country, old_dates, new_dates):
    '''
    Replace old_date by new_date in raw csv files
    '''
    with open('raw/{}videos.csv'.format(country), 'r', encoding='utf-8') as f:
        data_string = f.read()
    
    for old_date, new_date in zip(old_dates, new_dates):
        data_string = data_string.replace(old_date, new_date)
    
    return data_string


def get_category_name(country):
    '''
    Convert raw category json files to a Pandas DataFrame
    '''
    with open('raw/{}_category_id.json'.format(country), 'r') as f:
        json_cat = json.load(f)
        
    category_name = {'category_id': [], 'category_name': [], 'country': country}
    for item in json_cat['items']:
        category_name['category_id'] += [int(item['id'])]
        category_name['category_name'] += [item['snippet']['title']]
    
    return pd.DataFrame(category_name)


if __name__ == '__main__':
    # Cleanse date in GB and US csv files
    gb = cleanse_date(
        'GB',
        ['24.09l7yxJDFvTRM', '26.09t2oVUxTV4WA'],
        ['24.09\nl7yxJDFvTRM', '26.09\nt2oVUxTV4WA'])

    us = cleanse_date(
        'US',
        ['24.09xcaeyJTx4Co', '26.0903jeumSTSzc', '.jpg,100,09.10'],
        ['24.09\nxcaeyJTx4Co', '26.09\n03jeumSTSzc', '.jpg,09.10'])

    # Import as Pandas DataFrame
    gb_videos = pd.read_csv(StringIO(gb), dtype={'date': object}, na_values='[none]')
    us_videos = pd.read_csv(StringIO(us), dtype={'date': object}, na_values='[none]')

    gb_videos['country'] = 'GB'
    us_videos['country'] = 'US'

    videos = pd.concat([gb_videos, us_videos], ignore_index=True)

    # Change date to datetime format
    videos['date'] = pd.to_datetime(videos['date'] + '.2017', format='%d.%m.%Y')

    # Remove duplicates
    videos = videos.drop_duplicates().reset_index(drop=True)

    # Check increasing
    check_increasing = videos.groupby(['video_id', 'country'])['views'].apply(lambda x: x.is_monotonic)
    check_increasing = check_increasing.reset_index()
    check_increasing.columns = ['video_id', 'country', 'view_increasing']

    videos = videos.merge(
        check_increasing,
        on=['video_id', 'country'],
        how='left').query('view_increasing').drop('view_increasing', axis=1).reset_index(drop=True)

    # Get category names
    gb_category_names = get_category_name('GB')
    us_category_names = get_category_name('US')
    category_names = pd.concat([gb_category_names, us_category_names], ignore_index=True)
    videos = videos.merge(category_names, on=['category_id', 'country'], how='left')
    videos = videos[~pd.isna(videos['category_name'])].reset_index(drop=True)

    # Melt tags to another DataFrame
    videos_with_tags = videos[~pd.isna(videos['tags'])]

    video_tags = pd.DataFrame(
        videos_with_tags['tags'].str.split('|').tolist(),
        index=videos_with_tags['video_id']).stack()

    video_tags = video_tags.reset_index(['video_id', 0])
    video_tags.columns = ['video_id', 'tag']

    # Get last date of a video in trending by country
    latest_dates = videos.groupby(['video_id', 'country'])['date'].max().reset_index()
    latest_dates['latest_date'] = 1

    videos = videos.merge(latest_dates, on=['video_id', 'country', 'date'], how='left')
    videos['latest_date'].fillna(0, inplace=True)
    videos['latest_date'] = videos['latest_date'].astype(int)

    # Select necessary columns for analysis only
    videos = videos[
        ['video_id', 'title', 'channel_title', 'category_name', 'views',
         'likes', 'dislikes', 'comment_total', 'date', 'country', 'latest_date']]

    # Output cleansed data
    videos.to_csv('cleansed/videos.csv', index=False)
    video_tags.to_csv('cleansed/video_tags.csv', index=False)
