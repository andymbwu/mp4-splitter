import pandas as pd
import json

class TimestampToManifest:

    def __init__(self, filename: str):
        self.labels_df = pd.read_csv(filename)
        self.video_dicts = dict(iter(self.labels_df.groupby('Video ID')))
        self.all_manifests = [] # list of lists

    def generate_manifest_from_timestamps(self):
        for v_name, v_dict in self.video_dicts.items():
            split_counter = 0
            manifest = []

            start_ts_list = v_dict['Crash Start Timestamp'].values
            end_ts_list = v_dict['Crash Accident End Timestamp'].values
            crash_label_list = v_dict['Crash/Normal'].values

            for i in range(len(start_ts_list)):
                manifest_entry = {}
                manifest_entry['start_time'] = start_ts_list[i]
                manifest_entry['end_time'] = end_ts_list[i]
                manifest_entry['rename_to'] = v_name.split('.')[0] + '_' + str(split_counter) + '_' + crash_label_list[i] + '.' + v_name.split('.')[1]
                manifest.append(manifest_entry)
                split_counter += 1
            self.all_manifests.append((v_name.split('.')[0], json.dumps(manifest)))

    def dump_manifests_to_file(self):
        for manifest in self.all_manifests:
            with open (manifest[0] + '.json', 'w') as file:
                file.write("%s\n" % manifest[1])

converter = TimestampToManifest("labels/labels.csv")
converter.generate_manifest_from_timestamps()
converter.dump_manifests_to_file()
