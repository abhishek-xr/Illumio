import csv
from collections import defaultdict

# Making use of default libraries only

class LogTagger:
    def __init__(self, lookup_file):
        self.lookup = self._read_lookup_table(lookup_file)

    def _read_lookup_table(self, filename):
        # Reading lookup table from CSV file
        lookup = defaultdict(list)
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    key = (row['dstport'].strip(), row['protocol'].strip().lower())  # Lower casing to work for case insensitivity
                    lookup[key].append(row['tag'].strip())  # Append tag to the list for each port/protocol combination
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            return {}
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return {}
        return lookup

    def _generate_output(self, output_filename, tag_counts, port_protocol_counts):
        # Tag counts and Port/Protocol combination counts
        # Generating output file
        try:
            with open(output_filename + '_tag_counts.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Tag', 'Count'])
                # Sorting and writing the tag counts
                for tag, count in sorted(tag_counts.items(), key=lambda x: (x[1], x[0])):  # Sorting by count, then by tag name
                    writer.writerow([tag, count])

            with open(output_filename + '_port_protocol_counts.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Port', 'Protocol', 'Count'])
                # Sorting and writing the port/protocol counts
                for key, count in sorted(port_protocol_counts.items(), key=lambda x: (int(x[0][0]), x[1])):  # Sorting by port number
                    writer.writerow([key[0], key[1], count])
        except Exception as e:
            print(f"Error generating output files: {e}")

    def apply_tags_to_logs(self, logs_filename, output_filename):
        # Applying tags to log entries based on dstport and protocol
        tag_counts = defaultdict(int)
        port_protocol_counts = defaultdict(int)

        try:
            with open(logs_filename, 'r', newline='') as infile, open(output_filename + '.csv', 'w', newline='') as outfile:
                # Assuming the AWS Flow Log Record format
                fieldnames = [
                    'Version', 'AccountID', 'InterfaceID', 'SrcAddr', 'DstAddr',
                    'SrcPort', 'DstPort', 'Protocol', 'Packets', 'Bytes',
                    'StartTime', 'EndTime', 'Action', 'LogStatus', 'Tag'
                ]
                reader = csv.reader(infile, delimiter=' ')
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

                for row in reader:
                    log_entry = {fn: val for fn, val in zip(fieldnames[:-1], row)}
                    # Assuming the port numbers are standard (6 for TCP, 17 for UDP, 1 for ICMP)
                    protocol = {'6': 'tcp', '17': 'udp', '1': 'icmp'}.get(log_entry['Protocol'], 'unknown')
                    key = (log_entry['DstPort'], protocol)
                    # Getting the list of tags for the given key
                    tags = self.lookup.get(key, ['Untagged'])
                    for tag in tags:
                        log_entry['Tag'] = tag
                        writer.writerow(log_entry)
                        tag_counts[tag] += 1
                    port_protocol_counts[key] += 1

            self._generate_output(output_filename, tag_counts, port_protocol_counts)

        except FileNotFoundError as e:
            print(f"Error: File {logs_filename} not found.")
            raise e  # Re-raise the exception so that it can be caught by the test
        except Exception as e:
            print(f"Error processing logs: {e}")

if __name__ == "__main__":
    # Using Lookup and sampleFlowLogs as plain txt files as mentioned in the requirements.
    log_tagger = LogTagger('lookup.txt')
    log_tagger.apply_tags_to_logs('sampleFlowLogs.txt', 'output')