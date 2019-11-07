#
#  Copyright 2019 [David Robert Wong]
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ********************
#  v0.1.0: drwnz (david.wong@tier4.jp)
#
#  rosbag_segment_extractor.py
#
#  Created on: November 6th 2019
#

import sys
import rosbag
import genpy
import subprocess
import yaml
import os
from pathlib import Path
import argparse


def show_progress(percent, length= 80):
    sys.stdout.write('\x1B[2K')  # Erase entire current line
    sys.stdout.write('\x1B[0E')  # Move to the beginning of the current line
    progress = "Progress: ["
    for i in range(0, length):
        if i < length * percent:
            progress += '='
        else:
            progress += ' '
    progress += "] " + str(round(percent * 100.0, 2)) + "%"
    sys.stdout.write(progress)
    sys.stdout.flush()


def main(args):
    parser = argparse.ArgumentParser(description='Rosbag segment extractor.')
    parser.add_argument('in_file', nargs=1, help='Input bag file')
    parser.add_argument('out_file', nargs='+', help='Output file to store the segment')
    parser.add_argument('segment_start', nargs='+', help='Time in seconds to start segment')
    parser.add_argument('segment_end', nargs='+', help='Time in seconds to end segment')

    args = parser.parse_args()

    input_bagfile = args.in_file[0]
    output_bagfile = args.out_file[0]
    segment_start = int(args.segment_start[0])
    segment_end = int(args.segment_end[0])

    segment_period = segment_end - segment_start

    info_dict = yaml.load(
        subprocess.Popen(['rosbag', 'info', '--yaml', input_bagfile], stdout=subprocess.PIPE).communicate()[0])
    bag_duration = info_dict['duration']
    start_time = info_dict['start']

    if segment_period > bag_duration:
        print(
            'Segment can not be extracted from the input bag file. The specified period ({period})is longer than the bag duration ({duration}).'.format(
                period=segment_period, duration=bag_duration))
        exit(1)

    base_name = Path(input_bagfile).stem

    outbag = rosbag.Bag(output_bagfile, 'w')
    segment_start_time = start_time + segment_start
    segment_end_time = start_time + segment_end

    for topic, msg, t in rosbag.Bag(input_bagfile).read_messages(start_time=genpy.Time.from_sec(segment_start_time), end_time=genpy.Time.from_sec(segment_end_time)):
        outbag.write(topic, msg, t)
        percent = (t.to_sec() - segment_start_time) / segment_period
        show_progress(percent)
    outbag.close()

if __name__ == "__main__":
    main(sys.argv[1:])
