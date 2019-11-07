# ROSBAG Segment Extractor

Extracts a segment out of a rosbag based on start and end time (relative to the start of the rosbag) and saves it into a new rosbag.

```
python rosbag_segment_extractor.py INPUT_ROSBAG_FILENAME OUTPUT_ROSBAG_FILENAME SEGMENT_START_TIME_IN_SECONDS SEGMENT_END_TIME_IN_SECONDS
```

# To Do

- Also allow filtering of topics
