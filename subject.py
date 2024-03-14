import argparse
import json
import os
import sys
import shutil


def mkdir(path):
    try:
        os.makedirs(path)
    except:
        if os.listdir(path) != []:
            print(f'{path} is not empty.')
            sys.exit(0)


def genChartInfo(info_type, chart, arg):
    chart_info = {'DiffName': '',
                  'Diff': '',
                  'FileName': '',
                  'Media': '',
                  'Video': 'Video.mp4',
                  'Bg': '',
                  'Icon': 'cyl://cyicons/ivy001',
                  'SongName': '',
                  'ThemeColor': '#FFBA1E1E',
                  'DiffTextColor': '#B3FF33FF',
                  'DiffBgColor': '#FF330033',
                  'StoryboardPath': None,
                  'Bookmarks': [],
                  'GenerateEventConfig': {
                          'IgnoreFrom': 0.8,
                          'IgnoreTo': 1.25,
                          'IgnoreSameTypeInterval': 480,
                          'UseLastEventAsRef': False,
                          'IgnorePosFunc': False,
                          'BaseTicks': None
                  }}
    chart_folder = f'./{arg.dest_folder}'
    chart_info['FileName'] = chart_folder+'/'
    chart_info['Media'] = arg.music
    chart_info['Bg'] = arg.bg
    chart_info['SongName'] = arg.songname

    if chart['type'] == 'standard':
        chart_info['DiffName'] = chart['charter']
        chart_info['FileName'] = str(chart_info['FileName']) + str(
            chart['charter'])+'.json'
    else:
        chart_info['Icon'] = 'cyl://cyicons/ilka001'
        chart_info['ThemeColor'] = '#FFFFFFFF'
        chart_info['DiffTextColor'] = '#B333CCFF'
        chart_info['DiffBgColor'] = '#FF003366'
        if info_type == 'public_cyl':
            chart_info['DiffName'] = chart['number']
            if chart['type'] == 'public':
                chart_info['Diff'] = chart['charter']
            else:
                chart_info['Diff'] = 'N/A'
            chart_info['FileName'] = str(
                chart_info['FileName']) + str(chart['number'])+'.json'
        elif info_type == 'private_cyl':
            chart_info['DiffName'] = chart['charter']
            chart_info['FileName'] = str(chart_info['FileName']) + str(
                chart['number'])+'.json'
    return chart_info


parser = argparse.ArgumentParser()
parser.description = 'Please enter the parameters of the subject.'
parser.add_argument('-t', '--time', help='set year and month, such as 202311',
                    dest='time', type=int, default='0')
parser.add_argument('-m', '--music', help='set music file, default music.ogg',
                    dest='music', type=str, default='music.ogg')
parser.add_argument('-b', '--bg', help='set background, default bg.png',
                    dest='bg', type=str, default='bg.png')
parser.add_argument('-s', '--songname', help='set song name',
                    dest='songname', type=str, default='Songname')
parser.add_argument('-c', '--chart', help='set raw chart folder, default raw',
                    dest='chart_folder', type=str, default='raw')
parser.add_argument('-d', '--dest', help='set dest chart folder, default charts',
                    dest='dest_folder', type=str, default='charts')
parser.add_argument('-o', '--owner', help='set subject owner',
                    dest='owner', type=str, default='')
subject_arg = parser.parse_args()

public_cyl = {'Version': 0,
              'ChartInfos': [],
              'LastOpenedChart': None,
              'LastEditedTime': 0.0,
              'LevelMetaConfig': None}
private_cyl = {'Version': 0,
               'ChartInfos': [],
               'LastOpenedChart': None,
               'LastEditedTime': 0.0,
               'LevelMetaConfig': None}
temp = []
mkdir(f'./{subject_arg.dest_folder}')
for x in os.listdir(f'./{subject_arg.chart_folder}'):
    path_now = os.path.join(f'./{subject_arg.chart_folder}/', x)
    if (x.endswith('.json') or x.endswith('.txt')):
        chart = x.split('.')[0]
        chart = chart.split('-')
        chart = {
            'time': chart[0],
            'type': chart[1],
            'charter': chart[2],
            'level': 2,
            'raw_path': path_now
        }
        temp.append(chart)
for chart in temp:
    if chart['type'] == 'standard':
        if chart['charter'] == subject_arg.owner:
            chart['level'] = -1
        else:
            chart['level'] = 0
charts = sorted(temp, key=lambda i: (
    i['level'], i['time'], i['type'], i['charter']))
chart_counter = 0
for chart in charts:
    if chart['type'] == 'standard':
        chart['number'] = 0
    else:
        chart_counter += 1
        chart['number'] = chart_counter
for chart in charts:
    src = chart['raw_path']
    dst_name = chart['charter']if chart['number'] == 0 else chart['number']
    dst = f'./{subject_arg.dest_folder}/'+str(dst_name)+'.json'
    shutil.copy(src, dst)
for chart in charts:
    pub_chart_info = genChartInfo('public_cyl', chart, subject_arg)
    prv_chart_info = genChartInfo('private_cyl', chart, subject_arg)
    public_cyl['ChartInfos'].append(pub_chart_info)
    private_cyl['ChartInfos'].append(prv_chart_info)
j_pub_chart_info = json.dumps(public_cyl, ensure_ascii=False,
                              indent=4, separators=(',', ': '))
j_prv_chart_info = json.dumps(private_cyl, ensure_ascii=False,
                              indent=4, separators=(',', ': '))
pub_file = f'[发布_{subject_arg.time}]{subject_arg.songname}.cyl'
prv_file = f'[评审_{subject_arg.time}]{subject_arg.songname}.cyl'
f_pub = open(pub_file, 'w', encoding='utf-8')
f_prv = open(prv_file, 'w', encoding='utf-8')
f_pub.write(j_pub_chart_info)
f_prv.write(j_prv_chart_info)
