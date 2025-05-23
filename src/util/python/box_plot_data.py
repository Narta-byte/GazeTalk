#!/usr/bin/env python3
import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# The file is run typing something like this with glasses:
# python .\src\util\python\box_plot_data.py "<TOTAL_PATH>\user_test_1_data" true
# without glasses
# python .\src\util\python\box_plot_data.py "<TOTAL_PATH>\user_test_1_data"

# ---------------------------
# CONFIGURATION
# ---------------------------
# Get the base directory from the command-line argument,
# or use the default value if none is supplied.
if len(sys.argv) > 1:
    BASE_DIR = sys.argv[1]
else:
    BASE_DIR = "user_test_1_data"  # default directory

if len(sys.argv) > 2:
    include_glasses = sys.argv[2].lower() == "true"
else:
    include_glasses = False  # default: do not include users with glasses

# Expected structure:
#   <BASE_DIR>/
#       Subject_1/
#           iphone/
#               writing/
#                   <some_file.json>
#           ipad/
#               writing/
#                   <some_file.json>
#       Subject_2/
#           ...
#
# Define the list of metric keys to be plotted.
ALL_METRICS = ["WPM", "KSPC", "MSDErrorRate", "RBA", "OR", "RTE", "ANSR"]

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def load_metrics_from_file(filepath, subject, device, include_glasses):
    """
    Loads JSON data from a file and extracts metrics events.
    If include_glasses is False and any test in the file indicates 
    that the participant uses glasses, then the file is completely skipped.
    """
    results = []
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {filepath}")
        return results

    # Use "testResults" key if available or assume data is a list.
    if isinstance(data, dict) and "testResults" in data:
        tests = data["testResults"]
    elif isinstance(data, list):
        tests = data
    else:
        print(f"Unexpected data structure in {filepath}")
        return results

    # Check across tests: if any test has glasses (when we don't want to include them)
    if not include_glasses:
        for test in tests:
            if not isinstance(test, list):
                continue
            # Look for the userSettings event in the test.
            user_settings = next((event for event in test 
                                  if isinstance(event, dict) and event.get("type") == "userSettings"), {})
            if user_settings.get("usesGlasses", False):
                print(f"Skipping {subject} on {device} because glasses usage detected.")
                return []  # Skip all metrics from this file.

    # Process tests normally if no glasses usage is found (or if including glasses).
    for test in tests:
        if not isinstance(test, list):
            continue
        # Look for a metrics event.
        metrics_event = next((event for event in test 
                              if isinstance(event, dict) and event.get("type") == "metrics"), None)
        if metrics_event:
            metrics_event["subject"] = subject
            metrics_event["device"] = device
            results.append(metrics_event)
    return results

def traverse_data_dir(base_dir, include_glasses):
    """
    Traverses the base directory.
    Assumes the following structure:
      base_dir/Subject/Device/writing/<any JSON file>
    Returns a list of metrics event dictionaries.
    """
    all_metrics = []
    for subject in os.listdir(base_dir):
        subject_path = os.path.join(base_dir, subject)
        if not os.path.isdir(subject_path):
            continue
        for device in os.listdir(subject_path):
            device_path = os.path.join(subject_path, device)
            if not os.path.isdir(device_path):
                continue
            # Look for a "writing" folder.
            writing_path = os.path.join(device_path, "writing")
            if not os.path.isdir(writing_path):
                print(f"Warning: 'writing' folder not found in {device_path}")
                continue
            # Since there's exactly one JSON file per folder, get that file.
            files = [f for f in os.listdir(writing_path) if f.lower().endswith(".json")]
            if not files:
                print(f"Warning: No JSON file found in {writing_path}")
                continue
            json_file = os.path.join(writing_path, files[0])
            metrics = load_metrics_from_file(json_file, subject, device, include_glasses)
            all_metrics.extend(metrics)
    return all_metrics

def plot_boxplots_per_metric(df, metric):
    """
    Given a DataFrame and a metric key, this function creates a box plot for that metric
    with the x-axis showing devices (iPhone and iPad) and the y-axis showing metric values.
    """
    metric_df = df[df["Metric"] == metric]
    plt.figure(figsize=(6, 4))
    ax = sns.boxplot(data=metric_df, x="device", y="Value", order=["iphone", "ipad"])
    plt.title(f"{metric} by Device")
    plt.xlabel("Device")
    plt.ylabel(metric)
    plt.tight_layout()
    print(f"Displaying plot for {metric}. Close the figure to continue...")
    plt.show()
    plt.close()

# ---------------------------
# MAIN SCRIPT
# ---------------------------
def main():
    sns.set(style="whitegrid")
    plt.ioff()  # Block until the figure is closed

    # Collect metrics events from all JSON files under the base directory.
    metrics_list = traverse_data_dir(BASE_DIR, include_glasses)
    if not metrics_list:
        print("No metrics data found.")
        return

    # Create a DataFrame.
    df = pd.DataFrame(metrics_list)
    print("Summary (by subject and device):")
    print(df.groupby(["subject", "device"]).size().unstack(fill_value=0))

    # Reshape data: melt the metrics columns into a long-format DataFrame.
    df_long = df.melt(id_vars=["subject", "device"], value_vars=ALL_METRICS,
                      var_name="Metric", value_name="Value")

    # For each metric, plot a box plot comparing iPhone vs. iPad.
    for metric in ALL_METRICS:
        plot_boxplots_per_metric(df_long, metric)

if __name__ == "__main__":
    main()
